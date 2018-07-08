import json
import collections as cl
from faker import Factory
import random

def race():
    fake = Factory.create('ja_JP')
    ys = []
    for i in range(10):
        datetime_race = fake.date_time_this_decade(before_now=True, after_now=True, tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")
        date_race = fake.date_time_this_decade(before_now=True, after_now=True, tzinfo=None).strftime("%Y-%m-%d")
        datetime_now = fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")
        fields = cl.OrderedDict()
        fields["number"] = random.randint(1, 12)
        fields["name"] = fake.last_name() + "記念"
        fields["arena"] = fake.town() + "競馬場"
        fields["departure_time"] = datetime_race
        fields["head_count"] = random.randint(10, 16)
        fields["course_id"] = random.randint(1, 3)
        fields["distance_id"] = random.randint(1, 6)
        fields["ground_condition_id"] = random.randint(1, 4)
        fields["date"] = date_race
        fields["created_at"] = datetime_now
        fields["updated_at"] = datetime_now
        data = cl.OrderedDict()
        data["model"] = "umauma_happy_app.race"
        data["fields"] = fields
        ys.append(data)
    fw = open('umauma_happy_app/fixtures/components/faker_race.json', 'w')
    json.dump(ys, fw, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    race()
