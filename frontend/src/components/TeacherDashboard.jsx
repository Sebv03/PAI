// frontend/src/components/TeacherDashboard.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../services/api';
import CourseList from './CourseList'; // Este componente muestra la lista
import CourseCreationForm from './CourseCreationForm';
import ConceptosManager from './ConceptosManager';
import RecursosManager from './RecursosManager';
import { Link } from 'react-router-dom'; // Asegúrate de que Link esté importado

const TeacherDashboard = ({ user }) => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('courses'); // Tab inicial: 'courses', 'conceptos', 'recursos'

    const fetchCourses = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await apiClient.get('/courses/me');
            setCourses(response.data);
        } catch (err) {
            console.error("Error al cargar los cursos:", err);
            setError(err.response?.data?.detail || "No se pudieron cargar los cursos.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCourses();
    }, []);

    const handleCourseCreated = () => {
        fetchCourses();
    };

    return (
        <div className="animate-fadeIn">
            <div className="card card-gradient mb-xl animate-slideUp" style={{ 
                border: 'none',
                boxShadow: 'var(--shadow-2xl)'
            }}>
                <h1 className="text-white mb-md" style={{ 
                    fontSize: '2.5rem',
                    fontWeight: '800',
                    marginBottom: '0.75rem'
                }}>
                    Panel de Docente
                </h1>
                <p className="text-white" style={{ 
                    opacity: '0.95',
                    fontSize: '1rem',
                    lineHeight: '1.6'
                }}>
                    Gestiona tus cursos, conceptos y recursos educativos
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
                    <div className="card mb-xl bg-gradient-blue animate-slideUp" style={{ borderColor: '#bfdbfe' }}>
                        <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>Crear Nuevo Curso</h3>
                        <CourseCreationForm onCourseCreated={handleCourseCreated} />
                    </div>

                    <div className="card animate-slideUp">
                        <h3 style={{ fontSize: '1.75rem', marginBottom: '1.5rem' }}>Mis Cursos</h3>
                        {loading ? (
                            <div className="loading-container">
                                <div className="spinner"></div>
                                <span>Cargando cursos...</span>
                            </div>
                        ) : error ? (
                            <div className="alert alert-error">
                                <p>{error}</p>
                            </div>
                        ) : courses.length === 0 ? (
                            <div className="text-center" style={{ padding: '3rem' }}>
                                <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>No tienes cursos creados aún.</p>
                                <p style={{ fontSize: '0.875rem', color: 'var(--text-tertiary)' }}>Crea tu primer curso usando el formulario de arriba</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 grid-md-2 grid-lg-3 gap-lg">
                                {courses.map(course => (
                                    <div key={course.id} className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                                        <h4 style={{ fontSize: '1.25rem', color: 'var(--primary)', marginBottom: '0.5rem' }}>{course.titulo || course.title}</h4>
                                        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1rem', flex: 1, 
                                            display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                            {course.descripcion || course.description || 'Sin descripción'}
                                        </p>
                                        <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginBottom: '1rem' }}>
                                            <p>ID: {course.id}</p>
                                            <p>Creado el: {new Date(course.fecha_creacion || course.created_at).toLocaleDateString('es-ES')}</p>
                                        </div>
                                        
                                        <Link 
                                            to={`/courses/${course.id}`} 
                                            className="btn btn-success btn-full"
                                        >
                                            Ver Detalles / Tareas
                                        </Link>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </>
            )}

            {activeTab === 'conceptos' && (
                <div className="animate-slideUp">
                    <ConceptosManager />
                </div>
            )}

            {activeTab === 'recursos' && (
                <div className="animate-slideUp">
                    <RecursosManager />
                </div>
            )}
        </div>
    );
};

export default TeacherDashboard;