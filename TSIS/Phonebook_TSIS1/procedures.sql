-- 1. add_phone
--    Adds a phone number to an existing contact (looked up by
--    first_name, case-insensitive).
-- ------------------------------------------------------------
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id
    FROM   contacts
    WHERE  first_name ILIKE p_contact_name
    LIMIT  1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO UPDATE
        SET type = EXCLUDED.type;
END;
$$;



-- 2. move_to_group
--    Moves a contact to a different group; creates the group
--    if it does not already exist.
-- ------------------------------------------------------------
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
    v_group_id   INT;
BEGIN
    -- Resolve (or create) the group
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM   groups
    WHERE  name = p_group_name;

    -- Resolve the contact
    SELECT id INTO v_contact_id
    FROM   contacts
    WHERE  first_name ILIKE p_contact_name
    LIMIT  1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    UPDATE contacts
    SET    group_id = v_group_id
    WHERE  id = v_contact_id;
END;
$$;



-- 3. search_contacts
--    Full-text pattern search across first_name, email, and
--    all phone numbers in the phones table.
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INT,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    v_pattern TEXT := '%' || p_query || '%';
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        cd.id,
        cd.first_name,
        cd.email,
        cd.birthday,
        cd.group_name,
        cd.phones
    FROM contact_details cd
    WHERE  cd.first_name ILIKE v_pattern
        OR cd.email      ILIKE v_pattern
        OR EXISTS (
            SELECT 1
            FROM   phones ph
            WHERE  ph.contact_id = cd.id
              AND  ph.phone LIKE v_pattern
        )
    ORDER BY cd.first_name;
END;
$$;
