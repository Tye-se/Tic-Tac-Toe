import random
from tkinter import *


def random_hex_color():
    return f"#{random.randint(0, 256**3):06x}"


FONT = ("Ariel", 50, "normal")


class GameUI(Tk):
    def __init__(self):
        super().__init__()
        self.grid_color = random_hex_color()
        self.x_color = random_hex_color()
        self.o_color = random_hex_color()

        # Defining grid here so the reset button will work.
        self.grid = ["a" for _ in range(9)]

        # Window
        self.title("Tic-Tac-Toe     RMB: place")

        # Width x Height + x + y
        self.geometry("600x670+620+100")
        self.config(bg="grey")
        self.iconbitmap("favicon.ico")

        self.resizable(False, False)
        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()

        # Canvas
        self.canvas = Canvas(width=600, height=600, bg="black", highlightthickness=0)
        self.canvas.grid(column=0, row=0, columnspan=3)

        self.draw_grid()

        # Buttons
        reset_button = Button(text="RESET", width=26, height=4, command=self.reset_ui, bg="DarkGrey")
        reset_button.grid(column=0, row=1)

        exit_button = Button(text="QUIT", width=26, height=4, command=self.exit_game, bg="DarkGrey")
        exit_button.grid(column=2, row=1)

        # Labels
        self.mouse_position = Label(text=f"(X=0, Y=0)", width=30, height=4, bg="DarkGrey")
        self.mouse_position.grid(column=1, row=1)

    def motion(self, event):
        self.mouse_position.config(text=f"(X={event.x}, Y={event.y})")

    def draw_grid(self):
        # (x0, y0) --> (x1, y2) 3x3 Grid
        self.canvas.create_line(200, 0, 200, 600, fill=self.grid_color, width=10)
        self.canvas.create_line(400, 0, 400, 600, fill=self.grid_color, width=10)
        self.canvas.create_line(0, 200, 600, 200, fill=self.grid_color, width=10)
        self.canvas.create_line(0, 400, 600, 400, fill=self.grid_color, width=10)

    def draw_x(self, x, y):
        self.canvas.create_line(x-100, y-100, x+100, y+100, fill=self.x_color, width=10)
        self.canvas.create_line(x+100, y-100, x-100, y+100, fill=self.x_color, width=10)

    def draw_o(self, x, y):
        self.canvas.create_arc(x-90, y-90, x+90, y+90,
                               fill=self.o_color,
                               outline=self.o_color,
                               start=0,
                               extent=359.9,
                               width=10,
                               style="arc")

    def draw_win_line(self, x_1, y_1, x_2, y_2):
        self.canvas.create_line(x_1, y_1, x_2, y_2, width=50, fill=random_hex_color())

    def draw_win_text(self, turn):
        self.canvas.create_text(300, 300, text=f"{turn.upper()} WINS!!!", fill="white", font=FONT)

    def draw_tie_text(self):
        self.canvas.create_text(300, 300, text=f"DRAW", fill="white", font=FONT)

    def reset_ui(self, *args):
        if args:
            print(args)
        self.grid_color = random_hex_color()
        self.x_color = random_hex_color()
        self.o_color = random_hex_color()
        self.canvas.create_rectangle(0, 0, 600, 600, fill="Black")
        self.draw_grid()
        self.grid = ["a" for _ in range(9)]

    def exit_game(self):
        self.destroy()


RESET_TIME = 1000  # MS


class Game:
    def __init__(self, bind):
        self.bind = bind
        self.ui = GameUI()
        self.turn = random.choice(["x", "o"])

    def reset(self):
        self.ui.bind(self.bind, self.place)
        self.ui.reset_ui()

    def switch_turn(self):
        if self.turn == "x":
            self.turn = "o"
        else:
            self.turn = "x"

    def place(self, event):
        x, y = event.x, event.y
        turn = self.turn
        if turn == "x":
            draw = self.ui.draw_x
        else:
            draw = self.ui.draw_o

        # Top row
        if x < 200 and y < 200 and self.ui.grid[0] == "a":
            draw(100, 100)
            self.ui.grid[0] = turn
            self.switch_turn()
        elif 200 < x < 400 and y < 200 and self.ui.grid[1] == "a":
            draw(300, 100)
            self.ui.grid[1] = turn
            self.switch_turn()
        elif 400 < x and y < 200 and self.ui.grid[2] == "a":
            draw(500, 100)
            self.ui.grid[2] = turn
            self.switch_turn()

        # Middle row
        elif x < 200 and 200 < y < 400 and self.ui.grid[3] == "a":
            draw(100, 300)
            self.ui.grid[3] = turn
            self.switch_turn()
        elif 200 < x < 400 and 200 < y < 400 and self.ui.grid[4] == "a":
            draw(300, 300)
            self.ui.grid[4] = turn
            self.switch_turn()
        elif 400 < x and 200 < y < 400 and self.ui.grid[5] == "a":
            draw(500, 300)
            self.ui.grid[5] = turn
            self.switch_turn()

        # Bottom row
        elif x < 200 and y > 400 and self.ui.grid[6] == "a":
            draw(100, 500)
            self.ui.grid[6] = turn
            self.switch_turn()
        elif 200 < x < 400 and y > 400 and self.ui.grid[7] == "a":
            draw(300, 500)
            self.ui.grid[7] = turn
            self.switch_turn()
        elif 400 < x and y > 400 and self.ui.grid[8] == "a":
            draw(500, 500)
            self.ui.grid[8] = turn
            self.switch_turn()

        self.check_win_condition(turn)

    def win(self, turn, x1, y1, x2, y2):
        self.ui.draw_win_line(x1, y1, x2, y2)
        self.ui.draw_win_text(turn)
        self.ui.after(RESET_TIME, self.reset)

    def check_win_condition(self, turn):
        # Unbinding to fix the multiple wins bug.
        self.ui.unbind(self.bind)

        # Row win
        if self.ui.grid[0] == turn and self.ui.grid[1] == turn and self.ui.grid[2] == turn:
            self.win(turn, 0, 100, 600, 100)
        elif self.ui.grid[3] == turn and self.ui.grid[4] == turn and self.ui.grid[5] == turn:
            self.win(turn, 0, 300, 600, 300)
        elif self.ui.grid[6] == turn and self.ui.grid[7] == turn and self.ui.grid[8] == turn:
            self.win(turn, 0, 500, 600, 500)

        # Column win
        elif self.ui.grid[0] == turn and self.ui.grid[3] == turn and self.ui.grid[6] == turn:
            self.win(turn, 100, 0, 100, 600)
        elif self.ui.grid[1] == turn and self.ui.grid[4] == turn and self.ui.grid[7] == turn:
            self.win(turn, 300, 0, 300, 600)
        elif self.ui.grid[2] == turn and self.ui.grid[5] == turn and self.ui.grid[8] == turn:
            self.win(turn, 500, 0, 500, 600)

        # Diagonal win
        elif self.ui.grid[0] == turn and self.ui.grid[4] == turn and self.ui.grid[8] == turn:
            self.win(turn, 0, 0, 600, 600)
        elif self.ui.grid[2] == turn and self.ui.grid[4] == turn and self.ui.grid[6] == turn:
            self.win(turn, 0, 600, 600, 0)

        # Draw
        elif "a" not in self.ui.grid:
            self.ui.draw_tie_text()
            self.ui.after(RESET_TIME, self.reset)

        # No win we rebind RMB -> self.place().
        else:
            self.ui.bind(self.bind, self.place)
