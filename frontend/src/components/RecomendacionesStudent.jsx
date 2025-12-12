// frontend/src/components/RecomendacionesStudent.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../services/api';

const RecomendacionesStudent = ({ studentId }) => {
    const [recomendaciones, setRecomendaciones] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all'); // 'all', 'unread', 'read'

    useEffect(() => {
        fetchRecomendaciones();
    }, [studentId, filter]);

    const fetchRecomendaciones = async () => {
        setLoading(true);
        setError(null);
        try {
            const endpoint = filter === 'unread' 
                ? '/recomendaciones/me?solo_no_vistas=true'
                : '/recomendaciones/me';
            
            const response = await apiClient.get(endpoint);
            setRecomendaciones(response.data || []);
        } catch (err) {
            console.error("Error al cargar recomendaciones:", err);
            setError(err.response?.data?.detail || "No se pudieron cargar las recomendaciones.");
        } finally {
            setLoading(false);
        }
    };

    const handleMarkAsViewed = async (recomendacionId) => {
        try {
            await apiClient.patch(`/recomendaciones/${recomendacionId}/view`);
            // Actualizar estado local
            setRecomendaciones(prev => prev.map(rec => 
                rec.id === recomendacionId 
                    ? { ...rec, vista: true, fecha_vista: new Date().toISOString() }
                    : rec
            ));
        } catch (err) {
            console.error("Error al marcar como vista:", err);
            alert(err.response?.data?.detail || "Error al actualizar la recomendación.");
        }
    };

    const handleDeleteRecomendacion = async (recomendacionId) => {
        // Confirmar antes de eliminar
        if (!window.confirm('¿Estás seguro de que quieres descartar esta recomendación? No podrás recuperarla.')) {
            return;
        }

        try {
            await apiClient.delete(`/recomendaciones/${recomendacionId}`);
            // Remover de la lista local
            setRecomendaciones(prev => prev.filter(rec => rec.id !== recomendacionId));
        } catch (err) {
            console.error("Error al eliminar recomendación:", err);
            alert(err.response?.data?.detail || "Error al eliminar la recomendación.");
        }
    };

    const getRecursoIcon = (tipo) => {
        const icons = {
            'video_youtube': '🎥',
            'pdf': '📄',
            'ejercicio_interactivo': '📝',
            'articulo': '📰'
        };
        return icons[tipo] || '📚';
    };

    const getNivelBadge = (nivel) => {
        const styles = {
            'básico': { bg: '#dbeafe', color: '#1e40af' },
            'intermedio': { bg: '#fef3c7', color: '#92400e' },
            'avanzado': { bg: '#fee2e2', color: '#991b1b' }
        };
        const style = styles[nivel] || styles['básico'];
        return (
            <span style={{
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                backgroundColor: style.bg,
                color: style.color,
                fontSize: '0.75rem',
                fontWeight: '500'
            }}>
                {nivel}
            </span>
        );
    };

    if (loading) {
        return (
            <div className="card">
                <div className="loading-container">
                    <div className="spinner"></div>
                    <span>Cargando recomendaciones...</span>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card">
                <div className="alert alert-error">
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    const recomendacionesNoVistas = recomendaciones.filter(r => !r.vista).length;

    return (
        <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ fontSize: '1.5rem', margin: 0 }}>
                    Recursos Recomendados
                    {recomendacionesNoVistas > 0 && (
                        <span style={{
                            marginLeft: '0.5rem',
                            padding: '0.25rem 0.5rem',
                            borderRadius: '12px',
                            backgroundColor: '#ef4444',
                            color: 'white',
                            fontSize: '0.875rem'
                        }}>
                            {recomendacionesNoVistas} nuevas
                        </span>
                    )}
                </h2>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                        onClick={() => setFilter('all')}
                        className={`btn btn-sm ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
                    >
                        Todas
                    </button>
                    <button
                        onClick={() => setFilter('unread')}
                        className={`btn btn-sm ${filter === 'unread' ? 'btn-primary' : 'btn-secondary'}`}
                    >
                        No vistas
                    </button>
                </div>
            </div>

            {recomendaciones.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '3rem 1rem' }}>
                    <p style={{ fontSize: '1.125rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                        {filter === 'unread' 
                            ? 'No tienes recomendaciones sin leer'
                            : 'Aún no tienes recomendaciones'}
                    </p>
                    <p style={{ fontSize: '0.875rem', color: '#9ca3af' }}>
                        {filter === 'unread'
                            ? 'Cuando obtengas una nota baja en una tarea, recibirás recursos recomendados aquí.'
                            : 'Las recomendaciones aparecerán aquí cuando necesites ayuda con alguna tarea.'}
                    </p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '1rem' }}>
                    {recomendaciones.map((rec) => {
                        const recurso = rec.recurso;
                        const tarea = rec.tarea;
                        
                        return (
                            <div
                                key={rec.id}
                                style={{
                                    border: rec.vista ? '1px solid #e5e7eb' : '2px solid #3b82f6',
                                    borderRadius: '8px',
                                    padding: '1rem',
                                    backgroundColor: rec.vista ? '#ffffff' : '#eff6ff',
                                    position: 'relative'
                                }}
                            >
                                {/* Indicador de "nueva" en la esquina superior izquierda */}
                                {!rec.vista && (
                                    <div style={{
                                        position: 'absolute',
                                        top: '0.5rem',
                                        left: '0.5rem',
                                        width: '12px',
                                        height: '12px',
                                        borderRadius: '50%',
                                        backgroundColor: '#ef4444'
                                    }}></div>
                                )}
                                
                                {/* Botón de descartar en la esquina superior derecha */}
                                <button
                                    onClick={() => handleDeleteRecomendacion(rec.id)}
                                    className="btn btn-danger btn-sm"
                                    title="Descartar esta recomendación"
                                    style={{
                                        position: 'absolute',
                                        top: '0.5rem',
                                        right: '0.5rem',
                                        padding: '0.375rem 0.5rem',
                                        fontSize: '0.875rem',
                                        minWidth: 'auto',
                                        lineHeight: '1',
                                        opacity: 0.8,
                                        transition: 'opacity 0.2s'
                                    }}
                                    onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
                                    onMouseLeave={(e) => e.currentTarget.style.opacity = '0.8'}
                                >
                                    🗑️
                                </button>
                                
                                <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start', paddingRight: '2rem' }}>
                                    <div style={{ fontSize: '2rem' }}>
                                        {recurso ? getRecursoIcon(recurso.tipo) : '📚'}
                                    </div>
                                    
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                                            <div>
                                                <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                                                    {recurso?.titulo || 'Recurso no disponible'}
                                                </h3>
                                                {tarea && (
                                                    <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                                                        Para la tarea: <strong>{tarea.titulo}</strong>
                                                    </p>
                                                )}
                                            </div>
                                            {recurso?.nivel_dificultad && getNivelBadge(recurso.nivel_dificultad)}
                                        </div>
                                        
                                        {recurso?.descripcion && (
                                            <p style={{ fontSize: '0.875rem', color: '#4b5563', marginBottom: '0.75rem' }}>
                                                {recurso.descripcion}
                                            </p>
                                        )}
                                        
                                        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '0.75rem' }}>
                                            {recurso?.url && (
                                                <a
                                                    href={recurso.url}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="btn btn-primary btn-sm"
                                                    onClick={() => !rec.vista && handleMarkAsViewed(rec.id)}
                                                >
                                                    {recurso.tipo === 'video_youtube' ? '▶️ Ver Video' : '📖 Abrir Recurso'}
                                                </a>
                                            )}
                                            {!rec.vista && (
                                                <button
                                                    onClick={() => handleMarkAsViewed(rec.id)}
                                                    className="btn btn-secondary btn-sm"
                                                >
                                                    Marcar como vista
                                                </button>
                                            )}
                                        </div>
                                        
                                        <div style={{ fontSize: '0.75rem', color: '#9ca3af' }}>
                                            Recomendado el {new Date(rec.fecha_recomendacion).toLocaleDateString('es-ES', {
                                                year: 'numeric',
                                                month: 'long',
                                                day: 'numeric',
                                                hour: '2-digit',
                                                minute: '2-digit'
                                            })}
                                            {rec.vista && rec.fecha_vista && (
                                                <span> · Vista el {new Date(rec.fecha_vista).toLocaleDateString('es-ES')}</span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default RecomendacionesStudent;

