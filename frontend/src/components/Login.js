import React, { useState } from "react";
import { login } from "../api";
import "./Login.css"; // Подключаем CSS

const Login = ({ setToken }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = await login(username, password);
            setToken(data.access_token);
        } catch (error) {
            setError("Login failed. Please check your username and password.");
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>Login</h2>
                {error && <p className="error-message">{error}</p>}
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="input-field"
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="input-field"
                />
                <button type="submit" className="submit-button">Login</button>
            </form>
        </div>
    );
};

export default Login;
