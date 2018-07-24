from django.shortcuts import render, get_object_or_404, get_list_or_404
from umauma_happy_app.models import *
from django.http import HttpResponse
import itertools


# Create your views here.


def index(request):
    user_list = User.objects.all
    context = {'user_list': user_list}
    return render(request, 'self_analysis/index.html', context)


# 指定したユーザの的中購入履歴をリストで返す
def get_hit_history_by_user(user):
    history_list_all = list(History.objects.all())

    # 的中した購入履歴のみを抽出
    # ここでの的中判定ロジックは単純に3着以内とする
    hit_history_list = filter(lambda history: history.user == user and history.data.rank <= 3, history_list_all)

    return hit_history_list


# 指定したユーザの的中購入履歴に紐づくすべての重みリストを返す [ [(Weight, Weight), (Weight, Weight, Weight), ...] ]
def get_hit_wight_list_by_user(user):
    hit_history_list = get_hit_history_by_user(user)

    # それぞれの的中購入履歴に対応する重みリストを取り出す
    history_weight_list = []
    for history in hit_history_list:
        history_weight = tuple(get_list_or_404(Weight, history=history))
        history_weight_list.append(history_weight)

    return history_weight_list


# 指定ユーザの要素ごとの的中回数をリスト形式で返す [ (factor1, 9), (factor2, 7), ... ]
def get_hit_factor_rank_by_user(user):
    factor_list_all = list(Factor.objects.all())
    history_weight_list = get_hit_wight_list_by_user(user)

    hit_factor_rank = {}
    # 要素別的中ランキング(重みは用いない、的中回数のみ)の作成

    for factor in factor_list_all:
        hit_factor_rank[factor] = 0

    for history_weight in history_weight_list:
        for weight in history_weight:
            hit_factor_rank[weight.factor] += 1

    # itemsはタプル型オブジェクトを要素とするリストを返す
    hit_factor_rank = list(hit_factor_rank.items())
    hit_factor_rank.sort(key=lambda x: -x[1])
    return hit_factor_rank


# 指定ユーザの要素の組み合わせごとの的中回数を二次元配列で返す [ [5, <factor1,factor2>], [3, <factor6, factor8>], ...]
def get_hit_factor_combinations_by_user(user):
    combination_num = 2     # 組み合わせ要素数。まずは2つの要素の組み合わせ
    factor_list_all = list(Factor.objects.all())
    factor_combinations_all = itertools.combinations(factor_list_all, combination_num)
    history_weight_list = get_hit_wight_list_by_user(user)

    hit_factor_pattern_dic = {}

    for factor_combination in factor_combinations_all:
        hit_factor_pattern_dic[factor_combination] = 0

    for history_weight in history_weight_list:  # history_weight = 1つの的中購入履歴に関連する重みタプル
        history_factor = list(map(lambda weight: weight.factor, history_weight))
        # 1つの的中購入履歴に関して要素の組み合わせを求め,それがfactor_combinationと一致するかどうかを判定
        history_factor_combination_list = list(itertools.combinations(history_factor, combination_num))
        for history_factor_combination in history_factor_combination_list:
            # 順不同にする
            key = list(filter(lambda key: set(key) == set(history_factor_combination), hit_factor_pattern_dic.keys()))[0]
            hit_factor_pattern_dic[key] += 1

    # hit_factor内と同様にソートしてreturn
    hit_factor_pattern_list = [[k, v] for k, v in hit_factor_pattern_dic.items() if v > 0]   # 的中回数が1回以上のもののみ抽出
    hit_factor_pattern_list.sort(key=lambda x: -x[1])
    return hit_factor_pattern_list


def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    context = {'user': user,
               'hit_rank_list': get_hit_factor_rank_by_user(user),
               'hit_factor_pattern': get_hit_factor_combinations_by_user(user), }

    return render(request, 'self_analysis/detail.html', context)
