
from config import BASE_DATA_DIR


class FileConfig:
    def __init__(self, file_name: str, skiprows: int) -> None:
        self.file_name = file_name
        self.skiprows = skiprows
        
    def get_relative_file_path(self) -> str:
        """Относительный путь файла"""
        return BASE_DATA_DIR + '/' + self.file_name
    
    
    @staticmethod
    def check_write_permission(file_path: str) -> bool:
        """
        Проверяет, можно ли записывать в указанный файл.
        :param file_path: Путь к файлу.
        :return: True, если запись возможна, иначе False.
        """
        try:
            # Пытаемся открыть файл в режиме записи
            with open(file_path, 'w'):
                pass
            return True
        except PermissionError:
            print(f"Ошибка: Нет прав на запись в файл {file_path}. Возможно, файл уже используется.")
            return False
        except Exception as e:
            print(f"Ошибка при проверке прав на запись: {e}")
            return False