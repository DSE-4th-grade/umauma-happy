from django.shortcuts import render, get_object_or_404
from umauma_happy_app.models import *
from django.http import HttpResponse

# Create your views here.


def index(request):
    user_list = User.objects.all
    context = {'user_list': user_list}
    return render(request, 'self_analysis/index.html', context)


def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    history_list_all = list(History.objects.all())
    history_list = filter(lambda history: history.user == user and history.data.rank <= 3, history_list_all)

    # それぞれの購入履歴に対応する重みリストを取り出す
    filtered_weight_list = []
    for history in history_list:
        weight_list = list(Weight.objects.filter(history=history))
        filtered_weight_list.extend(weight_list)

    # 重複を削除する
#    list(set(filtered_weight_list))

    context = {'user': user,
               'history_list': history_list_all,
               'weight_list': filtered_weight_list}

    return render(request, 'self_analysis/detail.html', context)
