from logic import Minesweeper

def choose_difficulty():
    print("Choose difficulty:")
    print("1. Easy (5x5, 5 mines)")
    print("2. Medium (8x8, 10 mines)")
    print("3. Hard (10x10, 20 mines)")

    choice = input("> ")

    if choice == "1":
        return 5, 5, 5
    elif choice == "2":
        return 8, 8, 10
    else:
        return 10, 10, 20


def main():
    rows, cols, mines = choose_difficulty()
    game = Minesweeper(rows, cols, mines)

    while True:
        game.print_board()
        action = input("\nEnter move (row column), or u=undo, r=redo, q=quit: ").lower()

        if action == "q":
            break
        elif action == "u":
            game.undo()
            continue
        elif action == "r":
            game.redo()
            continue

        try:
            r, c = map(int, action.split())
        except:
            print("Invalid input.")
            continue

        if not (0 <= r < rows and 0 <= c < cols):
            print("Out of bounds.")
            continue

        game.save_state()
        result = game.reveal(r, c)

        if result == "lose":
            game.print_board()
            print("You hit a mine. Game over.")
            break

        if game.check_win():
            game.print_board()
            print("You win!")
            break


if __name__ == "__main__":
    main()