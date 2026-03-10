# My Project

This is a project that does stuff. It was created in 2024.

## About

This project is a web application. It uses Go for the backend and React for the frontend. The database is PostgreSQL. We also use Redis for caching. The project structure follows clean architecture principles but not really strictly.

## How to install

First you need to install Go. Go to the Go website and download it. Then install Node.js. You also need Docker. Make sure Docker is running. Then you need to install PostgreSQL. Actually you don't need to install PostgreSQL separately because we use Docker for that. But you still need the psql client. Or you can use any PostgreSQL client. DBeaver is good.

After you install everything, clone the repo:
```
git clone https://github.com/example/myproject.git
```

Then go into the directory:
```
cd myproject
```

Then run:
```
make setup
```

This will set up everything. If it doesn't work, try:
```
docker-compose up -d
go mod download
npm install
```

## How to run

To run the project:
```
make run
```

Or you can run the backend and frontend separately:
```
go run cmd/server/main.go
```

```
cd frontend && npm start
```

## Environment variables

You need to set these environment variables:
- DATABASE_URL - the database URL
- REDIS_URL - the Redis URL
- JWT_SECRET - the JWT secret
- API_PORT - the port for the API (default 8080)
- FRONTEND_URL - the frontend URL for CORS
- LOG_LEVEL - the log level (debug, info, warn, error)
- SMTP_HOST - for sending emails
- SMTP_PORT - for sending emails
- SMTP_USER - for sending emails
- SMTP_PASS - for sending emails

## API

The API has these endpoints:
- POST /api/auth/login - login
- POST /api/auth/register - register
- GET /api/users - get all users
- GET /api/users/:id - get user by id
- PUT /api/users/:id - update user
- DELETE /api/users/:id - delete user
- GET /api/products - get all products
- POST /api/products - create product
- GET /api/products/:id - get product by id
- PUT /api/products/:id - update product
- DELETE /api/products/:id - delete product
- GET /api/orders - get all orders
- POST /api/orders - create order

## Testing

To run tests:
```
make test
```

To run tests with coverage:
```
make test-coverage
```

## Deployment

We deploy to AWS. The deployment is done through CI/CD pipeline in GitLab. When you push to main, it automatically deploys to staging. To deploy to production, you need to create a tag.

## Contributing

Please create a branch from main and submit a PR. Make sure tests pass. Use conventional commits.

## Team

- Alice - backend
- Bob - frontend
- Charlie - devops
- Diana - design

## License

MIT
