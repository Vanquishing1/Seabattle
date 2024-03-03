import random

class Ship:
    def __init__(self, size, position):
        self.size = size
        self.position = position  # Положение корабля на доске
        self.hits = 0  # Количество попаданий

    def is_sunk(self):
        return self.hits == self.size

class Board:
    def __init__(self):
        self.size = 6
        self.ships = []
        self.board = [['О' for _ in range(self.size)] for _ in range(self.size)]
        self.shots_fired = set()

    def place_ship(self, ship):
        for x, y in ship.position:
            if not (0 <= x < self.size and 0 <= y < self.size) or self.board[x][y] != 'О':
                raise ValueError("Unable to place ship at the specified position.")
        for x, y in ship.position:
            self.board[x][y] = '■'

    def print_board(self):
        print("   | 1 | 2 | 3 | 4 | 5 | 6|")
        for i, row in enumerate(self.board, start=1):
            print(f"{i} | {' | '.join(row)} |")

    def player_turn(self, x, y):
        if (x, y) in self.shots_fired:
            raise ValueError("You've already fired at this location.")
        self.shots_fired.add((x, y))

        if self.board[x][y] == '■':
            print("Hit!")
            for ship in self.ships:
                if (x, y) in ship.position:
                    ship.hits += 1
                    if ship.is_sunk():
                        print("You sunk a ship!")
            self.board[x][y] = 'X'
        else:
            print("Miss!")
            self.board[x][y] = 'T'

    def computer_turn(self):
        x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        while (x, y) in self.shots_fired:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

        self.shots_fired.add((x, y))

        if self.board[x][y] == '■':
            print(f"Computer hit at {x+1}, {y+1}!")
            for ship in self.ships:
                if (x, y) in ship.position:
                    ship.hits += 1
                    if ship.is_sunk():
                        print("Computer sunk a ship!")
            self.board[x][y] = 'X'
        else:
            print(f"Computer missed at {x+1}, {y+1}!")
            self.board[x][y] = 'T'

def main():
    player_board = Board()
    computer_board = Board()

    player_ships = [Ship(3, [(0, 0), (0, 1), (0, 2)]),
                    Ship(2, [(1, 4), (1, 5)]),
                    Ship(1, [(3, 0)]),
                    Ship(1, [(3, 2)]),
                    Ship(1, [(3, 4)]),
                    Ship(1, [(5, 0)])]

    computer_ships = [Ship(3, [(0, 3), (0, 4), (0, 5)]),
                      Ship(2, [(1, 0), (1, 1)]),
                      Ship(2, [(3, 2), (4, 2)]),
                      Ship(1, [(4, 4)]),
                      Ship(1, [(5, 4)])]

    for ship in player_ships:
        player_board.place_ship(ship)
        player_board.ships.append(ship)

    for ship in computer_ships:
        computer_board.place_ship(ship)
        computer_board.ships.append(ship)

    player_turns = 0
    computer_turns = 0

    while True:
        print("\nYour board:")
        player_board.print_board()
        print("\nComputer's board:")
        computer_board.print_board()

        try:
            x = int(input("Enter the row number (1-6): ")) - 1
            y = int(input("Enter the column number (1-6): ")) - 1
            player_board.player_turn(x, y)
            player_turns += 1
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")
            continue

        if all(ship.is_sunk() for ship in computer_board.ships):
            print("Congratulations! You won!")
            break

        computer_board.computer_turn()
        computer_turns += 1

        if all(ship.is_sunk() for ship in player_board.ships):
            print("Sorry, you lost. Better luck next time.")
            break

    print(f"\nYour total turns: {player_turns}")
    print(f"Computer's total turns: {computer_turns}")

if __name__ == "__main__":
    main()
