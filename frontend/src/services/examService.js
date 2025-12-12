import apiClient from './api';

const examService = {
    // Create an exam with FormData (supports file upload)
    createExam: (formData) => apiClient.post('/api/v1/exams/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    }),

    // Get exams for a course
    getExamsByCourse: (courseId) => apiClient.get(`/api/v1/exams/course/${courseId}`),

    // Get single exam
    getExam: (examId) => apiClient.get(`/api/v1/exams/${examId}`),

    // Submit an exam (Student)
    submitExam: (examId, data) => apiClient.post(`/api/v1/exams/${examId}/submit`, data),

    // Get my submission (Student)
    getMySubmission: (examId) => apiClient.get(`/api/v1/exams/${examId}/my-submission`),

    // Get all submissions (Teacher)
    getSubmissions: (examId) => apiClient.get(`/api/v1/exams/${examId}/submissions`),

    // Grade a submission (Teacher)
    gradeSubmission: (submissionId, data) => apiClient.put(`/api/v1/exams/submissions/${submissionId}`, data)
};

export default examService;
