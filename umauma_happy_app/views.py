from django.shortcuts import render, get_object_or_404, get_list_or_404
from umauma_happy_app.models import *
from django.http import HttpResponse

factor_dict = {
    'jockey': '騎手',
    'distance_suitabililty': '距離適性',
    'past_achievement': '前走成績',
    'horse_order': '枠番',
    'leg_quality': '脚質',
    'paddock': 'パドック',
    'horse_weight': '馬体重',
    'handicap': '斤量',
    'odds': 'オッズ',
    'stable': '厩舎',
    'pedigree': '血統',
    'trainer': '調教師',
    # 'popularity': '人気'
}


def index(request):
    race_list = list(Race.objects.all())
    context = {'race_list': race_list}
    return render(request, 'umauma_happy_app/index.html', context)


def purchase(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    data_list = list(get_list_or_404(Data, race=race))
    context = {
        'race': race,
        'data_list': data_list,
        'factor_dict': factor_dict
    }
    return render(request, 'umauma_happy_app/purchase.html', context)


def purchase_do(request):
    data_id = request.POST['data']
    data = get_object_or_404(Data, pk=data_id)
    # ログイン機能未実装のため, とりあえずユーザは1固定
    user = get_object_or_404(User, pk=1)
    history = History(user=user, data=data)
    history.save()

    weight_list = []
    for key, value in factor_dict.items():
        factor = get_object_or_404(Factor, name=value)
        weight = Weight(history=history, factor=factor, value=request.POST[key])
        factor_weight_tuple = (factor.name, weight.value)
        weight_list.append(factor_weight_tuple)
        weight.save()

    context = {
        'data': data,
        'weight_list': weight_list
    }
    return render(request, 'umauma_happy_app/purchase_do.html', context)