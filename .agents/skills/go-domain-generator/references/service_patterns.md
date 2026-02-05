# Domain Service Patterns

Domain service patterns for complex business logic.

## Basic Domain Service

```go
package service

import (
    "context"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/entity"
    "gitlab.awesome-poc-th.com/libero-engineering/auxiliary-systems/consent/internal/domain/repository"
)

// OrderService handles business logic for Order domain
type OrderService struct {
    repo repository.OrderRepository
}

// NewOrderService creates a new instance of OrderService
func NewOrderService(repo repository.OrderRepository) *OrderService {
    return &OrderService{repo: repo}
}

// Create creates a new order
func (s *OrderService) Create(ctx context.Context, param *entity.NewOrderParam) (*entity.Order, error) {
    order := entity.NewOrder(param)
    if err := s.repo.Create(ctx, order); err != nil {
        return nil, err
    }
    return order, nil
}

// GetByID retrieves an order by ID
func (s *OrderService) GetByID(ctx context.Context, id string) (*entity.Order, error) {
    return s.repo.GetByID(ctx, id)
}

// Update updates an existing order
func (s *OrderService) Update(ctx context.Context, id string, param *entity.UpdateOrderParam) (*entity.Order, error) {
    order, err := s.repo.GetByID(ctx, id)
    if err != nil {
        return nil, err
    }
    order.Update(param)
    if err := s.repo.Update(ctx, order); err != nil {
        return nil, err
    }
    return order, nil
}

// Delete deletes an order by ID
func (s *OrderService) Delete(ctx context.Context, id string) error {
    return s.repo.Delete(ctx, id)
}
```

## Domain Service with Multiple Repositories

```go
type OrderProcessingService struct {
    orderRepo    repository.OrderRepository
    customerRepo repository.CustomerRepository
    productRepo  repository.ProductRepository
    inventoryRepo repository.InventoryRepository
}

func NewOrderProcessingService(
    orderRepo repository.OrderRepository,
    customerRepo repository.CustomerRepository,
    productRepo repository.ProductRepository,
    inventoryRepo repository.InventoryRepository,
) *OrderProcessingService {
    return &OrderProcessingService{
        orderRepo:     orderRepo,
        customerRepo:  customerRepo,
        productRepo:   productRepo,
        inventoryRepo: inventoryRepo,
    }
}

func (s *OrderProcessingService) ProcessOrder(ctx context.Context, customerID string, items []OrderItemInput) (*entity.Order, error) {
    // Validate customer exists
    customer, err := s.customerRepo.GetByID(ctx, customerID)
    if err != nil {
        return nil, err
    }
    if customer == nil {
        return nil, errs.New("customer not found")
    }
    
    // Validate products and check inventory
    for _, item := range items {
        product, err := s.productRepo.GetByID(ctx, item.ProductID)
        if err != nil {
            return nil, err
        }
        if product == nil {
            return nil, errs.Newf("product not found: %s", item.ProductID)
        }
        
        available, err := s.inventoryRepo.CheckAvailability(ctx, item.ProductID, item.Quantity)
        if err != nil {
            return nil, err
        }
        if !available {
            return nil, errs.Newf("insufficient inventory for product: %s", item.ProductID)
        }
    }
    
    // Create order
    // ... implementation
}
```

## Domain Service with Business Rules

```go
// PricingService handles complex pricing calculations
type PricingService struct{}

func NewPricingService() *PricingService {
    return &PricingService{}
}

type PricingResult struct {
    Subtotal      float64
    Discount      float64
    Tax           float64
    Total         float64
    AppliedOffers []string
}

func (s *PricingService) CalculatePrice(
    ctx context.Context,
    items []*entity.OrderItem,
    customer *entity.Customer,
    offers []*entity.Offer,
) (*PricingResult, error) {
    result := &PricingResult{}
    
    // Calculate subtotal
    for _, item := range items {
        result.Subtotal += item.UnitPrice * float64(item.Quantity)
    }
    
    // Apply customer discount
    if customer.IsVIP() {
        vipDiscount := result.Subtotal * 0.10
        result.Discount += vipDiscount
        result.AppliedOffers = append(result.AppliedOffers, "VIP Discount 10%")
    }
    
    // Apply promotional offers
    for _, offer := range offers {
        if offer.IsValid() && offer.MatchesItems(items) {
            discount := offer.CalculateDiscount(items)
            result.Discount += discount
            result.AppliedOffers = append(result.AppliedOffers, offer.Name)
        }
    }
    
    // Calculate tax
    taxableAmount := result.Subtotal - result.Discount
    result.Tax = taxableAmount * 0.07
    
    // Calculate total
    result.Total = taxableAmount + result.Tax
    
    return result, nil
}
```

## Domain Service with Validation

```go
// OrderValidationService handles order validation logic
type OrderValidationService struct {
    productRepo repository.ProductRepository
}

func NewOrderValidationService(productRepo repository.ProductRepository) *OrderValidationService {
    return &OrderValidationService{productRepo: productRepo}
}

type ValidationError struct {
    Field   string
    Message string
}

type ValidationResult struct {
    IsValid bool
    Errors  []ValidationError
}

func (s *OrderValidationService) ValidateOrder(ctx context.Context, items []OrderItemInput) (*ValidationResult, error) {
    result := &ValidationResult{
        IsValid: true,
        Errors:  []ValidationError{},
    }
    
    if len(items) == 0 {
        result.IsValid = false
        result.Errors = append(result.Errors, ValidationError{
            Field:   "items",
            Message: "order must contain at least one item",
        })
        return result, nil
    }
    
    for i, item := range items {
        if item.Quantity <= 0 {
            result.IsValid = false
            result.Errors = append(result.Errors, ValidationError{
                Field:   fmt.Sprintf("items[%d].quantity", i),
                Message: "quantity must be greater than 0",
            })
        }
        
        product, err := s.productRepo.GetByID(ctx, item.ProductID)
        if err != nil {
            return nil, err
        }
        if product == nil {
            result.IsValid = false
            result.Errors = append(result.Errors, ValidationError{
                Field:   fmt.Sprintf("items[%d].product_id", i),
                Message: fmt.Sprintf("product not found: %s", item.ProductID),
            })
        }
    }
    
    return result, nil
}
```

## Domain Service with Event Publishing

```go
type OrderEventService struct {
    repo          repository.OrderRepository
    eventPublisher EventPublisher
}

func NewOrderEventService(
    repo repository.OrderRepository,
    eventPublisher EventPublisher,
) *OrderEventService {
    return &OrderEventService{
        repo:          repo,
        eventPublisher: eventPublisher,
    }
}

func (s *OrderEventService) ConfirmOrder(ctx context.Context, orderID string) (*entity.Order, error) {
    order, err := s.repo.GetByID(ctx, orderID)
    if err != nil {
        return nil, err
    }
    
    if err := order.Confirm(); err != nil {
        return nil, err
    }
    
    if err := s.repo.Update(ctx, order); err != nil {
        return nil, err
    }
    
    // Publish event
    event := &OrderConfirmedEvent{
        OrderID:    order.ID,
        CustomerID: order.CustomerID,
        ConfirmedAt: clock.Now(),
    }
    
    if err := s.eventPublisher.Publish(ctx, event); err != nil {
        // Log error but don't fail the operation
        log.Printf("failed to publish order confirmed event: %v", err)
    }
    
    return order, nil
}
```

## Domain Service with Saga Pattern

```go
// OrderSagaService handles complex multi-step order processing
type OrderSagaService struct {
    orderRepo     repository.OrderRepository
    paymentRepo   repository.PaymentRepository
    inventoryRepo repository.InventoryRepository
    shippingRepo  repository.ShippingRepository
}

func (s *OrderSagaService) ProcessOrderSaga(ctx context.Context, orderID string) error {
    // Step 1: Reserve inventory
    order, err := s.orderRepo.GetByID(ctx, orderID)
    if err != nil {
        return err
    }
    
    for _, item := range order.Items {
        if err := s.inventoryRepo.Reserve(ctx, item.ProductID, item.Quantity); err != nil {
            // Compensate: release already reserved items
            s.compensateInventoryReservation(ctx, order.Items[:])
            return fmt.Errorf("failed to reserve inventory: %w", err)
        }
    }
    
    // Step 2: Process payment
    payment, err := s.paymentRepo.ProcessPayment(ctx, order)
    if err != nil {
        // Compensate: release inventory
        s.compensateInventoryReservation(ctx, order.Items)
        return fmt.Errorf("failed to process payment: %w", err)
    }
    
    // Step 3: Create shipment
    shipment, err := s.shippingRepo.CreateShipment(ctx, order)
    if err != nil {
        // Compensate: refund payment and release inventory
        s.compensatePayment(ctx, payment.ID)
        s.compensateInventoryReservation(ctx, order.Items)
        return fmt.Errorf("failed to create shipment: %w", err)
    }
    
    // Update order status
    order.MarkAsProcessing(shipment.ID)
    return s.orderRepo.Update(ctx, order)
}

func (s *OrderSagaService) compensateInventoryReservation(ctx context.Context, items []*entity.OrderItem) {
    for _, item := range items {
        if err := s.inventoryRepo.Release(ctx, item.ProductID, item.Quantity); err != nil {
            log.Printf("failed to compensate inventory reservation: %v", err)
        }
    }
}

func (s *OrderSagaService) compensatePayment(ctx context.Context, paymentID string) {
    if err := s.paymentRepo.Refund(ctx, paymentID); err != nil {
        log.Printf("failed to compensate payment: %v", err)
    }
}
```
