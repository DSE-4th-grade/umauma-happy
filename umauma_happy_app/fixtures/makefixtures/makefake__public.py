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