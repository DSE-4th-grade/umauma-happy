import makefixtures  # makefakeファイルをimport
import json

if __name__ == '__main__':
    # seed_fakerではスクレイピングデータやユーザーデータなどのダミーデータのfixtureファイルを作成
    # ここでできたfixtureファイルをDBに反映させるには'python manage.py loaddata seed_faker'を実行する
    # PrimaryKeyを設定していないので、loaddataを実行した際に重複が生じることがある
    # 重複が生じた場合、Uniqueな要素がある場合、Errorになる可能性がある
    makefixtures.race()  # 各# modelのfixtureファイルを作成
    makefixtures.user()

    component_data = []  # 各fixtureファイルのjsonを格納するためのリスト
    master_data = []  # 各fixtureファイルを結合したデータを格納するためのリスト
    src = ["umauma_happy_app/fixtures/components/faker_user.json",
           "umauma_happy_app/fixtures/components/faker_race.json"]  # 作成した各fixtureファイルのソース
    for i in range(len(src)):
        fr = open(src[i], 'r')
        component_data = json.load(fr)
        master_data.extend(component_data)  # 各fixtureデータを結合
    fw = open('umauma_happy_app/fixtures/seed_faker.json', 'w')
    json.dump(master_data, fw, indent=2, ensure_ascii=False)  # 結合したfixtureファイルを出力
