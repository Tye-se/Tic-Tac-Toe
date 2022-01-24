from tic_tac_toe import Game

# Binding to RMB because LMB will cause issues.
BIND = "<Button-3>"


def main():
    game = Game(BIND)

    # For getting mouse coordinates.
    game.ui.bind("<Motion>", game.ui.motion)

    game.ui.bind(BIND, game.place)

    game.ui.bind("<MouseWheel>", game.ui.reset_ui)

    game.ui.mainloop()


if __name__ == "__main__":
    main()
