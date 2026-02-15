const API_BASE_URL = 'http://localhost:8000';

export const apiFetch = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`;

    const defaultHeaders = {
        'Content-Type': 'application/json',
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            throw new Error(error.detail || response.statusText);
        }
        return await response.json();
    } catch (error) {
        console.error(`API Fetch Error (${endpoint}):`, error);
        throw error;
    }
};

export default API_BASE_URL;
