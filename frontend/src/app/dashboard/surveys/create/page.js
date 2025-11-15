"use client";

import { useRouter } from "next/navigation";

import { useState } from "react";
import styles from "./create.module.css";

import Button from '../../../../components/_block/button/button';

import AppInnerHeader from '../../../../components/app/app-inner-header/app-inner-header.jsx'

export default function CreateSurveyPage() {
    const router = useRouter();

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [questions, setQuestions] = useState([
        { id: Date.now(), type: "open", text: "", required: false, options: [] }
    ]);

    const addQuestion = () => {
        setQuestions([
            ...questions,
            { id: Date.now(), type: "open", text: "", required: false, options: [] }
        ]);
    };

    const updateQuestion = (id, field, value) => {
        setQuestions(
            questions.map((q) =>
                q.id === id ? { ...q, [field]: value } : q
            )
        );
    };

    const addOption = (id) => {
        setQuestions(
            questions.map((q) =>
                q.id === id
                    ? { ...q, options: [...(q.options || []), ""] }
                    : q
            )
        );
    };

    const updateOption = (id, index, value) => {
        setQuestions(
            questions.map((q) =>
                q.id === id
                    ? {
                        ...q,
                        options: q.options.map((opt, i) =>
                            i === index ? value : opt
                        ),
                    }
                    : q
            )
        );
    };

    const submitSurvey = async () => {
        const payload = {
            title,
            description,
            questions: questions.map((q) => ({
                type: q.type,
                text: q.text,
                required: q.required,
                options: q.type === "open" ? null : q.options,
            })),
        };

        const res = await fetch("http://127.0.0.1:8000/surveys/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await res.json();
        console.log("Created:", data);
        router.push("/dashboard/surveys");
    };

    return (
        <div>
           <AppInnerHeader></AppInnerHeader>
            <div className={styles.page}>
    

                <h1 className={styles.title}>Create New Survey</h1>

                <div className={styles.formBlock}>
                    <label>Title</label>
                    <input
                        className={styles.input}
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />

                    <label>Description</label>
                    <textarea
                        className={styles.textarea}
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>

                <h2 className={styles.subtitle}>Questions</h2>

                <div className={styles.questions}>
                    {questions.map((q) => (
                        <div key={q.id} className={styles.question}>
                            <select
                                value={q.type}
                                onChange={(e) =>
                                    updateQuestion(q.id, "type", e.target.value)
                                }
                                className={styles.select}
                            >
                                <option value="open">Open</option>
                                <option value="yes_no">Yes / No</option>
                                <option value="single_choice">Single Choice</option>
                                <option value="multiple_choice">
                                    Multiple Choice
                                </option>
                                <option value="scale">Scale 1–5</option>
                            </select>

                            <input
                                className={styles.input}
                                placeholder="Question text"
                                value={q.text}
                                onChange={(e) =>
                                    updateQuestion(q.id, "text", e.target.value)
                                }
                            />

                            <label className={styles.checkbox}>
                                <input
                                    type="checkbox"
                                    checked={q.required}
                                    onChange={(e) =>
                                        updateQuestion(
                                            q.id,
                                            "required",
                                            e.target.checked
                                        )
                                    }
                                />
                                Required
                            </label>

                            {(q.type === "single_choice" ||
                                q.type === "multiple_choice") && (
                                    <div className={styles.options}>
                                        <button
                                            className={styles.btnSmall}
                                            onClick={() => addOption(q.id)}
                                        >
                                            + Add Option
                                        </button>

                                        {q.options.map((opt, i) => (
                                            <input
                                                key={i}
                                                className={styles.input}
                                                placeholder={`Option ${i + 1}`}
                                                value={opt}
                                                onChange={(e) =>
                                                    updateOption(
                                                        q.id,
                                                        i,
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        ))}
                                    </div>
                                )}
                        </div>
                    ))}
                </div>
                <div className={styles.buttonBox}>
                    <Button  effect="light" onClick={addQuestion} className={styles.addButton}>
                        + Add Question
                    </Button>

                    <Button onClick={submitSurvey} className={styles.submitButton}>
                        Add Survey
                    </Button>
                </div>



            </div>
        </div>


    );


}