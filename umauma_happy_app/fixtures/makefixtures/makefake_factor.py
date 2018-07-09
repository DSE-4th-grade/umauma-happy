import json
import collections as cl
import datetime

def factor():
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    ys = []  # json書き込み用配列に追加
    value = ["騎手", "距離適性", "前走成績", "枠番", "脚質", "パドック", "馬体重", "斤量", "オッズ", "厩舎", "血統", "競馬場", "調教師"]
    for i in range(len(value)):
        date = datetime.datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")  # created_at & updated_at用
        fields = cl.OrderedDict()  # 格納するフィールドを定義
        fields["name"] = value[i]
        fields["created_at"] = date
        fields["updated_at"] = date
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.factor"  # 対象のmodelを設定
        data["pk"] = i+1  # PrimaryKeyを設定
        data["fields"] = fields  # 格納するフィールドを設定
        ys.append(data)  # json書き込み用配列に追加
    fw = open('umauma_happy_app/fixtures/components/faker_factor.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)  # 中間fixtureファイルを出力


if __name__ == '__main__':
    factor()
