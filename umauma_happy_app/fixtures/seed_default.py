import makefixtures
import json

if __name__ == '__main__':
    # seed_defaultでは変更・追加が少ないtableのfixtureファイルを作成
    # 下記のクラスでは追加ライブラリは使用していない
    # ここでできたfixtureファイルをDBに反映させるには'python manage.py loaddata seed_default'を実行する
    # PrimaryKeyを設定しているので、何度loaddataを実行しても重複は起こさない(要素数を変えた場合を除く)
    makefixtures.cource()  # 各modelのfixtureファイルを作成
    makefixtures.distance()
    makefixtures.distancesuitability()
    makefixtures.factor()
    makefixtures.groundcondition()
    makefixtures.legquality()

    component_data = []  # 各fixtureファイルのjsonを格納するためのリスト
    master_data = []  # 各fixtureファイルを結合したデータを格納するためのリスト
    src = ["umauma_happy_app/fixtures/components/faker_course.json",
           "umauma_happy_app/fixtures/components/faker_distance.json",
           "umauma_happy_app/fixtures/components/faker_distancesuitability.json",
           "umauma_happy_app/fixtures/components/faker_factor.json",
           "umauma_happy_app/fixtures/components/faker_groundcondition.json",
           "umauma_happy_app/fixtures/components/faker_legquality.json"]  # 作成した各fixtureファイルのソース
    for i in range(len(src)):
        fr = open(src[i], 'r')
        component_data = json.load(fr)
        master_data.extend(component_data)  # 各fixtureデータを結合
    fw = open('umauma_happy_app/fixtures/seed_default.json', 'w')
    json.dump(master_data, fw, indent=2, ensure_ascii=False)  # 結合したfixtureファイルを出力
