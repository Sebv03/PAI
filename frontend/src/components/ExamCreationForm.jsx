import React, { useState } from 'react';
import examService from '../services/examService';

const ExamCreationForm = ({ courseId, onExamCreated, onCancel }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [date, setDate] = useState('');
    const [pdfFile, setPdfFile] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Estado para nueva pregunta
    const [newQuestion, setNewQuestion] = useState({
        texto: '',
        tipo: 'essay', // 'essay' o 'multiple_choice'
        puntos: 1,
        opciones: []
    });
    const [showQuestionForm, setShowQuestionForm] = useState(false);
    const [newOption, setNewOption] = useState({ texto: '', es_correcta: false });

    const handleAddQuestion = () => {
        if (!newQuestion.texto.trim()) {
            alert('Por favor, ingresa el texto de la pregunta');
            return;
        }

        if (newQuestion.tipo === 'multiple_choice' && newQuestion.opciones.length < 2) {
            alert('Las preguntas de opción múltiple deben tener al menos 2 opciones');
            return;
        }

        if (newQuestion.tipo === 'multiple_choice') {
            const hasCorrect = newQuestion.opciones.some(o => o.es_correcta);
            if (!hasCorrect) {
                alert('Debes marcar al menos una opción como correcta');
                return;
            }
        }

        const questionToAdd = {
            ...newQuestion,
            orden: questions.length + 1
        };

        setQuestions([...questions, questionToAdd]);
        setNewQuestion({
            texto: '',
            tipo: 'essay',
            puntos: 1,
            opciones: []
        });
        setShowQuestionForm(false);
    };

    const handleAddOption = () => {
        if (!newOption.texto.trim()) {
            alert('Por favor, ingresa el texto de la opción');
            return;
        }

        setNewQuestion({
            ...newQuestion,
            opciones: [...newQuestion.opciones, { ...newOption, orden: newQuestion.opciones.length + 1 }]
        });
        setNewOption({ texto: '', es_correcta: false });
    };

    const handleRemoveQuestion = (index) => {
        setQuestions(questions.filter((_, i) => i !== index));
    };

    const handleRemoveOption = (index) => {
        setNewQuestion({
            ...newQuestion,
            opciones: newQuestion.opciones.filter((_, i) => i !== index)
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('title', title);
            formData.append('description', description || '');
            formData.append('course_id', courseId);
            
            if (date) {
                formData.append('scheduled_at', new Date(date).toISOString());
            }

            if (pdfFile) {
                formData.append('pdf_file', pdfFile);
            }

            if (questions.length > 0) {
                formData.append('questions_json', JSON.stringify(questions));
            }

            await examService.createExam(formData);
            
            // Reset form
            setTitle('');
            setDescription('');
            setDate('');
            setPdfFile(null);
            setQuestions([]);
            
            if (onExamCreated) {
                onExamCreated();
            }
        } catch (err) {
            console.error('Error creating exam:', err);
            setError(err.response?.data?.detail || 'Error al crear la prueba');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card" style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
            <h3 style={{ marginBottom: '1.5rem' }}>📝 Crear Nueva Prueba</h3>

            {error && (
                <div className="alert alert-error" style={{ marginBottom: '1rem' }}>
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                {/* Información básica */}
                <div className="form-group">
                    <label className="label">Título de la Prueba *</label>
                    <input
                        className="input-field"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                        required
                        placeholder="Ej: Prueba de Matemáticas - Unidad 1"
                    />
                </div>

                <div className="form-group">
                    <label className="label">Descripción</label>
                    <textarea
                        className="input-field"
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        rows={3}
                        placeholder="Descripción opcional de la prueba..."
                    />
                </div>

                <div className="form-group">
                    <label className="label">Fecha y Hora Programada</label>
                    <input
                        type="datetime-local"
                        className="input-field"
                        value={date}
                        onChange={e => setDate(e.target.value)}
                    />
                </div>

                {/* Subir PDF */}
                <div className="form-group">
                    <label className="label">📄 Subir PDF del Examen (Opcional)</label>
                    <input
                        type="file"
                        accept=".pdf"
                        className="input-field"
                        onChange={e => setPdfFile(e.target.files[0])}
                    />
                    {pdfFile && (
                        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                            ✅ Archivo seleccionado: {pdfFile.name}
                        </p>
                    )}
                </div>

                {/* Preguntas */}
                <div style={{ marginTop: '2rem', borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h4>Preguntas ({questions.length})</h4>
                        <button
                            type="button"
                            className="btn btn-secondary btn-sm"
                            onClick={() => setShowQuestionForm(!showQuestionForm)}
                        >
                            {showQuestionForm ? '❌ Cancelar' : '+ Agregar Pregunta'}
                        </button>
                    </div>

                    {/* Formulario de nueva pregunta */}
                    {showQuestionForm && (
                        <div className="card" style={{ background: 'var(--bg-secondary)', padding: '1.5rem', marginBottom: '1rem' }}>
                            <h5 style={{ marginBottom: '1rem' }}>Nueva Pregunta</h5>
                            
                            <div className="form-group">
                                <label className="label">Texto de la Pregunta *</label>
                                <textarea
                                    className="input-field"
                                    value={newQuestion.texto}
                                    onChange={e => setNewQuestion({ ...newQuestion, texto: e.target.value })}
                                    rows={3}
                                    placeholder="Escribe la pregunta aquí..."
                                />
                            </div>

                            <div className="form-group">
                                <label className="label">Tipo de Pregunta *</label>
                                <select
                                    className="input-field"
                                    value={newQuestion.tipo}
                                    onChange={e => setNewQuestion({ ...newQuestion, tipo: e.target.value, opciones: [] })}
                                >
                                    <option value="essay">Desarrollo / Ensayo</option>
                                    <option value="multiple_choice">Opción Múltiple</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label className="label">Puntos</label>
                                <input
                                    type="number"
                                    min="1"
                                    className="input-field"
                                    value={newQuestion.puntos}
                                    onChange={e => setNewQuestion({ ...newQuestion, puntos: parseInt(e.target.value) || 1 })}
                                />
                            </div>

                            {/* Opciones para preguntas de opción múltiple */}
                            {newQuestion.tipo === 'multiple_choice' && (
                                <div style={{ marginTop: '1rem', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '0.5rem' }}>
                                    <h6 style={{ marginBottom: '0.75rem' }}>Opciones de Respuesta</h6>
                                    
                                    {newQuestion.opciones.map((opcion, idx) => (
                                        <div key={idx} style={{ 
                                            display: 'flex', 
                                            alignItems: 'center', 
                                            gap: '0.5rem',
                                            marginBottom: '0.5rem',
                                            padding: '0.5rem',
                                            background: opcion.es_correcta ? '#d1fae5' : 'white',
                                            borderRadius: '0.25rem'
                                        }}>
                                            <span style={{ fontWeight: 'bold' }}>{idx + 1}.</span>
                                            <span style={{ flex: 1 }}>{opcion.texto}</span>
                                            {opcion.es_correcta && <span style={{ color: 'green' }}>✓ Correcta</span>}
                                            <button
                                                type="button"
                                                className="btn btn-ghost btn-sm"
                                                onClick={() => handleRemoveOption(idx)}
                                            >
                                                Eliminar
                                            </button>
                                        </div>
                                    ))}

                                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem' }}>
                                        <input
                                            type="text"
                                            className="input-field"
                                            style={{ flex: 1 }}
                                            value={newOption.texto}
                                            onChange={e => setNewOption({ ...newOption, texto: e.target.value })}
                                            placeholder="Texto de la opción..."
                                            onKeyPress={e => e.key === 'Enter' && handleAddOption()}
                                        />
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                                            <input
                                                type="checkbox"
                                                checked={newOption.es_correcta}
                                                onChange={e => setNewOption({ ...newOption, es_correcta: e.target.checked })}
                                            />
                                            Correcta
                                        </label>
                                        <button
                                            type="button"
                                            className="btn btn-primary btn-sm"
                                            onClick={handleAddOption}
                                        >
                                            Agregar
                                        </button>
                                    </div>
                                </div>
                            )}

                            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                                <button
                                    type="button"
                                    className="btn btn-primary"
                                    onClick={handleAddQuestion}
                                >
                                    Agregar Pregunta
                                </button>
                                <button
                                    type="button"
                                    className="btn btn-ghost"
                                    onClick={() => {
                                        setShowQuestionForm(false);
                                        setNewQuestion({ texto: '', tipo: 'essay', puntos: 1, opciones: [] });
                                        setNewOption({ texto: '', es_correcta: false });
                                    }}
                                >
                                    Cancelar
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Lista de preguntas agregadas */}
                    {questions.length > 0 && (
                        <div style={{ marginTop: '1rem' }}>
                            {questions.map((q, idx) => (
                                <div key={idx} className="card" style={{ marginBottom: '0.75rem', padding: '1rem' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                        <div style={{ flex: 1 }}>
                                            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '0.5rem' }}>
                                                <strong>Pregunta {idx + 1}</strong>
                                                <span className="badge badge-info">{q.tipo === 'essay' ? 'Desarrollo' : 'Opción Múltiple'}</span>
                                                <span className="badge badge-secondary">{q.puntos} punto{q.puntos !== 1 ? 's' : ''}</span>
                                            </div>
                                            <p style={{ margin: '0.5rem 0' }}>{q.texto}</p>
                                            {q.tipo === 'multiple_choice' && q.opciones.length > 0 && (
                                                <div style={{ marginTop: '0.5rem', paddingLeft: '1rem' }}>
                                                    <strong>Opciones:</strong>
                                                    <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>
                                                        {q.opciones.map((opt, optIdx) => (
                                                            <li key={optIdx} style={{ color: opt.es_correcta ? 'green' : 'inherit' }}>
                                                                {opt.texto} {opt.es_correcta && '✓'}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                        </div>
                                        <button
                                            type="button"
                                            className="btn btn-ghost btn-sm"
                                            onClick={() => handleRemoveQuestion(idx)}
                                        >
                                            Eliminar
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {questions.length === 0 && !showQuestionForm && (
                        <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic', textAlign: 'center', padding: '1rem' }}>
                            No hay preguntas agregadas. Puedes crear preguntas o subir un PDF con el examen.
                        </p>
                    )}
                </div>

                {/* Botones de acción */}
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '2rem', justifyContent: 'flex-end' }}>
                    <button
                        type="button"
                        className="btn btn-ghost"
                        onClick={onCancel}
                        disabled={loading}
                    >
                        Cancelar
                    </button>
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading || !title.trim()}
                    >
                        {loading ? 'Creando...' : 'Crear Prueba'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ExamCreationForm;

