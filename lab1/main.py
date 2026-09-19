from src.vector.cli_API.vector_cli_application import run as run_vector_ui
from src.matrix.cli_API.matrix_cli_application import run as run_matrix_ui


MAIN_MENU = {
    "1": ("Вектор", run_vector_ui),
    "2": ("Матрица", run_matrix_ui),
}


def print_main_menu() -> None:
    print("\n=== Главное меню ===")
    for key, (label, _) in MAIN_MENU.items():
        print(f"{key}. {label}")
    print("0. Выход")


def main() -> None:
    while True:
        print_main_menu()
        choice = input("Выберите лабораторную работу: ")
        if choice == "0":
            print("Завершение работы.")
            break

        entry = MAIN_MENU.get(choice)
        if entry is None:
            print("Неверный выбор, попробуйте снова")
            continue

        entry[1]()  # запускает run() соответствующего UI-модуля


if __name__ == "__main__":
    main()