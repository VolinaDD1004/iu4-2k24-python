import os
import argparse
from colorama import Fore, Style


def print_tree(directory: str, max_depth: int, cur_depth: int = 1, dir_count: int = 0, file_count: int = 0):
    if cur_depth > max_depth:
        return dir_count, file_count

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            dir_count += 1
            print(f"{'|  ' * (cur_depth - 1)}|--{Fore.BLUE}{item}{Style.RESET_ALL}")
            dir_count, file_count = print_tree(item_path, max_depth, cur_depth + 1, dir_count, file_count)
        elif os.path.islink(item_path):
            file_count += 1
            target = os.readlink(item_path)
            print(f"{'|  ' * (cur_depth - 1)}|-- {Fore.LIGHTMAGENTA_EX}{item}{Style.RESET_ALL} -> {Fore.BLUE}{target}{Style.RESET_ALL}")
        else:
            file_count += 1
            print(f"{'|  ' * (cur_depth - 1)}|-- {Fore.GREEN}{item}{Style.RESET_ALL}")

    return dir_count, file_count

def main():
    parser = argparse.ArgumentParser(description="Аналог функции tree на python")
    parser.add_argument("directory", nargs='?', default=os.getcwd(), help="Начальная директория")
    parser.add_argument("-L", "--max-depth", type=int, default=float('inf'), help="Глубина дерева")
    args = parser.parse_args()

    dir_count, file_count = print_tree(args.directory, args.max_depth)
    print('\n', dir_count, "directories,", file_count, "files")


if __name__ == "__main__":
    main()
