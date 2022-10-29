from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileName:
    how_to_get: str = Path('textcloud', 'how_to_get.txt')
    how_to_use: str = Path('textcloud', 'how_to_use.txt')
    admin_message: str = Path('textcloud', 'admin_message.txt')
    sales: str = Path('textcloud', 'sales.txt')
    friend: str = Path('textcloud', 'friend.txt')
    start: str = Path('textcloud', 'start.txt')


class TextCloud:
    files = FileName()

    @staticmethod
    def read(filename: Path) -> str:
        with open(filename, mode='r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def write(filename: Path, text: str) -> None:
        with open(filename, mode='w', encoding='utf-8') as file:
            file.write(text)
