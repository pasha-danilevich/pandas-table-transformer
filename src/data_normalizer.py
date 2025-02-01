from typing import List, Tuple, Optional
import pandas as pd
from config import NOTIFICATION_ONLY_COLUMN_ORDER

class BaseDataNormalizer:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def _get_parsed_services_lines(self, row: str) -> List[Tuple[str, str, str]]:
        """
        Парсит строки услуг и возвращает список кортежей с исходной строкой, номером и описанием.
        """
        service_lines = row.split("\n")
        result: List[Tuple[str, str, str]] = []

        for line in service_lines:
            if not line.strip():  # Пропускаем пустые строки
                continue

            # Парсим строку на номер и описание
            number, description = self.__parse_line(line=line)

            # Добавляем результат в список
            result.append((line.strip(), number, description))

        return result

    def __parse_line(self, line: str) -> Tuple[str, str]:
        """Разделяет строку на номер и описание."""
        if "." in line:
            number, description = line.split(" ", 1)
            number = number.strip()
            description = description.strip()
        else:
            number = ""
            description = line.strip()

        return number, description

    def _make_new_record(
        self,
        count: int,
        row: pd.Series,
        line: str,
        number: str,
        description: str
    ) -> pd.DataFrame:
        """Создает новую запись в виде DataFrame."""
        new_record = pd.DataFrame({
            "Номер": [count],
            "Регистрационный номер": [row["Регистрационный номер"]],
            "Дата поступления": [row["Дата поступления"]],
            "Вид деятельности": [row["Вид деятельности"]],
            "Уведомитель": [row["Уведомитель"]],
            "ИНН": [row["ИНН"]],
            "Адрес объекта осуществления": [row["Адрес объекта осуществления"]],
            "ФИАС": [row["ФИАС"]],
            "Работы и услуги": [line.strip()],
            "__": [number],
            "Деятельность": [description],
        }, dtype="object")
        return new_record


class NotificationOnlyNormalizer(BaseDataNormalizer):
        
    def normalize(self) -> pd.DataFrame:
        """Нормализует данные и возвращает DataFrame."""
        print("In process...")

        # Создаем пустой DataFrame для результата
        result = pd.DataFrame(columns=NOTIFICATION_ONLY_COLUMN_ORDER)

        count = 0
        spare_row: Optional[pd.Series] = None  

        for _, row in self.df.iterrows():
            # Проверяем, является ли вся строка пустой (все значения NaN)
            if pd.isna(row["Работы и услуги"]):
                continue  # Пропускаем пустые строки

            parsed_services_lines = self._get_parsed_services_lines(row["Работы и услуги"])

            if not pd.isna(row["Регистрационный номер"]):
                # Если 'Регистрационный номер' не пустой, записываем в запасную строку
                spare_row = row

                for line_tuple in parsed_services_lines:
                    line, number, description = line_tuple

                    new_record = self._make_new_record(
                        count=count,
                        row=row,
                        line=line,
                        number=number,
                        description=description,
                    )

                    result = pd.concat([result, new_record], ignore_index=True)
                    count += 1

            else:
                # Строки нет - используем запасную
                if spare_row is not None:
                    for line_tuple in parsed_services_lines:
                        line, number, description = line_tuple

                        new_record = self._make_new_record(
                            count=count,
                            row=spare_row,
                            line=line,
                            number=number,
                            description=description,
                        )

                        result = pd.concat([result, new_record], ignore_index=True)
                        count += 1

            if count == 100:
                break

        print("Done.")
        return result


class LicensesOnlyNormalizer(BaseDataNormalizer):
    def __init__(self, df_list: list[pd.DataFrame]) -> None:
        self.df_list = df_list
        
    def normalize(self) -> pd.DataFrame:
        """Нормализует данные и возвращает DataFrame."""
        for df in self.df_list:
            print(df.columns)
            
        return self.df_list[0]
