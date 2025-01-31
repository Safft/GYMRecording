const API_URL = "http://fastapi:8000";

export async function login(username, password) {
    const response = await fetch(`${API_URL}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
    });

    if (!response.ok) {
        throw new Error("Login failed");
    }
    return await response.json();
}

export async function getExercises(token) {
    const response = await fetch(`${API_URL}/exercises/`, {
        headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch exercises");
    }
    return await response.json();
}

export async function addExercise(token, exerciseData) {
    const response = await fetch(`${API_URL}/exercises/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(exerciseData),
    });

    if (!response.ok) {
        throw new Error("Failed to add exercise");
    }
    return await response.json();
}
