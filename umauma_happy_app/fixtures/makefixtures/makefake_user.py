import json
import collections as cl
from faker import Factory

def user():
    fake = Factory.create('ja_JP')
    ys = []  # json書き込み用配列に追加
    for i in range(4):
        date = fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")
        fields = cl.OrderedDict()  # 格納するフィールドを定義
        fields["system_id"] = fake.user_name()
        fields["name"] = fake.name()
        fields["created_at"] = date
        fields["updated_at"] = date
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.user"  # 対象のmodelを設定
        data["fields"] = fields  # 格納するフィールドを設定
        ys.append(data)  # json書き込み用配列に追加
    fw = open('umauma_happy_app/fixtures/components/faker_user.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user()
