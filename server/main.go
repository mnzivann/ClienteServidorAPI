package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	_ "modernc.org/sqlite" // Driver de SQLite
)

var db *sql.DB

type Message struct {
	ID     string `json:"id"`
	Sender string `json:"sender"`
	Text   string `json:"text"`
}

func initDatabase() {
	var err error
	// Abre (o crea) el archivo de la base de datos SQL
	db, err = sql.Open("sqlite", "./clienteservidor.db")
	if err != nil {
		log.Fatal("Error abriendo la base de datos:", err)
	}

	// Crear tabla de usuarios
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS users (
		name TEXT PRIMARY KEY
	);`)
	if err != nil {
		log.Fatal(err)
	}

	// Crear tabla de mensajes con llave foránea
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS messages (
		id TEXT PRIMARY KEY,
		sender TEXT,
		text TEXT,
		FOREIGN KEY (sender) REFERENCES users(name) ON DELETE CASCADE
	);`)
	if err != nil {
		log.Fatal(err)
	}
}

func handleMessages(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == http.MethodOptions { return }

	switch r.Method {
	case http.MethodGet: // LEER (SELECT)
		rows, err := db.Query("SELECT id, sender, text FROM messages")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer rows.Close()

		var messages []Message
		for rows.Next() {
			var m Message
			rows.Scan(&m.ID, &m.Sender, &m.Text)
			messages = append(messages, m)
		}
		
		// Si la tabla está vacía, retornar un arreglo vacío en vez de null
		if messages == nil {
			messages = []Message{}
		}
		
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(messages)

	case http.MethodPost: // CREAR (INSERT)
		var msg Message
		json.NewDecoder(r.Body).Decode(&msg)
		msg.ID = fmt.Sprintf("%d", time.Now().UnixMilli())

		// 1. Insertar el usuario (IGNORE evita el error si ya existe)
		db.Exec("INSERT OR IGNORE INTO users (name) VALUES (?)", msg.Sender)
		
		// 2. Insertar el mensaje
		db.Exec("INSERT INTO messages (id, sender, text) VALUES (?, ?, ?)", msg.ID, msg.Sender, msg.Text)

		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(msg)

	case http.MethodPut: // ACTUALIZAR (UPDATE)
		var msg Message
		json.NewDecoder(r.Body).Decode(&msg)
		
		db.Exec("UPDATE messages SET text = ? WHERE id = ?", msg.Text, msg.ID)
		json.NewEncoder(w).Encode(map[string]string{"status": "Actualizado"})

	case http.MethodDelete: // ELIMINAR (DELETE)
		id := r.URL.Query().Get("id")
		db.Exec("DELETE FROM messages WHERE id = ?", id)
		json.NewEncoder(w).Encode(map[string]string{"status": "Eliminado"})
	}
}

func handleUsers(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, DELETE, OPTIONS")
	
	if r.Method == http.MethodOptions { return }

	if r.Method == http.MethodGet { // SELECT USUARIOS
		rows, _ := db.Query("SELECT name FROM users")
		defer rows.Close()

		var users []string
		for rows.Next() {
			var name string
			rows.Scan(&name)
			users = append(users, name)
		}
		
		if users == nil {
			users = []string{}
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(users)
		
	} else if r.Method == http.MethodDelete { // DELETE USUARIO Y SUS MENSAJES
		name := r.URL.Query().Get("name")
		
		db.Exec("DELETE FROM messages WHERE sender = ?", name)
		db.Exec("DELETE FROM users WHERE name = ?", name)
		
		json.NewEncoder(w).Encode(map[string]string{"status": "Usuario y mensajes eliminados"})
	}
}

func main() {
	initDatabase()
	http.HandleFunc("/api/clienteservidor/messages", handleMessages)
	http.HandleFunc("/api/clienteservidor/users", handleUsers)
	
	log.Println("Servidor Go corriendo con Base de Datos SQLite en puerto 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}