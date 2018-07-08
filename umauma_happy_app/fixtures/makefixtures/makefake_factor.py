import json
import collections as cl
from datetime import timezone, datetime, timedelta

def factor():
    jst = timezone(timedelta(hours=+9), 'JST')
    ys = []
    value = ["騎手", "距離適性", "前走成績", "枠番", "脚質", "パドック", "馬体重", "斤量", "オッズ", "厩舎", "血統", "競馬場", "調教師"]
    for i in range(len(value)):
        date = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        fields = cl.OrderedDict()
        fields["name"] = value[i]
        fields["created_at"] = date
        fields["updated_at"] = date
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.factor"
        data["pk"] = i+1
        data["fields"] = fields
        ys.append(data)
    fw = open('umauma_happy_app/fixtures/components/faker_factor.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    factor()
