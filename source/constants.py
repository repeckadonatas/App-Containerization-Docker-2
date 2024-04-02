import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path


PATH_TO_DATA_STORAGE = Path(__file__).cwd() / 'source/data/'
PATH_TO_API = Path(__file__).cwd() / 'source/api_key.txt'
PATH_TO_METALS_LIST = Path(__file__).cwd() / 'source/metals.txt'


def env_config() -> os.environ:
    """
    Gets database connection credentials from .env file.
    :return: os.environ
    """
    load_dotenv(find_dotenv('.env', usecwd=True))

    return os.environ


def read_api() -> str:
    with open(PATH_TO_API, 'r', encoding='utf-8') as key:
        api_key = key.readline()
    return api_key
    
    
def read_metals_list() -> list:
    metals = []
    with open(PATH_TO_METALS_LIST, 'r', encoding='utf-8') as file:
        for metal in file:
            metal = metal.strip().rstrip(',')
            metals.append(metal)
    return metals

