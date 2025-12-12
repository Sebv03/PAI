import React, { useState, useEffect } from 'react';
import examService from '../services/examService';
import useAuthStore from '../store/authStore';
import { useNavigate } from 'react-router-dom';
import ExamCreationForm from './ExamCreationForm';

const ExamsList = ({ courseId, isTeacher }) => {
    const [exams, setExams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const navigate = useNavigate();

    const fetchExams = async () => {
        try {
            const response = await examService.getExamsByCourse(courseId);
            setExams(response.data);
        } catch (error) {
            console.error("Error fetching exams:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (courseId) fetchExams();
    }, [courseId]);

    const handleExamCreated = () => {
        setShowCreateModal(false);
        fetchExams();
    };

    return (
        <div style={{ marginTop: '2rem' }}>
            <div className="flex justify-between items-center" style={{ marginBottom: '1.5rem' }}>
                <h3>📝 Pruebas / Exámenes</h3>
                {isTeacher && (
                    <button
                        className="btn btn-primary btn-sm"
                        onClick={() => setShowCreateModal(true)}
                    >
                        + Crear Prueba
                    </button>
                )}
            </div>

            {loading ? (
                <div className="spinner"></div>
            ) : exams.length === 0 ? (
                <p>No hay pruebas programadas.</p>
            ) : (
                <div className="grid gap-md">
                    {exams.map(exam => (
                        <div key={exam.id} className="card" style={{ padding: '1rem' }}>
                            <div className="flex justify-between items-center">
                                <div>
                                    <h5 style={{ margin: 0 }}>{exam.title}</h5>
                                    <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                        {exam.scheduled_at ? new Date(exam.scheduled_at).toLocaleDateString() : 'Sin fecha'}
                                    </p>
                                </div>
                                <button
                                    className="btn btn-secondary btn-sm"
                                    onClick={() => navigate(`/exams/${exam.id}`)}
                                >
                                    {isTeacher ? 'Ver / Calificar' : 'Entrar'}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Create Modal */}
            {showCreateModal && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    backgroundColor: 'rgba(0,0,0,0.5)', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center', 
                    zIndex: 1000,
                    overflowY: 'auto',
                    padding: '2rem'
                }}>
                    <div style={{ width: '100%', maxWidth: '900px', maxHeight: '90vh', overflowY: 'auto' }}>
                        <ExamCreationForm
                            courseId={courseId}
                            onExamCreated={handleExamCreated}
                            onCancel={() => setShowCreateModal(false)}
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default ExamsList;
