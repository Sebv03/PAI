-- Script de migración para cambiar las columnas de la tabla users a español
-- IMPORTANTE: Hacer backup antes de ejecutar

BEGIN;

-- ============================================
-- TABLA: users
-- ============================================
DO $$
BEGIN
    -- Renombrar email a correo
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='users' AND column_name='email') THEN
        ALTER TABLE users RENAME COLUMN email TO correo;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'users_email_key') THEN
            ALTER TABLE users RENAME CONSTRAINT users_email_key TO users_correo_key;
        END IF;
        -- Renombrar índice si existe
        IF EXISTS (SELECT 1 FROM pg_indexes 
                   WHERE tablename='users' AND indexname='ix_users_email') THEN
            ALTER INDEX ix_users_email RENAME TO ix_users_correo;
        END IF;
    END IF;
    
    -- Renombrar full_name a nombre_completo
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='users' AND column_name='full_name') THEN
        ALTER TABLE users RENAME COLUMN full_name TO nombre_completo;
        -- Renombrar índice si existe
        IF EXISTS (SELECT 1 FROM pg_indexes 
                   WHERE tablename='users' AND indexname='ix_users_full_name') THEN
            ALTER INDEX ix_users_full_name RENAME TO ix_users_nombre_completo;
        END IF;
    END IF;
    
    -- Renombrar hashed_password a contraseña_hash
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='users' AND column_name='hashed_password') THEN
        ALTER TABLE users RENAME COLUMN hashed_password TO "contraseña_hash";
    END IF;
    
    -- Renombrar is_active a activo
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='users' AND column_name='is_active') THEN
        ALTER TABLE users RENAME COLUMN is_active TO activo;
    END IF;
    
    -- Renombrar role a rol
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='users' AND column_name='role') THEN
        ALTER TABLE users RENAME COLUMN role TO rol;
    END IF;
END $$;

COMMIT;

-- Verificar cambios
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

