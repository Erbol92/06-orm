from datetime import datetime, timedelta
from random import randint


def generate_random_date():
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2024, 1, 1)
    """Генерирует случайную дату между start_date и end_date."""
    return start_date + timedelta(days=randint(0, (end_date - start_date).days))
