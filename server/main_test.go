package main

import (
	"encoding/json"
	"testing"
)

// Prueba para verificar que la estructura de Go interpreta bien el JSON de la API
func TestMessageJSONMapping(t *testing.T) {
	// Simulamos los datos que enviaría tu interfaz de Python
	jsonData := []byte(`{"id":"12345", "sender":"Ivan", "text":"Hola desde el test"}`)

	var msg Message
	err := json.Unmarshal(jsonData, &msg)

	// Verificamos que no haya errores al traducir
	if err != nil {
		t.Fatalf("Error crítico: No se pudo parsear el JSON: %v", err)
	}

	// Verificamos que los datos se hayan asignado correctamente
	if msg.Sender != "Ivan" {
		t.Errorf("Se esperaba 'Ivan', pero se obtuvo '%s'", msg.Sender)
	}
	
	if msg.Text != "Hola desde el test" {
		t.Errorf("Se esperaba 'Hola desde el test', pero se obtuvo '%s'", msg.Text)
	}
}