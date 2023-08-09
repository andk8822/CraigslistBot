import os.path


def test_csv_writer(prepare_data_and_create_table):
    """Тест на запись готовых вакансий из списка в таблицу."""
    assert os.path.exists(f'csv/{prepare_data_and_create_table}'), 'Тестовая таблица не была создана'
