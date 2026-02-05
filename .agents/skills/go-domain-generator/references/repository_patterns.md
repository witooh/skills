# Repository Patterns

Repository interface patterns for Clean Architecture.

## Basic Repository Interface

```go
package repository

import (
    "context"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
)

//go:generate mockgen -typed --package mocks --destination ./mocks/order_repo_mock.go . OrderRepository
type OrderRepository interface {
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    GetAll(ctx context.Context) ([]*entity.Order, error)
    Update(ctx context.Context, order *entity.Order) error
    Delete(ctx context.Context, id string) error
}
```

## Repository with Query Methods

```go
type OrderRepository interface {
    // CRUD operations
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    Update(ctx context.Context, order *entity.Order) error
    Delete(ctx context.Context, id string) error
    
    // Query methods
    GetByCustomerID(ctx context.Context, customerID string) ([]*entity.Order, error)
    GetByStatus(ctx context.Context, status entity.OrderStatus) ([]*entity.Order, error)
    GetByDateRange(ctx context.Context, start, end time.Time) ([]*entity.Order, error)
    
    // Search methods
    Search(ctx context.Context, criteria OrderSearchCriteria) ([]*entity.Order, error)
    
    // Count methods
    CountByStatus(ctx context.Context, status entity.OrderStatus) (int64, error)
    CountByCustomer(ctx context.Context, customerID string) (int64, error)
}

type OrderSearchCriteria struct {
    CustomerID *string
    Status     *entity.OrderStatus
    FromDate   *time.Time
    ToDate     *time.Time
    Limit      int
    Offset     int
}
```

## Repository with Transaction Support

```go
type OrderRepository interface {
    // Basic CRUD
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    Update(ctx context.Context, order *entity.Order) error
    Delete(ctx context.Context, id string) error
    
    // Transaction support
    CreateWithTransaction(ctx context.Context, order *entity.Order, auditLog *entity.AuditLog) error
    UpdateWithTransaction(ctx context.Context, order *entity.Order, auditLog *entity.AuditLog) error
}
```

## Repository with Pagination

```go
type Pagination struct {
    Limit  int
    Offset int
}

type PaginatedResult struct {
    Items      []*entity.Order
    TotalCount int64
    HasMore    bool
}

type OrderRepository interface {
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    
    // Paginated queries
    GetAllPaginated(ctx context.Context, pagination Pagination) (*PaginatedResult, error)
    GetByCustomerPaginated(ctx context.Context, customerID string, pagination Pagination) (*PaginatedResult, error)
}
```

## Repository with Existence Check

```go
type OrderRepository interface {
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    
    // Existence checks
    ExistsByID(ctx context.Context, id string) (bool, error)
    ExistsByOrderNumber(ctx context.Context, orderNumber string) (bool, error)
    
    // Unique constraint checks
    IsOrderNumberUnique(ctx context.Context, orderNumber string, excludeID *string) (bool, error)
}
```

## Repository for Aggregate Roots

```go
type OrderRepository interface {
    // Aggregate root operations
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    GetByIDWithItems(ctx context.Context, id string) (*entity.Order, error)
    Update(ctx context.Context, order *entity.Order) error
    Delete(ctx context.Context, id string) error
    
    // Child entity operations
    AddItem(ctx context.Context, orderID string, item *entity.OrderItem) error
    RemoveItem(ctx context.Context, orderID string, itemID string) error
    UpdateItem(ctx context.Context, orderID string, item *entity.OrderItem) error
    GetItems(ctx context.Context, orderID string) ([]*entity.OrderItem, error)
}
```

## Repository with Soft Delete

```go
type OrderRepository interface {
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    GetByIDIncludeDeleted(ctx context.Context, id string) (*entity.Order, error)
    Update(ctx context.Context, order *entity.Order) error
    
    // Soft delete
    Delete(ctx context.Context, id string) error          // Soft delete
    HardDelete(ctx context.Context, id string) error      // Permanent delete
    Restore(ctx context.Context, id string) error         // Restore soft-deleted
    
    // Query with deleted filter
    GetAll(ctx context.Context, includeDeleted bool) ([]*entity.Order, error)
}
```

## Repository with Bulk Operations

```go
type OrderRepository interface {
    Create(ctx context.Context, order *entity.Order) error
    GetByID(ctx context.Context, id string) (*entity.Order, error)
    Update(ctx context.Context, order *entity.Order) error
    Delete(ctx context.Context, id string) error
    
    // Bulk operations
    CreateMany(ctx context.Context, orders []*entity.Order) error
    UpdateMany(ctx context.Context, orders []*entity.Order) error
    DeleteMany(ctx context.Context, ids []string) error
}
```
