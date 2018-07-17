import collections as cl
import json

from faker import Factory
from .makefake__public import FakeNumber  # 固定数部分をimport


def jockey():
    fake = Factory.create('ja_JP')
    ys = []  # json書き込み用配列に追加
    for i in range(FakeNumber.total_jockey):
        date = fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")  # created_at & updated_at用
        link_array = fake.profile(fields='website')  # fakerからリンクを辞書として取得
        link = link_array["website"]  # 辞書からリストへ
        fields = cl.OrderedDict()  # 格納するフィールドを定義
        fields["name"] = fake.name()
        fields["link"] = link[0]  # リストから最初のリンクだけを取得
        fields["created_at"] = date
        fields["updated_at"] = date
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.jockey"  # 対象のmodelを設定
        data["pk"] = i + 1  # PrimaryKeyを設定
        data["fields"] = fields  # 格納するフィールドを設定
        ys.append(data)  # json書き込み用配列に追加
    fw = open('umauma_happy_app/fixtures/components/faker_jockey.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)  # 中間fixtureファイルを出力


if __name__ == '__main__':
    jockey()
