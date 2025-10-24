import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess, os, sys, json

# ================= FUNCIONES AUXILIARES =================

def cargar_ultimos():
    """Carga la lista de últimos juegos desde un archivo JSON."""
    if os.path.exists("ultimos.json"):
        with open("ultimos.json", "r") as f:
            return json.load(f)
    return []

def guardar_ultimo(nombre_juego, archivo_juego):
    """Guarda el último juego jugado en un archivo JSON."""
    ultimos = cargar_ultimos()

    # Eliminar duplicados
    ultimos = [j for j in ultimos if j["nombre"] != nombre_juego]

    # Agregar nuevo al principio
    ultimos.insert(0, {"nombre": nombre_juego, "archivo": archivo_juego})

    # Mantener solo 3
    ultimos = ultimos[:3]

    with open("ultimos.json", "w") as f:
        json.dump(ultimos, f, indent=2)

    actualizar_ultimos()


def abrir_juego(ruta_juego, nombre_juego):
    """Abre un archivo de juego Python y lo registra como último jugado."""
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(ruta_actual, ruta_juego)

        guardar_ultimo(nombre_juego, ruta_completa)
        subprocess.Popen([sys.executable, ruta_completa])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el juego:\n{e}")


# ================= VENTANA PRINCIPAL =================

root = tk.Tk()
root.title("🎮 Menú de Jueguitos")
root.geometry("900x600")
root.configure(bg="#444444")
root.resizable(False, False)

contenedor = tk.Frame(root, bg="#444444")
contenedor.pack(fill="both", expand=True)

# ----- Columna Izquierda (Logo + Últimos Jugados) -----
col_izq = tk.Frame(contenedor, bg="#444444")
col_izq.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# LOGO
try:
    imagen = Image.open("infologo.png")
    imagen = imagen.resize((600, 200))
    logo_img = ImageTk.PhotoImage(imagen)
    logo = tk.Label(col_izq, image=logo_img, bg="#444444")
    logo.image = logo_img
    logo.pack(side="top", pady=10)
except FileNotFoundError:
    tk.Label(col_izq, text="LOGO", bg="#444444", fg="white", font=("Arial", 24)).pack(pady=20)

# FRAME: Últimos Jugados
frame_saves = tk.Frame(col_izq, bg="#222222", bd=7, relief="ridge", padx=10, pady=10)
frame_saves.pack(side="top", fill="both", expand=True, pady=10)

# ================= ACTUALIZAR ÚLTIMOS JUGADOS =================
def actualizar_ultimos():
    """Actualiza la lista visual de últimos juegos jugados."""
    for widget in frame_saves.winfo_children():
        widget.destroy()

    tk.Label(frame_saves, text="Últimos Jugados", font=("Arial", 16),
             fg="white", bg="#222222").pack(pady=5)

    ultimos = cargar_ultimos()

    if not ultimos:
        tk.Label(frame_saves, text="(Aún no jugaste nada)", fg="gray", bg="#222222").pack(pady=10)
    else:
        for juego in ultimos:
            def abrir(j=juego):
                subprocess.Popen([sys.executable, j["archivo"]])

            slot = tk.Button(frame_saves,
                             text=juego["nombre"],
                             width=25, height=2,
                             bg="#666666", fg="white",
                             command=abrir)
            slot.pack(fill="x", pady=5)

# Cargar lista inicial
actualizar_ultimos()

# ----- Columna Derecha (Botones de Juegos) -----
frame_buttons = tk.Frame(contenedor, bg="#333333", bd=7, relief="ridge", padx=10, pady=10)
frame_buttons.pack(side="right", fill="y", padx=10, pady=10)

tk.Label(frame_buttons, text="Selecciona un juego", font=("Arial", 16, "bold"),
         bg="#333333", fg="white").pack(pady=10)

botones = [
    ("Viborita 🐍", lambda: abrir_juego("snake.py", "Viborita 🐍")),
    ("Juego 2", lambda: abrir_juego("juego2.py", "Juego 2")),
    ("Juego 3", lambda: abrir_juego("juego3.py", "Juego 3")),
    ("Juego 4", lambda: abrir_juego("juego4.py", "Juego 4")),
    ("Juego 5", lambda: abrir_juego("juego5.py", "Juego 5")),
]

for txt, cmd in botones:
    b = tk.Button(frame_buttons, text=txt, font=("Arial", 14, "bold"),
                  width=20, height=3, bg="#885522", fg="white", command=cmd)
    b.pack(pady=10)

root.mainloop()
