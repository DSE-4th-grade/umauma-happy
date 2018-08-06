from collections import OrderedDict
from umauma_happy_app.models import *

import datetime
import time


def is_hit(history):
    """
    historyレコードが当たっているか判定する
    :param history: History object
    :return:boolean
    """
    if history.data.rank <= 3:
        return True
    else:
        return False


def calculate_hit_percentage(factor_counter, factor_list):
    """
    与えられた要素辞書に格納されている使用回数と的中回数を使って的中率を計算する
    factor_counter[factor]['use']に使用回数
    factor_counter[factor]['hit']に的中回数が格納されていることが前提
    :param factor_counter: Dictionary
    :param factor_list: List
    :return:
    """
    for factor in factor_list:
        if factor_counter[factor]['use'] == 0:
            factor_counter[factor]['hit_percentage'] = '{:.3f}'.format(0)
        else:
            factor_counter[factor]['hit_percentage'] \
                = '{:0=6.3f}'.format((factor_counter[factor]['hit'] / factor_counter[factor]['use']) * 100)
    # 結果を的中率, 同点なら使用回数順になるように並び替え
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: (x[1]['hit_percentage'], x[1]['use']), reverse=True))
    return factor_counter


def calculate_use_percentage(factor_counter, factor_list):
    """
    与えられた要素辞書に格納されている使用回数を使って使用率を計算する
    factor_counter[factor]['use']に使用回数が格納されていることが前提
    :param factor_counter: Dictionary
    :param factor_list: List
    :return:
    """
    # 全要素数を計算
    total_use = 0
    for factor in factor_list:
        total_use += factor_counter[factor]['use']
    # 使用率を計算
    if total_use == 0:
        for factor in factor_list:
            factor_counter[factor]['use_percentage'] = 0
    else:
        for factor in factor_list:
            factor_counter[factor]['use_percentage'] \
                = '{:0=6.3f}'.format((factor_counter[factor]['use'] / total_use) * 100)
    # 結果を使用数順に並び替え
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: x[1]['use'], reverse=True))
    return factor_counter


def count_factor(weight_list):
    """
    与えられたweightリストに対して,要素の使用回数,的中回数,的中率を辞書で返す
    factor_counter[factor]['use']に使用回数
    factor_counter[factor]['hit']に的中回数
    factor_counter[factor]['hit_percentage']に的中率を格納する
    :param weight_list: List
    :return factor_counter: Dictionary
    """
    factor_list_all = list(Factor.objects.all())
    pre_time = time.time()  # 経過時間表示用
    factor_counter = init_factor_counter()  # 結果を格納する辞書を初期化
    # 要素別使用回数と的中回数を計算
    for weight in weight_list:
        factor_counter[weight.factor]['use'] += 1
        if is_hit(weight.history):
            factor_counter[weight.factor]['hit'] += 1
    # 的中率,使用率を計算
    factor_counter = calculate_use_percentage(factor_counter, factor_list_all)
    factor_counter = calculate_hit_percentage(factor_counter, factor_list_all)
    return factor_counter


def count_factor_only_use(weight_list):
    """
    与えられたweightリストに対して,要素の使用回数,的中回数,的中率を辞書で返す
    factor_counter[factor]['use']に使用回数
    factor_counter[factor]['hit']に的中回数
    factor_counter[factor]['percentage']に的中率を格納する
    :param weight_list: List
    :return factor_counter: Dictionary
    """
    factor_list_all = list(Factor.objects.all())
    pre_time = time.time()  # 経過時間表示用
    factor_counter = init_factor_counter_only_use()  # 結果を格納する辞書を初期化
    # 要素別使用回数を計算
    for weight in weight_list:
        factor_counter[weight.factor]['use'] += 1
    # 使用率を計算
    factor_counter = calculate_use_percentage(factor_counter, factor_list_all)
    return factor_counter


def get_weight(number=None):
    """
    指定された数だけweightテーブルからデータを返す. 指定しない場合は全件取得.
    :param number: int
    :return all_weight: List
    """
    if number is not None:
        return list(Weight.objects.all()[:number])
    else:
        return list(Weight.objects.all())


def get_weight_by_races(race_list):
    """
    渡されたRaceListのweightを返す.
    :param race_list: List
    :return: List
    """
    # 指定された期間のraceを取得
    print(f'{datetime.datetime.now()} | Get data in {len(race_list)}Races.')
    weight_list = []
    # raceからweightを取得
    for race in race_list:
        weight_list.extend(get_weight_by_race(race))
    return weight_list


def get_weight_by_race(race):
    """
    与えられたRaceを指定しているweightをリストで返す
    :param race: Object
    :return: List
    """
    data_list = {}
    history_list = {}
    weight_list = []
    print(f'{datetime.datetime.now()} | Get data about{race}.'.encode('utf-8'))
    data_list[race] = list(race.data_set.all())
    for data in data_list[race]:
        history_list[data] = list(data.history_set.all())
        for history in history_list[data]:
            weight_list.extend(list(history.weight_set.all()))
    return weight_list


def get_race_by_period(start, end):
    """
    指定された期間のraceを返す.(start <= race.departure_time <= end)
    :param start: String(YYYY-MM-DD HH:MM:ss) or Datetime
    :param end: String(YYYY-MM-DD HH:MM:ss) or Datetime
    :return: List
    """
    return list(Race.objects.filter(departure_time__range=[start, end]))


def is_not_null_rank_in_data(race):
    """
    与えられたレースの結果が格納されているか判定
    :param race: Object
    :return: boolean
    """
    data_list = list(race.data_set.all())
    for data in data_list:
        if data.rank is None:
            return False
    return True


def init_factor_counter():
    """
    factorの使用回数等を格納するfactor_counterを初期化
    :return: Dictionary
    """
    factor_list_all = list(Factor.objects.all())
    factor_counter = {}
    for factor in factor_list_all:
        factor_counter[factor] = {}
        factor_counter[factor]['use'] = 0
        factor_counter[factor]['hit'] = 0
    return factor_counter


def init_factor_counter_only_use():
    """
    factorの使用回数を格納するfactor_counterを初期化
    :return: Dictionary
    """
    factor_list_all = list(Factor.objects.all())
    factor_counter = {}
    for factor in factor_list_all:
        factor_counter[factor] = {}
        factor_counter[factor]['use'] = 0
    return factor_counter


