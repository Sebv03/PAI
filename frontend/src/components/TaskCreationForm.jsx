// frontend/src/components/TaskCreationForm.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../services/api';

const TaskCreationForm = ({ courseId, onTaskCreated }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [dueDate, setDueDate] = useState(''); // Formato "YYYY-MM-DDTHH:mm" para input datetime-local
    const [selectedConcepts, setSelectedConcepts] = useState([]); // IDs de conceptos seleccionados
    const [conceptos, setConceptos] = useState([]); // Lista de conceptos disponibles
    const [loadingConceptos, setLoadingConceptos] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false);

    // Cargar conceptos disponibles al montar el componente
    useEffect(() => {
        const fetchConceptos = async () => {
            setLoadingConceptos(true);
            try {
                const response = await apiClient.get('/conceptos/');
                setConceptos(response.data || []);
            } catch (err) {
                console.error("Error al cargar conceptos:", err);
                // No mostrar error al usuario, simplemente no habrá conceptos disponibles
            } finally {
                setLoadingConceptos(false);
            }
        };
        fetchConceptos();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(false);
        setLoading(true);

        // Validar campos
        if (!title || !dueDate) {
            setError("El título y la fecha límite son obligatorios.");
            setLoading(false);
            return;
        }

        // Convertir la fecha al formato ISO 8601 que el backend espera
        // El input datetime-local da formato "YYYY-MM-DDTHH:mm"
        // Necesitamos convertirlo a ISO 8601 completo: "YYYY-MM-DDTHH:mm:ss"
        let formattedDueDate;
        
        try {
            // Crear un objeto Date desde el valor del input
            const dateObj = new Date(dueDate);
            
            // Validar que la fecha sea válida
            if (isNaN(dateObj.getTime())) {
                setError("La fecha ingresada no es válida.");
                setLoading(false);
                return;
            }
            
            // Convertir a ISO string y tomar solo la parte de fecha/hora (sin timezone)
            // Formato: "YYYY-MM-DDTHH:mm:ss"
            formattedDueDate = dateObj.toISOString().slice(0, 19);
            
            console.log('Fecha original:', dueDate);
            console.log('Fecha formateada:', formattedDueDate);
        } catch (dateError) {
            console.error("Error al formatear la fecha:", dateError);
            setError("Error al procesar la fecha. Por favor, verifica el formato.");
            setLoading(false);
            return;
        }
        
        try {
            const newTask = {
                titulo: title,
                descripcion: description || null, // Asegurar que sea null si está vacío
                fecha_limite: formattedDueDate,
                course_id: courseId
            };
            
            console.log('Enviando tarea al servidor:', newTask);
            
            const response = await apiClient.post('/tasks/', newTask);
            console.log("Tarea creada:", response.data);
            
            // Asociar conceptos a la tarea si se seleccionaron
            if (selectedConcepts.length > 0) {
                try {
                    await apiClient.post(`/tasks/${response.data.id}/conceptos`, {
                        concepto_ids: selectedConcepts
                    });
                    console.log(`Conceptos asociados a la tarea ${response.data.id}`);
                } catch (conceptErr) {
                    console.error("Error al asociar conceptos:", conceptErr);
                    // No fallar la creación de la tarea si falla asociar conceptos
                    // Solo mostrar un warning
                    setError((prev) => prev ? prev + " (Nota: La tarea se creó pero hubo un error al asociar conceptos)" : "La tarea se creó pero hubo un error al asociar conceptos. Puedes asociarlos manualmente más tarde.");
                }
            }
            
            setSuccess(true);
            setTitle('');
            setDescription('');
            setDueDate('');
            setSelectedConcepts([]);
            if (onTaskCreated) {
                onTaskCreated(); // Notifica al componente padre para que refresque la lista
            }
        } catch (err) {
            console.error("Error al crear la tarea:", err);
            console.error("Error response:", err.response);
            console.error("Error data:", err.response?.data);
            
            // Manejar diferentes tipos de errores de FastAPI
            let errorMessage = "Error al crear la tarea.";
            
            if (err.response?.data) {
                const errorData = err.response.data;
                
                // Si es un error 422 (Unprocessable Entity) de Pydantic, puede venir como array
                if (Array.isArray(errorData.detail)) {
                    // Extraer mensajes de validación de Pydantic
                    errorMessage = errorData.detail
                        .map((error) => {
                            const field = error.loc ? error.loc.join('.') : 'campo';
                            return `${field}: ${error.msg}`;
                        })
                        .join(', ');
                } else if (typeof errorData.detail === 'string') {
                    // Si es un string simple
                    errorMessage = errorData.detail;
                } else if (errorData.message) {
                    // Algunos errores pueden venir con 'message'
                    errorMessage = errorData.message;
                } else {
                    // Si es un objeto, convertirlo a string legible
                    errorMessage = JSON.stringify(errorData);
                }
            } else if (err.message) {
                errorMessage = err.message;
            }
            
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '15px' }}>
            {error && <p style={{ color: 'red', marginBottom: '10px' }}>{error}</p>}
            {success && <p style={{ color: 'green', marginBottom: '10px' }}>Tarea creada con éxito!</p>}

            <div>
                <label htmlFor="taskTitle" style={{ display: 'block', marginBottom: '5px' }}>Título:</label>
                <input
                    type="text"
                    id="taskTitle"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                />
            </div>
            <div>
                <label htmlFor="taskDescription" style={{ display: 'block', marginBottom: '5px' }}>Descripción:</label>
                <textarea
                    id="taskDescription"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                ></textarea>
            </div>
            <div>
                <label htmlFor="taskDueDate" style={{ display: 'block', marginBottom: '5px' }}>Fecha Límite:</label>
                <input
                    type="datetime-local" // Este tipo de input es ideal para fechas y horas
                    id="taskDueDate"
                    value={dueDate}
                    onChange={(e) => setDueDate(e.target.value)}
                    required
                    style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                />
            </div>
            
            {/* Selector de Conceptos */}
            <div>
                <label htmlFor="taskConcepts" style={{ display: 'block', marginBottom: '5px' }}>
                    Conceptos Relacionados (Opcional):
                </label>
                <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                    Selecciona los conceptos pedagógicos relacionados con esta tarea. Esto permitirá que el sistema
                    genere recomendaciones automáticas cuando un estudiante obtenga una nota baja.
                </p>
                {loadingConceptos ? (
                    <div style={{ padding: '1rem', textAlign: 'center', color: '#6b7280' }}>
                        Cargando conceptos...
                    </div>
                ) : conceptos.length === 0 ? (
                    <div style={{ padding: '1rem', backgroundColor: '#fef3c7', borderRadius: '4px', color: '#92400e' }}>
                        <p style={{ margin: 0, fontSize: '0.875rem' }}>
                            ⚠️ No hay conceptos disponibles. Un administrador debe crear conceptos primero.
                        </p>
                    </div>
                ) : (
                    <div style={{
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        padding: '0.75rem',
                        maxHeight: '200px',
                        overflowY: 'auto',
                        backgroundColor: '#ffffff'
                    }}>
                        {/* Agrupar conceptos por categoría */}
                        {(() => {
                            const categorias = {};
                            conceptos.forEach(concepto => {
                                const categoria = concepto.categoria || 'Sin categoría';
                                if (!categorias[categoria]) {
                                    categorias[categoria] = [];
                                }
                                categorias[categoria].push(concepto);
                            });

                            return Object.entries(categorias).map(([categoria, conceptosCat]) => (
                                <div key={categoria} style={{ marginBottom: '1rem' }}>
                                    <h4 style={{ 
                                        fontSize: '0.875rem', 
                                        fontWeight: '600', 
                                        marginBottom: '0.5rem',
                                        color: '#374151'
                                    }}>
                                        {categoria}
                                    </h4>
                                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '0.5rem' }}>
                                        {conceptosCat.map(concepto => (
                                            <label
                                                key={concepto.id}
                                                style={{
                                                    display: 'flex',
                                                    alignItems: 'flex-start',
                                                    gap: '0.5rem',
                                                    padding: '0.5rem',
                                                    borderRadius: '4px',
                                                    cursor: 'pointer',
                                                    transition: 'background-color 0.2s',
                                                    backgroundColor: selectedConcepts.includes(concepto.id) ? '#dbeafe' : 'transparent'
                                                }}
                                                onMouseEnter={(e) => {
                                                    if (!selectedConcepts.includes(concepto.id)) {
                                                        e.currentTarget.style.backgroundColor = '#f3f4f6';
                                                    }
                                                }}
                                                onMouseLeave={(e) => {
                                                    if (!selectedConcepts.includes(concepto.id)) {
                                                        e.currentTarget.style.backgroundColor = 'transparent';
                                                    }
                                                }}
                                            >
                                                <input
                                                    type="checkbox"
                                                    checked={selectedConcepts.includes(concepto.id)}
                                                    onChange={(e) => {
                                                        if (e.target.checked) {
                                                            setSelectedConcepts([...selectedConcepts, concepto.id]);
                                                        } else {
                                                            setSelectedConcepts(selectedConcepts.filter(id => id !== concepto.id));
                                                        }
                                                    }}
                                                    style={{ marginTop: '0.25rem', cursor: 'pointer' }}
                                                />
                                                <div style={{ flex: 1 }}>
                                                    <div style={{ fontWeight: '500', fontSize: '0.875rem' }}>
                                                        {concepto.nombre}
                                                    </div>
                                                    {concepto.descripcion && (
                                                        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.25rem' }}>
                                                            {concepto.descripcion.length > 60 
                                                                ? concepto.descripcion.substring(0, 60) + '...'
                                                                : concepto.descripcion}
                                                        </div>
                                                    )}
                                                </div>
                                            </label>
                                        ))}
                                    </div>
                                </div>
                            ));
                        })()}
                    </div>
                )}
                {selectedConcepts.length > 0 && (
                    <p style={{ fontSize: '0.875rem', color: '#059669', marginTop: '0.5rem' }}>
                        ✓ {selectedConcepts.length} concepto(s) seleccionado(s)
                    </p>
                )}
            </div>
            
            <button 
                type="submit" 
                disabled={loading}
                style={{ 
                    padding: '10px 15px', 
                    backgroundColor: '#007bff', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px', 
                    cursor: loading ? 'not-allowed' : 'pointer' 
                }}
            >
                {loading ? 'Creando...' : 'Crear Tarea'}
            </button>
        </form>
    );
};

export default TaskCreationForm;