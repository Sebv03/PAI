// frontend/src/components/ConceptosManager.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../services/api';

const ConceptosManager = () => {
    const [conceptos, setConceptos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showForm, setShowForm] = useState(false);
    const [editingConcepto, setEditingConcepto] = useState(null);
    
    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        categoria: '',
        nivel: ''
    });

    useEffect(() => {
        fetchConceptos();
    }, []);

    const fetchConceptos = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await apiClient.get('/conceptos/');
            setConceptos(response.data);
        } catch (err) {
            console.error("Error al cargar conceptos:", err);
            setError(err.response?.data?.detail || "No se pudieron cargar los conceptos.");
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        
        try {
            if (editingConcepto) {
                // Actualizar concepto existente
                await apiClient.put(`/conceptos/${editingConcepto.id}`, formData);
            } else {
                // Crear nuevo concepto
                await apiClient.post('/conceptos/', formData);
            }
            
            // Limpiar formulario y recargar
            setFormData({ nombre: '', descripcion: '', categoria: '', nivel: '' });
            setShowForm(false);
            setEditingConcepto(null);
            fetchConceptos();
        } catch (err) {
            console.error("Error al guardar concepto:", err);
            setError(err.response?.data?.detail || "Error al guardar el concepto.");
        }
    };

    const handleEdit = (concepto) => {
        setEditingConcepto(concepto);
        setFormData({
            nombre: concepto.nombre || '',
            descripcion: concepto.descripcion || '',
            categoria: concepto.categoria || '',
            nivel: concepto.nivel || ''
        });
        setShowForm(true);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Estás seguro de eliminar este concepto?')) {
            return;
        }
        
        try {
            await apiClient.delete(`/conceptos/${id}`);
            fetchConceptos();
        } catch (err) {
            console.error("Error al eliminar concepto:", err);
            alert(err.response?.data?.detail || "Error al eliminar el concepto.");
        }
    };

    const handleCancel = () => {
        setShowForm(false);
        setEditingConcepto(null);
        setFormData({ nombre: '', descripcion: '', categoria: '', nivel: '' });
    };

    if (loading) {
        return <div className="loading-container"><div className="spinner"></div><span>Cargando conceptos...</span></div>;
    }

    return (
        <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ fontSize: '1.5rem', margin: 0 }}>Gestión de Conceptos</h2>
                {!showForm && (
                    <button
                        onClick={() => setShowForm(true)}
                        className="btn btn-primary"
                    >
                        + Nuevo Concepto
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
                        {editingConcepto ? 'Editar Concepto' : 'Nuevo Concepto'}
                    </h3>
                    <div style={{ display: 'grid', gap: '1rem' }}>
                        <div>
                            <label htmlFor="nombre" style={{ display: 'block', marginBottom: '0.5rem' }}>
                                Nombre <span style={{ color: 'red' }}>*</span>
                            </label>
                            <input
                                type="text"
                                id="nombre"
                                value={formData.nombre}
                                onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                                required
                                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                            />
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
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div>
                                <label htmlFor="categoria" style={{ display: 'block', marginBottom: '0.5rem' }}>Categoría</label>
                                <input
                                    type="text"
                                    id="categoria"
                                    value={formData.categoria}
                                    onChange={(e) => setFormData({ ...formData, categoria: e.target.value })}
                                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                    placeholder="Ej: Álgebra, Geometría"
                                />
                            </div>
                            <div>
                                <label htmlFor="nivel" style={{ display: 'block', marginBottom: '0.5rem' }}>Nivel</label>
                                <input
                                    type="text"
                                    id="nivel"
                                    value={formData.nivel}
                                    onChange={(e) => setFormData({ ...formData, nivel: e.target.value })}
                                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                    placeholder="Ej: 1° medio, 2° medio"
                                />
                            </div>
                        </div>
                        <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                            <button type="button" onClick={handleCancel} className="btn btn-secondary">
                                Cancelar
                            </button>
                            <button type="submit" className="btn btn-primary">
                                {editingConcepto ? 'Actualizar' : 'Crear'}
                            </button>
                        </div>
                    </div>
                </form>
            )}

            {conceptos.length === 0 ? (
                <p className="text-center py-8 text-gray-500 italic">
                    No hay conceptos registrados. Crea el primero haciendo clic en "Nuevo Concepto".
                </p>
            ) : (
                <div className="table-responsive">
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Nombre</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Categoría</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Nivel</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Descripción</th>
                                <th style={{ padding: '0.75rem', textAlign: 'right' }}>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {conceptos.map((concepto) => (
                                <tr key={concepto.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                                    <td style={{ padding: '0.75rem' }}><strong>{concepto.nombre}</strong></td>
                                    <td style={{ padding: '0.75rem' }}>{concepto.categoria || '-'}</td>
                                    <td style={{ padding: '0.75rem' }}>{concepto.nivel || '-'}</td>
                                    <td style={{ padding: '0.75rem' }}>{concepto.descripcion || '-'}</td>
                                    <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                                        <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                                            <button
                                                onClick={() => handleEdit(concepto)}
                                                className="btn btn-secondary btn-sm"
                                            >
                                                Editar
                                            </button>
                                            <button
                                                onClick={() => handleDelete(concepto.id)}
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

export default ConceptosManager;




