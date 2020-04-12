from datetime import date
from random import random

from config import COUNTRIES_DATA, SUBMISSION_PATH, TIME_SERIES_DATA
from extractor.load import load_countries_time_series
from extractor.save import save_predicts_to_csv


START_DATE = date(2020, 4, 5)
END_DATE = date(2020, 4, 7)

model = ''  # модель загружается откуда-то или импортируется класс с моделью

country_predicts = {}


def predict(model, time_series: list) -> list:
    """Принимает на вход список с данными и возвращает список предиктов."""

    return [random()]*3


countries_time_series = load_countries_time_series(TIME_SERIES_DATA, COUNTRIES_DATA)

for country, time_series in countries_time_series.items():
    country_predicts[country] = predict(model, time_series)  # делаем предикт для каждой страны

save_predicts_to_csv(country_predicts, SUBMISSION_PATH, START_DATE, END_DATE)