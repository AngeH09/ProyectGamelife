import csv
import tkinter as tk
import copy

# Cargar tablero desde CSV
def cargar_tablero_desde_csv(ruta_csv):
    tablero = []
    with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
        lector = csv.reader(archivo_csv)
        for fila in lector:
            tablero.append([int(celda) for celda in fila])
    return tablero

def cargar_tablero_inicial(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    celdas = []

    for i in range(filas):
        fila = []
        for j in range(columnas):
            if tablero[i][j] == 1:
                color = "black"
            else:
                color = "white"
            boton = tk.Label(ventana, width=4, height=2, bg=color, relief="solid", bd=1)
            boton.grid(row=i, column=j, padx=1, pady=1)
            fila.append(boton)
        celdas.append(fila)
    return celdas

# Contar vecinos vivos
def contar_vecinos(tablero, x, y):
    vecinos = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            ni = x + i
            nj = y + j
            if 0 <= ni < len(tablero) and 0 <= nj < len(tablero[0]):
                vecinos += tablero[ni][nj]
    return vecinos

# Calcular siguiente generación
def siguiente_generacion(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    nueva = copy.deepcopy(tablero)

    for i in range(filas):
        for j in range(columnas):
            vivos = contar_vecinos(tablero, i, j)
            if tablero[i][j] == 1:
                if 2 <= vivos <= 3:
                    nueva[i][j] = 1 
                else:
                    nueva[i][j] = 0
            else:
                if vivos == 3:
                    nueva[i][j] = 1
                else:
                    nueva[i][j] = 0
    return nueva

# Dibujar el tablero en pantalla
def actualizar_tablero():
    global tablero
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] == 1:
                color = "black"
            else: 
                color = "white"
            tablero_inicial[i][j].config(bg=color)
    tablero = siguiente_generacion(tablero)
    ventana.after(1000, actualizar_tablero)


# Inicio del programa
tablero = cargar_tablero_desde_csv("tablero_binario_9x9.csv")
ventana = tk.Tk()
ventana.title("Juego de la Vida - Animado")
tablero_inicial = cargar_tablero_inicial(tablero)
# Iniciar animación
actualizar_tablero()
ventana.mainloop()

