-- Script de migración FINAL para cambiar todas las columnas a español
-- IMPORTANTE: Hacer backup antes de ejecutar
-- Este script actualiza las columnas que aún están en inglés

BEGIN;

-- ============================================
-- TABLA: comments -> comentarios
-- ============================================
-- Verificar si las columnas existen antes de renombrarlas
DO $$
BEGIN
    -- Renombrar content a contenido
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='comments' AND column_name='content') THEN
        ALTER TABLE comments RENAME COLUMN content TO contenido;
    END IF;
    
    -- Renombrar created_at a fecha_creacion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='comments' AND column_name='created_at') THEN
        ALTER TABLE comments RENAME COLUMN created_at TO fecha_creacion;
    END IF;
    
    -- Renombrar announcement_id a anuncio_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='comments' AND column_name='announcement_id') THEN
        ALTER TABLE comments RENAME COLUMN announcement_id TO anuncio_id;
        
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'comments_announcement_id_fkey') THEN
            ALTER TABLE comments RENAME CONSTRAINT comments_announcement_id_fkey TO comments_anuncio_id_fkey;
        END IF;
    END IF;
    
    -- Renombrar author_id a autor_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='comments' AND column_name='author_id') THEN
        ALTER TABLE comments RENAME COLUMN author_id TO autor_id;
        
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'comments_author_id_fkey') THEN
            ALTER TABLE comments RENAME CONSTRAINT comments_author_id_fkey TO comments_autor_id_fkey;
        END IF;
    END IF;
END $$;

-- ============================================
-- Verificar y actualizar otras tablas si es necesario
-- ============================================

-- Verificar si announcements tiene columnas en inglés
DO $$
BEGIN
    -- Renombrar author_id a autor_id en announcements si existe
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

