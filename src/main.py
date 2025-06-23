import engine
import game


def main():
    # Loop between menu and game
    while True:
        # Waits until user starts game
        engine.menu()

        # Set up new game
        game.reset()
        running = True

        while running:
            running = game.update()


if __name__ == "__main__":
    main()
