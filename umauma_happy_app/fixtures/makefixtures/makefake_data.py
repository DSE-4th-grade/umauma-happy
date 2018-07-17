import collections as cl
import json
import random

from faker import Factory
from .makefake__public import FakeNumber  # 固定数部分をimport

def data():
    fake = Factory.create('ja_JP')
    ys = []  # json書き込み用配列に追加
    today_horses = []  # その日行われるレース分の馬リスト
    horse_count = 0  # today_horsesリストのid
    all_horse = range(1, FakeNumber.total_horse, 1)  # 登録されている全馬のidのリスト
    all_jockey = range(1, FakeNumber.total_jockey, 1)  # 登録されている全ジョッキーのidのリスト
    odds_sample = [2.0, 3.9, 4.2, 6.3, 7.3, 14.1, 23.6, 25.2, 61.1, 70.1, 75.2, 156.9, 167.3, 186.1,
                   200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0]  # オッズのサンプル
    for i in range(FakeNumber.total_races):
        date = fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")  # created_at & updated_at用
        thistime_jockeys = random.sample(all_jockey, FakeNumber.head_count)  # レース毎のジョッキーリストを作成
        shuffled_int1 = list(range(0, FakeNumber.head_count))  # オッズ選択用にintリストを作成
        random.shuffle(shuffled_int1)  # オッズ選択用にintリストをシャッフル
        shuffled_int2 = list(range(0, FakeNumber.head_count))  # ランク選択用にintリストを作成
        random.shuffle(shuffled_int2)  # ランク選択用にintリストをシャッフル
        if i % FakeNumber.total_race == 0:  # その日の全レースが終わった時に馬リストをリセット
            today_horses = random.sample(all_horse, FakeNumber.head_count * FakeNumber.total_race)  # その日行われるレース分の馬リストを作成
            horse_count = 0  # today_horsesリストのidを初期化
        for j in range(FakeNumber.head_count):
            fields = cl.OrderedDict()  # 格納するフィールドを定義
            fields["horse_id"] = today_horses[horse_count]  # 上で作成した馬リストから重複が起きない様に選択
            fields["race_id"] = i + 1
            fields["jockey_id"] = thistime_jockeys[j]  # 重複のないジョッキーリストから今回のジョッキーを選択
            fields["sex"] = random.randint(0, 1)
            fields["handicap"] = random.randint(50, 60)
            fields["stable_id"] = random.randint(1, FakeNumber.total_stable)
            fields["trainer_id"] = random.randint(1, FakeNumber.total_trainer)
            fields["distance_suitability"] = random.randint(1, 5)
            fields["horse_order"] = j + 1
            fields["leg_quality_id"] = random.randint(1, 4)
            fields["odds"] = odds_sample[shuffled_int1[j]]  # odd_sampleからランダムの要素を選択
            fields["popularity"] = shuffled_int1[j] + 1  # odds_sampleで選んだid
            fields["rank"] = shuffled_int2[j] + 1  # 上で作成した重複のないランダムなinteger
            fields["created_at"] = date
            fields["updated_at"] = date
            data_ = cl.OrderedDict()
            data_["model"] = "umauma_happy_app.data"  # 対象のmodelを設定
            data_["pk"] = i * FakeNumber.head_count + j + 1  # PrimaryKeyを設定
            data_["fields"] = fields  # 格納するフィールドを設定
            ys.append(data_)  # json書き込み用配列に追加
            horse_count = horse_count + 1  # today_horsesリストのidを進める
    fw = open('umauma_happy_app/fixtures/components/faker_data.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)  # 中間fixtureファイルを出力


if __name__ == '__main__':
    data()
