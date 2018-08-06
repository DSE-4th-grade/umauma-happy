import json
import collections as cl
from faker import Factory
import random
import datetime
from .makefake__public import FakeNumber  # 固定数部分をimport
from .makefake__public import StaticValue
from .makefake__public import RandomValue

def race():
    fake = Factory.create('ja_JP')
    ys = []  # json書き込み用配列に追加
    datetime_now = fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")  # created_at & updated_at用
    for i in range(FakeNumber.total_past_race_arena):
        datetime_race = fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)  # レースのdeparture_time
        arena = fake.town() + "競馬場"
        for j in range(FakeNumber.total_race):  # 同じ競馬場で同日に12レースを30分刻みで作成
            datetime_race_now = (datetime_race + datetime.timedelta(minutes=j * 30)).strftime("%Y-%m-%d %H:%M:%S")
            fields = cl.OrderedDict()  # 格納するフィールドを定義
            fields["number"] = j + 1
            fields["name"] = fake.last_name() + "記念"
            fields["arena"] = arena
            fields["departure_time"] = datetime_race_now
            fields["head_count"] = FakeNumber.head_count  # dataフィールドを作成する際に使用するため固定
            fields["course_id"] = random.randint(1, len(StaticValue.course_value))  # 芝,ダート,障害のどれかを選択
            fields["distance"] = random.choice(RandomValue.distance_sample)  # 距離を選択(int)
            fields["ground_condition_id"] = random.randint(1, len(StaticValue.ground_condition_value))  # 馬場状態を選択
            fields["created_at"] = datetime_now
            fields["updated_at"] = datetime_now
            data = cl.OrderedDict()
            data["model"] = "umauma_happy_app.race"  # 対象のmodelを設定
            data["pk"] = i * FakeNumber.total_race + j + 1  # PrimaryKeyを設定
            data["fields"] = fields  # 格納するフィールドを設定
            ys.append(data)  # json書き込み用配列に追加
    for i in range(FakeNumber.total_future_race_arena):
        datetime_race = fake.date_time_this_decade(before_now=False, after_now=True, tzinfo=None)  # レースのdeparture_time
        arena = fake.town() + "競馬場"
        for j in range(FakeNumber.total_race):  # 同じ競馬場で同日に12レースを30分刻みで作成
            datetime_race_now = (datetime_race + datetime.timedelta(minutes=j * 30)).strftime("%Y-%m-%d %H:%M:%S")
            fields = cl.OrderedDict()  # 格納するフィールドを定義
            fields["number"] = j + 1
            fields["name"] = fake.last_name() + "記念"
            fields["arena"] = arena
            fields["departure_time"] = datetime_race_now
            fields["head_count"] = FakeNumber.head_count  # dataフィールドを作成する際に使用するため固定
            fields["course_id"] = random.randint(1, len(StaticValue.course_value))  # 芝,ダート,障害のどれかを選択
            fields["distance"] = random.choice(RandomValue.distance_sample)  # 距離を選択(int)
            fields["ground_condition_id"] = random.randint(1, len(StaticValue.ground_condition_value))  # 馬場状態を選択
            fields["created_at"] = datetime_now
            fields["updated_at"] = datetime_now
            data = cl.OrderedDict()
            data["model"] = "umauma_happy_app.race"  # 対象のmodelを設定
            data["pk"] = FakeNumber.total_past_races + (i * FakeNumber.total_race) + j + 1  # PrimaryKeyを設定
            data["fields"] = fields  # 格納するフィールドを設定
            ys.append(data)  # json書き込み用配列に追加
    fw = open('umauma_happy_app/fixtures/components/faker_race.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)  # 中間fixtureファイルを出力


if __name__ == '__main__':
    race()
