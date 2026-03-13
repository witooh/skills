# Go Framework Scan Patterns

How to discover routes and extract endpoint details from Go web frameworks. Start by detecting which framework is used — check `go.mod` for the import path.

## Framework Detection

| Import in go.mod | Framework |
|------------------|-----------|
| `github.com/gofiber/fiber` | Fiber |
| `github.com/labstack/echo` | Echo |
| `github.com/go-chi/chi` | Chi |
| `github.com/gin-gonic/gin` | Gin |

## Route Registration Patterns

### Fiber

```go
// Direct registration
app.Get("/api/v1/users", handler.ListUsers)
app.Post("/api/v1/users", handler.CreateUser)
app.Get("/api/v1/users/:id", handler.GetUser)

// Group registration
api := app.Group("/api/v1")
users := api.Group("/users")
users.Get("/", handler.ListUsers)
users.Post("/", handler.CreateUser)
users.Get("/:id", handler.GetUser)
```

**Search patterns:**
```
app.Get(    app.Post(    app.Put(    app.Patch(    app.Delete(
.Group(
```

**Handler signature:** `func(c *fiber.Ctx) error`

**Parameter extraction:**
- Path params: `c.Params("id")`
- Query params: `c.Query("page")`, `c.QueryInt("limit")`
- Body parsing: `c.BodyParser(&req)`

### Echo

```go
// Direct registration
e.GET("/api/v1/users", handler.ListUsers)
e.POST("/api/v1/users", handler.CreateUser)
e.GET("/api/v1/users/:id", handler.GetUser)

// Group registration
api := e.Group("/api/v1")
users := api.Group("/users")
users.GET("/", handler.ListUsers)
```

**Search patterns:**
```
e.GET(    e.POST(    e.PUT(    e.PATCH(    e.DELETE(
.Group(
```

**Handler signature:** `func(c echo.Context) error`

**Parameter extraction:**
- Path params: `c.Param("id")`
- Query params: `c.QueryParam("page")`
- Body parsing: `c.Bind(&req)`

### Chi

```go
// Direct registration
r.Get("/api/v1/users", handler.ListUsers)
r.Post("/api/v1/users", handler.CreateUser)
r.Get("/api/v1/users/{id}", handler.GetUser)

// Group registration
r.Route("/api/v1", func(r chi.Router) {
    r.Route("/users", func(r chi.Router) {
        r.Get("/", handler.ListUsers)
        r.Post("/", handler.CreateUser)
        r.Get("/{id}", handler.GetUser)
    })
})
```

**Search patterns:**
```
r.Get(    r.Post(    r.Put(    r.Patch(    r.Delete(
r.Route(
```

**Handler signature:** `func(w http.ResponseWriter, r *http.Request)`

**Parameter extraction:**
- Path params: `chi.URLParam(r, "id")`
- Query params: `r.URL.Query().Get("page")`
- Body parsing: `json.NewDecoder(r.Body).Decode(&req)`

### Gin

```go
// Direct registration
r.GET("/api/v1/users", handler.ListUsers)
r.POST("/api/v1/users", handler.CreateUser)
r.GET("/api/v1/users/:id", handler.GetUser)

// Group registration
api := r.Group("/api/v1")
users := api.Group("/users")
users.GET("/", handler.ListUsers)
```

**Search patterns:**
```
r.GET(    r.POST(    r.PUT(    r.PATCH(    r.DELETE(
.Group(
```

**Handler signature:** `func(c *gin.Context)`

**Parameter extraction:**
- Path params: `c.Param("id")`
- Query params: `c.Query("page")`, `c.DefaultQuery("page", "1")`
- Body parsing: `c.ShouldBindJSON(&req)`

## Extracting Request/Response Structs

After finding a handler, trace the request and response types:

### Request Structs

Look for structs with JSON tags used in body parsing:

```go
type CreateUserRequest struct {
    Name     string `json:"name" validate:"required"`
    Email    string `json:"email" validate:"required,email"`
    Age      int    `json:"age,omitempty" validate:"min=0,max=150"`
}
```

**Tag interpretation:**
- `json:"name"` → field name in JSON
- `json:",omitempty"` → optional field
- `validate:"required"` → mandatory (M)
- `validate:"min=X,max=Y"` → range constraint (note in Remark)
- `validate:"oneof=a b c"` → enum values (note in Remark)

**Where to find:** Same package as handler, typically `request.go` or `dto.go`

### Response Structs

```go
type UserResponse struct {
    ID        string    `json:"id"`
    Name      string    `json:"name"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}
```

**Where to find:** Same package as handler, typically `response.go` or inline in handler

### Error Mapping

Look for error-to-status-code mapping in handlers:

```go
// Typed error checks (preferred pattern)
switch {
case errors.Is(err, domain.ErrNotFound):
    return c.Status(fiber.StatusNotFound).JSON(...)
case errors.Is(err, domain.ErrDuplicate):
    return c.Status(fiber.StatusConflict).JSON(...)
default:
    return c.Status(fiber.StatusInternalServerError).JSON(...)
}
```

Extract each case as an error response entry in the doc.

## Scan Strategy

1. **Find go.mod** → detect framework
2. **Find router file** → `Grep` for route registration patterns
3. **Resolve handler functions** → follow the function reference to its definition
4. **Find request/response structs** → `Grep` for struct types used in handlers
5. **Find error mapping** → look for status code assignments in handler error paths
6. **Find domain entities** → if response wraps an entity, trace to `entity.go`
