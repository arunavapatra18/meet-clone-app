import { writable } from "svelte/store";

export const is_authenticated = writable(false);

export async function checkAuth() {
    try {
        const response = await fetch("http://localhost:8000/auth/status/", {
            method: "GET",
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const isAuth = data.is_authenticated || false;

        is_authenticated.set(isAuth);
        return isAuth
    }
    catch (error) {
        console.error(error);
        is_authenticated.set(false);
        return false;
    }
}