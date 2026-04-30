

import csv
import json
import sys
from datetime import date, datetime

import psycopg2
from psycopg2.extras import RealDictCursor

# ── Connection ────────────────────────────────────────────────────────────────

conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="123",
    host="localhost",
    port="5432",
)
conn.autocommit = False          # explicit commits throughout


def cur():
    return conn.cursor(cursor_factory=RealDictCursor)


# ── Schema bootstrap ──────────────────────────────────────────────────────────

def create_tables():
    with cur() as c:
        c.execute(open("schema.sql").read())
        c.execute(open("procedures.sql").read())
    conn.commit()
    print("Schema ready.")


# Helpers 

def _resolve_group(name: str, cursor) -> int | None:
    """Return group id for *name*, None if blank."""
    if not name:
        return None
    cursor.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (name,)
    )
    cursor.execute("SELECT id FROM groups WHERE name=%s", (name,))
    row = cursor.fetchone()
    return row["id"] if row else None


def _print_rows(rows):
    if not rows:
        print("  (no results)")
        return
    for r in rows:
        phones = r.get("phones") or "—"
        bday   = r.get("birthday") or "—"
        print(
            f"  [{r['id']:>4}] {r['first_name']:<20}"
            f"   {(r.get('email') or '—'):<28}"
            f"   {bday!s:<12}"
            f"   {(r.get('group_name') or '—'):<10}"
            f"   {phones}"
        )


# 3.1  INSERT

def insert_from_console():
    name  = input("First name: ").strip()
    email = input("Email (optional): ").strip() or None
    bday  = input("Birthday YYYY-MM-DD (optional): ").strip() or None
    group = input("Group [Family/Work/Friend/Other]: ").strip() or None

    phone      = input("Phone number: ").strip()
    phone_type = input("Phone type [home/work/mobile] (default mobile): ").strip() or "mobile"

    with cur() as c:
        gid = _resolve_group(group, c)
        c.execute(
            """INSERT INTO contacts (first_name, email, birthday, group_id)
               VALUES (%s, %s, %s, %s) RETURNING id""",
            (name, email, bday, gid),
        )
        cid = c.fetchone()["id"]
        c.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (cid, phone, phone_type),
        )
    conn.commit()
    print(f"Contact '{name}' added (id={cid}).")


# 3.2  SEARCH & FILTER


def search_by_name():
    name = input("Name (partial): ").strip()
    with cur() as c:
        c.execute(
            "SELECT * FROM contact_details WHERE first_name ILIKE %s ORDER BY first_name",
            (f"%{name}%",),
        )
        _print_rows(c.fetchall())


def search_by_email():
    term = input("Email (partial): ").strip()
    with cur() as c:
        c.execute(
            "SELECT * FROM contact_details WHERE email ILIKE %s ORDER BY first_name",
            (f"%{term}%",),
        )
        _print_rows(c.fetchall())


def search_by_phone_prefix():
    prefix = input("Phone prefix: ").strip()
    with cur() as c:
        c.execute(
            """SELECT DISTINCT cd.*
               FROM   contact_details cd
               JOIN   phones p ON p.contact_id = cd.id
               WHERE  p.phone LIKE %s
               ORDER  BY cd.first_name""",
            (f"{prefix}%",),
        )
        _print_rows(c.fetchall())


def full_search():
    #Uses the search_contacts() PL/pgSQL function (matches name + email + phones)
    q = input("Search query: ").strip()
    with cur() as c:
        c.execute("SELECT * FROM search_contacts(%s)", (q,))
        _print_rows(c.fetchall())


def filter_by_group():
    with cur() as c:
        c.execute("SELECT name FROM groups ORDER BY name")
        groups = [r["name"] for r in c.fetchall()]
    print("Available groups:", ", ".join(groups))
    chosen = input("Group name: ").strip()
    sort   = _ask_sort()
    with cur() as c:
        c.execute(
            f"""SELECT cd.*
                FROM   contact_details cd
                WHERE  cd.group_name = %s
                ORDER  BY cd.{sort} NULLS LAST""",
            (chosen,),
        )
        _print_rows(c.fetchall())


def _ask_sort() -> str:
    print("Sort by: (1) name  (2) birthday  (3) date added")
    choice = input("Choice [1]: ").strip()
    return {"2": "birthday", "3": "created_at"}.get(choice, "first_name")


def paginated_list():
    #Navigate contacts page by page
    PAGE_SIZE = 10
    page = 1
    sort = _ask_sort()

    while True:
        with cur() as c:
            c.execute(
                "SELECT * FROM paginate_contacts(%s, %s, %s)",
                (page, PAGE_SIZE, sort),
            )
            rows = c.fetchall()

        print(f"\n── Page {page} ────────────")
        _print_rows(rows)

        nav = input("\n[n]ext  [p]rev  [q]uit: ").strip().lower()
        if nav == "n":
            if len(rows) == PAGE_SIZE:
                page += 1
            else:
                print("  Already on last page.")
        elif nav == "p":
            if page > 1:
                page -= 1
            else:
                print("  Already on first page.")
        else:
            break



# 3.3  UPDATE / DELETE


def update_contact():
    search = input("Name to update (partial): ").strip()
    with cur() as c:
        c.execute(
            "SELECT id, first_name FROM contacts WHERE first_name ILIKE %s",
            (f"%{search}%",),
        )
        matches = c.fetchall()

    if not matches:
        print("No contacts found.")
        return
    for m in matches:
        print(f"  [{m['id']}] {m['first_name']}")
    cid = int(input("Enter id to update: ").strip())

    new_name  = input("New name (blank to keep): ").strip() or None
    new_email = input("New email (blank to keep): ").strip() or None
    new_bday  = input("New birthday YYYY-MM-DD (blank to keep): ").strip() or None
    new_group = input("New group (blank to keep): ").strip() or None

    with cur() as c:
        if new_name:
            c.execute("UPDATE contacts SET first_name=%s WHERE id=%s", (new_name, cid))
        if new_email:
            c.execute("UPDATE contacts SET email=%s WHERE id=%s", (new_email, cid))
        if new_bday:
            c.execute("UPDATE contacts SET birthday=%s WHERE id=%s", (new_bday, cid))
        if new_group:
            gid = _resolve_group(new_group, c)
            c.execute("UPDATE contacts SET group_id=%s WHERE id=%s", (gid, cid))
    conn.commit()
    print("Contact updated.")


def add_phone_to_contact():
    #Wrapper around the add_phone stored procedure
    name  = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    ptype = input("Type [home/work/mobile]: ").strip() or "mobile"
    with cur() as c:
        c.callproc("add_phone", (name, phone, ptype))
    conn.commit()
    print("Phone added.")


def move_contact_to_group():
    #Wrapper around move_to_group stored procedure
    name  = input("Contact name: ").strip()
    group = input("Group name: ").strip()
    with cur() as c:
        c.callproc("move_to_group", (name, group))
    conn.commit()
    print(f"Contact moved to group '{group}'.")


def delete_contact():
    choice = input("Delete by (1) name  (2) id: ").strip()
    with cur() as c:
        if choice == "1":
            name = input("Name (exact): ").strip()
            c.execute("DELETE FROM contacts WHERE first_name=%s", (name,))
        elif choice == "2":
            cid = int(input("ID: ").strip())
            c.execute("DELETE FROM contacts WHERE id=%s", (cid,))
        else:
            print("Invalid choice.")
            return
    conn.commit()
    print("Contact deleted.")


# 3.4  IMPORT / EXPORT


def insert_from_csv():
    
    #Expected CSV columns (header row required):
    #first_name, phone, phone_type, email, birthday, group
    
    path = input("CSV file path: ").strip()
    inserted = skipped = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name  = row.get("first_name", "").strip()
            phone = row.get("phone",      "").strip()
            ptype = (row.get("phone_type", "mobile") or "mobile").strip()
            email = row.get("email",      "").strip() or None
            bday  = row.get("birthday",   "").strip() or None
            group = row.get("group",      "").strip() or None

            if not name or not phone:
                continue

            try:
                with cur() as c:
                    gid = _resolve_group(group, c)
                    c.execute(
                        """INSERT INTO contacts (first_name, email, birthday, group_id)
                           VALUES (%s, %s, %s, %s) RETURNING id""",
                        (name, email, bday, gid),
                    )
                    cid = c.fetchone()["id"]
                    c.execute(
                        """INSERT INTO phones (contact_id, phone, type)
                           VALUES (%s, %s, %s)
                           ON CONFLICT (contact_id, phone) DO NOTHING""",
                        (cid, phone, ptype),
                    )
                conn.commit()
                inserted += 1
            except Exception as e:
                conn.rollback()
                print(f"  Skipped {name}: {e}")
                skipped += 1

    print(f"CSV import done – inserted: {inserted}, skipped: {skipped}")


# JSON export 

def export_to_json():
    path = input("Output JSON file path [contacts.json]: ").strip() or "contacts.json"
    with cur() as c:
        c.execute(
            """SELECT c.id, c.first_name, c.email,
                      c.birthday::TEXT, c.created_at::TEXT,
                      g.name AS group_name,
                      JSON_AGG(
                          JSON_BUILD_OBJECT('phone', p.phone, 'type', p.type)
                          ORDER BY p.type
                      ) FILTER (WHERE p.id IS NOT NULL) AS phones
               FROM   contacts c
               LEFT JOIN groups g ON g.id = c.group_id
               LEFT JOIN phones p ON p.contact_id = c.id
               GROUP  BY c.id, c.first_name, c.email,
                         c.birthday, c.created_at, g.name
               ORDER  BY c.first_name"""
        )
        rows = c.fetchall()

    data = [dict(r) for r in rows]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Exported {len(data)} contacts → {path}")


# JSON import 

def import_from_json():
    path = input("JSON file path: ").strip()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    imported = skipped = overwritten = 0

    for item in data:
        name = item.get("first_name", "").strip()
        if not name:
            continue

        with cur() as c:
            c.execute(
                "SELECT id FROM contacts WHERE first_name=%s LIMIT 1", (name,)
            )
            existing = c.fetchone()

        if existing:
            choice = input(
                f"  '{name}' already exists. [s]kip / [o]verwrite: "
            ).strip().lower()
            if choice != "o":
                skipped += 1
                continue
            # Overwrite: delete existing record (cascade removes phones)
            with cur() as c:
                c.execute("DELETE FROM contacts WHERE id=%s", (existing["id"],))
            conn.commit()
            overwritten += 1

        try:
            with cur() as c:
                gid = _resolve_group(item.get("group_name"), c)
                c.execute(
                    """INSERT INTO contacts (first_name, email, birthday, group_id)
                       VALUES (%s, %s, %s, %s) RETURNING id""",
                    (
                        name,
                        item.get("email"),
                        item.get("birthday"),
                        gid,
                    ),
                )
                cid = c.fetchone()["id"]
                for ph in (item.get("phones") or []):
                    c.execute(
                        """INSERT INTO phones (contact_id, phone, type)
                           VALUES (%s, %s, %s)
                           ON CONFLICT (contact_id, phone) DO NOTHING""",
                        (cid, ph.get("phone"), ph.get("type", "mobile")),
                    )
            conn.commit()
            imported += 1
        except Exception as e:
            conn.rollback()
            print(f"  Error importing '{name}': {e}")
            skipped += 1

    print(f"JSON import done – imported: {imported}, overwritten: {overwritten}, skipped: {skipped}")



# Menu


MENU = """

      INSERT                                  
   1. Insert from CSV                     
   2. Insert manually                     

     SEARCH & FILTER                         
   3. Search by name                      
   4. Search by email                     
   5. Search by phone prefix              
   6. Full search (name + email + phones) 
   7. Filter by group                    
   8. Browse all (paginated)              

   UPDATE                                  
  9. Update contact fields               
  10. Add phone to contact                
  11. Move contact to group               

     DELETE                                  
  12. Delete contact                      
    IMPORT / EXPORT                         
  13. Export to JSON                      
  14. Import from JSON                    
   0. Exit                                

"""

ACTIONS = {
    "1":  insert_from_csv,
    "2":  insert_from_console,
    "3":  search_by_name,
    "4":  search_by_email,
    "5":  search_by_phone_prefix,
    "6":  full_search,
    "7":  filter_by_group,
    "8":  paginated_list,
    "9":  update_contact,
    "10": add_phone_to_contact,
    "11": move_contact_to_group,
    "12": delete_contact,
    "13": export_to_json,
    "14": import_from_json,
}


def menu():
    create_tables()
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        action = ACTIONS.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                conn.rollback()
                print(f"Error: {e}")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
    conn.close()
    print("Connection closed.")
