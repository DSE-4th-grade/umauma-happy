from django.shortcuts import render, get_object_or_404, get_list_or_404
from umauma_happy_app.models import *
from umauma_happy_app.utils import analysis
from collections import OrderedDict
import datetime

class SampleValues:
    analysis_number_samples = [100, 200, 500, 1000, 2000, 5000]


def index(request):
    """
    他者分析の分析内容の選択画面
    :param request:
    :return:
    """
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'weight_amount': len(get_weight())}
    return render(request, 'social_analysis/index.html', context)


def calculate(request, analysis_number=None):
    """
    他者分析の全ユーザー要素別的中率の表示
    :param request: Request
    :param analysis_number: int
    :return render: with Request request, Dictionary context
    """
    weights = get_weight(analysis_number)
    factor_count = analysis.count_factor(weights)
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'factor_count': factor_count,
               'analysis_number': analysis_number}
    return render(request, 'social_analysis/calculate.html', context)


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
