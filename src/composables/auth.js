// src/composables/auth.js
import { ref, readonly } from 'vue'

// This state is defined outside the function, so it's a singleton.
// Every component that calls useAuth() will share the same state.
const user = ref(null)

async function register({ name, email, phone, password }) {
  const response = await fetch('http://localhost:5000/api/register', { // Flask app on port 5000
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, phone, password })
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Registration failed');
  }
  user.value = { name, email, phone };
  return user.value;
}

async function login({ phone, password }) {
  // Use the Flask app on port 5000
  const response = await fetch('http://localhost:5000/api/login', { // Flask app on port 5000
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone, password })
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Login failed');
  }
  const data = await response.json();
  // Save token if needed, and set user
  user.value = { phone, token: data.access_token };
  return user.value;
}

function logout() {
  user.value = null;
}

export function useAuth() {
  return {
    user: readonly(user),
    register,
    login,
    logout
  }
}