import json
import collections as cl
from datetime import timezone, datetime, timedelta

def distancesuitability():
    jst = timezone(timedelta(hours=+9), 'JST')
    ys = []
    value = ["スプリント", "マイル", "中距離", "中長距離", "長距離"]
    for i in range(len(value)):
        date = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        fields = cl.OrderedDict()
        fields["value"] = value[i]
        fields["created_at"] = date
        fields["updated_at"] = date
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.distancesuitability"
        data["pk"] = i+1
        data["fields"] = fields
        ys.append(data)
    fw = open('umauma_happy_app/fixtures/components/faker_distancesuitability.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    distancesuitability()
