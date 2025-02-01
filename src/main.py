import pandas
from file_config import FileConfig
from data_normalizer import DataNormalizer
from config import BASE_NORMALIZED_DATA_DIR


if __name__ == '__main__':
    
    file = FileConfig('Реестр_уведомлений_Крым_ГОС_с_объ_24_12.xlsx', 3)
    df = pandas.read_excel(
        io=file.get_relative_file_path(), 
        skiprows=file.skiprows
    )
    
    # перед нормализацией проверить, можно ли писать в файл 
    is_can_write = FileConfig.check_write_permission(BASE_NORMALIZED_DATA_DIR + '/' +'output_data.xlsx')
    
    if is_can_write:
        
        normalizer_df_obj = DataNormalizer(df)
        normalized_df = normalizer_df_obj.only_notification()
        
        # Сохраняем результат в новый Excel-файл
        normalized_df.to_excel(
            BASE_NORMALIZED_DATA_DIR + '/' +'output_data.xlsx', 
            index=False
        )


