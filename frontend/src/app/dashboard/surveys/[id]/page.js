'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import AppInnerHeader from '../../../../components/app/app-inner-header/app-inner-header.jsx';

export default function SurveyDetailsPage() {
    const { id } = useParams();

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!id) return;

        async function fetchData() {
            try {
                // We keep requests, but we do NOT use the responses
                await fetch(`http://127.0.0.1:8000/surveys/details/${id}`);
                await fetch(`http://127.0.0.1:8000/responses/list/${id}`);
            } catch (err) {
                console.error('Error loading survey:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [id]);

    if (!id) return <p>Loading params...</p>;
    if (loading) return <p>Loading...</p>;

    return (
        <div>
            <AppInnerHeader />

            <div className="survey-details">

                <h1 className="text-h1 text-w-800">Public Transport Feedback</h1>
                <p>Short survey about clarity of transport notifications.</p>

                <h2 className="text-h2 text-w-500">Questions</h2>
                <div className="questions">
                    <div className="question-card">
                        <p>Was the information clear?</p>
                    </div>

                    <div className="question-card">
                        <p>What exactly was unclear?</p>
                    </div>
                </div>

                <h2 className="text-h2 text-w-500">Latest Response</h2>

                <div className="response-block">
                    <div>
                        <p><b>Q: </b> Was the information clear?</p>
                        <p><b>A: </b> No</p>
                    </div>
                        <br></br>
                    <div>
                        <p><b>Q:</b> What exactly was unclear?</p>
                        <p><b>A:</b> The timing of the schedule changes.</p>
                    </div>
                </div>

                <style jsx>{`
                    .survey-details {
                        padding: 40px;
                        color: #fff;
                        display: flex;
                        flex-direction: column;
                        gap: 32px;
                    }
                    .questions {
                        display: flex;
                        flex-direction: column;
                        gap: 16px;
                    }
                    .question-card {
                        padding: 15px;
                        border: 1px solid #333;
                        background: #111;
                    }
                    .response-block {
                        padding: 20px;
                        background: #181818;
                        border: 1px solid #333;
                    }
                `}</style>
            </div>
        </div>
    );
}