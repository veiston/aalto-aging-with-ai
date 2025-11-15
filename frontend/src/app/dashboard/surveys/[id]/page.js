

export default function SurveyDetailPage({ params }) {
    const { id } = params;

    // placeholder mock data
    const survey = {
        id,
        title: 'Public Transport Clarity Test',
        status: 'Published',
        date: '2025-11-15',
        questions: [
            { type: 'yes_no', text: 'Понятно ли вам уведомление?' },
            { type: 'open', text: 'Что показалось непонятным?' },
            { type: 'choices', text: 'Как вы обычно получаете уведомления?', options: ['Email', 'SMS', 'Бумага', 'Телефонные звонки'] }
        ],
        responses: [
            { id: 1, answers: ['Да', 'Ничего', 'Бумага'] },
            { id: 2, answers: ['Нет', 'Текст слишком длинный', 'Email'] }
        ]
    };

    return (
        <div className="page-container">
            <h1 className="page-title">{survey.title}</h1>
            <p className="survey-meta">Status: {survey.status}</p>
            <p className="survey-meta">Date: {survey.date}</p>

            <h2 className="section-title">Questions JSON</h2>
            <pre className="json-block">
                {JSON.stringify(survey, null, 2)}
            </pre>

            <h2 className="section-title">Responses</h2>
            <table className="survey-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Answers</th>
                    </tr>
                </thead>
                <tbody>
                    {survey.responses.map((r) => (
                        <tr key={r.id}>
                            <td>{r.id}</td>
                            <td>{r.answers.join(', ')}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div className="button-row">
                <button className="btn-danger">Stop Survey</button>
                <button className="btn-primary">Download CSV</button>
            </div>
        </div>
    );
}