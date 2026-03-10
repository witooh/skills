package handler

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
)

type UserHandler struct {
	db Database
}

type User struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	if id == "" {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "id is required"}`))
		return
	}

	userId, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "invalid id"}`))
		return
	}

	user, err := h.db.FindUser(userId)
	if err != nil {
		log.Println("error finding user:", err)
		w.WriteHeader(500)
		w.Write([]byte(`{"error": "internal error"}`))
		return
	}

	data, _ := json.Marshal(user)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(200)
	w.Write(data)
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
	var user User
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "invalid body"}`))
		return
	}

	if user.Name == "" {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "name is required"}`))
		return
	}

	if user.Email == "" {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "email is required"}`))
		return
	}

	user.CreatedAt = time.Now()
	err = h.db.CreateUser(&user)
	if err != nil {
		log.Println("error creating user:", err)
		w.WriteHeader(500)
		w.Write([]byte(`{"error": "internal error"}`))
		return
	}

	data, _ := json.Marshal(user)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(201)
	w.Write(data)
}

func (h *UserHandler) UpdateUser(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	if id == "" {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "id is required"}`))
		return
	}

	userId, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "invalid id"}`))
		return
	}

	var user User
	err = json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "invalid body"}`))
		return
	}

	user.ID = userId
	err = h.db.UpdateUser(&user)
	if err != nil {
		log.Println("error updating user:", err)
		w.WriteHeader(500)
		w.Write([]byte(`{"error": "internal error"}`))
		return
	}

	data, _ := json.Marshal(user)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(200)
	w.Write(data)
}

func (h *UserHandler) DeleteUser(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	if id == "" {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "id is required"}`))
		return
	}

	userId, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write([]byte(`{"error": "invalid id"}`))
		return
	}

	err = h.db.DeleteUser(userId)
	if err != nil {
		log.Println("error deleting user:", err)
		w.WriteHeader(500)
		w.Write([]byte(`{"error": "internal error"}`))
		return
	}

	w.WriteHeader(204)
}

type Database interface {
	FindUser(id int) (*User, error)
	CreateUser(user *User) error
	UpdateUser(user *User) error
	DeleteUser(id int) error
}

func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	data, _ := json.Marshal(v)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write(data)
}

func writeError(w http.ResponseWriter, status int, msg string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	fmt.Fprintf(w, `{"error": "%s"}`, msg)
}
