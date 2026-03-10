# MyProject

A web application built with **Go** (backend), **React** (frontend), **PostgreSQL**, and **Redis**, following clean architecture principles.

## Prerequisites

| Tool | Purpose |
|------|---------|
| Go 1.21+ | Backend runtime |
| Node.js 18+ | Frontend toolchain |
| Docker & Docker Compose | Database, Redis, and local services |

> A PostgreSQL client (e.g. `psql`, DBeaver) is optional but useful for debugging.

## Quick Start

```bash
git clone https://github.com/example/myproject.git
cd myproject
make setup   # spins up Docker services, installs Go & npm deps
make run     # starts backend + frontend
```

If `make setup` fails, run the steps manually:

```bash
docker-compose up -d
go mod download
cd frontend && npm install
```

To run backend and frontend separately:

```bash
# Terminal 1 - Backend
go run cmd/server/main.go

# Terminal 2 - Frontend
cd frontend && npm start
```

## Configuration

Copy `.env.example` to `.env` and fill in the values.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | -- | PostgreSQL connection string |
| `REDIS_URL` | Yes | -- | Redis connection string |
| `JWT_SECRET` | Yes | -- | Secret key for JWT signing |
| `API_PORT` | No | `8080` | HTTP port for the API server |
| `FRONTEND_URL` | No | -- | Allowed origin for CORS |
| `LOG_LEVEL` | No | `info` | `debug` / `info` / `warn` / `error` |
| `SMTP_HOST` | No | -- | SMTP server host (for emails) |
| `SMTP_PORT` | No | -- | SMTP server port |
| `SMTP_USER` | No | -- | SMTP username |
| `SMTP_PASS` | No | -- | SMTP password |

## API Endpoints

### Auth

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate and receive a token |

### Users

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/users` | List all users |
| GET | `/api/users/:id` | Get a user by ID |
| PUT | `/api/users/:id` | Update a user |
| DELETE | `/api/users/:id` | Delete a user |

### Products

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/products` | List all products |
| POST | `/api/products` | Create a product |
| GET | `/api/products/:id` | Get a product by ID |
| PUT | `/api/products/:id` | Update a product |
| DELETE | `/api/products/:id` | Delete a product |

### Orders

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/orders` | List all orders |
| POST | `/api/orders` | Create an order |

## Testing

```bash
make test            # run all tests
make test-coverage   # run tests with coverage report
```

## Deployment

Deployment runs through the **GitLab CI/CD** pipeline on AWS:

1. Push to `main` -- auto-deploys to **staging**.
2. Create a Git tag -- triggers **production** deploy.

## Contributing

1. Branch from `main`.
2. Follow [Conventional Commits](https://www.conventionalcommits.org/).
3. Ensure all tests pass.
4. Open a pull request.

## License

MIT
