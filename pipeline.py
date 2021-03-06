from datetime import date

from numpy.linalg import LinAlgError

from config.constants import ACTUAL_AMOUNT_OF_PREDICTIONS, COUNTRIES_WITH_COLONIES
from config.path import (
    COUNTRIES_DATA,
    RUSSIAN_REGIONS_DATA,
    SUBMISSION_PATH,
    TIME_SERIES_CONFIRMED_DATA,
    TIME_SERIES_CONFIRMED_DATA_RUSSIA,
    TIME_SERIES_DEATHS_DATA,
    TIME_SERIES_DEATHS_DATA_RUSSIA
)
from extractor.load import CountriesLoader, RegionsLoader
from extractor.save import Saver
from model.sarimax_model import SarimaxModel

START_DATE = date(2020, 4, 5)
END_DATE = date(2020, 12, 31)

orders = [
    (1, 3, 3),
    (1, 3, 2),
    (2, 3, 4),
    (4, 3, 3),
    (4, 3, 4),
    (4, 4, 4),
]
order_default = (1, 1, 1)


def get_mean_of_predicts(series, model, orders, amount):
    predicts = []
    for order in orders:
        try:
            predicts.append(model.predict(series, order, amount))
        except LinAlgError:
            predicts.append(model.predict(series, order_default, amount))
    return [round(sum(item) / len(item)) for item in zip(*predicts)]


def predict_time_series(time_series, model, orders, amount):
    predicts = {}
    for country, series in time_series.items():
        predicts[country] = get_mean_of_predicts(series, model, orders, amount)
    return predicts


regions_loader = RegionsLoader(RUSSIAN_REGIONS_DATA)
countries_loader = CountriesLoader(COUNTRIES_DATA, COUNTRIES_WITH_COLONIES)
saver = Saver()
sarimax_model = SarimaxModel()

countries_data = countries_loader.load_time_series(TIME_SERIES_CONFIRMED_DATA)
regions_data = regions_loader.load_time_series(TIME_SERIES_CONFIRMED_DATA_RUSSIA)

countries_deaths_data = countries_loader.load_time_series(TIME_SERIES_DEATHS_DATA)
regions_deaths_data = regions_loader.load_time_series(TIME_SERIES_DEATHS_DATA_RUSSIA)

cases_predicts = [
    predict_time_series(countries_data, sarimax_model, orders, ACTUAL_AMOUNT_OF_PREDICTIONS),
    predict_time_series(regions_data, sarimax_model, orders, ACTUAL_AMOUNT_OF_PREDICTIONS)
]

deaths_predicts = [
    predict_time_series(countries_deaths_data, sarimax_model, orders, ACTUAL_AMOUNT_OF_PREDICTIONS),
    predict_time_series(regions_deaths_data, sarimax_model, orders, ACTUAL_AMOUNT_OF_PREDICTIONS)
]

saver.save(SUBMISSION_PATH, cases_predicts, deaths_predicts, START_DATE, END_DATE)
