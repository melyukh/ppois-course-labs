from src.matrix.classes.matrix import Matrix

_session_matrices: dict[str, Matrix] = {}

def _read_matrix_from_input() -> Matrix:
    print("(вводите строки чисел через пробел, пустая строка — конец ввода)")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    text = "\n".join(lines)
    return Matrix.generate_from_string(text)


def _read_matrix_from_file() -> Matrix:
    path = input("Введите путь к файлу: ")
    return Matrix.generate_from_file(path)


def _obtain_matrix(prompt: str) -> Matrix:
    """
    Универсальный способ получить матрицу для операции:
    - ввести с клавиатуры,
    - загрузить из файла,
    - взять уже сохранённую в этой сессии.
    """
    print(f"\n{prompt}")
    print("1. Ввести вручную")
    print("2. Загрузить из файла")
    if _session_matrices:
        print("3. Взять сохранённую матрицу")
    choice = input("Выберите способ: ")

    if choice == "1":
        return _read_matrix_from_input()
    elif choice == "2":
        return _read_matrix_from_file()
    elif choice == "3" and _session_matrices:
        return _select_saved_matrix()
    else:
        raise ValueError("Неверный выбор способа ввода матрицы")


def _select_saved_matrix() -> Matrix:
    if not _session_matrices:
        raise ValueError("Нет сохранённых матриц в этой сессии")
    print("Сохранённые матрицы:")
    keys = list(_session_matrices.keys())
    for i, key in enumerate(keys, start=1):
        print(f"{i}. {key}")
    idx = int(input("Выберите номер: ")) - 1
    if idx < 0 or idx >= len(keys):
        raise ValueError("Неверный номер")
    return _session_matrices[keys[idx]]


def _save_matrix_to_session(matrix: Matrix) -> None:
    save = input("Сохранить эту матрицу для дальнейшего использования? (y/n): ")
    if save.strip().lower() == "y":
        name = input("Введите имя для сохранённой матрицы: ").strip() or f"matrix_{len(_session_matrices) + 1}"
        _session_matrices[name] = matrix
        print(f"Матрица сохранена как '{name}'")


def _print_matrix(label: str, matrix: Matrix) -> None:
    print(f"{label}:\n{matrix}")


def _read_number(prompt: str) -> float:
    return float(input(prompt))


def _read_int(prompt: str) -> int:
    return int(input(prompt))


def action_load_or_create() -> None:
    """Явно создать/загрузить матрицу и предложить сохранить её на сессию."""
    m = _obtain_matrix("Создание/загрузка матрицы:")
    _print_matrix("Матрица", m)
    _save_matrix_to_session(m)


def action_resize() -> None:
    m = _obtain_matrix("Матрица для изменения размера:")
    rows = _read_int("Новое число строк: ")
    cols = _read_int("Новое число столбцов: ")
    m.resize(rows, cols)
    _print_matrix("Результат", m)
    _save_matrix_to_session(m)


def action_submatrix() -> None:
    m = _obtain_matrix("Матрица для извлечения подматрицы:")
    rows = _read_int("Число строк подматрицы: ")
    cols = _read_int("Число столбцов подматрицы: ")
    row_start = _read_int("Начальная строка (с 0): ")
    col_start = _read_int("Начальный столбец (с 0): ")
    sub = m.submatrix(rows, cols, row_start, col_start)
    _print_matrix("Подматрица", sub)
    _save_matrix_to_session(sub)


def action_transpose() -> None:
    m = _obtain_matrix("Матрица для транспонирования:")
    result = m.transpose()
    _print_matrix("Транспонированная матрица", result)
    _save_matrix_to_session(result)


def action_check_type() -> None:
    m = _obtain_matrix("Матрица для проверки типа:")
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

def action_add() -> None:
    m1 = _obtain_matrix("Первая матрица:")
    m2 = _obtain_matrix("Вторая матрица:")
    result = m1 + m2
    _print_matrix("Результат сложения", result)
    _save_matrix_to_session(result)


def action_add_number() -> None:
    m = _obtain_matrix("Матрица:")
    number = _read_number("Введите число: ")
    result = m + number
    _print_matrix("Результат", result)
    _save_matrix_to_session(result)


def action_sub() -> None:
    m1 = _obtain_matrix("Первая матрица (из которой вычитаем):")
    m2 = _obtain_matrix("Вторая матрица (вычитаемая):")
    result = m1 - m2
    _print_matrix("Результат вычитания", result)
    _save_matrix_to_session(result)


def action_mul() -> None:
    m1 = _obtain_matrix("Первая матрица:")
    m2 = _obtain_matrix("Вторая матрица:")
    result = m1 * m2
    _print_matrix("Результат умножения", result)
    _save_matrix_to_session(result)


def action_mul_number() -> None:
    m = _obtain_matrix("Матрица:")
    number = _read_number("Введите число: ")
    result = m * number
    _print_matrix("Результат", result)
    _save_matrix_to_session(result)


def action_div_number() -> None:
    m = _obtain_matrix("Матрица:")
    number = _read_number("Введите число: ")
    result = m / number
    _print_matrix("Результат", result)
    _save_matrix_to_session(result)


def action_pow() -> None:
    m = _obtain_matrix("Квадратная матрица:")
    power = _read_int("Введите степень (целое, >= 0): ")
    result = m ** power
    _print_matrix("Результат", result)
    _save_matrix_to_session(result)


def action_determinant() -> None:
    m = _obtain_matrix("Квадратная матрица:")
    print(f"Определитель: {m.determinant()}")


def action_norm() -> None:
    m = _obtain_matrix("Матрица:")
    print(f"Норма Фробениуса: {m.norm()}")


def action_list_saved() -> None:
    if not _session_matrices:
        print("Нет сохранённых матриц в этой сессии")
        return
    for name, m in _session_matrices.items():
        print(f"\n--- {name} ---")
        print(m)


MENU = {
    "1": ("Ввести/загрузить матрицу", action_load_or_create),
    "2": ("Изменить размер матрицы", action_resize),
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
    "15": ("Показать сохранённые матрицы", action_list_saved),
}


def print_menu() -> None:
    for key, (label, _) in MENU.items():
        print(f"{key}. {label}")
    print("0. Назад")


def run() -> None:
    while True:
        print("\n--- Матрицы ---")
        if _session_matrices:
            print(f"(сохранено матриц в сессии: {len(_session_matrices)})")
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