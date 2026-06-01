FROM golang:alpine
# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código fuente
COPY main.go .

# 1. Inicializar un módulo nuevo desde cero dentro del contenedor
RUN go mod init clienteservidor-api

# 2. Descargar la librería de SQLite
RUN go get modernc.org/sqlite

# 3. Limpiar y organizar las dependencias automáticamente
RUN go mod tidy

# 4. Compilar el binario
RUN go build -o main .

# Exponer el puerto
EXPOSE 8080

# Ejecutar el binario
CMD ["./main"]