-- Script de migración COMPLETO para cambiar todas las columnas a español
-- IMPORTANTE: Hacer backup antes de ejecutar
-- Este script actualiza TODAS las columnas que aún están en inglés

BEGIN;

-- ============================================
-- TABLA: announcements
-- ============================================
DO $$
BEGIN
    -- Renombrar title a titulo
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='announcements' AND column_name='title') THEN
        ALTER TABLE announcements RENAME COLUMN title TO titulo;
    END IF;
    
    -- Renombrar content a contenido
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='announcements' AND column_name='content') THEN
        ALTER TABLE announcements RENAME COLUMN content TO contenido;
    END IF;
    
    -- Renombrar created_at a fecha_creacion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='announcements' AND column_name='created_at') THEN
        ALTER TABLE announcements RENAME COLUMN created_at TO fecha_creacion;
    END IF;
    
    -- Renombrar updated_at a fecha_actualizacion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='announcements' AND column_name='updated_at') THEN
        ALTER TABLE announcements RENAME COLUMN updated_at TO fecha_actualizacion;
    END IF;
    
    -- Renombrar course_id a curso_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='announcements' AND column_name='course_id') THEN
        ALTER TABLE announcements RENAME COLUMN course_id TO curso_id;
        
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'announcements_course_id_fkey') THEN
            ALTER TABLE announcements RENAME CONSTRAINT announcements_course_id_fkey TO announcements_curso_id_fkey;
        END IF;
    END IF;
    
    -- Renombrar author_id a autor_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='announcements' AND column_name='author_id') THEN
        ALTER TABLE announcements RENAME COLUMN author_id TO autor_id;
        
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'announcements_author_id_fkey') THEN
            ALTER TABLE announcements RENAME CONSTRAINT announcements_author_id_fkey TO announcements_autor_id_fkey;
        END IF;
    END IF;
END $$;

COMMIT;

-- Verificar cambios
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name IN ('comments', 'announcements')
ORDER BY table_name, ordinal_position;

