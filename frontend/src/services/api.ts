const API_URL = import.meta.env.VITE_API_URL as string;

interface LoginData {
  email: string;
  senha: string;
}

interface RegisterData {
  nome: string;
  email: string;
  senha: string;
}
 
interface AuthResponse {
  access_token: string;
  token_type: string;
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("token");

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw await response.json();
  }

  return response.json();
}

export const api = {
  login: (data: LoginData) =>
    request<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  registrar: (data: RegisterData) =>
    request<AuthResponse>("/auth/registrar", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};