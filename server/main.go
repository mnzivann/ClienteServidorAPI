package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"
)

type Message struct {
	Text string `json:"text"`
}

// Aquí guardaremos los mensajes en memoria
var messages []Message
var mutex sync.Mutex // Para evitar errores si llegan muchos mensajes a la vez

func handleMessages(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == http.MethodOptions {
		return
	}

	mutex.Lock()
	defer mutex.Unlock()

	// Si es GET, devolvemos la lista de mensajes (Para la App Servidor de Python)
	if r.Method == http.MethodGet {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(messages)
		return
	}

	// Si es POST, guardamos el nuevo mensaje (Desde la App Cliente de Python)
	if r.Method == http.MethodPost {
		var msg Message
		err := json.NewDecoder(r.Body).Decode(&msg)
		if err != nil {
			http.Error(w, "Error al leer el mensaje", http.StatusBadRequest)
			return
		}
		messages = append(messages, msg)
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(map[string]string{"status": "Mensaje guardado"})
		return
	}

	http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
}

func main() {
	// Nuevo nombre de ruta
	http.HandleFunc("/api/clienteservidor/messages", handleMessages)
	
	log.Println("API ClienteServidor en Go escuchando en el puerto 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}