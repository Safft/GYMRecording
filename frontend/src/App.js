import React, { useState } from "react";
import Login from "./components/Login";
import ExerciseList from "./components/ExerciseList";

const App = () => {
    const [token, setToken] = useState(null);

    return (
        <div>
            <h1>Gym Tracker</h1>
            {!token ? (
                <Login setToken={setToken} />
            ) : (
                <ExerciseList token={token} />
            )}
        </div>
    );
};

export default App;
