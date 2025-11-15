'use client';

import { useEffect, useState } from 'react';

import Button from '../../../components/_block/button/button'
import AppInnerHeader from '../../../components/app/app-inner-header/app-inner-header.jsx'
import Link from 'next/link';

export default function SurveysPage() {
    const [surveys, setSurveys] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchSurveys() {
            try {
                const res = await fetch('http://127.0.0.1:8000/surveys/list', {
                    method: 'GET'
                });
                const data = await res.json();
                setSurveys(data);
            } catch (err) {
                console.error('Error loading surveys:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchSurveys();
    }, []);

    return (
        <div>
            <AppInnerHeader />
            <div className="surveys-page">
                <h1 className="text-h1 text-w-800">My Surveys</h1>

                {loading && <p>Loading...</p>}

                {!loading && surveys.length === 0 && (
                    <p>No surveys created yet.</p>
                )}

                <div className="survey-list">
                    {surveys.map((s) => (
                        <div key={s.id} className="survey-card">
                            <h3 className="text-h3 text-w-600">{s.title}</h3>
                            <p>{s.description}</p>
                            <Link href={`/dashboard/surveys/${s.id}`}>
                                <Button>Open</Button>
                            </Link>
                        </div>
                    ))}
                </div>

                <style jsx>{`
                    .surveys-page {
                        padding: 40px;
                        color: #fff;
                        display: flex;
                        flex-direction: column;
                        gap: 20px;
                    }
                    .survey-list {
                        display: grid;
                        gap: 20px;
                        margin-top: 20px;
                    }
                    .survey-card {
                        padding: 20px;
                        border: 1px solid #444;
                        border-radius: 8px;
                        background: #111;
                    }
                    .survey-card h3 {
                        margin: 0 0 8px 0;
                    }
                    p {
                        padding-block: 10px 20px;
                    }
                    a {
                        color: #FFF;
                    }
                `}</style>
            </div>
        </div>
    );
}
