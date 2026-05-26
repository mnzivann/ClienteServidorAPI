package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

type Message struct {
	ID     string `json:"id"`
	Sender string `json:"sender"`
	Text   string `json:"text"`
}

type DatabaseSchema struct {
	Users    []string  `json:"users"`
	Messages []Message `json:"messages"`
}

var db DatabaseSchema = DatabaseSchema{Users: []string{}, Messages: []Message{}}
var mutex sync.Mutex
const dbFilename = "database.json"

func initDatabase() {
	file, err := os.ReadFile(dbFilename)
	if err == nil {
		json.Unmarshal(file, &db)
	}
}

func saveDatabase() {
	data, _ := json.MarshalIndent(db, "", "  ")
	os.WriteFile(dbFilename, data, 0644)
}

func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}

func handleMessages(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == http.MethodOptions { return }

	mutex.Lock()
	defer mutex.Unlock()

	switch r.Method {
	case http.MethodGet: // LEER
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(db.Messages)

	case http.MethodPost: // CREAR
		var msg Message
		json.NewDecoder(r.Body).Decode(&msg)
		// Generar ID único basado en milisegundos
		msg.ID = fmt.Sprintf("%d", time.Now().UnixMilli())
		
		db.Messages = append(db.Messages, msg)
		if !contains(db.Users, msg.Sender) && msg.Sender != "" {
			db.Users = append(db.Users, msg.Sender)
		}
		saveDatabase()
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(msg)

	case http.MethodPut: // ACTUALIZAR
		var msg Message
		json.NewDecoder(r.Body).Decode(&msg)
		for i, m := range db.Messages {
			if m.ID == msg.ID {
				db.Messages[i].Text = msg.Text
				break
			}
		}
		saveDatabase()
		json.NewEncoder(w).Encode(map[string]string{"status": "Mensaje actualizado"})

	case http.MethodDelete: // ELIMINAR MENSAJE
		id := r.URL.Query().Get("id")
		for i, m := range db.Messages {
			if m.ID == id {
				// Borrar elemento del slice
				db.Messages = append(db.Messages[:i], db.Messages[i+1:]...)
				break
			}
		}
		saveDatabase()
		json.NewEncoder(w).Encode(map[string]string{"status": "Mensaje eliminado"})
	}
}

func handleUsers(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, DELETE, OPTIONS")
	
	if r.Method == http.MethodOptions { return }

	mutex.Lock()
	defer mutex.Unlock()

	if r.Method == http.MethodGet { // LEER USUARIOS
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(db.Users)
		
	} else if r.Method == http.MethodDelete { // ELIMINAR USUARIO (Y SUS MENSAJES)
		name := r.URL.Query().Get("name")
		
		// Borrar usuario de la lista
		for i, u := range db.Users {
			if u == name {
				db.Users = append(db.Users[:i], db.Users[i+1:]...)
				break
			}
		}
		
		// Borrar en cascada todos los mensajes que le pertenecen
		var remainingMessages []Message
		for _, m := range db.Messages {
			if m.Sender != name {
				remainingMessages = append(remainingMessages, m)
			}
		}
		db.Messages = remainingMessages
		saveDatabase()
		json.NewEncoder(w).Encode(map[string]string{"status": "Usuario eliminado"})
	}
}

func main() {
	initDatabase()
	http.HandleFunc("/api/clienteservidor/messages", handleMessages)
	http.HandleFunc("/api/clienteservidor/users", handleUsers)
	
	log.Println("Servidor Go CRUD corriendo en puerto 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}