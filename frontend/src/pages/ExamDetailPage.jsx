import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import examService from '../services/examService';
import useAuthStore from '../store/authStore';
import apiClient from '../services/api';

const ExamDetailPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { user, setUser } = useAuthStore();

    const [exam, setExam] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isTeacher, setIsTeacher] = useState(false);

    // Student State
    const [submission, setSubmission] = useState(null);
    const [content, setContent] = useState('');

    // Teacher State
    const [submissions, setSubmissions] = useState([]);
    const [gradingId, setGradingId] = useState(null);
    const [grade, setGrade] = useState('');
    const [feedback, setFeedback] = useState('');

    useEffect(() => {
        const init = async () => {
            try {
                // Cargar datos del usuario si no están disponibles
                let currentUser = user;
                if (!currentUser) {
                    try {
                        const userRes = await apiClient.get('/users/me');
                        currentUser = userRes.data;
                        if (setUser) {
                            setUser(currentUser);
                        }
                    } catch (userErr) {
                        console.error("Error al cargar datos del usuario:", userErr);
                        alert("Error al cargar datos del usuario. Por favor, inicia sesión nuevamente.");
                        navigate('/login');
                        return;
                    }
                }

                // Cargar datos del examen
                const examRes = await examService.getExam(id);
                setExam(examRes.data);

                // Verificar si es profesor o administrador
                // El rol viene del backend como string en minúsculas: "docente", "administrador", "estudiante"
                let userRol = currentUser?.rol;
                if (typeof userRol === 'object' && userRol !== null) {
                    // Si es un objeto, tomar el valor
                    userRol = userRol.value || userRol.toString();
                }
                userRol = String(userRol || '').toLowerCase().trim();
                
                // Verificar si es DOCENTE o ADMINISTRADOR (comparación en minúsculas)
                const teacherRole = userRol === 'docente' || userRol === 'administrador';
                setIsTeacher(teacherRole);

                console.log("Usuario completo:", currentUser);
                console.log("Rol normalizado:", userRol);
                console.log("Es profesor:", teacherRole);

                if (teacherRole) {
                    // Cargar entregas para profesor
                    const subsRes = await examService.getSubmissions(id);
                    setSubmissions(subsRes.data);
                } else {
                    // Cargar entrega del estudiante
                    try {
                        const mySub = await examService.getMySubmission(id);
                        setSubmission(mySub.data);
                    } catch (e) {
                        // Not submitted yet - esto es normal
                        console.log("Estudiante aún no ha entregado");
                    }
                }
            } catch (err) {
                console.error("Error al cargar examen:", err);
                alert("Error al cargar el examen. Por favor, intenta de nuevo.");
            } finally {
                setLoading(false);
            }
        };
        init();
    }, [id, user, setUser, navigate]);

    const handleStudentSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await examService.submitExam(id, { content });
            setSubmission(res.data);
            alert("Examen enviado correctamente");
        } catch (err) {
            alert("Error al enviar examen");
        }
    };

    const handleGradeSubmit = async (subId) => {
        // Validar nota antes de enviar
        const gradeNum = parseFloat(grade);
        if (isNaN(gradeNum) || gradeNum < 1.0 || gradeNum > 7.0) {
            alert("❌ La nota debe estar entre 1.0 y 7.0");
            return;
        }

        try {
            await examService.gradeSubmission(subId, {
                grade: gradeNum,
                feedback: feedback || null
            });
            
            // Recargar las entregas para obtener los datos actualizados del servidor
            try {
                const subsRes = await examService.getSubmissions(id);
                setSubmissions(subsRes.data);
            } catch (refreshErr) {
                console.error("Error al refrescar entregas:", refreshErr);
                // Fallback: actualizar estado local
                setSubmissions(prev => prev.map(s => s.id === subId ? { 
                    ...s, 
                    grade: gradeNum, 
                    feedback: feedback || null 
                } : s));
            }
            
            setGradingId(null);
            setGrade('');
            setFeedback('');
            alert("✅ Calificación guardada correctamente");
        } catch (err) {
            console.error("Error al calificar:", err);
            const errorMsg = err.response?.data?.detail || "Error al calificar. Verifica que la nota esté entre 1.0 y 7.0";
            alert(`❌ ${errorMsg}`);
        }
    };

    if (loading) return <div className="spinner"></div>;
    if (!exam) return <p>Examen no encontrado</p>;

    return (
        <div className="container" style={{ padding: '2rem 0' }}>
            <button onClick={() => navigate(-1)} className="btn btn-ghost mb-md">← Volver</button>

            <div className="card mb-lg">
                <h1>{exam.title}</h1>
                <p>{exam.description}</p>
                <div className="flex gap-md">
                    <span className="badge badge-info">Fecha: {new Date(exam.scheduled_at).toLocaleDateString()}</span>
                </div>
            </div>

            {isTeacher ? (
                // --- TEACHER VIEW ---
                <div>
                    <div style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        marginBottom: '1.5rem'
                    }}>
                        <h3>Entregas de Estudiantes</h3>
                        <div style={{ 
                            padding: '0.5rem 1rem', 
                            background: 'var(--bg-tertiary)', 
                            borderRadius: '0.5rem',
                            fontSize: '0.9rem'
                        }}>
                            Total: {submissions.length} {submissions.length === 1 ? 'entrega' : 'entregas'}
                        </div>
                    </div>

                    {submissions.length === 0 ? (
                        <div className="card" style={{ 
                            textAlign: 'center', 
                            padding: '3rem',
                            background: 'var(--bg-secondary)'
                        }}>
                            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
                                📝 Aún no hay entregas de estudiantes
                            </p>
                            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                                Los estudiantes aparecerán aquí cuando entreguen sus respuestas
                            </p>
                        </div>
                    ) : (
                        <div className="grid gap-md">
                            {submissions.map((sub, index) => (
                                <div key={sub.id} className="card" style={{ 
                                    border: gradingId === sub.id ? '2px solid var(--primary)' : '1px solid var(--border-color)',
                                    transition: 'all 0.3s ease'
                                }}>
                                    {/* Header con información del estudiante */}
                                    <div style={{ 
                                        display: 'flex', 
                                        justifyContent: 'space-between', 
                                        alignItems: 'flex-start',
                                        marginBottom: '1rem',
                                        paddingBottom: '1rem',
                                        borderBottom: '1px solid var(--border-color)'
                                    }}>
                                        <div>
                                            <h5 style={{ margin: '0 0 0.25rem 0', fontSize: '1.1rem' }}>
                                                👤 {sub.student_name || 'Estudiante'}
                                            </h5>
                                            <p style={{ 
                                                margin: 0, 
                                                fontSize: '0.85rem', 
                                                color: 'var(--text-secondary)' 
                                            }}>
                                                📧 {sub.student_email || 'Sin email'}
                                            </p>
                                            <p style={{ 
                                                margin: '0.25rem 0 0 0', 
                                                fontSize: '0.85rem', 
                                                color: 'var(--text-secondary)' 
                                            }}>
                                                📅 Entregado: {sub.submitted_at ? 
                                                    new Date(sub.submitted_at).toLocaleString('es-CL') : 
                                                    'Fecha no disponible'}
                                            </p>
                                        </div>
                                        <div style={{ textAlign: 'right' }}>
                                            {sub.grade ? (
                                                <span className={`badge ${sub.grade < 4.0 ? 'badge-danger' : sub.grade >= 6.0 ? 'badge-success' : 'badge-warning'}`} 
                                                      style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>
                                                    Nota: {sub.grade.toFixed(1)} / 7.0
                                                </span>
                                            ) : (
                                                <span className="badge badge-warning" style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>
                                                    ⏳ Sin calificar
                                                </span>
                                            )}
                                        </div>
                                    </div>

                                    {/* Respuesta del estudiante */}
                                    <div style={{ 
                                        background: 'var(--bg-tertiary)', 
                                        padding: '1.25rem', 
                                        borderRadius: '0.5rem', 
                                        marginBottom: '1rem',
                                        minHeight: '100px'
                                    }}>
                                        <strong style={{ 
                                            display: 'block', 
                                            marginBottom: '0.75rem',
                                            color: 'var(--text-primary)',
                                            fontSize: '0.95rem'
                                        }}>
                                            📝 Respuesta del estudiante:
                                        </strong>
                                        <div style={{ 
                                            whiteSpace: 'pre-wrap',
                                            wordWrap: 'break-word',
                                            lineHeight: '1.6',
                                            color: 'var(--text-primary)'
                                        }}>
                                            {sub.content || '(Sin respuesta)'}
                                        </div>
                                    </div>

                                    {/* Formulario de calificación o botón */}
                                    {gradingId === sub.id ? (
                                        <div style={{ 
                                            borderTop: '2px solid var(--primary)', 
                                            paddingTop: '1.5rem',
                                            background: 'var(--bg-secondary)',
                                            padding: '1.5rem',
                                            borderRadius: '0.5rem',
                                            marginTop: '1rem'
                                        }}>
                                            <h6 style={{ marginBottom: '1rem', fontSize: '1rem' }}>
                                                ✏️ Calificar Entrega
                                            </h6>
                                            <div className="form-group">
                                                <label className="label">Nota (1.0 - 7.0) *</label>
                                                <input
                                                    type="number" 
                                                    step="0.1" 
                                                    min="1.0" 
                                                    max="7.0"
                                                    className="input-field"
                                                    value={grade} 
                                                    onChange={e => setGrade(e.target.value)}
                                                    placeholder="Ej: 5.5"
                                                    required
                                                    style={{ fontSize: '1rem' }}
                                                />
                                                <small style={{ 
                                                    color: 'var(--text-secondary)', 
                                                    fontSize: '0.85rem',
                                                    marginTop: '0.25rem',
                                                    display: 'block'
                                                }}>
                                                    Escala chilena: 1.0 (insuficiente) a 7.0 (excelente)
                                                </small>
                                            </div>
                                            <div className="form-group" style={{ marginTop: '1rem' }}>
                                                <label className="label">Retroalimentación / Comentarios</label>
                                                <textarea
                                                    className="input-field"
                                                    rows={4}
                                                    value={feedback} 
                                                    onChange={e => setFeedback(e.target.value)}
                                                    placeholder="Escribe comentarios, observaciones o sugerencias para el estudiante..."
                                                    style={{ fontSize: '0.95rem' }}
                                                />
                                                <small style={{ 
                                                    color: 'var(--text-secondary)', 
                                                    fontSize: '0.85rem',
                                                    marginTop: '0.25rem',
                                                    display: 'block'
                                                }}>
                                                    Opcional: Ayuda al estudiante a entender su calificación
                                                </small>
                                            </div>
                                            <div className="flex gap-sm" style={{ marginTop: '1.5rem' }}>
                                                <button 
                                                    className="btn btn-primary" 
                                                    onClick={() => handleGradeSubmit(sub.id)}
                                                    disabled={!grade || parseFloat(grade) < 1.0 || parseFloat(grade) > 7.0}
                                                >
                                                    💾 Guardar Calificación
                                                </button>
                                                <button 
                                                    className="btn btn-ghost" 
                                                    onClick={() => {
                                                        setGradingId(null);
                                                        setGrade('');
                                                        setFeedback('');
                                                    }}
                                                >
                                                    Cancelar
                                                </button>
                                            </div>
                                        </div>
                                    ) : (
                                        <div style={{ 
                                            display: 'flex', 
                                            justifyContent: 'space-between', 
                                            alignItems: 'center',
                                            paddingTop: '1rem',
                                            borderTop: '1px solid var(--border-color)'
                                        }}>
                                            <div>
                                                {sub.grade && sub.feedback && (
                                                    <div style={{ 
                                                        background: 'var(--bg-secondary)', 
                                                        padding: '0.75rem', 
                                                        borderRadius: '0.5rem',
                                                        marginTop: '0.5rem'
                                                    }}>
                                                        <strong style={{ fontSize: '0.9rem' }}>📝 Comentarios:</strong>
                                                        <p style={{ 
                                                            margin: '0.5rem 0 0 0', 
                                                            fontSize: '0.9rem',
                                                            whiteSpace: 'pre-wrap'
                                                        }}>
                                                            {sub.feedback}
                                                        </p>
                                                    </div>
                                                )}
                                            </div>
                                            <button 
                                                className={`btn ${sub.grade ? 'btn-secondary' : 'btn-primary'}`} 
                                                onClick={() => {
                                                    setGradingId(sub.id);
                                                    setGrade(sub.grade ? sub.grade.toString() : '');
                                                    setFeedback(sub.feedback || '');
                                                }}
                                                style={{ minWidth: '120px' }}
                                            >
                                                {sub.grade ? '✏️ Re-calificar' : '⭐ Calificar'}
                                            </button>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            ) : (
                // --- STUDENT VIEW ---
                <div className="card">
                    {submission ? (
                        <div>
                            <div className="alert alert-success">
                                ✅ Examen entregado el {new Date(submission.submitted_at).toLocaleString()}
                            </div>
                            <div className="mb-md">
                                <strong>Tu respuesta:</strong>
                                <p>{submission.content}</p>
                            </div>
                            {submission.grade && (
                                <div style={{
                                    padding: '1rem',
                                    background: submission.grade < 4.0 ? 'var(--danger)' : '#d1fae5',
                                    color: submission.grade < 4.0 ? 'white' : 'inherit',
                                    borderRadius: '0.5rem'
                                }}>
                                    <h4>Nota: {submission.grade} / 7.0</h4>
                                    <p>{submission.feedback}</p>
                                </div>
                            )}
                        </div>
                    ) : (
                        <form onSubmit={handleStudentSubmit}>
                            <div className="form-group">
                                <label className="label">Escribe tus respuestas:</label>
                                <textarea
                                    className="input-field" rows={10}
                                    value={content} onChange={e => setContent(e.target.value)}
                                    placeholder="Desarrolla tu respuesta aquí..."
                                    required
                                />
                            </div>
                            <button type="submit" className="btn btn-primary btn-full">Enviar Examen</button>
                        </form>
                    )}
                </div>
            )}
        </div>
    );
};

export default ExamDetailPage;
