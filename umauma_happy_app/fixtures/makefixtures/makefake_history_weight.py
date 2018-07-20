import json
import collections as cl
from faker import Factory
from .makefake__public import FakeNumber  # 固定数部分をimport
import random

def history_weight():
    fake = Factory.create('ja_JP')
    ys = []  # json書き込み用配列に追加
    pk_count_h = 1  # historyテーブルのPrimaryKey
    pk_count_w = 1  # weightテーブルのPrimaryKey
    for i in range(FakeNumber.total_races):
        for j in range(FakeNumber.total_user):
            rand = random.random()
            if FakeNumber.purchase_probability_0 > rand:  # 各レースに対して,各ユーザーが何枚馬券を購入するか確率的に決める
                purchase = 0
            elif FakeNumber.purchase_probability_1_encode > rand:
                purchase = 1
            elif FakeNumber.purchase_probability_2_encode > rand:
                purchase = 2
            else:
                purchase = 3
            shuffled_int1 = list(range(1, FakeNumber.head_count + 1))  # data選択用にintリストを作成
            random.shuffle(shuffled_int1)  # data選択用にintリストをシャッフル
            for k in range(purchase):
                date = fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")  # created_at & updated_at用
                fields = cl.OrderedDict()  # 格納するフィールドを定義
                fields["user_id"] = j + 1
                fields["data_id"] = i * FakeNumber.head_count + shuffled_int1[k]
                fields["created_at"] = date
                fields["updated_at"] = date
                data = cl.OrderedDict()
                data["model"] = "umauma_happy_app.history"  # 対象のmodelを設定
                data["pk"] = pk_count_h  # PrimaryKeyを設定
                data["fields"] = fields  # 格納するフィールドを設定
                ys.append(data)  # json書き込み用配列に追加

                shuffled_int2 = list(range(1, 13 + 1))  # 要素選択用にintリストを作成
                random.shuffle(shuffled_int2)  # 要素選択用にintリストをシャッフル
                # 各購入馬に対してファクター項目数をランダムで決める
                random_factor_num = random.randint(FakeNumber.purchase_factor_num_l, FakeNumber.purchase_factor_num_g)
                for l in range(random_factor_num):
                    fields = cl.OrderedDict()  # 格納するフィールドを定義
                    fields["history_id"] = pk_count_h
                    fields["factor_id"] = shuffled_int2[l]
                    fields["value"] = 1 / random_factor_num
                    fields["created_at"] = date
                    fields["updated_at"] = date
                    data = cl.OrderedDict()
                    data["model"] = "umauma_happy_app.weight"  # 対象のmodelを設定
                    data["pk"] = pk_count_w  # PrimaryKeyを設定
                    data["fields"] = fields  # 格納するフィールドを設定
                    ys.append(data)  # json書き込み用配列に追加
                    pk_count_w += 1
                pk_count_h += 1

    fw = open('umauma_happy_app/fixtures/components/faker_history_weight.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)  # 中間fixtureファイルを出力


if __name__ == '__main__':
    history_weight()
