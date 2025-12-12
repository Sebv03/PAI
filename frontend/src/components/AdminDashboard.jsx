// frontend/src/components/AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../services/api';
import ConceptosManager from './ConceptosManager';
import RecursosManager from './RecursosManager';


const AdminDashboard = ({ user }) => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    // Student Management State
    const [showStudentsModal, setShowStudentsModal] = useState(false);
    const [selectedCourseForStudents, setSelectedCourseForStudents] = useState(null);
    const [courseStudents, setCourseStudents] = useState([]);
    const [loadingStudents, setLoadingStudents] = useState(false);

    const [deletingCourse, setDeletingCourse] = useState(null); // ID del curso que se está eliminando
    const [activeTab, setActiveTab] = useState('courses'); // Tab inicial: 'courses', 'conceptos', 'recursos'

    const fetchCourses = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await apiClient.get('/courses/');
            setCourses(response.data);
        } catch (err) {
            console.error("Error al cargar datos:", err);
            // setError(err.response?.data?.detail || "No se pudieron cargar los datos.");
        } finally {
            setLoading(false);
        }
    };



    // Handlers para Gestión de Estudiantes
    const handleViewStudents = async (course) => {
        setSelectedCourseForStudents(course);
        setShowStudentsModal(true);
        setLoadingStudents(true);
        try {
            const response = await apiClient.get(`/enrollments/course/${course.id}/students`);
            setCourseStudents(response.data);
        } catch (error) {
            console.error("Error fetching students:", error);
            alert("Error al cargar estudiantes");
        } finally {
            setLoadingStudents(false);
        }
    };

    const handleRemoveStudent = async (studentId) => {
        if (!window.confirm("¿Seguro que deseas eliminar a este estudiante del curso?")) return;

        try {
            await apiClient.delete(`/enrollments/course/${selectedCourseForStudents.id}/student/${studentId}`);
            // Recargar lista
            const response = await apiClient.get(`/enrollments/course/${selectedCourseForStudents.id}/students`);
            setCourseStudents(response.data);
        } catch (error) {
            console.error("Error removing student:", error);
            alert("Error al eliminar estudiante");
        }
    };

    const closeStudentsModal = () => {
        setShowStudentsModal(false);
        setSelectedCourseForStudents(null);
        setCourseStudents([]);
    };

    const handleEditCourse = (course) => {
        // Por ahora, solo un alert, o redirigir a un modal de edición si existiera
        const newTitle = prompt("Editar título del curso:", course.titulo);
        if (newTitle && newTitle !== course.titulo) {
            // Lógica de update simple (opcional)
            apiClient.put(`/courses/${course.id}`, { ...course, titulo: newTitle })
                .then(() => fetchCourses())
                .catch(err => alert("Error al editar: " + err.message));
        }
    };

    // Eliminar un curso
    const handleDeleteCourse = async (courseId) => {
        const course = courses.find(c => c.id === courseId);
        const courseTitle = course?.titulo || course?.title || 'este curso';

        // Confirmar eliminación
        const confirmed = window.confirm(
            `¿Estás seguro de que deseas eliminar el curso "${courseTitle}"?\n\n` +
            `Esta acción eliminará:\n` +
            `- Todas las tareas del curso\n` +
            `- Todas las inscripciones\n` +
            `- Todos los anuncios y comentarios\n` +
            `- Todas las entregas asociadas\n\n` +
            `Esta acción NO se puede deshacer.`
        );

        if (!confirmed) {
            return;
        }

        setDeletingCourse(courseId);
        try {
            await apiClient.delete(`/courses/${courseId}`);

            // Si el curso seleccionado era el que se está eliminando, cerrar el panel de predicciones


            // Recargar lista de cursos
            await fetchCourses();

            alert(`Curso "${courseTitle}" eliminado exitosamente.`);
        } catch (err) {
            console.error("Error al eliminar curso:", err);
            alert("Error al eliminar curso: " + (err.response?.data?.detail || err.message));
        } finally {
            setDeletingCourse(null);
        }
    };

    useEffect(() => {
        fetchCourses();
    }, []);



    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Cargando cursos...</p>
            </div>
        );
    }

    return (
        <div className="animate-fadeIn">
            <div className="card card-gradient mb-xl animate-slideUp" style={{
                border: 'none',
                boxShadow: 'var(--shadow-2xl)',
                background: 'var(--primary-gradient)'
            }}>
                <h1 className="mb-md" style={{
                    fontSize: '2.5rem',
                    fontWeight: '800',
                    marginBottom: '0.75rem',
                    color: '#ffffff',
                    textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
                    WebkitTextFillColor: '#ffffff',
                    background: 'none',
                    WebkitBackgroundClip: 'unset',
                    backgroundClip: 'unset'
                }}>
                    Dashboard de Administrador
                </h1>
                <p style={{
                    opacity: 0.95,
                    fontSize: '1rem',
                    lineHeight: '1.6',
                    color: '#ffffff',
                    textShadow: '1px 1px 2px rgba(0, 0, 0, 0.3)'
                }}>
                </p>
            </div>



            {error && (
                <div className="alert alert-error mb-lg animate-fadeIn">
                    <p style={{ margin: 0 }}>{error}</p>
                </div>
            )}

            {/* Tabs de Navegación Modernos */}
            <div className="card mb-lg animate-slideUp">
                <div style={{
                    display: 'flex',
                    gap: '0.5rem',
                    borderBottom: '2px solid var(--border-color-light)',
                    marginBottom: '1rem'
                }}>
                    <button
                        onClick={() => setActiveTab('courses')}
                        className="btn-tab"
                        style={{
                            padding: '0.875rem 1.75rem',
                            border: 'none',
                            background: activeTab === 'courses' ? 'var(--primary-gradient)' : 'transparent',
                            color: activeTab === 'courses' ? 'white' : 'var(--text-secondary)',
                            fontWeight: activeTab === 'courses' ? '700' : '500',
                            cursor: 'pointer',
                            transition: 'all var(--transition-base)',
                            borderRadius: 'var(--border-radius) var(--border-radius) 0 0',
                            borderBottom: activeTab === 'courses' ? '3px solid transparent' : '3px solid transparent',
                            position: 'relative',
                            bottom: '-2px'
                        }}
                        onMouseEnter={(e) => {
                            if (activeTab !== 'courses') {
                                e.currentTarget.style.background = 'var(--bg-tertiary)';
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (activeTab !== 'courses') {
                                e.currentTarget.style.background = 'transparent';
                            }
                        }}
                    >
                        📚 Cursos
                    </button>
                    <button
                        onClick={() => setActiveTab('conceptos')}
                        className="btn-tab"
                        style={{
                            padding: '0.875rem 1.75rem',
                            border: 'none',
                            background: activeTab === 'conceptos' ? 'var(--primary-gradient)' : 'transparent',
                            color: activeTab === 'conceptos' ? 'white' : 'var(--text-secondary)',
                            fontWeight: activeTab === 'conceptos' ? '700' : '500',
                            cursor: 'pointer',
                            transition: 'all var(--transition-base)',
                            borderRadius: 'var(--border-radius) var(--border-radius) 0 0',
                            borderBottom: activeTab === 'conceptos' ? '3px solid transparent' : '3px solid transparent',
                            position: 'relative',
                            bottom: '-2px'
                        }}
                        onMouseEnter={(e) => {
                            if (activeTab !== 'conceptos') {
                                e.currentTarget.style.background = 'var(--bg-tertiary)';
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (activeTab !== 'conceptos') {
                                e.currentTarget.style.background = 'transparent';
                            }
                        }}
                    >
                        💡 Conceptos
                    </button>
                    <button
                        onClick={() => setActiveTab('recursos')}
                        className="btn-tab"
                        style={{
                            padding: '0.875rem 1.75rem',
                            border: 'none',
                            background: activeTab === 'recursos' ? 'var(--primary-gradient)' : 'transparent',
                            color: activeTab === 'recursos' ? 'white' : 'var(--text-secondary)',
                            fontWeight: activeTab === 'recursos' ? '700' : '500',
                            cursor: 'pointer',
                            transition: 'all var(--transition-base)',
                            borderRadius: 'var(--border-radius) var(--border-radius) 0 0',
                            borderBottom: activeTab === 'recursos' ? '3px solid transparent' : '3px solid transparent',
                            position: 'relative',
                            bottom: '-2px'
                        }}
                        onMouseEnter={(e) => {
                            if (activeTab !== 'recursos') {
                                e.currentTarget.style.background = 'var(--bg-tertiary)';
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (activeTab !== 'recursos') {
                                e.currentTarget.style.background = 'transparent';
                            }
                        }}
                    >
                        📖 Recursos
                    </button>
                </div>
            </div>

            {/* Contenido según tab activo */}
            {activeTab === 'courses' && (
                <>
                    {/* Lista de Cursos */}
                    <div className="card mb-lg">
                        <h2 className="text-xl font-semibold mb-4">Todos los Cursos ({courses.length})</h2>

                        {courses.length === 0 ? (
                            <p className="text-center py-8 text-gray-500 italic">
                                No hay cursos en la plataforma
                            </p>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {courses.map((course) => (
                                    <div
                                        key={course.id}
                                        className="card hover:shadow-lg transition-shadow duration-200"
                                        style={{ cursor: 'pointer' }}
                                    >
                                        <div className="flex flex-col flex-1 mb-4">
                                            <h3 className="text-xl font-bold text-blue-600 mb-2">
                                                {course.titulo || course.title}
                                            </h3>
                                            <p className="text-sm text-gray-600 line-clamp-3 mb-4">
                                                {course.descripcion || course.description || 'Sin descripción'}
                                            </p>
                                            <div className="space-y-1 text-xs text-gray-500">
                                                <p><strong>Docente:</strong> {course.propietario_nombre || course.owner_name || 'N/A'}</p>
                                                <p><strong>Creado:</strong> {(course.fecha_creacion || course.created_at) ? new Date(course.fecha_creacion || course.created_at).toLocaleDateString() : 'N/A'}</p>
                                            </div>
                                        </div>
                                        <div className="flex gap-2 justify-end mt-4">
                                            <button
                                                onClick={() => handleViewStudents(course)}
                                                className="btn btn-secondary btn-sm"
                                                title="Ver estudiantes"
                                            >
                                                👥
                                            </button>
                                            <button
                                                onClick={() => handleEditCourse(course)}
                                                className="btn btn-primary btn-sm"
                                                title="Editar curso"
                                            >
                                                ✏️
                                            </button>
                                            <button
                                                onClick={() => handleDeleteCourse(course.id)}
                                                disabled={deletingCourse === course.id}
                                                className="btn btn-danger btn-sm"
                                                title="Eliminar curso"
                                            >
                                                {deletingCourse === course.id ? '...' : '🗑️'}
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>


                </>
            )}

            {/* MODAL GESTIÓN ESTUDIANTES */}
            {showStudentsModal && selectedCourseForStudents && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 animate-fadeIn">
                    <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-xl font-bold">Estudiantes en: {selectedCourseForStudents.titulo}</h3>
                            <button onClick={closeStudentsModal} className="text-gray-500 hover:text-gray-700 text-xl">
                                ✕
                            </button>
                        </div>

                        {loadingStudents ? (
                            <div className="flex flex-col items-center justify-center py-12">
                                <div className="spinner mb-4"></div>
                                <p className="text-gray-500">Cargando lista de estudiantes...</p>
                            </div>
                        ) : courseStudents.length === 0 ? (
                            <div className="text-center py-12">
                                <div className="text-6xl mb-4">🎓</div>
                                <p className="text-gray-500 text-lg">No hay estudiantes inscritos en este curso.</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 gap-4">
                                {courseStudents.map(student => (
                                    <div
                                        key={student.id}
                                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:shadow-md transition-all border border-gray-100"
                                    >
                                        <div className="flex items-center gap-4">
                                            <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-lg">
                                                {student.full_name ? student.full_name.charAt(0).toUpperCase() : '?'}
                                            </div>
                                            <div>
                                                <h4 className="font-bold text-gray-800">{student.full_name || 'Sin Nombre'}</h4>
                                                <p className="text-sm text-gray-500">{student.email}</p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => handleRemoveStudent(student.id)}
                                            className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                                            title="Eliminar estudiante"
                                        >
                                            🗑️
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}

                        <div className="mt-6 text-right">
                            <button onClick={closeStudentsModal} className="btn btn-secondary">
                                Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {activeTab === 'conceptos' && (
                <ConceptosManager />
            )}

            {activeTab === 'recursos' && (
                <RecursosManager />
            )}


        </div>
    );
};

export default AdminDashboard;

