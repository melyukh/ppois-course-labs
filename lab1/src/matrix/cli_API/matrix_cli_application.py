from src.matrix.classes.matrix import Matrix


def read_matrix(prompt: str) -> Matrix:
    """Считать матрицу с консоли построчно, до пустой строки."""
    print(prompt)
    print("(вводите строки чисел через пробел, пустая строка — конец ввода)")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    text = "\n".join(lines)
    return Matrix.generate_from_string(text)


def read_matrix_from_file() -> Matrix:
    path = input("Введите путь к файлу: ")
    return Matrix.generate_from_file(path)


def print_matrix(label: str, matrix: Matrix) -> None:
    print(f"{label}:\n{matrix}")


def read_number(prompt: str) -> float:
    return float(input(prompt))


def read_int(prompt: str) -> int:
    return int(input(prompt))


# --- Структурные операции ---

def action_resize() -> None:
    m = read_matrix("Введите матрицу:")
    rows = read_int("Новое число строк: ")
    cols = read_int("Новое число столбцов: ")
    m.resize(rows, cols)
    print_matrix("Результат", m)


def action_load_from_file() -> None:
    m = read_matrix_from_file()
    print_matrix("Загруженная матрица", m)


def action_submatrix() -> None:
    m = read_matrix("Введите матрицу:")
    rows = read_int("Число строк подматрицы: ")
    cols = read_int("Число столбцов подматрицы: ")
    row_start = read_int("Начальная строка (с 0): ")
    col_start = read_int("Начальный столбец (с 0): ")
    sub = m.submatrix(rows, cols, row_start, col_start)
    print_matrix("Подматрица", sub)


def action_transpose() -> None:
    m = read_matrix("Введите матрицу:")
    print_matrix("Транспонированная матрица", m.transpose())


def action_check_type() -> None:
    m = read_matrix("Введите матрицу:")
    checks = {
        "Квадратная": m.is_square(),
        "Диагональная": m.is_diagonal(),
        "Нулевая": m.is_zero(),
        "Единичная": m.is_identity(),
        "Симметрическая": m.is_symmetry(),
        "Верхняя треугольная": m.is_high_triangular(),
        "Нижняя треугольная": m.is_low_triangular(),
    }
    for name, result in checks.items():
        print(f"{name}: {'да' if result else 'нет'}")


# --- Арифметика ---

def action_add() -> None:
    m1 = read_matrix("Введите первую матрицу:")
    m2 = read_matrix("Введите вторую матрицу:")
    print_matrix("Результат сложения", m1 + m2)


def action_add_number() -> None:
    m = read_matrix("Введите матрицу:")
    number = read_number("Введите число: ")
    print_matrix("Результат", m + number)


def action_sub() -> None:
    m1 = read_matrix("Введите первую матрицу:")
    m2 = read_matrix("Введите вторую матрицу:")
    print_matrix("Результат вычитания", m1 - m2)


def action_mul() -> None:
    m1 = read_matrix("Введите первую матрицу:")
    m2 = read_matrix("Введите вторую матрицу:")
    print_matrix("Результат умножения", m1 * m2)


def action_mul_number() -> None:
    m = read_matrix("Введите матрицу:")
    number = read_number("Введите число: ")
    print_matrix("Результат", m * number)


def action_div_number() -> None:
    m = read_matrix("Введите матрицу:")
    number = read_number("Введите число: ")
    print_matrix("Результат", m / number)


def action_pow() -> None:
    m = read_matrix("Введите квадратную матрицу:")
    power = read_int("Введите степень (целое, >= 0): ")
    print_matrix("Результат", m ** power)


def action_determinant() -> None:
    m = read_matrix("Введите квадратную матрицу:")
    print(f"Определитель: {m.determinant()}")


def action_norm() -> None:
    m = read_matrix("Введите матрицу:")
    print(f"Норма Фробениуса: {m.norm()}")


MENU = {
    "1": ("Изменить размер матрицы", action_resize),
    "2": ("Загрузить матрицу из файла", action_load_from_file),
    "3": ("Извлечь подматрицу", action_submatrix),
    "4": ("Транспонировать матрицу", action_transpose),
    "5": ("Проверить тип матрицы", action_check_type),
    "6": ("Сложить две матрицы", action_add),
    "7": ("Прибавить число к матрице", action_add_number),
    "8": ("Вычесть матрицу из матрицы", action_sub),
    "9": ("Перемножить две матрицы", action_mul),
    "10": ("Умножить матрицу на число", action_mul_number),
    "11": ("Разделить матрицу на число", action_div_number),
    "12": ("Возвести матрицу в степень", action_pow),
    "13": ("Вычислить определитель", action_determinant),
    "14": ("Вычислить норму", action_norm),
}


def print_menu() -> None:
    for key, (label, _) in MENU.items():
        print(f"{key}. {label}")
    print("0. Назад")


def run() -> None:
    while True:
        print("\n--- Матрицы ---")
        print_menu()
        choice = input("Выберите действие: ")
        if choice == "0":
            break

        action = MENU.get(choice)
        if action is None:
            print("Неверный выбор, попробуйте снова")
            continue

        try:
            action[1]()
        except (ValueError, TypeError, ZeroDivisionError, FileNotFoundError) as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    run()