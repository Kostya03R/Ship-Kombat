import random

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, length, orient):
        self.bow = bow
        self.length = length
        self.orient = orient
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            x = self.bow.x + i if self.orient == 0 else self.bow.x
            y = self.bow.y + i if self.orient == 1 else self.bow.y
            ship_dots.append(Dot(x, y))
        return ship_dots

class Board:
    def __init__(self, size=6):
        self.size = size
        self.field = [["O"] * size for _ in range(size)]
        self.ships = []
        self.busy = []

    def add_ship(self, ship):
        for dot in ship.dots:
            if not self.in_bounds(dot) or dot in self.busy:
                raise Exception("Невозможно разместить корабль")
        for dot in ship.dots:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    check_dot = Dot(dot.x + dx, dot.y + dy)
                    if self.in_bounds(check_dot) and check_dot in self.busy:
                        raise Exception("Расстояние между кораблями должно быть минимум 1 клетка")
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)
        self.ships.append(ship)

    def in_bounds(self, dot):
        return 0 <= dot.x < self.size and 0 <= dot.y < self.size

    def shot(self, dot):
        if not self.in_bounds(dot):
            raise Exception("Выстрел за границы поля")
        if self.field[dot.x][dot.y] in ["X", "T"]:
            raise Exception("Эта позиция уже была обстреляна")
        if self.field[dot.x][dot.y] == "■":
            self.field[dot.x][dot.y] = "X"
            for ship in self.ships:
                if dot in ship.dots:
                    ship.lives -= 1
                    if ship.lives == 0:
                        return "Убит"
                    else:
                        return "Ранен"
        else:
            self.field[dot.x][dot.y] = "T"
            return "Мимо"

    def all_ships_sunk(self):
        return all(ship.lives == 0 for ship in self.ships)

    def print_board(self, show_ships=False):
        print("  " + " ".join(str(i+1) for i in range(self.size)))
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = self.field[i][j]
                if cell == "■" and not show_ships:
                    row.append("O")
                else:
                    row.append(cell)
            print(f"{i+1} " + " ".join(row))

class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def move(self):
        pass

class User(Player):
    def manual_setup(self):
        ships_to_place = [3, 2, 2, 1, 1, 1, 1]
        print("Настройка ваших кораблей.")
        self.own_board.print_board(show_ships=True)
        for ship_length in ships_to_place:
            placed = False
            while not placed:
                try:
                    print(f"\nРазмещайте корабль длиной {ship_length}.")
                    coords = input("Введите координаты начала корабля (например, 1 1): ").split()
                    if len(coords) != 2:
                        raise ValueError("Введите два числа.")
                    x, y = int(coords[0]) - 1, int(coords[1]) - 1
                    orient_input = input("Введите ориентацию (1 для горизонтально, 0 для вертикально): ").upper()
                    if orient_input not in ["0", "1"]:
                        raise ValueError("Ориентация должна быть 0 или 1.")
                    orient = 0 if orient_input == "0" else 1
                    ship = Ship(Dot(x, y), ship_length, orient)
                    self.own_board.add_ship(ship)
                    self.own_board.print_board(show_ships=True)
                    placed = True
                except Exception as e:
                    print(f"Ошибка: {e}. Попробуйте снова.")

    def move(self):
        while True:
            try:
                coords = input("Введите координаты выстрела (например, 1 3): ").split()
                if len(coords) != 2:
                    raise ValueError
                x, y = int(coords[0]) - 1, int(coords[1]) - 1
                dot = Dot(x, y)
                result = self.enemy_board.shot(dot)
                print(result)
                return result == "Мимо"
            except Exception as e:
                print(f"Ошибка: {e}. Попробуйте снова.")

class AI(Player):
    def move(self):
        while True:
            try:
                x = random.randint(0, self.enemy_board.size - 1)
                y = random.randint(0, self.enemy_board.size - 1)
                dot = Dot(x, y)
                result = self.enemy_board.shot(dot)
                print(f"Компьютер стреляет в ({x+1}, {y+1}): {result}")
                return result == "Мимо"
            except:
                continue

class Game:
    def __init__(self, size=6):
        self.size = size
        self.user_board = None
        self.ai_board = None
        self.user = None
        self.ai = None

    def random_board(self):
        while True:
            board = Board(self.size)
            try:
                for ship_length in [3, 2, 2, 1, 1, 1, 1]:
                    attempts = 0
                    while attempts < 2000:
                        attempts += 1
                        orient = random.randint(0, 1)
                        x = random.randint(0, self.size - 1)
                        y = random.randint(0, self.size - 1)
                        ship = Ship(Dot(x, y), ship_length, orient)
                        try:
                            board.add_ship(ship)
                            break
                        except:
                            continue
                    else:
                        raise Exception("Не удалось разместить все корабли")
                return board
            except:
                continue

    def greet(self):
        print("Добро пожаловать в морской бой!")
        print("Перед началом разместите свои корабли.")
        print("Введите координаты и ориентацию для каждого корабля.")
        print("Ориентация: 1 - горизонтально, 0 - вертикально.")
        print("")

    def loop(self):
        while True:
            print("\nВаша доска:")
            self.user_board.print_board(show_ships=True)
            print("\nДоска противника:")
            self.ai_board.print_board(show_ships=False)

            print("\nВаш ход:")
            self.user.move()
            if self.ai_board.all_ships_sunk():
                print("Поздравляем! Вы победили!")
                break

            print("\nХод компьютера:")
            self.ai.move()
            if self.user_board.all_ships_sunk():
                print("YOU LOSE! :(")
                break

    def start(self):
        self.greet()
        print("Генерируем доски для компьютера...")
        self.ai_board = self.random_board()
        print("Размещайте ваши корабли.")
        self.user_board = Board(self.size)
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)
        self.user.manual_setup()
        print("\nВаше поле с кораблями:")
        self.user_board.print_board(show_ships=True)
        print("\nПоле противника:")
        self.ai_board.print_board(show_ships=False)
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.start()