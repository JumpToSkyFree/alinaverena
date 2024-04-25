import os
from typing import Any
from django.db import models
from alinaverenabackend.settings import CURRENCIES_FILE_PATH, COUNTRIES_FILE_PATH, LANGUAGES_FILE_PATH
import json


class CurrenciesSourceNotFound(Exception):
    def __init__(self, *args) -> None:
        self.message = "Currencies source file don't exist."
        super().__init__(self.message, *args)


class CurrenciesCurrencyNotFound(Exception):
    def __init__(self, currency_name: str, *args: object) -> None:
        self.message = f"Currency {currency_name} not found in currencies data."
        super().__init__(self.message, *args)


class CountriesSourceNotFound(Exception):
    def __init__(self, *args) -> None:
        self.message = "Countries source file don't exist."
        super().__init__(self.message, *args)


class CountryNotFound(Exception):
    def __init__(self, country_code: str, *args: object) -> None:
        self.message = f"Country {country_code} not found in countries data."
        super().__init__(self.message, *args)


class LanguagesSourceNotFound(Exception):
    def __init__(self, *args) -> None:
        self.message = "Languages source file don't exist."
        super().__init__(self.message, *args)


class LanguageNotFound(Exception):
    def __init__(self, language_code: str, *args: object) -> None:
        self.message = f"Language code {language_code} not found in languages data."
        super().__init__(self.message, *args)


def source_file_exists_or_raise_exception(source_path: str, exception_type):
    if os.access(source_path, os.R_OK) is False:
        raise exception_type()


def source_file_load_data(source_path: str, cls):
    with open(source_path, 'r') as source:
        cls.data = json.load(source)


class Currencies:
    def __init__(self, currencies_source: str = os.path.join(os.getcwd(), "currencies.json")) -> None:
        #         if os.access(currencies_source, os.R_OK) is False:
        #             raise CurrenciesSourceNotFound()

        self.data = {}

        source_file_exists_or_raise_exception(
            currencies_source, CurrenciesSourceNotFound)

        self.currencies_source = currencies_source

        # with open(self.currencies_source, 'r') as source:
        #     self.currencies_data = json.load(source)

        source_file_load_data(currencies_source, self)

    def get_currency(self, currency_name: str):
        if not currency_name in self.data:
            raise CurrenciesCurrencyNotFound(currency_name=currency_name)

        return self.data[currency_name]

    def get_all_currencies(self):
        return self.data

    def get_django_currencies_as_choices(self):
        return [(key, value['symbol'] + ' ' + value['name']) for key, value in self.data.items()]


class Countries:
    def __init__(self, countries_source: str = os.path.join(os.getcwd(), "./countries.json")):
        self.data = {}

        source_file_exists_or_raise_exception(
            countries_source, CurrenciesSourceNotFound)

        self.countries_source = countries_source

        # with open(self.countries_source, 'r') as source:
        #     self.countries_data = json.load(source)

        source_file_load_data(countries_source, self)

    def get_country_by_code(self, country_code: str):
        if not country_code in self.data:
            raise CountryNotFound(country_code=country_code)

        return self.data[country_code]

    def get_django_countries_as_choices(self):
        return [(key, value) for key, value in self.data.items()]


class Languages:
    def __init__(self, languages_source: str = os.path.join(os.getcwd(), "./languages.json")):
        self.languages_source = languages_source
        self.data = {}

        source_file_exists_or_raise_exception(
            languages_source, LanguagesSourceNotFound)

        source_file_load_data(languages_source, self)

    def get_language_by_code(self, language_code: str):
        if language_code not in self.data:
            raise LanguageNotFound(language_code=language_code)

        return self.data[language_code]

    def get_django_languages_as_choices(self):
        return [(value['name'], value['nativeName'] + ' — ' + value['name']) for _, value in self.data.items()]


class LanguageField(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        kwargs['choices'] = Languages(languages_source=os.path.join(os.path.join(
            os.getcwd(), LANGUAGES_FILE_PATH), "languages.json")).get_django_languages_as_choices()
        super().__init__(*args, db_collation=db_collation, **kwargs)

    def deconstruct(self):
        return super().deconstruct()


class CountryField(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        # TODO: add countries choices.
        kwargs['choices'] = Countries(countries_source=os.path.join(os.path.join(
            os.getcwd(), COUNTRIES_FILE_PATH), "countries.json")).get_django_countries_as_choices()
        super().__init__(*args, db_collation=db_collation, **kwargs)

    def deconstruct(self):
        return super().deconstruct()


class CurrencyField(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        kwargs['choices'] = Currencies(currencies_source=os.path.join(os.path.join(
            os.getcwd(), CURRENCIES_FILE_PATH), "currencies.json")).get_django_currencies_as_choices()
        super().__init__(*args, db_collation=db_collation, **kwargs)

    def deconstruct(self):
        return super().deconstruct()


class ProductFeatures(models.Field):
    description = "Product features"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(verbose_name="", *args, **kwargs)

    def deconstruct(self) -> Any:
        return super().deconstruct()
