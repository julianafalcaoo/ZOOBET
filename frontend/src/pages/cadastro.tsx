import { useState } from "react";
import { api } from "../services/api";
import "./auth.css";

export default function Cadastro() {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");

  const handleCadastro = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    if (senha !== confirmarSenha) {
      alert("As senhas não coincidem");
      return;
    }
    
    const response = await api.registrar({
      nome,
      email,
      senha,
    });

    localStorage.setItem("token", response.access_token);
  };

  return (
    <div className="container">
      <form className="card" onSubmit={handleCadastro}>
        <h2>Criar Conta</h2>

        <input
          type="text"
          placeholder="Nome completo"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
        />

        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Confirmar senha"
          value={confirmarSenha}
          onChange={(e) => setConfirmarSenha(e.target.value)}
          required
        />

        <button type="submit">Criar Conta</button>
      </form>
    </div>
  );
}