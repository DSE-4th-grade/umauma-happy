from collections import OrderedDict
from umauma_happy_app.models import *

import datetime


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
            factor_counter[factor]['percentage'] = '{:.3f}'.format(0)
        else:
            factor_counter[factor]['percentage'] \
                = '{:0=6.3f}'.format((factor_counter[factor]['hit'] / factor_counter[factor]['use']) * 100)
    # 結果を的中率, 同点なら使用回数順になるように並び替え
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: x[1]['use'], reverse=True))
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: x[1]['percentage'], reverse=True))
    return factor_counter


def count_factor(weight_list):
    """
    与えられたweightリストに対して,要素の使用回数,的中回数,的中率を辞書で返す
    factor_counter[factor]['use']に使用回数
    factor_counter[factor]['hit']に的中回数
    factor_counter[factor]['percentage']に的中率を格納する
    :param weight_list: List
    :return factor_counter: Dictionary
    """
    factor_list_all = list(Factor.objects.all())
    pre_time = datetime.datetime.now()  # 経過時間表示用
    # 結果を格納する辞書を初期化
    factor_counter = {}
    for factor in factor_list_all:
        factor_counter[factor] = {}
        factor_counter[factor]['use'] = 0
        factor_counter[factor]['hit'] = 0
    # 要素別使用回数と的中回数を計算
    print(f'{datetime.datetime.now()}' + ' | ' + f'{len(weight_list)}' + '件の使用回数と的中回数の計算を行います.[開始]')
    for weight in weight_list:
        factor_counter[weight.factor]['use'] += 1
        if is_hit(weight.history):
            factor_counter[weight.factor]['hit'] += 1
        # if weight.id % 100 == 0:
            # print('{0} | {1}件処理しました.'.format(datetime.datetime.now(), weight.id))
    print(f'{datetime.datetime.now()}' + ' | ' + f'{len(weight_list)}' + '件の使用回数と的中回数の計算を行いました.処理時間：'
          + f'{datetime.datetime.now() - pre_time}' + '[完了]')
    # 的中率を計算
    factor_counter = calculate_hit_percentage(factor_counter, factor_list_all)
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


def get_weight_by_time(start, end):
    """
    指定された期間のweightを返す.(start <= weight.history.data.race.departure_time <= end)
    :param start: String(YYYY-MM-DD HH:MM:ss) or Datetime
    :param end: String(YYYY-MM-DD HH:MM:ss) or Datetime
    :return:
    """
    # 指定された期間のraceを取得
    race_list = list(Race.objects.filter(departure_time__range=[start, end]))
    print(f'{datetime.datetime.now()}' + ' | ' + f'{len(race_list)}' + '件のレースのデータを取得します.')
    data_list = {}
    history_list = {}
    weight_list = []
    # raceからweightを取得
    for race in race_list:
        print(f'{datetime.datetime.now()}' + ' | ' + f'{race}' + 'についてのデータを取得します.')
        data_list[race] = list(race.data_set.all())
        for data in data_list[race]:
            history_list[data] = list(data.history_set.all())
            for history in history_list[data]:
                weight_list.extend(list(history.weight_set.all()))
    return weight_list