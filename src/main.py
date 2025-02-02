import pandas as pd
from file_config import FileConfig
from data_normalizer import LicensesOnlyNormalizer, NotificationOnlyNormalizer
from config import BASE_NORMALIZED_DATA_DIR


from typing import Type, Union

def normalize(input_file: FileConfig, output_path: str):
    df = pd.read_excel(
        io=input_file.get_relative_file_path(),
        skiprows=input_file.skiprows
    )
    
    normalizer_obj = NotificationOnlyNormalizer(df)  # Создаем экземпляр нормализатора
    normalized_df = normalizer_obj.normalize()
    normalized_df.to_excel(output_path, index=False)
    print(f"Данные успешно сохранены в файл: {output_path}")
    
def normalize_list(input_files: list[FileConfig], output_path: str):
    """
    Нормализует данные из входного файла и сохраняет результат в новый файл.

    :param input_file: Конфигурация входного файла.
    :param normalizer: Класс для нормализации данных (NotificationOnlyNormalizer или LicensesOnlyNormalizer).
    :param output_file_name: Имя выходного файла.
    """
    
    
    # Чтение данных из Excel-файла
    df_list: list[pd.DataFrame] = []
    for file in input_files:
        df = pd.read_excel(
            io=file.get_relative_file_path(),
            skiprows=file.skiprows
        )
        df_list.append(df)

    df = pd.concat(df_list, axis=0)
    normalizer_obj = LicensesOnlyNormalizer(df)  # Создаем экземпляр нормализатора
    normalized_df = normalizer_obj.normalize()

    # Сохранение нормализованных данных в Excel
    normalized_df.to_excel(output_path, index=False)
    print(f"Данные успешно сохранены в файл: {output_path}")


def marge_notification_license():
    # Загрузка данных
    df_license = pd.read_excel('normalized_data/'+'normalized_license.xlsx')
    df_license = df_license.rename(columns={'Работы/услуги': 'Работы и услуги'})
    df_notifications = pd.read_excel('normalized_data/'+'normalized_notifications.xlsx')

    df_notifications = df_notifications.drop(columns=['Номер'])

    # Объединение данных по ИНН
    merged_df = pd.merge(
        df_notifications,
        df_license,
        on='ИНН',
        how='outer',  # Используем outer join, чтобы сохранить все строки
        suffixes=('_notif', '_lic')  # Добавляем суффиксы для одинаковых столбцов
    )

    # Переименование столбцов для соответствия Уведомление_Лицензии_small.xlsx
    merged_df = merged_df.rename(columns={
        'Дата поступления': 'Дата поступления',
        'Вид деятельности': 'Вид деятельности',
        'Уведомитель': 'Уведомитель',
        'Адрес объекта осуществления': 'Адрес объекта осуществления',
        'ФИАС': 'ФИАС',
        'Работы и услуги': 'Работы и услуги',
        '__': '___x',
        'Деятельность': 'Деятельность',
        'Наименование организации': 'Наименование организации',
        'Полное наименование организации': 'Полное наименование организации',
        'ОГРН': 'ОГРН',
        'Регион организации': 'Регион организации',
        'Юридический адрес': 'Юридический адрес',
        'Регион объекта': 'Регион объекта',
        'Адрес объекта': 'Адрес объекта',
        'Тип населенного пункта': 'Тип населенного пункта',
        'Тип объекта': 'Тип объекта',
        '№': '№',
        'Дата': 'Дата',
        'Статус': 'Статус',
        'Работы/услуги': 'Работы/услуги',
        '__': '___y'
    })

    # # Объединение столбцов 
    # merged_df['Работы и услуги'] = merged_df['Работы и услуги'].combine_first(merged_df['Работы/услуги'])
    
    merged_df['Деятельность'] = merged_df['Деятельность_notif'].combine_first(merged_df['Деятельность_lic'])

    # Удаление лишнего столбца 
    merged_df = merged_df.drop(columns=['Деятельность_lic', 'Деятельность_notif'])

    # Упорядочивание столбцов в соответствии с Уведомление_Лицензии_small.xlsx
    columns_order = [
        'Регистрационный номер', 'Дата поступления', 'Вид деятельности', 
        'Уведомитель', 'ИНН', 'Адрес объекта осуществления', 
        'ФИАС', 'Работы и услуги',  # Обновленный столбец
        '___x', 'Деятельность', 
        'Наименование организации', 
        'Полное наименование организации', 
        'ОГРН', 
        'Регион организации', 
        'Юридический адрес', 
        'Регион объекта', 
        'Адрес объекта', 
        'Тип населенного пункта', 
        'Тип объекта', 
        '№', 
        'Дата', 
        'Статус'
    ]

    # Приведение столбцов к нужному порядку
    merged_df = merged_df[columns_order] if all(col in merged_df.columns for col in columns_order) else merged_df

    # Сохранение результата
    merged_df.to_excel('normalized_data/'+'notification_license.xlsx', index=False)

    print("Файл 'notification_license.xlsx' успешно создан.")



if __name__ == '__main__':
    input_file = FileConfig('Реестр_уведомлений_Крым_ГОС_с_объ_24_12.xlsx', 3)
    output_file_name = "normalized_notifications"

    # Проверка прав на запись в файл
    output_path = f"{BASE_NORMALIZED_DATA_DIR}/{output_file_name}.xlsx"
    if FileConfig.check_write_permission(output_path):
        normalize(input_file, output_path)
        
    
    input_files = [FileConfig('Подведы_ГБУ вариант 2.xlsx', 12),
                   FileConfig('Подведы МЗ РК_ГАУ.xlsx', 13),
                   FileConfig('Подведы МЗ РК санатории.xlsx', 13),
                   FileConfig('Семашко расширенный.xlsx', 12),]
    
    
    
    output_file_name = "normalized_license"

    # Проверка прав на запись в файл
    output_path = f"{BASE_NORMALIZED_DATA_DIR}/{output_file_name}.xlsx"
    if FileConfig.check_write_permission(output_path):
        normalize_list(input_files, output_path)
    

    # marge_notification_license() ValueError: This sheet is too large!
    



