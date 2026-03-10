package handler

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
)

// Database defines the persistence interface for user operations.
type Database interface {
	FindUser(id int) (*User, error)
	CreateUser(user *User) error
	UpdateUser(user *User) error
	DeleteUser(id int) error
}

// User represents a user entity.
type User struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

// UserHandler provides HTTP handlers for user CRUD operations.
type UserHandler struct {
	db Database
}

// NewUserHandler creates a UserHandler with the given Database.
func NewUserHandler(db Database) *UserHandler {
	return &UserHandler{db: db}
}

// GetUser handles GET requests to retrieve a user by ID.
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
	userID, ok := parseIDParam(w, r)
	if !ok {
		return
	}

	user, err := h.db.FindUser(userID)
	if err != nil {
		log.Printf("error finding user (id=%d): %v", userID, err)
		writeError(w, http.StatusInternalServerError, "internal error")
		return
	}

	writeJSON(w, http.StatusOK, user)
}

// CreateUser handles POST requests to create a new user.
func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		writeError(w, http.StatusBadRequest, "invalid body")
		return
	}

	if user.Name == "" {
		writeError(w, http.StatusBadRequest, "name is required")
		return
	}
	if user.Email == "" {
		writeError(w, http.StatusBadRequest, "email is required")
		return
	}

	user.CreatedAt = time.Now()

	if err := h.db.CreateUser(&user); err != nil {
		log.Printf("error creating user: %v", err)
		writeError(w, http.StatusInternalServerError, "internal error")
		return
	}

	writeJSON(w, http.StatusCreated, user)
}

// UpdateUser handles PUT requests to update an existing user.
func (h *UserHandler) UpdateUser(w http.ResponseWriter, r *http.Request) {
	userID, ok := parseIDParam(w, r)
	if !ok {
		return
	}

	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		writeError(w, http.StatusBadRequest, "invalid body")
		return
	}

	user.ID = userID

	if err := h.db.UpdateUser(&user); err != nil {
		log.Printf("error updating user (id=%d): %v", userID, err)
		writeError(w, http.StatusInternalServerError, "internal error")
		return
	}

	writeJSON(w, http.StatusOK, user)
}

// DeleteUser handles DELETE requests to remove a user by ID.
func (h *UserHandler) DeleteUser(w http.ResponseWriter, r *http.Request) {
	userID, ok := parseIDParam(w, r)
	if !ok {
		return
	}

	if err := h.db.DeleteUser(userID); err != nil {
		log.Printf("error deleting user (id=%d): %v", userID, err)
		writeError(w, http.StatusInternalServerError, "internal error")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// --- helpers -----------------------------------------------------------------

// parseIDParam extracts and validates the "id" query parameter.
// It writes an error response and returns false if the parameter is missing or
// not a valid integer.
func parseIDParam(w http.ResponseWriter, r *http.Request) (int, bool) {
	raw := r.URL.Query().Get("id")
	if raw == "" {
		writeError(w, http.StatusBadRequest, "id is required")
		return 0, false
	}

	id, err := strconv.Atoi(raw)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid id")
		return 0, false
	}

	return id, true
}

// writeJSON marshals v as JSON and writes it with the given status code.
func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	data, err := json.Marshal(v)
	if err != nil {
		log.Printf("error marshalling JSON: %v", err)
		writeError(w, http.StatusInternalServerError, "internal error")
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write(data)
}

// writeError writes a JSON error response with the given status code and message.
func writeError(w http.ResponseWriter, status int, msg string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	fmt.Fprintf(w, `{"error": "%s"}`, msg)
}
