from django.shortcuts import render, get_object_or_404, get_list_or_404
from umauma_happy_app.models import *
from collections import OrderedDict
import datetime


def index(request, analysis_number=None):
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
    if number is not None:
        all_weight = list(Weight.objects.all()[:number])
    else:
        all_weight = list(Weight.objects.all())
    return all_weight


def count_factor(weight_list):
    factor_list_all = list(Factor.objects.all())
    factor_counter = {}
    pretime = datetime.datetime.now()
    for factor in factor_list_all:
        factor_counter[factor] = {}
        factor_counter[factor]['use'] = 0
        factor_counter[factor]['hit'] = 0
    print('{0} | {1}件処理します.[開始]'.format(datetime.datetime.now(), len(weight_list)))
    for weight in weight_list:
        for factor in factor_list_all:
            if weight.factor == factor:
                factor_counter[factor]['use'] += 1
                if judge_hit_or_not(weight):
                    factor_counter[factor]['hit'] += 1
                continue
        if weight.id % 100 == 0:
            print('{0} | {1}件処理しました.'.format(datetime.datetime.now(), weight.id))
    print('{0} | {1}件処理しました.処理時間：{2}[完了]'.format(datetime.datetime.now(), len(weight_list), datetime.datetime.now() - pretime))
    for factor in factor_list_all:
        if factor_counter[factor]['use'] == 0:
            factor_counter[factor]['percentage'] = '{:.3f}'.format(0)
        else:
            factor_counter[factor]['percentage'] = '{:0=6.3f}'.format((factor_counter[factor]['hit'] / factor_counter[factor]['use']) * 100)
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: x[1]['use'], reverse=True))
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: x[1]['percentage'], reverse=True))
    return factor_counter


# 与えられたweightが当たっているか判定
def judge_hit_or_not(weight):
    if weight.history.data.rank < 3:
        return True
    else:
        return False