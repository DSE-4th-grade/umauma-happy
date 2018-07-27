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
    pre_time = datetime.datetime.now()  # 経過時間表示用
    weights = analysis.get_weight(analysis_number)
    factor_count = analysis.count_factor(weights)
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'factor_count': factor_count,
               'analysis_number': analysis_number,
               'calculation_duration': datetime.datetime.now() - pre_time}
    return render(request, 'social_analysis/calculate.html', context)


def calculate_by_time(request, start, end):
    """
    他者分析の全ユーザー該当期間の要素別的中率の表示
    :param request: Request
    :param start: String(YYYY-MM-DD HH:MM:ss)
    :param end: String(YYYY-MM-DD HH:MM:ss)
    :return render: with Request request, Dictionary context
    """
    pre_time = datetime.datetime.now()  # 経過時間表示用
    weights = analysis.get_weight_by_time(start, end)
    factor_count = analysis.count_factor(weights)
    context = {'analysis_number_samples': SampleValues.analysis_number_samples,
               'factor_count': factor_count,
               'analysis_start': start,
               'analysis_end': end,
               'analysis_number': len(weights),
               'calculation_duration': datetime.datetime.now() - pre_time}
    return render(request, 'social_analysis/calculate.html', context)
