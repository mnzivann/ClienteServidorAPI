package main

import (
	"encoding/json"
	"log"
	"net/http"
)

// Estructura de los datos
type Task struct {
	ID     string `json:"id"`
	Title  string `json:"title"`
	Status string `json:"status"`
}

// Datos simulados
var tasks = []Task{
	{ID: "1", Title: "Revisar cableado del nodo ESP32", Status: "Pendiente"},
	{ID: "2", Title: "Actualizar roles en Ubuntu Server", Status: "Completado"},
	{ID: "3", Title: "Calibrar sensor ultrasónico", Status: "Pendiente"},
}

// Controlador del endpoint
func getTasks(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	// Permitir conexiones desde cualquier cliente (CORS básico)
	w.Header().Set("Access-Control-Allow-Origin", "*") 
	json.NewEncoder(w).Encode(tasks)
}

func main() {
	http.HandleFunc("/api/techdash/tasks", getTasks)
	
	log.Println("Servidor Go corriendo en el puerto 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}