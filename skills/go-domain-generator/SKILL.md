---
name: go-domain-generator
description: Generate DDD + Clean Architecture domain code for Go projects following strict encapsulation rules. Creates entities with private fields, getters, constructors, restore functions, and behavior methods. Use when creating new domain models in internal/domain/ with entity/, repository/, and service/ structure. Trigger when user asks to create domain, generate domain code, or scaffold new domain entity.
---

# Go Domain Generator

Generate DDD + Clean Architecture domain code following strict encapsulation rules from AGENTS.md.

## Architecture Overview

```
internal/domain/
├── entity/          # Business logic, validation, domain calculations
├── repository/      # Data access interfaces (implementation in infrastructure/)
└── service/         # Domain services for logic spanning multiple entities
```

## Entity Design Rules (MUST FOLLOW)

| Rule | Description |
|------|-------------|
| Private fields | All struct fields lowercase (unexported) |
| Getters | Read-only access via `FieldName() Type` methods |
| Constructor | `NewXxx()` or `NewXxx(param *NewXxxParam)` for creation |
| Behavior methods | State changes via methods with business logic |
| Update methods | `Update(param *UpdateXxxParam)` for partial updates |
| Restore function | `RestoreXxx()` for repository reads only |
| No setters | Do NOT create individual `SetField()` methods |

## Repository Naming Conventions

| Prefix | Meaning | Returns |
|--------|---------|---------|
| `GetXxx` | Get single entity by identifier | `(*Entity, error)` |
| `GetAll` | Get all entities (no filter) | `([]*Entity, error)` |
| `QueryXxx` | Query with conditions/filters | `([]*Entity, error)` or `(*Entity, error)` |
| `Create` | Create new entity | `error` |
| `Update` | Update existing entity | `error` |
| `Delete` | Delete entity | `error` |
| `Exists` | Check existence | `(bool, error)` |
| `Count` | Count entities | `(int64, error)` |

## Generation Steps

### Step 1: Entity (`internal/domain/entity/{domain_snake}.go`)

```go
package entity

import (
    "time"

    "github.com/google/uuid"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/clock"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/errs"
)

// Status type definition
type {DomainName}Status string

const (
    {DomainName}StatusActive   {DomainName}Status = "active"
    {DomainName}StatusInactive {DomainName}Status = "inactive"
)

// {DomainName} entity with private fields
type {DomainName} struct {
    id        string
    name      string
    status    {DomainName}Status
    createdAt time.Time
    updatedAt time.Time
}

// Getters - read-only access to private fields
func (e *{DomainName}) ID() string             { return e.id }
func (e *{DomainName}) Name() string           { return e.name }
func (e *{DomainName}) Status() {DomainName}Status { return e.status }
func (e *{DomainName}) CreatedAt() time.Time   { return e.createdAt }
func (e *{DomainName}) UpdatedAt() time.Time   { return e.updatedAt }

// New{DomainName}Param for entity creation
type New{DomainName}Param struct {
    Name   string
    Status {DomainName}Status
}

// New{DomainName} is the ONLY way to create new entities.
// Use this for all new entity creation.
func New{DomainName}(param *New{DomainName}Param) *{DomainName} {
    now := clock.Now()
    return &{DomainName}{
        id:        uuid.New().String(),
        name:      param.Name,
        status:    param.Status,
        createdAt: now,
        updatedAt: now,
    }
}

// Restore{DomainName} creates a {DomainName} from database fields.
// ONLY use in repository layer for database reads.
func Restore{DomainName}(
    id string,
    name string,
    status {DomainName}Status,
    createdAt time.Time,
    updatedAt time.Time,
) *{DomainName} {
    return &{DomainName}{
        id:        id,
        name:      name,
        status:    status,
        createdAt: createdAt,
        updatedAt: updatedAt,
    }
}

// Status check methods
func (e *{DomainName}) IsActive() bool   { return e.status == {DomainName}StatusActive }
func (e *{DomainName}) IsInactive() bool { return e.status == {DomainName}StatusInactive }

// Behavior Methods (Domain Logic)
// State changes MUST go through these methods with business rules.

func (e *{DomainName}) Activate() error {
    if e.IsActive() {
        return errs.New("{domain_name} is already active")
    }
    e.status = {DomainName}StatusActive
    e.updatedAt = clock.Now()
    return nil
}

func (e *{DomainName}) Deactivate() error {
    if e.IsInactive() {
        return errs.New("{domain_name} is already inactive")
    }
    e.status = {DomainName}StatusInactive
    e.updatedAt = clock.Now()
    return nil
}

// Update{DomainName}Param for partial updates
type Update{DomainName}Param struct {
    Name   *string
    Status *{DomainName}Status
}

// Update applies partial updates with validation.
// Use for updates from external input (API, etc).
func (e *{DomainName}) Update(param *Update{DomainName}Param) error {
    now := clock.Now()
    
    if param.Name != nil {
        if *param.Name == "" {
            return errs.New("name cannot be empty")
        }
        e.name = *param.Name
    }
    
    if param.Status != nil {
        e.status = *param.Status
    }
    
    e.updatedAt = now
    return nil
}
```

### Step 2: Repository Interface (`internal/domain/repository/{domain_snake}_repository.go`)

```go
package repository

import (
    "context"

    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
)

//go:generate mockgen -typed --package mocks --destination ./mocks/{domain_snake}_repo_mock.go . {DomainName}Repository

// {DomainName}Repository defines data access operations for {DomainName}.
// Implementation lives in internal/infrastructure/persistence/
// 
// Naming conventions:
// - GetXxx: Get single entity by identifier
// - GetAll: Get all entities (no filter)
// - QueryXxx: Query with conditions/filters
type {DomainName}Repository interface {
    // Create creates a new entity
    Create(ctx context.Context, e *entity.{DomainName}) error
    
    // GetByID retrieves a single entity by ID
    GetByID(ctx context.Context, id string) (*entity.{DomainName}, error)
    
    // GetAll retrieves all entities
    GetAll(ctx context.Context) ([]*entity.{DomainName}, error)
    
    // Update updates an existing entity
    Update(ctx context.Context, e *entity.{DomainName}) error
    
    // Delete deletes an entity by ID
    Delete(ctx context.Context, id string) error
}
```

### Step 3: Domain Service (`internal/domain/service/{domain_snake}_service.go`)

```go
package service

import (
    "context"

    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/repository"
)

// {DomainName}Service handles business logic for {DomainName} domain.
// For logic spanning multiple entities or not belonging to a single entity.
// Does NOT orchestrate flow—that's the usecase's job.
type {DomainName}Service struct {
    repo repository.{DomainName}Repository
}

// New{DomainName}Service creates a new instance of {DomainName}Service.
func New{DomainName}Service(repo repository.{DomainName}Repository) *{DomainName}Service {
    return &{DomainName}Service{repo: repo}
}

// Create creates a new {DomainName}.
func (s *{DomainName}Service) Create(ctx context.Context, param *entity.New{DomainName}Param) (*entity.{DomainName}, error) {
    e := entity.New{DomainName}(param)
    if err := s.repo.Create(ctx, e); err != nil {
        return nil, err
    }
    return e, nil
}

// GetByID retrieves a {DomainName} by ID.
func (s *{DomainName}Service) GetByID(ctx context.Context, id string) (*entity.{DomainName}, error) {
    return s.repo.GetByID(ctx, id)
}

// GetAll retrieves all {DomainName}s.
func (s *{DomainName}Service) GetAll(ctx context.Context) ([]*entity.{DomainName}, error) {
    return s.repo.GetAll(ctx)
}

// Update updates a {DomainName} with partial data.
func (s *{DomainName}Service) Update(ctx context.Context, id string, param *entity.Update{DomainName}Param) (*entity.{DomainName}, error) {
    e, err := s.repo.GetByID(ctx, id)
    if err != nil {
        return nil, err
    }
    if err := e.Update(param); err != nil {
        return nil, err
    }
    if err := s.repo.Update(ctx, e); err != nil {
        return nil, err
    }
    return e, nil
}

// Activate activates a {DomainName}.
func (s *{DomainName}Service) Activate(ctx context.Context, id string) (*entity.{DomainName}, error) {
    e, err := s.repo.GetByID(ctx, id)
    if err != nil {
        return nil, err
    }
    if err := e.Activate(); err != nil {
        return nil, err
    }
    if err := s.repo.Update(ctx, e); err != nil {
        return nil, err
    }
    return e, nil
}

// Deactivate deactivates a {DomainName}.
func (s *{DomainName}Service) Deactivate(ctx context.Context, id string) (*entity.{DomainName}, error) {
    e, err := s.repo.GetByID(ctx, id)
    if err != nil {
        return nil, err
    }
    if err := e.Deactivate(); err != nil {
        return nil, err
    }
    if err := s.repo.Update(ctx, e); err != nil {
        return nil, err
    }
    return e, nil
}

// Delete deletes a {DomainName} by ID.
func (s *{DomainName}Service) Delete(ctx context.Context, id string) error {
    return s.repo.Delete(ctx, id)
}
```

## Repository Implementation Example

Repository implementation goes in `internal/infrastructure/persistence/`:

```go
// File: internal/infrastructure/persistence/postgres/{domain_snake}_repository.go

package postgres

import (
    "context"
    
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/errs"
    "github.com/jackc/pgx/v5"
)

type {domainName}Repository struct {
    db *pgx.Conn
}

func New{DomainName}Repository(db *pgx.Conn) repository.{DomainName}Repository {
    return &{domainName}Repository{db: db}
}

// GetByID retrieves a single entity by ID
func (r *{domainName}Repository) GetByID(ctx context.Context, id string) (*entity.{DomainName}, error) {
    var (
        eID        string
        name       string
        status     entity.{DomainName}Status
        createdAt  time.Time
        updatedAt  time.Time
    )

    err := r.db.QueryRow(ctx,
        `SELECT id, name, status, created_at, updated_at 
         FROM {domain_snake}s WHERE id = $1`, id,
    ).Scan(&eID, &name, &status, &createdAt, &updatedAt)
    
    if err != nil {
        if errs.Is(err, pgx.ErrNoRows) {
            return nil, nil
        }
        return nil, errs.WithStack(err)
    }

    // Use restore function - ONLY place where entity fields are set from DB
    return entity.Restore{DomainName}(eID, name, status, createdAt, updatedAt), nil
}

// Create creates a new entity
func (r *{domainName}Repository) Create(ctx context.Context, e *entity.{DomainName}) error {
    _, err := r.db.Exec(ctx,
        `INSERT INTO {domain_snake}s (id, name, status, created_at, updated_at) 
         VALUES ($1, $2, $3, $4, $5)`,
        e.ID(), e.Name(), e.Status(), e.CreatedAt(), e.UpdatedAt(),
    )
    return errs.WithStack(err)
}

// Update updates an existing entity
func (r *{domainName}Repository) Update(ctx context.Context, e *entity.{DomainName}) error {
    _, err := r.db.Exec(ctx,
        `UPDATE {domain_snake}s 
         SET name = $1, status = $2, updated_at = $3 
         WHERE id = $4`,
        e.Name(), e.Status(), e.UpdatedAt(), e.ID(),
    )
    return errs.WithStack(err)
}

// Delete deletes an entity by ID
func (r *{domainName}Repository) Delete(ctx context.Context, id string) error {
    _, err := r.db.Exec(ctx, `DELETE FROM {domain_snake}s WHERE id = $1`, id)
    return errs.WithStack(err)
}

// GetAll retrieves all entities
func (r *{domainName}Repository) GetAll(ctx context.Context) ([]*entity.{DomainName}, error) {
    rows, err := r.db.Query(ctx,
        `SELECT id, name, status, created_at, updated_at FROM {domain_snake}s`,
    )
    if err != nil {
        return nil, errs.WithStack(err)
    }
    defer rows.Close()

    var result []*entity.{DomainName}
    for rows.Next() {
        var (
            eID       string
            name      string
            status    entity.{DomainName}Status
            createdAt time.Time
            updatedAt time.Time
        )
        if err := rows.Scan(&eID, &name, &status, &createdAt, &updatedAt); err != nil {
            return nil, errs.WithStack(err)
        }
        result = append(result, entity.Restore{DomainName}(eID, name, status, createdAt, updatedAt))
    }
    return result, nil
}
```

## Customization Guidelines

### Adding Repository Methods with Conventions

```go
type {DomainName}Repository interface {
    // Basic CRUD
    Create(ctx context.Context, e *entity.{DomainName}) error
    GetByID(ctx context.Context, id string) (*entity.{DomainName}, error)
    GetAll(ctx context.Context) ([]*entity.{DomainName}, error)
    Update(ctx context.Context, e *entity.{DomainName}) error
    Delete(ctx context.Context, id string) error
    
    // GetXxx - Get single entity by identifier
    GetByEmail(ctx context.Context, email string) (*entity.{DomainName}, error)
    GetByCode(ctx context.Context, code string) (*entity.{DomainName}, error)
    
    // QueryXxx - Query with conditions/filters
    QueryByStatus(ctx context.Context, status entity.{DomainName}Status) ([]*entity.{DomainName}, error)
    QueryByDateRange(ctx context.Context, start, end time.Time) ([]*entity.{DomainName}, error)
    QueryWithFilters(ctx context.Context, filters QueryFilters) ([]*entity.{DomainName}, error)
    
    // Exists - Check existence
    ExistsByEmail(ctx context.Context, email string) (bool, error)
    
    // Count - Count entities
    CountByStatus(ctx context.Context, status entity.{DomainName}Status) (int64, error)
}
```

### Adding Fields to Entity

1. Add private field to struct
2. Add getter method
3. Update `NewXxx()` and `RestoreXxx()` constructors
4. Update repository implementation

```go
type Order struct {
    id         string
    customerID string      // Add this
    total      float64     // Add this
    items      []*OrderItem // Add this
    status     OrderStatus
    createdAt  time.Time
    updatedAt  time.Time
}

// Add getters
func (o *Order) CustomerID() string { return o.customerID }
func (o *Order) Total() float64     { return o.total }
func (o *Order) Items() []*OrderItem { return o.items }
```

### Adding Business Methods

```go
// Example: Order entity with items
func (o *Order) AddItem(productID string, quantity int, price float64) error {
    if o.status != OrderStatusPending {
        return errs.New("can only add items to pending orders")
    }
    if quantity <= 0 {
        return errs.New("quantity must be positive")
    }
    
    item := &OrderItem{
        productID: productID,
        quantity:  quantity,
        price:     price,
    }
    o.items = append(o.items, item)
    o.total += price * float64(quantity)
    o.updatedAt = clock.Now()
    return nil
}

func (o *Order) RemoveItem(productID string) error {
    if o.status != OrderStatusPending {
        return errs.New("can only remove items from pending orders")
    }
    // ... removal logic
    o.updatedAt = clock.Now()
    return nil
}
```

## References

See `references/` directory for detailed patterns:
- `entity_patterns.md` - Entity patterns and examples
- `repository_patterns.md` - Repository interface patterns  
- `service_patterns.md` - Domain service patterns

## Transaction Pattern (Usecase Controls Transaction)

In Clean Architecture, **usecase** controls transaction boundaries (Begin/Commit/Rollback), while **domain service** contains pure business logic without knowing about transactions.

### Architecture

```
usecase/                    ← Orchestrates flow, controls transaction
├── order_usecase.go

domain/service/             ← Pure business logic, no transaction knowledge
├── order_service.go

domain/repository/          ← Interfaces, accepts transaction
├── transaction.go
├── order_repository.go
└── payment_repository.go

infrastructure/persistence/ ← Implementation
└── postgres/
    ├── transaction.go
    ├── order_repository.go
    └── payment_repository.go
```

### Step 1: Transaction Interface

```go
// File: internal/domain/repository/transaction.go

package repository

import "context"

// Transaction represents a database transaction
type Transaction interface {
    Commit() error
    Rollback() error
}

// TransactionManager manages database transactions
type TransactionManager interface {
    Begin(ctx context.Context) (Transaction, error)
}
```

### Step 2: Repository Interfaces with Transaction

```go
// File: internal/domain/repository/order_repository.go

package repository

import (
    "context"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
)

//go:generate mockgen -typed --package mocks --destination ./mocks/order_repo_mock.go . OrderRepository

type OrderRepository interface {
    Create(ctx context.Context, tx Transaction, order *entity.Order) error
    GetByID(ctx context.Context, tx Transaction, id string) (*entity.Order, error)
    Update(ctx context.Context, tx Transaction, order *entity.Order) error
    Delete(ctx context.Context, tx Transaction, id string) error
}
```

```go
// File: internal/domain/repository/payment_repository.go

package repository

import (
    "context"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
)

//go:generate mockgen -typed --package mocks --destination ./mocks/payment_repo_mock.go . PaymentRepository

type PaymentRepository interface {
    Create(ctx context.Context, tx Transaction, payment *entity.Payment) error
    GetByID(ctx context.Context, tx Transaction, id string) (*entity.Payment, error)
    Update(ctx context.Context, tx Transaction, payment *entity.Payment) error
    GetByOrderID(ctx context.Context, tx Transaction, orderID string) (*entity.Payment, error)
}
```

### Step 3: Domain Service (Pure Business Logic)

```go
// File: internal/domain/service/order_service.go

package service

import (
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/errs"
)

// OrderService contains pure business logic, NO transaction knowledge
type OrderService struct{}

func NewOrderService() *OrderService {
    return &OrderService{}
}

// CalculateTotal calculates order total from items
func (s *OrderService) CalculateTotal(items []*entity.OrderItem) float64 {
    var total float64
    for _, item := range items {
        total += item.Price() * float64(item.Quantity())
    }
    return total
}

// ValidateOrder validates order business rules
func (s *OrderService) ValidateOrder(order *entity.Order) error {
    if len(order.Items()) == 0 {
        return errs.New("order must have at least one item")
    }
    if order.Total() <= 0 {
        return errs.New("order total must be greater than zero")
    }
    return nil
}

// CanCancel checks if order can be cancelled
func (s *OrderService) CanCancel(order *entity.Order) error {
    if order.Status() == entity.OrderStatusShipped {
        return errs.New("cannot cancel shipped order")
    }
    if order.Status() == entity.OrderStatusCancelled {
        return errs.New("order is already cancelled")
    }
    return nil
}
```

### Step 4: Usecase (Controls Transaction)

```go
// File: internal/usecase/order_usecase.go

package usecase

import (
    "context"
    
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/repository"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/service"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/errs"
)

// OrderUsecase orchestrates order operations and controls transactions
type OrderUsecase struct {
    txManager      repository.TransactionManager
    orderRepo      repository.OrderRepository
    paymentRepo    repository.PaymentRepository
    orderService   *service.OrderService
}

func NewOrderUsecase(
    txManager repository.TransactionManager,
    orderRepo repository.OrderRepository,
    paymentRepo repository.PaymentRepository,
    orderService *service.OrderService,
) *OrderUsecase {
    return &OrderUsecase{
        txManager:    txManager,
        orderRepo:    orderRepo,
        paymentRepo:  paymentRepo,
        orderService: orderService,
    }
}

// CreateOrderWithPayment creates order and payment in atomic transaction
func (uc *OrderUsecase) CreateOrderWithPayment(
    ctx context.Context,
    orderParam *entity.NewOrderParam,
    paymentParam *entity.NewPaymentParam,
) (*entity.Order, *entity.Payment, error) {
    
    // 1. Begin transaction
    tx, err := uc.txManager.Begin(ctx)
    if err != nil {
        return nil, nil, errs.WithStack(err)
    }
    
    // 2. Defer rollback (will be no-op if committed)
    defer func() {
        if tx != nil {
            _ = tx.Rollback()
        }
    }()
    
    // 3. Create order
    order := entity.NewOrder(orderParam)
    
    // 4. Validate business rules (pure logic, no transaction)
    if err := uc.orderService.ValidateOrder(order); err != nil {
        return nil, nil, err
    }
    
    // 5. Save order within transaction
    if err := uc.orderRepo.Create(ctx, tx, order); err != nil {
        return nil, nil, err
    }
    
    // 6. Create payment linked to order
    payment := entity.NewPayment(&entity.NewPaymentParam{
        OrderID: order.ID(),
        Amount:  order.Total(),
        Status:  entity.PaymentStatusPending,
    })
    
    // 7. Save payment within same transaction
    if err := uc.paymentRepo.Create(ctx, tx, payment); err != nil {
        return nil, nil, err
    }
    
    // 8. Commit transaction
    if err := tx.Commit(); err != nil {
        return nil, nil, errs.WithStack(err)
    }
    
    // 9. Set tx to nil so defer rollback won't execute
    tx = nil
    
    return order, payment, nil
}

// CancelOrder cancels order and refunds payment in transaction
func (uc *OrderUsecase) CancelOrder(ctx context.Context, orderID string) error {
    
    // 1. Begin transaction
    tx, err := uc.txManager.Begin(ctx)
    if err != nil {
        return errs.WithStack(err)
    }
    defer func() {
        if tx != nil {
            _ = tx.Rollback()
        }
    }()
    
    // 2. Get order
    order, err := uc.orderRepo.GetByID(ctx, tx, orderID)
    if err != nil {
        return err
    }
    if order == nil {
        return errs.Newf("order not found: %s", orderID)
    }
    
    // 3. Check business rules (pure logic)
    if err := uc.orderService.CanCancel(order); err != nil {
        return err
    }
    
    // 4. Cancel order
    if err := order.Cancel(); err != nil {
        return err
    }
    
    // 5. Update order
    if err := uc.orderRepo.Update(ctx, tx, order); err != nil {
        return err
    }
    
    // 6. Get and refund payment
    payment, err := uc.paymentRepo.GetByOrderID(ctx, tx, orderID)
    if err != nil {
        return err
    }
    if payment != nil && payment.Status() == entity.PaymentStatusCompleted {
        if err := payment.Refund(); err != nil {
            return err
        }
        if err := uc.paymentRepo.Update(ctx, tx, payment); err != nil {
            return err
        }
    }
    
    // 7. Commit
    if err := tx.Commit(); err != nil {
        return errs.WithStack(err)
    }
    tx = nil
    
    return nil
}
```

### Step 5: Infrastructure Implementation

```go
// File: internal/infrastructure/persistence/postgres/transaction.go

package postgres

import (
    "context"
    "github.com/jackc/pgx/v5"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/repository"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/errs"
)

// pgxTransaction wraps pgx transaction
type pgxTransaction struct {
    tx pgx.Tx
}

func (t *pgxTransaction) Commit() error {
    return t.tx.Commit(context.Background())
}

func (t *pgxTransaction) Rollback() error {
    return t.tx.Rollback(context.Background())
}

// pgxTransactionManager implements repository.TransactionManager
type pgxTransactionManager struct {
    db *pgx.Conn
}

func NewTransactionManager(db *pgx.Conn) repository.TransactionManager {
    return &pgxTransactionManager{db: db}
}

func (tm *pgxTransactionManager) Begin(ctx context.Context) (repository.Transaction, error) {
    tx, err := tm.db.Begin(ctx)
    if err != nil {
        return nil, errs.WithStack(err)
    }
    return &pgxTransaction{tx: tx}, nil
}
```

```go
// File: internal/infrastructure/persistence/postgres/order_repository.go

package postgres

import (
    "context"
    "github.com/jackc/pgx/v5"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/repository"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/errs"
)

type orderRepository struct {
    db *pgx.Conn
}

func NewOrderRepository(db *pgx.Conn) repository.OrderRepository {
    return &orderRepository{db: db}
}

func (r *orderRepository) Create(ctx context.Context, tx repository.Transaction, order *entity.Order) error {
    // Extract pgx transaction from interface
    pgxTx := tx.(*pgxTransaction).tx
    
    _, err := pgxTx.Exec(ctx,
        `INSERT INTO orders (id, customer_id, total, status, created_at, updated_at) 
         VALUES ($1, $2, $3, $4, $5, $6)`,
        order.ID(), order.CustomerID(), order.Total(), order.Status(), 
        order.CreatedAt(), order.UpdatedAt(),
    )
    return errs.WithStack(err)
}

func (r *orderRepository) GetByID(ctx context.Context, tx repository.Transaction, id string) (*entity.Order, error) {
    pgxTx := tx.(*pgxTransaction).tx
    
    var (
        orderID    string
        customerID string
        total      float64
        status     entity.OrderStatus
        createdAt  time.Time
        updatedAt  time.Time
    )
    
    err := pgxTx.QueryRow(ctx,
        `SELECT id, customer_id, total, status, created_at, updated_at 
         FROM orders WHERE id = $1`, id,
    ).Scan(&orderID, &customerID, &total, &status, &createdAt, &updatedAt)
    
    if err != nil {
        if errs.Is(err, pgx.ErrNoRows) {
            return nil, nil
        }
        return nil, errs.WithStack(err)
    }
    
    return entity.RestoreOrder(orderID, customerID, total, status, createdAt, updatedAt), nil
}

func (r *orderRepository) Update(ctx context.Context, tx repository.Transaction, order *entity.Order) error {
    pgxTx := tx.(*pgxTransaction).tx
    
    _, err := pgxTx.Exec(ctx,
        `UPDATE orders 
         SET customer_id = $1, total = $2, status = $3, updated_at = $4 
         WHERE id = $5`,
        order.CustomerID(), order.Total(), order.Status(), 
        order.UpdatedAt(), order.ID(),
    )
    return errs.WithStack(err)
}

func (r *orderRepository) Delete(ctx context.Context, tx repository.Transaction, id string) error {
    pgxTx := tx.(*pgxTransaction).tx
    
    _, err := pgxTx.Exec(ctx, `DELETE FROM orders WHERE id = $1`, id)
    return errs.WithStack(err)
}
```

### Key Principles

| Layer | Responsibility | Transaction Knowledge |
|-------|---------------|----------------------|
| **Usecase** | Orchestrate flow, control transaction boundaries | ✅ Yes (Begin/Commit/Rollback) |
| **Domain Service** | Pure business logic, validation | ❌ No |
| **Repository** | Data access, accept transaction | ✅ Yes (as parameter) |
| **Entity** | Business rules, state changes | ❌ No |

### Testing

```go
// Mock transaction for testing
type mockTransaction struct {
    committed   bool
    rolledBack  bool
}

func (m *mockTransaction) Commit() error {
    m.committed = true
    return nil
}

func (m *mockTransaction) Rollback() error {
    m.rolledBack = true
    return nil
}

// Test usecase
type mockTxManager struct {
    tx *mockTransaction
}

func (m *mockTxManager) Begin(ctx context.Context) (repository.Transaction, error) {
    return m.tx, nil
}

func TestOrderUsecase_CreateOrderWithPayment(t *testing.T) {
    // Arrange
    mockTx := &mockTransaction{}
    txManager := &mockTxManager{tx: mockTx}
    orderRepo := &mockOrderRepo{}
    paymentRepo := &mockPaymentRepo{}
    orderService := service.NewOrderService()
    
    uc := NewOrderUsecase(txManager, orderRepo, paymentRepo, orderService)
    
    // Act
    order, payment, err := uc.CreateOrderWithPayment(ctx, orderParam, paymentParam)
    
    // Assert
    assert.NoError(t, err)
    assert.NotNil(t, order)
    assert.NotNil(t, payment)
    assert.True(t, mockTx.committed)
    assert.False(t, mockTx.rolledBack)
}
```
