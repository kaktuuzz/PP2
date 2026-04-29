

-- 1. Groups / categories
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL   -- 'Family', 'Work', 'Friend', 'Other'
);

-- Seed the four standard groups
INSERT INTO groups (name) VALUES
    ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;


-- 2. Contacts (extended)
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    email      VARCHAR(150),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- 3. Phones  (1-to-many, replaces the old phone column)
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20)  NOT NULL,
    type       VARCHAR(10)  NOT NULL DEFAULT 'mobile'
                    CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);


CREATE OR REPLACE VIEW contact_details AS
SELECT
    c.id,
    c.first_name,
    c.email,
    c.birthday,
    c.created_at,
    g.name                              AS group_name,
    STRING_AGG(p.phone || ' (' || p.type || ')', ', '
               ORDER BY p.type)         AS phones
FROM contacts  c
LEFT JOIN groups g ON g.id  = c.group_id
LEFT JOIN phones p ON p.contact_id = c.id
GROUP BY c.id, c.first_name, c.email, c.birthday, c.created_at, g.name;



CREATE OR REPLACE FUNCTION paginate_contacts(
    p_page      INT DEFAULT 1,
    p_page_size INT DEFAULT 10,
    p_order_by  TEXT DEFAULT 'first_name'   -- 'first_name' | 'birthday' | 'created_at'
)
RETURNS TABLE (
    id         INT,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT
) LANGUAGE plpgsql AS $$
DECLARE
    v_offset INT := (p_page - 1) * p_page_size;
    v_sql    TEXT;
BEGIN
    -- Whitelist sort columns to prevent SQL injection
    IF p_order_by NOT IN ('first_name', 'birthday', 'created_at') THEN
        p_order_by := 'first_name';
    END IF;

    v_sql := format(
        'SELECT cd.id, cd.first_name, cd.email, cd.birthday,
                cd.group_name, cd.phones
         FROM   contact_details cd
         ORDER  BY cd.%I NULLS LAST
         LIMIT  $1 OFFSET $2',
        p_order_by
    );

    RETURN QUERY EXECUTE v_sql USING p_page_size, v_offset;
END;
$$;
