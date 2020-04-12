import pandas as pd


def load_countries_codes(countries_path: str) -> list:
    countries = pd.read_csv(countries_path)
    return list(countries['iso_alpha3'])


def load_countries_names(countries_path: str) -> list:
    countries = pd.read_csv(countries_path)
    return list(countries['ccse_name'])


def load_countries_time_series(filename: str, countries_path: str) -> dict:
    """Принимает на вход путь до csv файла.

    Парсит его в словарь вида {'RUS': [1,2,3]}
    """

    countries_dict = {}

    data = pd.read_csv(filename)
    countries = load_countries_names(countries_path)
    countries_codes = load_countries_codes(countries_path)
    for index, country in enumerate(countries):
        countries_dict[countries_codes[index]] = data[data['Country/Region'] == country].values.tolist()[0][4:]
    return countries_dict