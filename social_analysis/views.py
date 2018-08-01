from django.shortcuts import render, get_object_or_404, get_list_or_404
from umauma_happy_app.models import *
from umauma_happy_app.utils import analysis
from collections import OrderedDict
import datetime
import time


class SampleValues:
    analysis_number_samples = [100, 200, 500, 1000, 2000, 5000]


def index(request):
    """
    他者分析の分析内容の選択画面
    :param request: Request
    :return render: with Request request, Dictionary context
    """
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'weight_amount': len(analysis.get_weight())}
    return render(request, 'social_analysis/index.html', context)


def calculate(request, analysis_number=None):
    """
    他者分析の全ユーザー要素別的中率の表示
    :param request: Request
    :param analysis_number: int
    :return render: with Request request, Dictionary context
    """
    pre_time = time.time()  # 経過時間表示用
    weights = analysis.get_weight(analysis_number)
    factor_count = analysis.count_factor(weights)
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'factor_count': factor_count,
               'analysis_number': analysis_number,
               'calculation_duration': time.time() - pre_time}
    return render(request, 'social_analysis/calculate.html', context)


def calculate_by_period(request, start, end):
    """
    他者分析の全ユーザー該当期間の要素別的中率の表示
    :param request: Request
    :param start: String(YYYY-MM-DD HH:MM:ss)
    :param end: String(YYYY-MM-DD HH:MM:ss)
    :return render: with Request request, Dictionary context
    """
    pre_time = datetime.datetime.now()  # 経過時間表示用
    race_list = analysis.get_race_by_period(start, end)
    count_factor_by_races(race_list)
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'analysis_start': start,
               'analysis_end': end,
               'analysis_race_number': len(race_list),
               'calculation_duration': datetime.datetime.now() - pre_time}
    return render(request, 'social_analysis/calculate.html', context)


def calculate_remaining(request):
    """
    未処理のレースに対して,的中率を計算する
    :param request: Request
    :return factor_counter: Dictionary
    """
    pre_time = datetime.datetime.now()  # 経過時間表示用
    reservation_race_list = []
    race_list = Race.objects.all()
    for race in race_list:
        if is_calculated_factor_aggregate(race) is False:
            reservation_race_list.append(race)
    count_factor_by_races(reservation_race_list)
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'analysis_race_number': len(reservation_race_list),
               'calculation_duration': datetime.datetime.now() - pre_time}
    return render(request, 'social_analysis/calculate.html', context)


def show_all_aggregate(request):
    """
    計算済みの要素別的中率を要素別に表示(全期間)
    :param request:
    :return:
    """
    pre_time = time.time()  # 経過時間表示用
    factor_list_all = list(Factor.objects.all())
    analysis_number = 0
    factor_counter = analysis.init_factor_counter()  # 結果を格納する辞書を初期化
    analysis_data_list = list(EntireFactorAggregate.objects.all())
    for analysis_data in analysis_data_list:
        factor_counter[analysis_data.factor]['use'] += analysis_data.use
        factor_counter[analysis_data.factor]['hit'] += analysis_data.hit
        analysis_number += analysis_data.use
    # 的中率を計算
    factor_counter = analysis.calculate_hit_percentage(factor_counter, factor_list_all)
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'factor_count': factor_counter,
               'analysis_number': analysis_number,
               'analysis_race_number': int(len(analysis_data_list) / len(factor_list_all)),
               'calculation_duration': time.time() - pre_time}
    return render(request, 'social_analysis/calculate.html', context)


def is_calculated_factor_aggregate(race, factor=None):
    """
    与えられたレースの全ユーザの使用率が計算済みか判定
    :param race: Object
    :return: boolean
    """
    if factor is None:
        analysis_data_list = list(EntireFactorAggregate.objects.filter(race_id=race.id))
        if len(analysis_data_list) == 0:
            return False
        else:
            return True
    else:
        analysis_data_list = list(EntireFactorAggregate.objects.filter(race_id=race.id, factor_id=factor.id))
        if len(analysis_data_list) == 0:
            return False
        else:
            return True


def save(factor_count, race):
    """
    全ユーザーの要素別使用回数,的中回数,的中率をレース毎にDBに保存
    :param factor_count: Dictionary
    :param race: String or Datetime
    :return:
    """
    for key, value in factor_count.items():
        if is_calculated_factor_aggregate(race, key):
            analysis_data_list = list(EntireFactorAggregate.objects.filter(factor_id=key.id, race_id=race.id))
            analysis_data = analysis_data_list[0]
        else:
            analysis_data = EntireFactorAggregate()
        if value['hit'] is not None and value['percentage'] is not None:
            analysis_data.hit = value['hit']
            analysis_data.percentage = value['percentage']
        analysis_data.use = value['use']
        analysis_data.factor_id = key.id
        analysis_data.race_id = race.id
        analysis_data.save()
    print(f'{datetime.datetime.now()}' + ' | ' + f'{len(factor_count)}' + '件のデータをEntireFactorAggregateに保存しました.')
    return


def count_factor_by_races(race_list):
    """
    与えられたRaceリストを指定しているweightの的中率等を計算し, レース毎にDBに保存
    :param race_list: List
    :return factor_counter: Dictionary
    """
    for race in race_list:
        weights = analysis.get_weight_by_race(race)
        if analysis.is_not_null_rank_in_data(race):
            factor_counter = analysis.count_factor(weights)
        else:
            factor_counter = analysis.count_factor_only_use(weights)
        save(factor_counter, race)
    return
