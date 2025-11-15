

'use client';

import { useState } from 'react';

export default function CreateSurveyPage() {
    const [title, setTitle] = useState('');
    const [questions, setQuestions] = useState([]);

    const addQuestion = () => {
        setQuestions([
            ...questions,
            { id: Date.now(), type: 'open', text: '', options: [] }
        ]);
    };

    const updateQuestion = (id, key, value) => {
        setQuestions(
            questions.map(q => q.id === id ? { ...q, [key]: value } : q)
        );
    };

    const updateOptions = (id, optionsString) => {
        const options = optionsString.split('\n').map(o => o.trim()).filter(Boolean);
        updateQuestion(id, 'options', options);
    };

    const removeQuestion = (id) => {
        setQuestions(questions.filter(q => q.id !== id));
    };

    const saveSurvey = () => {
        const payload = {
            title,
            questions
        };
        console.log('Survey saved (mock):', payload);
        alert('Survey created (mock)');
    };

    return (
        <div className="page-container">
            <h1 className="page-title">Create Survey</h1>

            <label className="form-label">Title</label>
            <input
                className="form-input"
                value={title}
                onChange={e => setTitle(e.target.value)}
                placeholder="Enter survey title"
            />

            <h2 className="section-title">Questions</h2>

            {questions.map((q) => (
                <div key={q.id} className="question-block">
                    
                    <label className="form-label">Question type</label>
                    <select
                        className="form-input"
                        value={q.type}
                        onChange={e => updateQuestion(q.id, 'type', e.target.value)}
                    >
                        <option value="open">Open question</option>
                        <option value="yes_no">Yes / No</option>
                        <option value="choices">Multiple choice</option>
                        <option value="single">Single choice</option>
                        <option value="scale">Scale 1–5</option>
                    </select>

                    <label className="form-label">Question text</label>
                    <input
                        className="form-input"
                        value={q.text}
                        onChange={e => updateQuestion(q.id, 'text', e.target.value)}
                        placeholder="Enter question"
                    />

                    {q.type === 'choices' && (
                        <>
                            <label className="form-label">Options (one per line)</label>
                            <textarea
                                className="form-textarea"
                                onChange={e => updateOptions(q.id, e.target.value)}
                                placeholder="Option 1&#10;Option 2&#10;Option 3"
                            />
                        </>
                    )}

                    <button className="btn-danger" onClick={() => removeQuestion(q.id)}>
                        Delete question
                    </button>

                </div>
            ))}

            <button className="btn-primary" onClick={addQuestion}>
                Add Question
            </button>

            <button className="btn-primary" onClick={saveSurvey} style={{ marginLeft: '10px' }}>
                Save Survey
            </button>
        </div>
    );
}