package main

import "testing"

func TestContains(t *testing.T) {
	// Simulamos un grupo de usuarios
	usuarios := []string{"Jorge", "Hazziel", "Admin"}

	// Prueba 1: Debería encontrar a Hazziel
	if !contains(usuarios, "Hazziel") {
		t.Errorf("Error: Se esperaba encontrar a 'Hazziel' en la lista, pero la función devolvió falso")
	}

	// Prueba 2: NO debería encontrar a un usuario que no existe
	if contains(usuarios, "Desconocido") {
		t.Errorf("Error: La función devolvió verdadero para 'Desconocido', pero no está en la lista")
	}
}