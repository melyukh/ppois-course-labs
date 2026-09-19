from lab1.src.vector.classes.vector import Vector


def read_vector(prompt: str) -> Vector:
    """Считать вектор с консоли, используя публичный API класса."""
    text = input(prompt)
    return Vector.generate_from_string(text)


def print_vector(label: str, vector: Vector) -> None:
    """Вывести вектор в консоль."""
    print(f"{label}: {vector}")


def action_add() -> None:
    v1 = read_vector("Введите первый вектор (x y z): ")
    v2 = read_vector("Введите второй вектор (x y z): ")
    print_vector("Результат сложения", v1 + v2)


def action_sub() -> None:
    v1 = read_vector("Введите первый вектор (x y z): ")
    v2 = read_vector("Введите второй вектор (x y z): ")
    print_vector("Результат вычитания", v1 - v2)


def action_length() -> None:
    v = read_vector("Введите вектор (x y z): ")
    print(f"Длина: {v.length}")


def action_compare() -> None:
    v1 = read_vector("Введите первый вектор (x y z): ")
    v2 = read_vector("Введите второй вектор (x y z): ")
    print(f"Равны по длине: {v1 == v2}")
    print(f"Не равны: {v1 != v2}")


def action_copy() -> None:
    v = read_vector("Введите вектор (x y z): ")
    v_copy = v.copy()
    print_vector("Оригинал", v)
    print_vector("Копия", v_copy)


MENU = {
    "1": ("Сложение векторов", action_add),
    "2": ("Вычитание векторов", action_sub),
    "3": ("Длина вектора", action_length),
    "4": ("Сравнение векторов", action_compare),
    "5": ("Копирование вектора", action_copy),
}


def print_menu() -> None:
    for key, (label, _) in MENU.items():
        print(f"{key}. {label}")
    print("0. Выход")


def run() -> None:
    while True:
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
        except (ValueError, TypeError, ZeroDivisionError) as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    run()