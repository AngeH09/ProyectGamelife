import tkinter as tk
from tkinter import filedialog
import copy

def cargar_tablero_desde_csv(ruta_csv):
    tablero = []
    with open(ruta_csv, 'r', encoding='utf-8') as archivo_csv:
        lector = archivo_csv.read()
        lector = lector.strip().split("\n")
        for fila in lector:
            fila = fila.split(",")
            tablero.append([int(celda) for celda in fila])
    return tablero

def cargar_tablero_inicial(tablero, ventana):
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
            boton.grid(row=i+1, column=j+1, padx=1, pady=1)
            fila.append(boton)
        celdas.append(fila)
    return celdas

def contar_vecinos(tablero, x, y):
    vecinos = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            ni = x + i
            nj = y + j
            if ni < len(tablero) and nj < len(tablero[0]):
                vecinos += tablero[ni][nj]
            elif ni < len(tablero) and nj == len(tablero[0]):
                vecinos += tablero[ni][0]
            elif ni == len(tablero) and nj < len(tablero[0]):
                vecinos += tablero[0][nj]
            elif ni == len(tablero) and nj == len(tablero[0]):
                vecinos += tablero[0][0]
                
    return vecinos

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

class App:
    def __init__(self,  width = 500, height = 500, name = "Window"):
        self.simulaciones = int(input("Ingrese cuántas simulaciones quiere realizar: "))
        self.n = 0
        self.path_name = ""
        self.tablero = []
        self.tablero_inicial = []
        self.window = tk.Tk()
        self.window.title(name)
        self.window.geometry(f"{width}x{height}")
        
        self.SetContent()
        
        self.window.mainloop()
        
    def SetContent(self):
        self.fileButton = tk.Button(master = self.window, text = "Open file", 
                                    height = 4, width = 10, command = self.getFile)
        self.fileButton.grid(row=0, column = 0)
        
    def getFile(self):
        archivo = filedialog.askopenfile()
        if archivo:
            self.path_name = archivo.name
        self.tablero = cargar_tablero_desde_csv(self.path_name)
        self.tablero_inicial = cargar_tablero_inicial(self.tablero, self.window)
        self.actualizar_tablero()
        
    def actualizar_tablero(self):
        if self.n <= self.simulaciones:
            self.n += 1
            for i in range(len(self.tablero)):
                for j in range(len(self.tablero[0])):
                    if self.tablero[i][j] == 1:
                        color = "black"
                    else: 
                        color = "white"
                    self.tablero_inicial[i][j].config(bg=color)
            self.tablero = siguiente_generacion(self.tablero)
            self.window.after(1000, self.actualizar_tablero)
        
app = App(width = 750, height = 500, name = "Juego_de_la_Vida")