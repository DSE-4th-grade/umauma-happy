import json
import collections as cl
from faker import Factory
import random
import datetime


def race():
    fake = Factory.create('ja_JP')
    ys = []  # json書き込み用配列に追加
    for i in range(10):  # 10競馬場分作成
        datetime_race = fake.date_time_this_decade(before_now=True, after_now=True, tzinfo=None)  # レースのdeparture_time
        date_race = fake.date_time_this_decade(before_now=True, after_now=True, tzinfo=None).strftime("%Y-%m-%d")  # レースのdate
        datetime_now = fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")  # created_at&updated_at用
        arena = fake.town() + "競馬場"
        for j in range(12):  # 同じ競馬場で同日に1~12レースを30分刻みで作成
            datetime_race_now = (datetime_race + datetime.timedelta(minutes=j * 30)).strftime("%Y-%m-%d %H:%M:%S")
            fields = cl.OrderedDict()  # 格納するフィールドを定義
            fields["number"] = j + 1
            fields["name"] = fake.last_name() + "記念"
            fields["arena"] = arena
            fields["departure_time"] = datetime_race_now
            fields["head_count"] = random.randint(10, 16)
            fields["course_id"] = random.randint(1, 3)
            fields["distance_id"] = random.randint(1, 6)
            fields["ground_condition_id"] = random.randint(1, 4)
            fields["date"] = date_race
            fields["created_at"] = datetime_now
            fields["updated_at"] = datetime_now
            data = cl.OrderedDict()
            data["model"] = "umauma_happy_app.race"  # 対象のmodelを設定
            data["fields"] = fields  # 格納するフィールドを設定
            ys.append(data)  # json書き込み用配列に追加
    fw = open('umauma_happy_app/fixtures/components/faker_race.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    race()
