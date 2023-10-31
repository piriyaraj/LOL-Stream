import json
from entities.match_data import MatchData


def save(data: MatchData,folder) -> None:
    with open(f'{folder}/match_data.json', 'w',encoding='utf-8') as data_file:
        json.dump(data, data_file)


def load(path) -> MatchData:
    with open(path, 'r',encoding='utf-8') as data_file:
        match_data = json.load(data_file)
    return match_data
