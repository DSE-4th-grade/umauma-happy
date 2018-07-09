import json
import collections as cl
import datetime

def distance():
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    ys = []  # json書き込み用配列に追加
    value = [1000, 1200, 1400, 1600, 1800, 2000]
    for i in range(len(value)):
        date = datetime.datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")  # created_at & updated_at用
        fields = cl.OrderedDict()  # 格納するフィールドを定義
        fields["value"] = value[i]
        fields["created_at"] = date
        fields["updated_at"] = date
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.distance"  # 対象のmodelを設定
        data["pk"] = i+1
        data["fields"] = fields  # PrimaryKeyを設定
        ys.append(data)  # json書き込み用配列に追加
    fw = open('umauma_happy_app/fixtures/components/faker_distance.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)  # 中間fixtureファイルを出力


if __name__ == '__main__':
    distance()
