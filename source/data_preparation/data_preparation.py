import os
import json
import pytz
import pandas as pd
from pathlib import Path


def get_files_in_directory():
    """
    Reads JSON files in a set directory.
    Returns a list of names of files in the directory
    to be iterated through.
    :return a list of file names in the directory
    """
    path_to_files = Path(__file__).cwd() / 'Source/data/input/'
    files_in_path = os.scandir(path_to_files)

    list_of_files = []
    for file in files_in_path:
        if file.is_dir() or file.is_file():
            list_of_files.append(file.name)
    return list_of_files


def create_dataframe(file_json):
    """
    Creates a pandas dataframe from a JSON file.
    Requires a name of the file.
    """
    path_to_files = Path(__file__).cwd() / 'Source/data/input/'
    with open(path_to_files / file_json) as jfile:
        json_data = json.load(jfile)
        df = pd.DataFrame(pd.json_normalize(json_data))

    return df


def flatten_json_file(dataframe: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Flattens the supplied dataframe and returns a new dataframe.
    :param col: a name of the column to be flattened
    :param dataframe: dataframe to flatten
    :return: new dataframe with flattened json data
    """
    dataframe_flat = dataframe[col].apply(pd.Series)
    dataframe_flat_0 = dataframe_flat[0].apply(pd.Series)
    dataframe_flat_0.columns = ['weather_id', 'weather_main', 'weather_description', 'weather_icon']
    dataframe_new = pd.concat([dataframe, dataframe_flat_0], axis=1)
    dataframe_new = dataframe_new.drop(columns=[col], axis=1)
    return dataframe_new


def change_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Changes the column names of the dataframe to their new column names.
    :param dataframe: a pandas dataframe to change column names
    :return: dataframe with new column names
    """
    new_names = {"dt": "date_local",
                 "name": "city",
                 "id": "country_id",
                 "coord.lon": "longitude",
                 "coord.lat": "latitude",
                 "main.temp": "main_temp",
                 "main.feels_like": "main_feels_like",
                 "main.temp_min": "main_temp_min",
                 "main.temp_max": "main_temp_max",
                 "main.pressure": "pressure",
                 "main.humidity": "humidity",
                 "wind.speed": "wind_speed",
                 "wind.deg": "wind_deg",
                 "clouds.all": "clouds",
                 "sys.type": "sys_type",
                 "sys.id": "sys_id",
                 "sys.country": "country",
                 "sys.sunrise": "sunrise_local",
                 "sys.sunset": "sunset_local"}
    dataframe.rename(columns=new_names, inplace=True)
    return dataframe


def change_datetime_format(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Change datetime format of a given dataframe to ISO 8601 format.
    Datetime returned is adjusted for 'Europe/Vilnius' time zone.
    :param dataframe: dataframe to change datetime format for.
    :return: dataframe with changed datetime format.
    """
    date_cols = ['date_local', 'sunrise_local', 'sunset_local']
    local_timezone = pytz.timezone('Europe/Vilnius')
    dataframe['date_vilnius'] = (pd.to_datetime(dataframe['date_local'], unit='s', errors='coerce', utc=True)
                                 .dt.tz_convert(local_timezone))

    for i in date_cols:
        dataframe[i] = dataframe[i] + dataframe['timezone']
        dataframe[i] = pd.to_datetime(dataframe[i], unit='s', errors='coerce')

    return dataframe


def reorder_dataframe_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Reorders the columns of a dataframe.
    :param dataframe: dataframe to reorder columns for
    :return: dataframe with reordered columns
    """
    reordered_columns = ['longitude', 'latitude', 'country_id', 'country', 'city', 'main_temp', 'main_feels_like',
                         'main_temp_min', 'main_temp_max', 'date_vilnius', 'date_local', 'timezone', 'sunrise_local',
                         'sunset_local', 'weather_id', 'weather_main', 'weather_description', 'weather_icon',
                         'pressure', 'humidity', 'wind_speed', 'wind_deg', 'clouds', 'visibility', 'base',
                         'sys_type', 'sys_id', 'cod']

    dataframe = dataframe.reindex(columns=reordered_columns)
    return dataframe
