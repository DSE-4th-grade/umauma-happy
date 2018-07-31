from umauma_happy_app.models import *
from .scraping_view import list1, data_sex, data_handicap, data_odds, data_popularity, data_past_achievement,   \
     race_number,race_date, race_name, race_arena, race_head_count, groundcondition_value, course_value, \
    distance_value, jockey_name, jockey_link, stable_name, trainer_link, horse_name, horse_birth, horse_link


def save_horse_data(horse_name, horse_birth, horse_link):
    save_num = 0
    for i in range(len(horse_link)):
        if len(Horse.objects.filter(link=horse_link[i])) == 0:
            h = Horse(name=horse_name[i], birth_year=horse_birth[i][:4], link=horse_link[i])
            h.save()
            save_num += 1
    return save_num


def save_jockey_data(jockey_name, jockey_link):
    save_num = 0
    for i in range(len(jockey_link)):
        if len(Jockey.objects.filter(link=jockey_link[i])) == 0:
            j = Jockey(name=jockey_name[i], link=jockey_link[i])
            j.save()
            save_num += 1
    return save_num

def save_trainer_data(trainer_name, trainer_link):
    # trainerモデルにもリンクを追加する必要がある
    save_num = 0
    for i in range(len(trainer_name)):
        if len(Trainer.objects.filter(name=trainer_name[i])) == 0:
            t = Trainer(name=trainer_name[i])
            t.save()
            save_num += 1
    return save_num

def save_stable_data(stable_name, stable_link):
    # trainerモデルにもリンクを追加する必要がある
    save_num = 0
    for i in range(len(stable_name)):
        if len(Stable.objects.filter(name=stable_name[i])) == 0:
            t = Stable(name=stable_name[i])
            t.save()
            save_num += 1
    return save_num


def save_race_data(race_number, race_name, race_arena, groundcondition_value, course_value, distance_value, race_head_count):
    r_number = race_number[:-2]  # 終端のRを削除
    p1 = groundcondition_value.find('馬場：')
    p2 = groundcondition_value.find('発走：')
    g_condition_str = groundcondition_value[p1+3:p2-2]
    # g_condition_strが空白文字なら馬場状態は未定
    if len(g_condition_str.lstrip()) == 0:
        g_condition = GroundCondition.objects.get(value="未定")
    else:
        g_condition = GroundCondition.objects.get(value=g_condition_str)
    c_value = Course.objects.get(value=course_value)
    d_value = distance_value[:-2]
    departure_time = groundcondition_value[p2+3:]
    replaced_departure_time = departure_time.replace('-', '0')
    replaced_race_date = race_date.replace('/', '-')
    d_time = replaced_race_date + ' ' + replaced_departure_time
    d_time = d_time[1:]
    r = Race(number=r_number, name=race_name, arena=race_arena, ground_condition=g_condition, course=c_value,
             distance=d_value, departure_time=d_time, head_count=race_head_count)
    if len(Race.objects.filter(name=race_name, departure_time=d_time)) == 0:
        r.save()
    return r

def save_data(race, order):
    ##>>>>>>>> 脚質と距離適性をどうきめるか未定、とりあえずid1
    distance_suitability = DistanceSuitability.objects.get(id=1)
    leg_quality = LegQuality.objects.get(id=1)
    ##>>>>>>レース前はrank未定
    data = Data(horse=Horse.objects.get(link=horse_link[order]),
                race=Race.objects.get(departure_time=race.departure_time),
                jockey=Jockey.objects.get(link=jockey_link[order]),
                sex=1, handicap=50,
                stable=Stable.objects.get(name=stable_name[order]),
                trainer=Trainer.objects.get(name=stable_name[order]),
                distance_suitability=distance_suitability, horse_order=order,
                leg_quality=leg_quality, odds=1.0,
                popularity=1, rank=0)
    data.save()
    return data

horseobj = save_horse_data(horse_name, horse_birth, horse_link)
save_jockey_data(jockey_name, jockey_link)
print(stable_name)
save_trainer_data(stable_name, trainer_link)
# 調教師ひつようか
save_stable_data(stable_name, trainer_link)
raceobj = save_race_data(race_number, race_name, race_arena, groundcondition_value, course_value, distance_value, race_head_count)
for i in range(len(horse_link)):
    if len(Data.objects.filter(horse=horseobj, race=raceobj)) == 0:
        save_data(raceobj, i)

