import json
import collections as cl
from datetime import timezone, datetime, timedelta

def cource():
    jst = timezone(timedelta(hours=+9), 'JST')
    ys = []  # json書き込み用配列
    value = ["芝", "ダート", "障害"]
    for i in range(len(value)):
        date = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        fields = cl.OrderedDict()  # 格納するフィールドを定義
        fields["value"] = value[i]
        fields["created_at"] = date
        fields["updated_at"] = date
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.course"  # 対象のmodelを設定
        data["pk"] = i+1  # PrimaryKeyを設定
        data["fields"] = fields  # 格納するフィールドを設定
        ys.append(data)  # json書き込み用配列に追加
    fw = open('umauma_happy_app/fixtures/components/faker_course.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    cource()
