-- Script de migración para cambiar todas las columnas a español
-- IMPORTANTE: Hacer backup antes de ejecutar

BEGIN;

-- ============================================
-- TABLA: users -> usuarios (mantener nombre tabla en inglés por convención)
-- ============================================
ALTER TABLE users RENAME COLUMN email TO correo;
ALTER TABLE users RENAME COLUMN hashed_password TO contraseña_hash;
ALTER TABLE users RENAME COLUMN full_name TO nombre_completo;
ALTER TABLE users RENAME COLUMN role TO rol;
ALTER TABLE users RENAME COLUMN is_active TO activo;

-- ============================================
-- TABLA: courses -> cursos
-- ============================================
ALTER TABLE courses RENAME COLUMN title TO titulo;
ALTER TABLE courses RENAME COLUMN description TO descripcion;
ALTER TABLE courses RENAME COLUMN owner_id TO propietario_id;
ALTER TABLE courses RENAME COLUMN created_at TO fecha_creacion;

-- Actualizar foreign key constraint
ALTER TABLE courses RENAME CONSTRAINT courses_owner_id_fkey TO courses_propietario_id_fkey;

-- ============================================
-- TABLA: tasks -> tareas
-- ============================================
ALTER TABLE tasks RENAME COLUMN title TO titulo;
ALTER TABLE tasks RENAME COLUMN description TO descripcion;
ALTER TABLE tasks RENAME COLUMN due_date TO fecha_limite;
ALTER TABLE tasks RENAME COLUMN course_id TO curso_id;
ALTER TABLE tasks RENAME COLUMN created_at TO fecha_creacion;

-- Actualizar foreign key constraint
ALTER TABLE tasks RENAME CONSTRAINT tasks_course_id_fkey TO tasks_curso_id_fkey;

-- Actualizar índices
DROP INDEX IF EXISTS ix_tasks_title;
CREATE INDEX IF NOT EXISTS ix_tasks_titulo ON tasks(titulo);

-- ============================================
-- TABLA: enrollments -> inscripciones
-- ============================================
ALTER TABLE enrollments RENAME COLUMN student_id TO estudiante_id;
ALTER TABLE enrollments RENAME COLUMN course_id TO curso_id;
ALTER TABLE enrollments RENAME COLUMN enrollment_date TO fecha_inscripcion;

-- Actualizar foreign key constraints
ALTER TABLE enrollments RENAME CONSTRAINT enrollments_student_id_fkey TO enrollments_estudiante_id_fkey;
ALTER TABLE enrollments RENAME CONSTRAINT enrollments_course_id_fkey TO enrollments_curso_id_fkey;

-- ============================================
-- TABLA: submissions -> entregas
-- ============================================
ALTER TABLE submissions RENAME COLUMN content TO contenido;
ALTER TABLE submissions RENAME COLUMN file_path TO ruta_archivo;
ALTER TABLE submissions RENAME COLUMN grade TO calificacion;
ALTER TABLE submissions RENAME COLUMN feedback TO retroalimentacion;
ALTER TABLE submissions RENAME COLUMN submitted_at TO fecha_entrega;
ALTER TABLE submissions RENAME COLUMN student_id TO estudiante_id;
ALTER TABLE submissions RENAME COLUMN task_id TO tarea_id;

-- Actualizar foreign key constraints
ALTER TABLE submissions RENAME CONSTRAINT submissions_task_id_fkey TO submissions_tarea_id_fkey;
ALTER TABLE submissions RENAME CONSTRAINT submissions_user_id_fkey TO submissions_estudiante_id_fkey;

-- ============================================
-- TABLA: student_profiles -> perfiles_estudiantes
-- ============================================
ALTER TABLE student_profiles RENAME COLUMN student_id TO estudiante_id;
ALTER TABLE student_profiles RENAME COLUMN motivation TO motivacion;
ALTER TABLE student_profiles RENAME COLUMN available_time TO tiempo_disponible;
ALTER TABLE student_profiles RENAME COLUMN sleep_hours TO horas_sueno;
ALTER TABLE student_profiles RENAME COLUMN study_hours TO horas_estudio;
ALTER TABLE student_profiles RENAME COLUMN enjoyment_studying TO disfrute_estudio;
ALTER TABLE student_profiles RENAME COLUMN study_place_tranquility TO tranquilidad_lugar_estudio;
ALTER TABLE student_profiles RENAME COLUMN academic_pressure TO presion_academica;
ALTER TABLE student_profiles RENAME COLUMN gender TO genero;
ALTER TABLE student_profiles RENAME COLUMN created_at TO fecha_creacion;
ALTER TABLE student_profiles RENAME COLUMN updated_at TO fecha_actualizacion;

-- Actualizar foreign key constraint
ALTER TABLE student_profiles RENAME CONSTRAINT student_profiles_student_id_fkey TO student_profiles_estudiante_id_fkey;

-- Actualizar índices
DROP INDEX IF EXISTS ix_student_profiles_student_id;
CREATE INDEX IF NOT EXISTS ix_student_profiles_estudiante_id ON student_profiles(estudiante_id);

-- ============================================
-- TABLA: announcements -> anuncios
-- ============================================
ALTER TABLE announcements RENAME COLUMN title TO titulo;
ALTER TABLE announcements RENAME COLUMN content TO contenido;
ALTER TABLE announcements RENAME COLUMN course_id TO curso_id;
ALTER TABLE announcements RENAME COLUMN author_id TO autor_id;
ALTER TABLE announcements RENAME COLUMN created_at TO fecha_creacion;
ALTER TABLE announcements RENAME COLUMN updated_at TO fecha_actualizacion;

-- Actualizar foreign key constraints
ALTER TABLE announcements RENAME CONSTRAINT announcements_course_id_fkey TO announcements_curso_id_fkey;
ALTER TABLE announcements RENAME CONSTRAINT announcements_author_id_fkey TO announcements_autor_id_fkey;

-- ============================================
-- TABLA: comments -> comentarios
-- ============================================
ALTER TABLE comments RENAME COLUMN content TO contenido;
ALTER TABLE comments RENAME COLUMN announcement_id TO anuncio_id;
ALTER TABLE comments RENAME COLUMN author_id TO autor_id;
ALTER TABLE comments RENAME COLUMN created_at TO fecha_creacion;

-- Actualizar foreign key constraints
ALTER TABLE comments RENAME CONSTRAINT comments_announcement_id_fkey TO comments_anuncio_id_fkey;
ALTER TABLE comments RENAME CONSTRAINT comments_author_id_fkey TO comments_autor_id_fkey;

COMMIT;

