import tkinter as tk
import random

# ---------- CONFIGURACIÓN ----------
CELL_SIZE = 20        # tamaño de cada celda (px)
INITIAL_LENGTH = 4
INITIAL_SPEED = 120   # tiempo (ms) entre frames; menor = más rápido
SPEED_INCREMENT = 5   # cuanto se acelera tras comer
# -----------------------------------

class SnakeGame:
    def __init__(self, root):
        self.root = root
        root.title("Viborita - Tkinter")
        self.width = 900
        self.height = 600
        # ajustar tamaño del canvas a pantalla pero cuadrar a múltiplos de CELL_SIZE
        self.columns = self.width // CELL_SIZE
        self.rows = self.height // CELL_SIZE

        # ventana centrada
        x_pos = (root.winfo_screenwidth() // 2) - (self.width // 2)
        y_pos = (root.winfo_screenheight() // 2) - (self.height // 2)
        root.geometry(f"{self.width}x{self.height}+{x_pos}+{y_pos}")

        # canvas
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # info (arriba)
        self.info_label = tk.Label(root, text="", font=("Consolas", 14))
        self.info_label.pack(fill="x")

        # estado del juego
        self.reset_game()

        # eventos de teclado
        root.bind("<Key>", self.on_key)

        # iniciar bucle de juego
        self.running = True
        self.after_id = None
        self.loop()

    def reset_game(self):
        self.direction = (1, 0)  # derecha
        self.snake = []
        start_x = self.columns // 4
        start_y = self.rows // 2
        for i in range(INITIAL_LENGTH):
            # la cabeza al final de la lista
            self.snake.append((start_x - i, start_y))
        self.place_food()
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_over = False
        self.paused = False
        self.update_info()

    def place_food(self):
        while True:
            fx = random.randint(1, self.columns - 2)
            fy = random.randint(1, self.rows - 2)
            if (fx, fy) not in self.snake:
                self.food = (fx, fy)
                break

    def on_key(self, event):
        key = event.keysym.lower()
        dx, dy = self.direction
        # flechas o wasd
        if key in ("up", "w"):
            if dy != 1: self.direction = (0, -1)
        elif key in ("down", "s"):
            if dy != -1: self.direction = (0, 1)
        elif key in ("left", "a"):
            if dx != 1: self.direction = (-1, 0)
        elif key in ("right", "d"):
            if dx != -1: self.direction = (1, 0)
        elif key == "p":
            self.toggle_pause()
        elif key == "escape":
            self.root.quit()
        elif key == "r" and self.game_over:
            # reiniciar
            self.reset_game()
            if not self.after_id:
                self.loop()

    def toggle_pause(self):
        if self.game_over:
            return
        self.paused = not self.paused
        self.update_info()
        if not self.paused and not self.after_id:
            self.loop()

    def loop(self):
        # main loop del juego, se llama con after
        if self.paused or self.game_over:
            self.after_id = None
            return

        # calcular nueva cabeza
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # colisiones con paredes -> game over
        x, y = new_head
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
            self.end_game()
            return

        # colisión con si misma -> game over
        if new_head in self.snake:
            self.end_game()
            return

        # insertar cabeza
        self.snake.insert(0, new_head)

        # si comió comida, aumentar score y no borrar cola
        if new_head == self.food:
            self.score += 10
            # acelerar un poco
            self.speed = max(30, self.speed - SPEED_INCREMENT)
            self.place_food()
        else:
            # quitar cola
            self.snake.pop()

        # dibujar
        self.draw()

        # programar siguiente frame
        self.after_id = self.root.after(self.speed, self.loop)

    def draw(self):
        self.canvas.delete("all")
        # dibujar comida
        fx, fy = self.food
        self.draw_cell(fx, fy, fill="red")
        # dibujar serpiente (cabeza distinta)
        for i, (sx, sy) in enumerate(self.snake):
            if i == 0:
                self.draw_cell(sx, sy, fill="#00FF00")  # cabeza
            else:
                self.draw_cell(sx, sy, fill="#008800")  # cuerpo
        self.update_info()

    def draw_cell(self, col, row, fill="#ffffff"):
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        # pequeño margen para "espacio" entre celdas
        pad = 1
        self.canvas.create_rectangle(x1+pad, y1+pad, x2-pad, y2-pad, fill=fill, width=0)

    def update_info(self):
        if self.game_over:
            text = f"GAME OVER — Puntaje: {self.score}  |  Presiona 'r' para reiniciar"
        elif self.paused:
            text = f"PAUSA — Puntaje: {self.score}  |  Presiona 'p' para continuar"
        else:
            text = f"Puntaje: {self.score}  |  Velocidad: {round(1000/self.speed,2)} FPS aprox.  |  'p' pausa, 'r' reiniciar (si game over)"
        self.info_label.config(text=text)

    def end_game(self):
        self.game_over = True
        self.update_info()
        # detener bucle
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)    
    game = SnakeGame(root)
    root.mainloop()
