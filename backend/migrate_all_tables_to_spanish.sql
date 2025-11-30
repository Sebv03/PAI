-- Script de migración COMPLETO para cambiar todas las columnas a español
-- Verifica si las columnas existen antes de renombrarlas
-- IMPORTANTE: Hacer backup antes de ejecutar

BEGIN;

-- ============================================
-- TABLA: courses
-- ============================================
DO $$
BEGIN
    -- Renombrar title a titulo
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='courses' AND column_name='title') THEN
        ALTER TABLE courses RENAME COLUMN title TO titulo;
        -- Renombrar índice si existe
        IF EXISTS (SELECT 1 FROM pg_indexes 
                   WHERE tablename='courses' AND indexname='ix_courses_title') THEN
            ALTER INDEX ix_courses_title RENAME TO ix_courses_titulo;
        END IF;
    END IF;
    
    -- Renombrar description a descripcion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='courses' AND column_name='description') THEN
        ALTER TABLE courses RENAME COLUMN description TO descripcion;
    END IF;
    
    -- Renombrar owner_id a propietario_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='courses' AND column_name='owner_id') THEN
        ALTER TABLE courses RENAME COLUMN owner_id TO propietario_id;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'courses_owner_id_fkey') THEN
            ALTER TABLE courses RENAME CONSTRAINT courses_owner_id_fkey TO courses_propietario_id_fkey;
        END IF;
    END IF;
    
    -- Renombrar created_at a fecha_creacion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='courses' AND column_name='created_at') THEN
        ALTER TABLE courses RENAME COLUMN created_at TO fecha_creacion;
    END IF;
END $$;

-- ============================================
-- TABLA: tasks
-- ============================================
DO $$
BEGIN
    -- Renombrar title a titulo
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='tasks' AND column_name='title') THEN
        ALTER TABLE tasks RENAME COLUMN title TO titulo;
        -- Renombrar índice si existe
        IF EXISTS (SELECT 1 FROM pg_indexes 
                   WHERE tablename='tasks' AND indexname='ix_tasks_title') THEN
            ALTER INDEX ix_tasks_title RENAME TO ix_tasks_titulo;
        END IF;
    END IF;
    
    -- Renombrar description a descripcion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='tasks' AND column_name='description') THEN
        ALTER TABLE tasks RENAME COLUMN description TO descripcion;
    END IF;
    
    -- Renombrar due_date a fecha_limite
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='tasks' AND column_name='due_date') THEN
        ALTER TABLE tasks RENAME COLUMN due_date TO fecha_limite;
    END IF;
    
    -- Renombrar course_id a curso_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='tasks' AND column_name='course_id') THEN
        ALTER TABLE tasks RENAME COLUMN course_id TO curso_id;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'tasks_course_id_fkey') THEN
            ALTER TABLE tasks RENAME CONSTRAINT tasks_course_id_fkey TO tasks_curso_id_fkey;
        END IF;
    END IF;
    
    -- Renombrar created_at a fecha_creacion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='tasks' AND column_name='created_at') THEN
        ALTER TABLE tasks RENAME COLUMN created_at TO fecha_creacion;
    END IF;
END $$;

-- ============================================
-- TABLA: enrollments
-- ============================================
DO $$
BEGIN
    -- Renombrar student_id a estudiante_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='enrollments' AND column_name='student_id') THEN
        ALTER TABLE enrollments RENAME COLUMN student_id TO estudiante_id;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'enrollments_student_id_fkey') THEN
            ALTER TABLE enrollments RENAME CONSTRAINT enrollments_student_id_fkey TO enrollments_estudiante_id_fkey;
        END IF;
    END IF;
    
    -- Renombrar course_id a curso_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='enrollments' AND column_name='course_id') THEN
        ALTER TABLE enrollments RENAME COLUMN course_id TO curso_id;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'enrollments_course_id_fkey') THEN
            ALTER TABLE enrollments RENAME CONSTRAINT enrollments_course_id_fkey TO enrollments_curso_id_fkey;
        END IF;
    END IF;
    
    -- Renombrar enrollment_date a fecha_inscripcion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='enrollments' AND column_name='enrollment_date') THEN
        ALTER TABLE enrollments RENAME COLUMN enrollment_date TO fecha_inscripcion;
    END IF;
END $$;

-- ============================================
-- TABLA: submissions
-- ============================================
DO $$
BEGIN
    -- Renombrar content a contenido
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='submissions' AND column_name='content') THEN
        ALTER TABLE submissions RENAME COLUMN content TO contenido;
    END IF;
    
    -- Renombrar file_path a ruta_archivo
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='submissions' AND column_name='file_path') THEN
        ALTER TABLE submissions RENAME COLUMN file_path TO ruta_archivo;
    END IF;
    
    -- Renombrar grade a calificacion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='submissions' AND column_name='grade') THEN
        ALTER TABLE submissions RENAME COLUMN grade TO calificacion;
    END IF;
    
    -- Renombrar feedback a retroalimentacion
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='submissions' AND column_name='feedback') THEN
        ALTER TABLE submissions RENAME COLUMN feedback TO retroalimentacion;
    END IF;
    
    -- Renombrar submitted_at a fecha_entrega
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='submissions' AND column_name='submitted_at') THEN
        ALTER TABLE submissions RENAME COLUMN submitted_at TO fecha_entrega;
    END IF;
    
    -- Renombrar student_id a estudiante_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='submissions' AND column_name='student_id') THEN
        ALTER TABLE submissions RENAME COLUMN student_id TO estudiante_id;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'submissions_student_id_fkey') THEN
            ALTER TABLE submissions RENAME CONSTRAINT submissions_student_id_fkey TO submissions_estudiante_id_fkey;
        END IF;
    END IF;
    
    -- Renombrar task_id a tarea_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='submissions' AND column_name='task_id') THEN
        ALTER TABLE submissions RENAME COLUMN task_id TO tarea_id;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'submissions_task_id_fkey') THEN
            ALTER TABLE submissions RENAME CONSTRAINT submissions_task_id_fkey TO submissions_tarea_id_fkey;
        END IF;
    END IF;
END $$;

-- ============================================
-- TABLA: student_profiles
-- ============================================
DO $$
BEGIN
    -- Renombrar student_id a estudiante_id
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='student_id') THEN
        ALTER TABLE student_profiles RENAME COLUMN student_id TO estudiante_id;
        -- Renombrar constraint si existe
        IF EXISTS (SELECT 1 FROM pg_constraint 
                   WHERE conname = 'student_profiles_student_id_fkey') THEN
            ALTER TABLE student_profiles RENAME CONSTRAINT student_profiles_student_id_fkey TO student_profiles_estudiante_id_fkey;
        END IF;
        -- Renombrar índice si existe
        IF EXISTS (SELECT 1 FROM pg_indexes 
                   WHERE tablename='student_profiles' AND indexname='ix_student_profiles_student_id') THEN
            ALTER INDEX ix_student_profiles_student_id RENAME TO ix_student_profiles_estudiante_id;
        END IF;
    END IF;
    
    -- Renombrar columnas del perfil
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='motivation') THEN
        ALTER TABLE student_profiles RENAME COLUMN motivation TO motivacion;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='available_time') THEN
        ALTER TABLE student_profiles RENAME COLUMN available_time TO tiempo_disponible;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='sleep_hours') THEN
        ALTER TABLE student_profiles RENAME COLUMN sleep_hours TO horas_sueno;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='study_hours') THEN
        ALTER TABLE student_profiles RENAME COLUMN study_hours TO horas_estudio;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='enjoyment_studying') THEN
        ALTER TABLE student_profiles RENAME COLUMN enjoyment_studying TO disfrute_estudio;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='study_place_tranquility') THEN
        ALTER TABLE student_profiles RENAME COLUMN study_place_tranquility TO tranquilidad_lugar_estudio;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='academic_pressure') THEN
        ALTER TABLE student_profiles RENAME COLUMN academic_pressure TO presion_academica;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='gender') THEN
        ALTER TABLE student_profiles RENAME COLUMN gender TO genero;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='created_at') THEN
        ALTER TABLE student_profiles RENAME COLUMN created_at TO fecha_creacion;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='student_profiles' AND column_name='updated_at') THEN
        ALTER TABLE student_profiles RENAME COLUMN updated_at TO fecha_actualizacion;
    END IF;
END $$;

COMMIT;

-- Verificar cambios
SELECT 'users' as tabla, column_name FROM information_schema.columns WHERE table_name='users' ORDER BY ordinal_position
UNION ALL
SELECT 'courses', column_name FROM information_schema.columns WHERE table_name='courses' ORDER BY ordinal_position
UNION ALL
SELECT 'tasks', column_name FROM information_schema.columns WHERE table_name='tasks' ORDER BY ordinal_position
UNION ALL
SELECT 'enrollments', column_name FROM information_schema.columns WHERE table_name='enrollments' ORDER BY ordinal_position
UNION ALL
SELECT 'submissions', column_name FROM information_schema.columns WHERE table_name='submissions' ORDER BY ordinal_position
UNION ALL
SELECT 'student_profiles', column_name FROM information_schema.columns WHERE table_name='student_profiles' ORDER BY ordinal_position;

