from django.shortcuts import render, get_object_or_404, get_list_or_404
from umauma_happy_app.models import *
from django.http import HttpResponse
import itertools
from umauma_happy_app.utils import analysis

# Create your views here.


def index(request):
    user_list = User.objects.all
    context = {'user_list': user_list}
    return render(request, 'self_analysis/index.html', context)


# 指定したユーザの的中購入履歴をリストで返す
def get_hit_history_by_user(user):
    history_list_all = list(History.objects.all())

    # 的中した購入履歴のみを抽出
    hit_history_list = filter(lambda history: history.user == user and analysis.is_hit(history)==True, history_list_all)

    return hit_history_list


# 指定したユーザの全ての購入履歴に紐づく重みリストを返す [Weight, Weight, Weight, ...]
def get_weight_list_by_user(user):
    history_list_all = list(History.objects.all())
    user_history_list = filter(lambda history: history.user == user, history_list_all)
    user_weight_list = []
    for history in user_history_list:
        history_weight = get_list_or_404(Weight, history=history)
        user_weight_list.extend(history_weight)
    return user_weight_list


# 指定したユーザの的中購入履歴に紐づくすべての重みリストを返す
# それぞれの的中購入履歴をタプルでまとめる [ [(Weight, Weight), (Weight, Weight, Weight), ...] ]
def get_hit_wight_list_by_user(user):
    hit_history_list = get_hit_history_by_user(user)

    # それぞれの的中購入履歴に対応する重みリストを取り出す
    history_weight_list = []
    for history in hit_history_list:
        history_weight = tuple(get_list_or_404(Weight, history=history))
        history_weight_list.append(history_weight)

    return history_weight_list


# 指定ユーザの要素の組み合わせごと
def get_hit_factor_combinations_by_user(user):
    combination_num = 2 # 組み合わせ数
    hit_history_weight_list = get_hit_wight_list_by_user(user)

    # 購入履歴ごとにタプルで区切られたすべての重みリスト [(Weight, Weight), (Weight, Weight, Weight),...]
    history_list_all = list(History.objects.all())
    user_history_list = filter(lambda history: history.user == user, history_list_all)
    user_weight_list = []
    # 購入履歴ごとに分けられていない重みリストを作成(factor_combination_counterの引数用)
    for history in user_history_list:
        history_weight = get_list_or_404(Weight, history=history)
        user_weight_list.append(history_weight)

    factor_combination_counter = analysis.init_factor_combination_counter() # 初期化

    # 要素の組み合わせごとに使用回数を記録する
    for user_weight in user_weight_list:
        history_factor = list(map(lambda weight: weight.factor, user_weight))
        com_list = list(itertools.combinations(history_factor, combination_num))
        for com in com_list:
            # 順不同にする
            key = list(filter(lambda key: set(key) == set(com), factor_combination_counter.keys()))[0]
            factor_combination_counter[key]['use'] += 1

    for history_weight in hit_history_weight_list:  # history_weight = 1つの的中購入履歴に関連する重みタプル
        hit_history_factor = list(map(lambda weight: weight.factor, history_weight))
        # 1つの的中購入履歴に関して要素の組み合わせを求め、factor_combination_counterをインクリメントしていく
        history_factor_combination_list = list(itertools.combinations(hit_history_factor, combination_num))
        for history_factor_combination in history_factor_combination_list:
            # 順不同にする
            key = list(filter(lambda key: set(key) == set(history_factor_combination), factor_combination_counter.keys()))[0]
            factor_combination_counter[key]['hit'] += 1

    # 的中率を計算する
    factor_list_all = list(Factor.objects.all())
    factor_combinations_all = itertools.combinations(factor_list_all, combination_num)
    factor_combination_counter = analysis.calculate_hit_percentage(factor_combination_counter, factor_combinations_all)

    return factor_combination_counter


def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    context = {'user': user,
               'factor_combination_counter': get_hit_factor_combinations_by_user(user),
               'factor_counter': analysis.count_factor(get_weight_list_by_user(user)),
               }

    return render(request, 'self_analysis/detail.html', context)
