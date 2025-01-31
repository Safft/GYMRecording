import React, { useEffect, useState } from "react";
import { getExercises, addExercise } from "../api";
import "./ExerciseList.css"; // Подключаем CSS

const ExerciseList = ({ token }) => {
    const [exercises, setExercises] = useState([]);
    const [newExercise, setNewExercise] = useState({
        exercise_name: "",
        sets: 0,
        reps: 0,
        weight: 0,
    });

    useEffect(() => {
        const fetchExercises = async () => {
            try {
                const data = await getExercises(token);
                setExercises(data);
            } catch (error) {
                console.error("Failed to fetch exercises:", error);
            }
        };
        fetchExercises();
    }, [token]);

    const handleAddExercise = async () => {
        try {
            const added = await addExercise(token, newExercise);
            setExercises([...exercises, added]);
        } catch (error) {
            console.error("Failed to add exercise:", error);
        }
    };

    return (
        <div className="exercise-container">
            <h2>Exercise Tracker</h2>
            <ul className="exercise-list">
                {exercises.map((exercise) => (
                    <li key={exercise.id} className="exercise-item">
                        <strong>{exercise.exercise_name}</strong>: {exercise.sets} sets x {exercise.reps} reps at {exercise.weight} kg
                    </li>
                ))}
            </ul>
            <div className="exercise-form">
                <h3>Add New Exercise</h3>
                <input
                    type="text"
                    placeholder="Exercise Name"
                    value={newExercise.exercise_name}
                    onChange={(e) =>
                        setNewExercise({ ...newExercise, exercise_name: e.target.value })
                    }
                    className="input-field"
                />
                <input
                    type="number"
                    placeholder="Sets"
                    value={newExercise.sets}
                    onChange={(e) =>
                        setNewExercise({ ...newExercise, sets: +e.target.value })
                    }
                    className="input-field"
                />
                <input
                    type="number"
                    placeholder="Reps"
                    value={newExercise.reps}
                    onChange={(e) =>
                        setNewExercise({ ...newExercise, reps: +e.target.value })
                    }
                    className="input-field"
                />
                <input
                    type="number"
                    placeholder="Weight"
                    value={newExercise.weight}
                    onChange={(e) =>
                        setNewExercise({ ...newExercise, weight: +e.target.value })
                    }
                    className="input-field"
                />
                <button onClick={handleAddExercise} className="submit-button">Add Exercise</button>
            </div>
        </div>
    );
};

export default ExerciseList;
