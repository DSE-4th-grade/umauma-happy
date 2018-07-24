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
        weights = get_weight(None)
        analysis_number = len(weights)
    elif analysis_number is None:
        weights = get_weight(DEFAULT_ANALYSIS_NUMBER)
        analysis_number = DEFAULT_ANALYSIS_NUMBER
    else:
        weights = get_weight(analysis_number)
    factor_count = analysis.count_factor(weights)
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
