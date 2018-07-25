class FakeNumber:
    head_count = 11  # 1レースに出場する馬の数
    total_horse = 200  # fakerで作成する馬の数
    total_jockey = 20  # fakerで作成する騎手の数
    total_race_arena = 10  # fakerで作成するレースの競馬場の数
    total_race = 12  # fakerで競馬場毎に作成するレースの数
    total_stable = 20  # fakerで作成する厩舎の数
    total_trainer = 20  # fakerで作成する厩舎の数
    total_user = 20  # fakerで作成するユーザーの数

    total_races = total_race_arena * total_race  # fakerで最終的に作成されるレースの数

    purchase_factor_num_l = 1  # 購入に対して考慮した最小のファクター数
    purchase_factor_num_g = 5  # 購入に対して考慮した最大ファクター数
    purchase_probability_0 = 0.4  # userがレースに対して0枚馬券を購入する確率
    purchase_probability_1 = 0.2  # userがレースに対して1枚馬券を購入する確率
    purchase_probability_2 = 0.2  # userがレースに対して2枚馬券を購入する確率
    purchase_probability_3 = 0.2  # userがレースに対して3枚馬券を購入する確率

    # userがレースに対して1枚以下馬券を購入する確率
    purchase_probability_1_encode = purchase_probability_0 + purchase_probability_1
    # userがレースに対して2枚以下馬券を購入する確率
    purchase_probability_2_encode = purchase_probability_0 + purchase_probability_1 + purchase_probability_2

class StaticValue:
    course_value = ["芝", "ダート", "障害"]
    distance_suitability_value = ["スプリント", "マイル", "中距離", "中長距離", "長距離"]
    factor_value = ["騎手", "距離適性", "前走成績", "枠番", "脚質", "パドック", "馬体重", "斤量", "オッズ", "厩舎", "血統", "競馬場", "調教師"]
    ground_condition_value = ["良", "稍重", "重", "不良"]
    leg_quality_value = ["逃げ", "先行", "差し", "追い込み"]

class RandomValue:
    distance_sample = [1000, 1200, 1400, 1600, 1800, 2000]  # 距離のサンプル
    odds_sample = [2.0, 3.9, 4.2, 6.3, 7.3, 14.1, 23.6, 25.2, 61.1, 70.1, 75.2, 156.9, 167.3, 186.1,
                   200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0]  # オッズのサンプル
