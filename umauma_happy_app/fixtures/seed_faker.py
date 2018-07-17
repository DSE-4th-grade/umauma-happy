import makefixtures  # makefakeファイルをimport
import json

if __name__ == '__main__':
    # seed_fakerではスクレイピングデータやユーザーデータなどのダミーデータのfixtureファイルを作成
    # Fakerライブラリを下記のクラスで使用するので、'pip3 install faker'を開発環境で実行する
    # ここでできたfixtureファイルをDBに反映させるには'python manage.py loaddata seed_faker'を実行する
    # PrimaryKeyを設定しているので、何度loaddataを実行しても重複は起こさない(要素数を変えた場合を除く)
    makefixtures.horse()  # 各modelのfixtureファイルを作成
    makefixtures.jockey()
    makefixtures.race()
    makefixtures.stable()
    makefixtures.user()

    component_data = []  # 各fixtureファイルのjsonを格納するためのリスト
    master_data = []  # 各fixtureファイルを結合したデータを格納するためのリスト
    src = ["umauma_happy_app/fixtures/components/faker_horse.json",
           "umauma_happy_app/fixtures/components/faker_jockey.json",
           "umauma_happy_app/fixtures/components/faker_race.json",
           "umauma_happy_app/fixtures/components/faker_stable.json",
           "umauma_happy_app/fixtures/components/faker_user.json"]  # 作成した各fixtureファイルのソース
    for i in range(len(src)):
        fr = open(src[i], 'r')
        component_data = json.load(fr)
        master_data.extend(component_data)  # 各fixtureデータを結合
    fw = open('umauma_happy_app/fixtures/seed_faker.json', 'w')
    json.dump(master_data, fw, indent=2, ensure_ascii=False)  # 結合したfixtureファイルを出力
