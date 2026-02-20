# ZOOBET
Sistema web full stack para simulação do Jogo do Bicho, desenvolvido para fins acadêmicos, na disciplina de Laboratório de Software.

## Stack definida:
Backend: FastAPI 
Frontend: React (Vite) 
Banco de Dados: PostgreSQL 
Infraestrutura: ambiente isolado via Docker
Versionamento: Git, GitHub, GitHub Projects, GitHub Actions

## Arquitetura do Sistema

O projeto segue uma arquitetura em camadas, separando responsabilidades:

- Camada de Apresentação (Frontend)
- Camada de Aplicação / Backend
- Camada de Dados
- Camada de Contrato de API: define endpoints REST consumidos pelo frontend.

## Endpoints
POST /auth/register: registrar novo usuário

POST /auth/login: autenticar usuário

GET /bets: listar apostas do usuário

POST /bets: criar nova aposta

GET /results: obter resultados dos sorteios


## RODAR O PROJETO
1. clonar 
git clone https://github.com/julianafalcaoo/ZOOBET.git
cd ZOOBET

2. inicializar container docker
docker-compose up --build
