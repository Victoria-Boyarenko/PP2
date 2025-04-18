-- Удаление старых версий
DROP FUNCTION IF EXISTS search_phonebook(TEXT);
DROP PROCEDURE IF EXISTS insert_or_update_user(TEXT, TEXT);
DROP FUNCTION IF EXISTS insert_many_users(TEXT[][]);
DROP FUNCTION IF EXISTS get_users_paginated(INT, INT);
DROP PROCEDURE IF EXISTS delete_user(TEXT);
DROP TABLE IF EXISTS phonebook_lab11;

-- Таблица
CREATE TABLE phonebook_lab11 (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    phone VARCHAR(20)
);

-- 1. Функция поиска по шаблону
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, username TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook_lab11.id, phonebook_lab11.username::TEXT, phonebook_lab11.phone::TEXT
    FROM phonebook_lab11
    WHERE phonebook_lab11.username ILIKE '%' || pattern || '%'
       OR phonebook_lab11.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Процедура вставки или обновления пользователя
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_username TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Обработка: %, %', p_username, p_phone;

    IF EXISTS (SELECT 1 FROM phonebook_lab11 WHERE username = p_username) THEN
        UPDATE phonebook_lab11 SET phone = p_phone WHERE username = p_username;
    ELSE
        INSERT INTO phonebook_lab11(username, phone) VALUES (p_username, p_phone);
    END IF;
END;
$$;

-- 3. Функция массовой вставки с проверкой номера
CREATE OR REPLACE FUNCTION insert_many_users(user_list TEXT[][])
RETURNS TABLE (username TEXT, phone TEXT, status TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    r TEXT[];
    exists_user BOOLEAN;
BEGIN
    FOREACH r SLICE 1 IN ARRAY user_list
    LOOP
        -- Проверка номера: начинается на 8 или 7 и ровно 11 цифр
        IF r[2] ~ '^[87][0-9]{10}$' THEN
            BEGIN
                SELECT EXISTS (
                    SELECT 1 FROM phonebook_lab11 WHERE username = r[1]
                ) INTO exists_user;

                CALL insert_or_update_user(r[1], r[2]);

                username := r[1];
                phone := r[2];
                status := CASE 
                    WHEN exists_user THEN 'updated'
                    ELSE 'inserted'
                END;
                RETURN NEXT;
            EXCEPTION WHEN OTHERS THEN
                username := r[1];
                phone := r[2];
                status := 'error';
                RETURN NEXT;
            END;
        ELSE
            username := r[1];
            phone := r[2];
            status := 'invalid';
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$;

-- 4. Пагинация
CREATE OR REPLACE FUNCTION get_users_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, username TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook_lab11.id, phonebook_lab11.username::TEXT, phonebook_lab11.phone::TEXT
    FROM phonebook_lab11
    ORDER BY phonebook_lab11.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- 5. Удаление по имени или номеру
CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook_lab11 WHERE username = p_value OR phone = p_value;
END;
$$;
