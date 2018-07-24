from django.shortcuts import render, get_object_or_404, get_list_or_404
from umauma_happy_app.models import *
from umauma_happy_app.utils import analysis
from collections import OrderedDict
import datetime


def index(request, analysis_number=None):
    """
    他者分析の全ユーザー要素別的中率の表示
    :param request: Request
    :param analysis_number: int
    :return render: with Request request, Dictionary context
    """
    DEFAULT_ANALYSIS_NUMBER = 100
    if analysis_number == 0:
        analysis_number = None
    elif analysis_number is None:
        analysis_number = DEFAULT_ANALYSIS_NUMBER
    weights = get_weight(analysis_number)
    factor_count = count_factor(weights)
    context = {'factor_count': factor_count,
               'analysis_number': analysis_number}
    return render(request, 'social_analysis/index.html', context)


def get_weight(number=None):
    """
    指定された数だけweightテーブルからデータを返す. 指定しない場合は全件取得.
    :param number: int
    :return all_weight: List
    """
    if number is not None:
        all_weight = list(Weight.objects.all()[:number])
    else:
        all_weight = list(Weight.objects.all())
    return all_weight

def count_factor(weight_list):
    """
    与えられたweightリストに対して,要素の使用回数,的中回数,的中率を辞書で返す
    :param weight_list: List
    :return factor_counter: Dictionary
    """
    factor_list_all = list(Factor.objects.all())
    pre_time = datetime.datetime.now()  # 経過時間表示用
    analysis_module = analysis  # 計算モジュールをインポート(計算高速化用)
    # 結果を格納する辞書を初期化
    factor_counter = {}
    for factor in factor_list_all:
        factor_counter[factor] = {}
        factor_counter[factor]['use'] = 0
        factor_counter[factor]['hit'] = 0
    # 要素別使用回数と的中回数を計算
    print('{0} | {1}件処理します.[開始]'.format(datetime.datetime.now(), len(weight_list)))
    for weight in weight_list:
        factor_counter[weight.factor]['use'] += 1
        if analysis_module.judge_hit_or_not(weight.history):
            factor_counter[weight.factor]['hit'] += 1
        # if weight.id % 100 == 0:
            # print('{0} | {1}件処理しました.'.format(datetime.datetime.now(), weight.id))
    print('{0} | {1}件処理しました.処理時間：{2}[完了]'
          .format(datetime.datetime.now(), len(weight_list), datetime.datetime.now() - pre_time))
    # 的中率を計算
    factor_counter = analysis_module.calculate_hit_percentage(factor_counter, factor_list_all)
    return factor_counter
