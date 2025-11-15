'use client';
export default function DashboardPage() {
    return (
        <div className="page-container">
            <h1 className="page-title">Dashboard</h1>

            <p className="page-subtitle">Welcome to your researcher workspace.</p>

            <div className="dashboard-grid">
                <a href="/dashboard/surveys/create" className="dashboard-card">
                    <h2>Create Survey</h2>
                    <p>Build a new voice-based survey for AR4U.</p>
                </a>

                <a href="/dashboard/surveys" className="dashboard-card">
                    <h2>All Surveys</h2>
                    <p>View, edit and monitor your surveys.</p>
                </a>
            </div>

            <style jsx>{`
                .dashboard-grid {
                    margin-top: 40px;
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 24px;
                }

                .dashboard-card {
                    display: block;
                    padding: 32px;
                    border: 1px solid rgba(255,255,255,0.15);
                    border-radius: 8px;
                    background: rgba(255,255,255,0.05);
                    text-decoration: none;
                    color: #f2f2f2;
                    transition: background 0.2s ease, border 0.2s ease;
                }

                .dashboard-card:hover {
                    background: rgba(255,255,255,0.12);
                    border-color: rgba(255,255,255,0.25);
                }

                .page-subtitle {
                    margin-top: 10px;
                    opacity: 0.7;
                }
            `}</style>
        </div>
    );
}
