export default function SurveysPage() {
    const surveys = [
        { id: 1, title: 'Public Transport Clarity Test', status: 'Published', date: '2025-11-15', responses: 12 },
        { id: 2, title: 'City Service Feedback', status: 'Draft', date: '2025-11-14', responses: 0 },
        { id: 3, title: 'Museum Micro‑Stories', status: 'Completed', date: '2025-11-10', responses: 34 }
    ];

    return (
        <div className="page-container">
            <h1 className="page-title">All Surveys</h1>

            <a href="/dashboard/surveys/create" className="btn-primary">Create Survey</a>

            <table className="survey-table">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th>Responses</th>
                    </tr>
                </thead>
                <tbody>
                    {surveys.map((s) => (
                        <tr key={s.id}>
                            <td>
                                <a href={`/dashboard/surveys/${s.id}`} className="survey-link">
                                    {s.title}
                                </a>
                            </td>
                            <td>{s.status}</td>
                            <td>{s.date}</td>
                            <td>{s.responses}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
