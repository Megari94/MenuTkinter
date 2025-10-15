import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def abrir_juego1():
    messagebox.showinfo("Juego 1", "Abriste el Juego 1")

def abrir_juego2():
    messagebox.showinfo("Juego 2", "Abriste el Juego 2")

def abrir_juego3():
    messagebox.showinfo("Juego 3", "Abriste el Juego 3")

def abrir_juego4():
    messagebox.showinfo("Juego 4", "Abriste el Juego 4")
    
def abrir_juego5():
    messagebox.showinfo("Juego 5", "Abriste el Juego 4")

# Ventana principal
root = tk.Tk()
root.title("Jueguitos Menu")
root.geometry("900x600")
root.configure(bg="#444444")

# ================= CONTENEDOR PRINCIPAL =================
contenedor = tk.Frame(root, bg="#444444")
contenedor.pack(fill="both", expand=True)

# ----- Columna Izquierda (Logo + Últimos Jugados) -----
col_izq = tk.Frame(contenedor, bg="#444444")
col_izq.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# LOGO (arriba en la izquierda)
imagen = Image.open("infologo.png")
imagen = imagen.resize((600, 200))  # redimensionar la imagen
logo_img = ImageTk.PhotoImage(imagen)

logo = tk.Label(col_izq, image=logo_img, bg="#444444")
logo.image = logo_img
logo.pack(side="top", pady=10)

# Últimos Jugados (abajo en la izquierda)
frame_saves = tk.Frame(col_izq, bg="#222222", bd=7, relief="ridge", padx=10, pady=10)
frame_saves.pack(side="top", fill="both", expand=True, pady=10)

tk.Label(frame_saves, text="Últimos Jugados", font=("Arial", 16), fg="white", bg="#222222").pack(pady=5)

for i in range(3):
    slot = tk.Button(frame_saves, text=f"Slot {i+1}", width=10, height=5, bg="#666666")
    slot.pack(side="left", padx=10, pady=10)

# ----- Columna Derecha (Botones de Juegos) -----
frame_buttons = tk.Frame(contenedor, bg="#333333", bd=7, relief="ridge", padx=10, pady=10)
frame_buttons.pack(side="right", fill="y", padx=10, pady=10)

# Frame interior que contendrá los botones y estará centrado
inner_buttons = tk.Frame(frame_buttons, bg="#333333")
inner_buttons.place(relx=0.5, rely=0.5, anchor="center")

botones = [
    ("Juego1", abrir_juego1),
    ("Juego2", abrir_juego2),
    ("Juego3", abrir_juego3),
    ("Juego4", abrir_juego4),
    ("Juego5", abrir_juego5)
]

for txt, cmd in botones:
    b = tk.Button(frame_buttons, text=txt, font=("Arial", 14, "bold"),
                  width=20, height=3, bg="#885522", fg="white", command=cmd)
    b.pack(pady=10)

root.mainloop()
