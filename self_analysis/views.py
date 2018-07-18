from django.shortcuts import render, get_object_or_404, get_list_or_404
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
    factor_list_all = list(Factor.objects.all())

    # 的中した購入履歴のみを抽出
    history_list = filter(lambda history: history.user == user and history.data.rank <= 3, history_list_all)

    # それぞれの的中購入履歴に対応する重みリストを取り出す
    # それぞれの的中購入履歴に関する要素の組み合わせパターンを抽出
    filtered_weight_list = []   # 的中購入履歴すべてに対する重みリスト ( [ [weight], [weight] ] )
    hit_pattern_list = []
    for history in history_list:
        filtered_weight = get_list_or_404(Weight, history=history)
        filtered_weight_list.extend(filtered_weight)
        pattern = []    # 1つの的中購入履歴に関する要素の組み合わせパターン ([騎手, 脚質])
        for weight in filtered_weight:
            pattern.extend(list(filter(lambda factor: factor.name == weight.factor.name, factor_list_all)))
        hit_pattern_list.append(pattern)    # 的中パターンをリスト化　([ [騎手, 脚質], [競馬場, 調教師], ・・・ ])

    #
    hit_factor_pattern_rank_list = []
    hit_rank_list = []

    # 要素別的中ランキング(重みは用いない、的中回数のみ)の作成
    for factor in factor_list_all:
        hit_factor_num = 0
        for w in filtered_weight_list:
            if w.factor == factor:
                hit_factor_num += 1
        hit_rank_list.append([hit_factor_num, factor])

    # 要素の組み合わせごとの的中ランキング(重みは用いない、 的中回数のみ)の作成
    for factor in factor_list_all:
        factor_list_all.remove(factor)
        for pair in factor_list_all:
            factor_set = set(list([factor, pair]))
            pattern_matched_num = 0
            for pattern in hit_pattern_list:
                if len(set(set(pattern) & factor_set)) == 2:
                    pattern_matched_num += 1
            if pattern_matched_num > 0:
                hit_factor_pattern_list = [pattern_matched_num, factor_set]
                hit_factor_pattern_rank_list.append(hit_factor_pattern_list)

    # 的中回数が多い順にソートする
    hit_rank_list.sort(key=lambda x: -x[0])
    hit_factor_pattern_rank_list.sort(key=lambda x: -x[0])


    context = {'user': user,
               'history_list': history_list_all,
               'weight_list': filtered_weight_list,
               'hit_rank_list': hit_rank_list,
               'hit_factor_pattern': hit_factor_pattern_rank_list,}


    return render(request, 'self_analysis/detail.html', context)
