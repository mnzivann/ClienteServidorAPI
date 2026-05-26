# Usar la imagen oficial de Go
FROM golang:1.21-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código fuente
COPY main.go .

# Inicializar el módulo y compilar el binario
RUN go mod init techdash-api
RUN go build -o main .

# Exponer el puerto
EXPOSE 8080

# Ejecutar el binario
CMD ["./main"]