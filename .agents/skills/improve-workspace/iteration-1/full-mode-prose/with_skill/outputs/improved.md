# MyProject

E-commerce web application with user management, product catalog, and order processing.

| Layer | Technology |
|---|---|
| Backend | Go |
| Frontend | React |
| Database | PostgreSQL |
| Cache | Redis |

## Prerequisites

- [Go](https://go.dev/) 1.21+
- [Node.js](https://nodejs.org/) 18+
- [Docker](https://www.docker.com/) (runs PostgreSQL and Redis)

## Quick Start

```bash
git clone https://github.com/example/myproject.git
cd myproject
cp .env.example .env   # edit with your values
make setup              # pulls Docker images, installs dependencies
make run                # starts backend (:8080) and frontend (:3000)
```

To run services separately:

```bash
go run cmd/server/main.go   # backend only
cd frontend && npm start     # frontend only
```

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | -- |
| `REDIS_URL` | Redis connection string | -- |
| `JWT_SECRET` | Token signing key | -- |
| `API_PORT` | Backend listen port | `8080` |
| `FRONTEND_URL` | Allowed CORS origin | -- |
| `LOG_LEVEL` | Logging verbosity (`debug`, `info`, `warn`, `error`) | `info` |
| `SMTP_HOST` | Mail server host | -- |
| `SMTP_PORT` | Mail server port | -- |
| `SMTP_USER` | Mail server username | -- |
| `SMTP_PASS` | Mail server password | -- |

## API Endpoints

### Auth

| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/login` | Log in |
| POST | `/api/auth/register` | Register new account |

### Users

| Method | Path | Description |
|---|---|---|
| GET | `/api/users` | List all users |
| GET | `/api/users/:id` | Get user by ID |
| PUT | `/api/users/:id` | Update user |
| DELETE | `/api/users/:id` | Delete user |

### Products

| Method | Path | Description |
|---|---|---|
| GET | `/api/products` | List all products |
| POST | `/api/products` | Create product |
| GET | `/api/products/:id` | Get product by ID |
| PUT | `/api/products/:id` | Update product |
| DELETE | `/api/products/:id` | Delete product |

### Orders

| Method | Path | Description |
|---|---|---|
| GET | `/api/orders` | List all orders |
| POST | `/api/orders` | Create order |

## Testing

```bash
make test              # run tests
make test-coverage     # run tests with coverage report
```

## Deployment

Deployed to AWS via GitLab CI/CD:

- **Push to `main`** — auto-deploys to staging
- **Create a tag** — deploys to production

## Contributing

1. Branch from `main`
2. Use [conventional commits](https://www.conventionalcommits.org/)
3. Ensure tests pass
4. Submit a pull request

## License

MIT
