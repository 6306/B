import tkinter as tk
from tkinter import messagebox
import random

# Constants
WIDTH, HEIGHT = 10, 10
NUM_MINES = 15
GRID_SIZE = 30

# Create the game grid
grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
mines = set()

# Create a Tkinter window
window = tk.Tk()
window.title("Mine Sweep")

# Initialize the 'buttons' list
buttons = []

# Inside the create_grid_buttons() function, create and configure buttons:
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        button = tk.Button(window, width=2, height=1, command=lambda x=x, y=y: on_click(x, y), font=('Arial', 12), relief=tk.SUNKEN, bg="white")
        button.grid(row=y, column=x)
        row.append(button)
    buttons.append(row)

# Functions
def generate_mines():
    for _ in range(NUM_MINES):
        while True:
            x, y = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
            if (x, y) not in mines:
                mines.add((x, y))
                break

def count_adjacent_mines(x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT and (x + dx, y + dy) in mines:
                count += 1
    return count

def on_click(x, y):
    if (x, y) in mines:
        buttons[y][x].config(text="X", state="disabled", bg="red")
        end_game("Game Over")
    else:
        mines_count = count_adjacent_mines(x, y)
        if mines_count == 0:
            reveal_empty(x, y)
        else:
            bg_color = "red" if mines_count > 3 else "orange" if mines_count == 3 else "yellow" if mines_count == 2 else "cyan" if mines_count == 1 else "gray"
            buttons[y][x].config(text=str(mines_count), state="disabled", bg=bg_color)
        check_win()

def reveal_empty(x, y):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT and grid[y][x] == ' ':
        mines_count = count_adjacent_mines(x, y)
        bg_color = "red" if mines_count > 3 else "orange" if mines_count == 3 else "yellow" if mines_count == 2 else "cyan" if mines_count == 1 else "gray"
        buttons[y][x].config(text=str(mines_count), state="disabled", bg=bg_color)
        grid[y][x] = str(mines_count)
        if mines_count == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    reveal_empty(x + dx, y + dy)


def end_game(message):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) in mines:
                buttons[y][x].config(text="X", state="disabled", bg="red")
    messagebox.showinfo("Game Over", message)
    window.quit()

def check_win():
    uncovered = sum(row.count(' ') for row in grid)
    if uncovered == NUM_MINES:
        end_game("You Win!")

# Generate mines and create the game grid
generate_mines()

# Start the game
window.mainloop()
