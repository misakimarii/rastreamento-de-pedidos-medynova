````md
# Sistema de Rastreamento de Pedidos

Sistema web desenvolvido para rastreamento de pedidos via Nota Fiscal, integrado à transportadora e com painel administrativo para atualização de planilhas.

---

## Objetivo

Permitir que clientes consultem o status de seus pedidos de forma simples e rápida utilizando o número da Nota Fiscal, reduzindo demandas internas e melhorando a experiência do cliente.

---

## Funcionalidades

## Área pública
- Consulta por Nota Fiscal
- Exibição do status do pedido
- Linha do tempo da entrega
- Previsão de entrega
- Tela de erro com contato via WhatsApp

## Área administrativa
- Login protegido
- Upload de nova planilha CSV
- Substituição automática da planilha atual
- Reimportação automática dos pedidos

## Backend
- API REST com FastAPI
- Integração com API externa da transportadora
- Scheduler automático
- Cache de consultas
- Autenticação administrativa

---

## Tecnologias Utilizadas

## Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- APScheduler
- Passlib
- JWT

## Frontend
- HTML5
- CSS3
- JavaScript Vanilla

---

## Estrutura do Projeto

```text
rastreamento-de-pedidos/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── jobs/
│   │   ├── utils/
│   │   └── main.py
│   ├── criar_usuario.py
│   ├── requirements.txt
│   └── .env
│
├── assets/
├── css/
├── js/
│
├── index.html
├── resultado.html
├── erro.html
├── admin-login.html
├── upload.html
│
├── .env.example
├── .gitignore
└── README.md
````

---

## Como Executar Localmente

## 1. Clone o projeto

```bash
git clone https://github.com/misakimarii/seu-repositorio.git
cd rastreamento-de-pedidos
```

---

## 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Criar arquivo .env

Crie dentro da pasta backend:

```env
AMPLA_USER=
AMPLA_SENHA=
BASE_URL=
SECRET_KEY=
```

---

## 4. Rodar API

```bash
uvicorn app.main:app --reload
```

API disponível em:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Frontend

Abrir `index.html`

ou usar Live Server no VS Code.

---

## Rotas Principais

## Públicas

```text
GET /rastreamento/{numero_nf}
```

Consulta rastreamento por Nota Fiscal.

---

## Administrativas

```text
POST /admin/login
POST /upload-planilha
```

---

## Fluxo da Planilha

1. Funcionário acessa área administrativa
2. Faz login
3. Envia novo CSV
4. Sistema substitui planilha antiga
5. Importa pedidos automaticamente
6. Base atualizada

---

## Segurança

* Senhas criptografadas
* Login autenticado
* Token JWT
* Variáveis sensíveis via `.env`
* `.gitignore` configurado

---

## Melhorias Futuras

* Dashboard administrativo
* Logs de uploads
* Histórico de planilhas
* Multiusuários
* Hospedagem em produção
* HTTPS + domínio oficial

---

## Projeto Real

Sistema desenvolvido para uso real em distribuidora farmacêutica, focado em rastreamento logístico e experiência do cliente.

---

## Desenvolvido por

**Mariana Faria**
Estudante de Análise e Desenvolvimento de Sistemas
Desenvolvedora Full Stack em formação
Recife - PE

GitHub: [https://github.com/misakimarii](https://github.com/misakimarii)
LinkedIn: [https://linkedin.com/in/mariana-faria-dev](https://linkedin.com/in/mariana-faria-dev)

```
```
