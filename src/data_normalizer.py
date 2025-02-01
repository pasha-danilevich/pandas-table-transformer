from typing import List, Tuple
from numpy import number
import pandas as pd

from config import NOTIFICATION_ONLY_COLUMN_ORDER, NOTIFICATION_ONLY_COLUMN_ORDER_TYPE


class DataNormalizer:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def only_notification(self) -> pd.DataFrame:
        
        print('In procces...')
        
        # Создаем пустой DataFrame для результата
        result = pd.DataFrame(
            columns=NOTIFICATION_ONLY_COLUMN_ORDER
            )

        count = 0
        spare_row = None
        
        # Проходим по каждой строке исходного DataFrame
        for _, row in self.df.iterrows(): 
            
            # Проверяем, является ли вся строка пустой (все значения NaN)
            if pd.isna(row['Работы и услуги']):
                continue  # Пропускаем пустые строки
            
            parsed_services_lines = self.__get_parsed_services_lines(row['Работы и услуги'])
            
            
            if not pd.isna(row['Регистрационный номер']):
                # Если 'Регистрационный номер' не пустой, то записываем в запасную строку, чтобы заполнить пробелы, когда они появятся
                spare_row = row

                for line in parsed_services_lines:
                    line, number, description = line
                    
                    new_record = self.__make_new_record(
                        count=count,
                        row=row,
                        line=line,
                        number=number,
                        description=description
                    )
                    
                    result = pd.concat([result, new_record], ignore_index=True)
                    count += 1
                    
            else:
                # Строки нет - используем запасную
                for line in parsed_services_lines:
                    line, number, description = line
                    
                    new_record = self.__make_new_record(
                        count=count,
                        row=spare_row,
                        line=line,
                        number=number,
                        description=description
                    )
                    
                    result = pd.concat([result, new_record], ignore_index=True)
                    count += 1
        
            if count == 3000:
                break
        
        print('Done.')
        return result
    
    
    def __get_parsed_services_lines(self, row) -> List[Tuple[str, str, str]]:
        """
        Парсит строки услуг и возвращает список кортежей с исходной строкой, номером и описанием.

        :param row: Строка услуг, содержащих услуги.
        :return: Список кортежей вида (исходная строка, номер, описание).
        """  

        service_lines = row.split('\n')
        
            
        result = []
        
        for line in service_lines:
            if not line.strip():  # Пропускаем пустые строки
                continue
            
            # Парсим строку на номер и описание
            number, description = self.__parse_line(line=line)
            
            # Добавляем результат в список
            result.append((line, number, description))
            
        return result
    
    
    def __parse_line(self, line) -> tuple:
        '''Разделяем строку на номер и описание'''
        if '.' in line:
            number, description = line.split(' ', 1)
            number = number.strip()
            description = description.strip()
        else:
            number = ''
            description = line.strip()
        
        return number, description
    
    
    def __make_new_record(self, count: int, row, line, number, description) -> pd.DataFrame:
        new_record = pd.DataFrame({
            'Номер': count,
            'Регистрационный номер': row['Регистрационный номер'],
            'Дата поступления': row['Дата поступления'],
            'Вид деятельности': row['Вид деятельности'],
            'Уведомитель': row['Уведомитель'],
            'ИНН': row['ИНН'],
            'Адрес объекта осуществления': row['Адрес объекта осуществления'],
            'ФИАС':  row['ФИАС'],
            'Работы и услуги': [line.strip()],
            '__': [number],
            'Деятельность': [description]
        }, dtype="object")
        return new_record