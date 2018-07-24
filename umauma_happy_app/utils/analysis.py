from collections import OrderedDict

def judge_hit_or_not(history):
    """
    historyレコードが当たっているか判定する
    :param history: History object
    :return:boolean
    """
    if history.data.rank < 3:
        return True
    else:
        return False


def calculate_hit_percentage(factor_counter, factor_list):
    """
    与えられた要素辞書に格納されている使用回数と的中回数を使って的中率を計算する
    :param factor_counter: Dictionary
    :param factor_list: List
    :return:
    """
    for factor in factor_list:
        if factor_counter[factor]['use'] == 0:
            factor_counter[factor]['percentage'] = '{:.3f}'.format(0)
        else:
            factor_counter[factor]['percentage'] \
                = '{:0=6.3f}'.format((factor_counter[factor]['hit'] / factor_counter[factor]['use']) * 100)
    # 結果を的中率, 同点なら使用回数順になるように並び替え
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: x[1]['use'], reverse=True))
    factor_counter = OrderedDict(sorted(factor_counter.items(), key=lambda x: x[1]['percentage'], reverse=True))
    return factor_counter