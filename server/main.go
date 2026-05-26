package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"sync"
)

// Estructura de los datos
type Message struct {
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

// Cargar datos del archivo persistente al iniciar
func initDatabase() {
	file, err := os.ReadFile(dbFilename)
	if err == nil {
		json.Unmarshal(file, &db)
	}
}

// Guardar datos en el archivo persistente
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
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}

	mutex.Lock()
	defer mutex.Unlock()

	// GET: Retornar todos los mensajes
	if r.Method == http.MethodGet {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(db.Messages)
		return
	}

	// POST: Guardar mensaje y registrar usuario en la Base de Datos
	if r.Method == http.MethodPost {
		var msg Message
		if err := json.NewDecoder(r.Body).Decode(&msg); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		db.Messages = append(db.Messages, msg)

		// Si el usuario no existe en la base de datos, lo registramos
		if !contains(db.Users, msg.Sender) && msg.Sender != "" {
			db.Users = append(db.Users, msg.Sender)
		}

		saveDatabase()

		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(map[string]string{"status": "Datos guardados en DB"})
		return
	}
}

func handleUsers(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	if r.Method == http.MethodGet {
		w.Header().Set("Content-Type", "application/json")
		mutex.Lock()
		json.NewEncoder(w).Encode(db.Users)
		mutex.Unlock()
		return
	}
}

func main() {
	initDatabase()
	http.HandleFunc("/api/clienteservidor/messages", handleMessages)
	http.HandleFunc("/api/clienteservidor/users", handleUsers)
	
	log.Println("Servidor ClienteServidor con Base de Datos corriendo en puerto 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}