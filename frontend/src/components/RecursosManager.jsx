// frontend/src/components/RecursosManager.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../services/api';

const RecursosManager = () => {
    const [recursos, setRecursos] = useState([]);
    const [conceptos, setConceptos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showForm, setShowForm] = useState(false);
    const [editingRecurso, setEditingRecurso] = useState(null);
    
    const [formData, setFormData] = useState({
        titulo: '',
        tipo: 'video_youtube',
        url: '',
        ruta_archivo: '',
        descripcion: '',
        duracion_minutos: '',
        nivel_dificultad: 'básico',
        autor: '',
        concepto_ids: []
    });

    useEffect(() => {
        fetchRecursos();
        fetchConceptos();
    }, []);

    const fetchRecursos = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await apiClient.get('/recursos/?solo_activos=false');
            setRecursos(response.data);
        } catch (err) {
            console.error("Error al cargar recursos:", err);
            setError(err.response?.data?.detail || "No se pudieron cargar los recursos.");
        } finally {
            setLoading(false);
        }
    };

    const fetchConceptos = async () => {
        try {
            const response = await apiClient.get('/conceptos/');
            setConceptos(response.data);
        } catch (err) {
            console.error("Error al cargar conceptos:", err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        
        try {
            const dataToSend = {
                ...formData,
                duracion_minutos: formData.duracion_minutos ? parseInt(formData.duracion_minutos) : null
            };
            
            if (editingRecurso) {
                // Actualizar recurso existente
                await apiClient.put(`/recursos/${editingRecurso.id}`, dataToSend);
            } else {
                // Crear nuevo recurso
                if (formData.concepto_ids.length > 0) {
                    // Crear con conceptos
                    await apiClient.post('/recursos/with-concepts', {
                        ...dataToSend,
                        activo: true,
                        conceptos: {
                            concepto_ids: formData.concepto_ids
                        }
                    });
                } else {
                    await apiClient.post('/recursos/', { ...dataToSend, activo: true });
                }
            }
            
            // Limpiar formulario y recargar
            resetForm();
            fetchRecursos();
        } catch (err) {
            console.error("Error al guardar recurso:", err);
            setError(err.response?.data?.detail || "Error al guardar el recurso.");
        }
    };

    const resetForm = () => {
        setFormData({
            titulo: '',
            tipo: 'video_youtube',
            url: '',
            ruta_archivo: '',
            descripcion: '',
            duracion_minutos: '',
            nivel_dificultad: 'básico',
            autor: '',
            concepto_ids: []
        });
        setShowForm(false);
        setEditingRecurso(null);
    };

    const handleEdit = (recurso) => {
        setEditingRecurso(recurso);
        setFormData({
            titulo: recurso.titulo || '',
            tipo: recurso.tipo || 'video_youtube',
            url: recurso.url || '',
            ruta_archivo: recurso.ruta_archivo || '',
            descripcion: recurso.descripcion || '',
            duracion_minutos: recurso.duracion_minutos?.toString() || '',
            nivel_dificultad: recurso.nivel_dificultad || 'básico',
            autor: recurso.autor || '',
            concepto_ids: [] // TODO: Cargar conceptos asociados
        });
        setShowForm(true);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Estás seguro de eliminar este recurso?')) {
            return;
        }
        
        try {
            await apiClient.delete(`/recursos/${id}`);
            fetchRecursos();
        } catch (err) {
            console.error("Error al eliminar recurso:", err);
            alert(err.response?.data?.detail || "Error al eliminar el recurso.");
        }
    };

    const handleToggleActivo = async (id) => {
        try {
            await apiClient.patch(`/recursos/${id}/toggle-activo`);
            fetchRecursos();
        } catch (err) {
            console.error("Error al cambiar estado:", err);
            alert(err.response?.data?.detail || "Error al cambiar el estado.");
        }
    };

    const handleConceptoToggle = (conceptoId) => {
        setFormData(prev => ({
            ...prev,
            concepto_ids: prev.concepto_ids.includes(conceptoId)
                ? prev.concepto_ids.filter(id => id !== conceptoId)
                : [...prev.concepto_ids, conceptoId]
        }));
    };

    if (loading) {
        return <div className="loading-container"><div className="spinner"></div><span>Cargando recursos...</span></div>;
    }

    return (
        <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ fontSize: '1.5rem', margin: 0 }}>Gestión de Recursos</h2>
                {!showForm && (
                    <button
                        onClick={() => setShowForm(true)}
                        className="btn btn-primary"
                    >
                        + Nuevo Recurso
                    </button>
                )}
            </div>

            {error && (
                <div className="alert alert-error" style={{ marginBottom: '1rem' }}>
                    <p>{error}</p>
                </div>
            )}

            {showForm && (
                <form onSubmit={handleSubmit} className="card" style={{ marginBottom: '1.5rem', background: '#f9fafb' }}>
                    <h3 style={{ marginBottom: '1rem' }}>
                        {editingRecurso ? 'Editar Recurso' : 'Nuevo Recurso'}
                    </h3>
                    <div style={{ display: 'grid', gap: '1rem' }}>
                        <div>
                            <label htmlFor="titulo" style={{ display: 'block', marginBottom: '0.5rem' }}>
                                Título <span style={{ color: 'red' }}>*</span>
                            </label>
                            <input
                                type="text"
                                id="titulo"
                                value={formData.titulo}
                                onChange={(e) => setFormData({ ...formData, titulo: e.target.value })}
                                required
                                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                            />
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div>
                                <label htmlFor="tipo" style={{ display: 'block', marginBottom: '0.5rem' }}>
                                    Tipo <span style={{ color: 'red' }}>*</span>
                                </label>
                                <select
                                    id="tipo"
                                    value={formData.tipo}
                                    onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
                                    required
                                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                >
                                    <option value="video_youtube">Video YouTube</option>
                                    <option value="pdf">PDF</option>
                                    <option value="ejercicio_interactivo">Ejercicio Interactivo</option>
                                    <option value="articulo">Artículo</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="nivel_dificultad" style={{ display: 'block', marginBottom: '0.5rem' }}>Nivel de Dificultad</label>
                                <select
                                    id="nivel_dificultad"
                                    value={formData.nivel_dificultad}
                                    onChange={(e) => setFormData({ ...formData, nivel_dificultad: e.target.value })}
                                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                >
                                    <option value="básico">Básico</option>
                                    <option value="intermedio">Intermedio</option>
                                    <option value="avanzado">Avanzado</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label htmlFor="url" style={{ display: 'block', marginBottom: '0.5rem' }}>URL</label>
                            <input
                                type="url"
                                id="url"
                                value={formData.url}
                                onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                                placeholder="https://..."
                                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                            />
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div>
                                <label htmlFor="duracion_minutos" style={{ display: 'block', marginBottom: '0.5rem' }}>Duración (minutos)</label>
                                <input
                                    type="number"
                                    id="duracion_minutos"
                                    value={formData.duracion_minutos}
                                    onChange={(e) => setFormData({ ...formData, duracion_minutos: e.target.value })}
                                    min="0"
                                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                />
                            </div>
                            <div>
                                <label htmlFor="autor" style={{ display: 'block', marginBottom: '0.5rem' }}>Autor</label>
                                <input
                                    type="text"
                                    id="autor"
                                    value={formData.autor}
                                    onChange={(e) => setFormData({ ...formData, autor: e.target.value })}
                                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                />
                            </div>
                        </div>
                        <div>
                            <label htmlFor="descripcion" style={{ display: 'block', marginBottom: '0.5rem' }}>Descripción</label>
                            <textarea
                                id="descripcion"
                                value={formData.descripcion}
                                onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', minHeight: '80px' }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem' }}>Conceptos Asociados</label>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.5rem', maxHeight: '150px', overflowY: 'auto', border: '1px solid #ccc', padding: '0.5rem', borderRadius: '4px' }}>
                                {conceptos.map(concepto => (
                                    <label key={concepto.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                                        <input
                                            type="checkbox"
                                            checked={formData.concepto_ids.includes(concepto.id)}
                                            onChange={() => handleConceptoToggle(concepto.id)}
                                        />
                                        <span>{concepto.nombre}</span>
                                    </label>
                                ))}
                            </div>
                        </div>
                        <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                            <button type="button" onClick={resetForm} className="btn btn-secondary">
                                Cancelar
                            </button>
                            <button type="submit" className="btn btn-primary">
                                {editingRecurso ? 'Actualizar' : 'Crear'}
                            </button>
                        </div>
                    </div>
                </form>
            )}

            {recursos.length === 0 ? (
                <p className="text-center py-8 text-gray-500 italic">
                    No hay recursos registrados. Crea el primero haciendo clic en "Nuevo Recurso".
                </p>
            ) : (
                <div className="table-responsive">
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Título</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Tipo</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Nivel</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Estado</th>
                                <th style={{ padding: '0.75rem', textAlign: 'right' }}>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recursos.map((recurso) => (
                                <tr key={recurso.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                                    <td style={{ padding: '0.75rem' }}><strong>{recurso.titulo}</strong></td>
                                    <td style={{ padding: '0.75rem' }}>{recurso.tipo}</td>
                                    <td style={{ padding: '0.75rem' }}>{recurso.nivel_dificultad || '-'}</td>
                                    <td style={{ padding: '0.75rem' }}>
                                        <span style={{ 
                                            padding: '0.25rem 0.5rem', 
                                            borderRadius: '4px',
                                            backgroundColor: recurso.activo ? '#d1fae5' : '#fee2e2',
                                            color: recurso.activo ? '#065f46' : '#991b1b',
                                            fontSize: '0.875rem'
                                        }}>
                                            {recurso.activo ? 'Activo' : 'Inactivo'}
                                        </span>
                                    </td>
                                    <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                                        <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                                            <button
                                                onClick={() => handleToggleActivo(recurso.id)}
                                                className={`btn btn-sm ${recurso.activo ? 'btn-warning' : 'btn-success'}`}
                                            >
                                                {recurso.activo ? 'Desactivar' : 'Activar'}
                                            </button>
                                            <button
                                                onClick={() => handleEdit(recurso)}
                                                className="btn btn-secondary btn-sm"
                                            >
                                                Editar
                                            </button>
                                            <button
                                                onClick={() => handleDelete(recurso.id)}
                                                className="btn btn-danger btn-sm"
                                            >
                                                Eliminar
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default RecursosManager;




