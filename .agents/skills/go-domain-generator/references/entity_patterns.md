# Entity Patterns

Common patterns for domain entities following DDD principles.

## Basic Entity Structure

```go
package entity

import (
    "time"
    "github.com/google/uuid"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/pkg/clock"
)

type Order struct {
    ID          string
    CustomerID  string
    TotalAmount float64
    Status      OrderStatus
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

## Status Type Pattern

```go
type OrderStatus string

const (
    OrderStatusPending    OrderStatus = "pending"
    OrderStatusConfirmed  OrderStatus = "confirmed"
    OrderStatusShipped    OrderStatus = "shipped"
    OrderStatusDelivered  OrderStatus = "delivered"
    OrderStatusCancelled  OrderStatus = "cancelled"
)
```

## Constructor Pattern

```go
type NewOrderParam struct {
    CustomerID  string
    TotalAmount float64
}

func NewOrder(param *NewOrderParam) *Order {
    now := clock.Now()
    return &Order{
        ID:          uuid.New().String(),
        CustomerID:  param.CustomerID,
        TotalAmount: param.TotalAmount,
        Status:      OrderStatusPending,
        CreatedAt:   now,
        UpdatedAt:   now,
    }
}
```

## Status Check Methods

```go
func (o *Order) IsPending() bool   { return o.Status == OrderStatusPending }
func (o *Order) IsConfirmed() bool { return o.Status == OrderStatusConfirmed }
func (o *Order) IsShipped() bool   { return o.Status == OrderStatusShipped }
func (o *Order) IsDelivered() bool { return o.Status == OrderStatusDelivered }
func (o *Order) IsCancelled() bool { return o.Status == OrderStatusCancelled }
```

## State Transition Methods

```go
func (o *Order) Confirm() error {
    if !o.IsPending() {
        return errs.New("only pending orders can be confirmed")
    }
    o.Status = OrderStatusConfirmed
    o.UpdatedAt = clock.Now()
    return nil
}

func (o *Order) Ship() error {
    if !o.IsConfirmed() {
        return errs.New("only confirmed orders can be shipped")
    }
    o.Status = OrderStatusShipped
    o.UpdatedAt = clock.Now()
    return nil
}

func (o *Order) Cancel() error {
    if o.IsDelivered() {
        return errs.New("delivered orders cannot be cancelled")
    }
    o.Status = OrderStatusCancelled
    o.UpdatedAt = clock.Now()
    return nil
}
```

## Update Pattern with Optional Fields

```go
type UpdateOrderParam struct {
    TotalAmount *float64
    Status      *OrderStatus
}

func (o *Order) Update(param *UpdateOrderParam) {
    now := clock.Now()
    
    if param.TotalAmount != nil {
        o.TotalAmount = *param.TotalAmount
    }
    if param.Status != nil {
        o.Status = *param.Status
    }
    
    o.UpdatedAt = now
}
```

## Value Object Pattern

```go
type Money struct {
    Amount   float64
    Currency string
}

func (m Money) Equals(other Money) bool {
    return m.Amount == other.Amount && m.Currency == other.Currency
}

type Address struct {
    Street  string
    City    string
    Country string
    ZipCode string
}
```

## Aggregate Root Pattern

```go
type Order struct {
    ID         string
    CustomerID string
    Items      []*OrderItem  // Value objects
    Status     OrderStatus
    CreatedAt  time.Time
    UpdatedAt  time.Time
}

type OrderItem struct {
    ProductID string
    Quantity  int
    UnitPrice float64
}

func (o *Order) AddItem(item *OrderItem) error {
    if o.IsConfirmed() {
        return errs.New("cannot add items to confirmed order")
    }
    o.Items = append(o.Items, item)
    o.UpdatedAt = clock.Now()
    return nil
}

func (o *Order) RemoveItem(productID string) error {
    if o.IsConfirmed() {
        return errs.New("cannot remove items from confirmed order")
    }
    // Remove logic...
    o.UpdatedAt = clock.Now()
    return nil
}

func (o *Order) TotalAmount() float64 {
    var total float64
    for _, item := range o.Items {
        total += item.UnitPrice * float64(item.Quantity)
    }
    return total
}
```

## Optional Fields Pattern

```go
type Customer struct {
    ID          string
    Email       string
    Phone       *string  // Optional
    DateOfBirth *time.Time  // Optional
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

## Validation Pattern

```go
func (c *Customer) Validate() error {
    if c.Email == "" {
        return errs.New("email is required")
    }
    if !isValidEmail(c.Email) {
        return errs.New("invalid email format")
    }
    return nil
}
```
