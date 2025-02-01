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
    


    # df_notification = pd.read_excel(
    #     io=f'{BASE_NORMALIZED_DATA_DIR}/normalized_notifications.xlsx',
    #     skiprows=0
    # )
    # df_license = pd.read_excel(
    #     io=f'{BASE_NORMALIZED_DATA_DIR}/normalized_license.xlsx',
    #     skiprows=0
    # )

    # # Объединение DataFrame по ИНН
    # result = pd.merge(df_notification, df_license, on='ИНН', how='outer')
    
    # result.to_excel(f"{BASE_NORMALIZED_DATA_DIR}/notification_license.xlsx", index=False) ValueError: This sheet is too large! Your sheet size is: 8848380, 27 Max sheet size is: 1048576, 16384
    # print(f"Данные успешно сохранены")
    