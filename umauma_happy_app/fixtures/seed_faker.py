import makefixtures
import json

if __name__ == '__main__':
    makefixtures.race()
    makefixtures.user()

    component_data = []
    master_data = []
    src = ["umauma_happy_app/fixtures/components/faker_user.json",
           "umauma_happy_app/fixtures/components/faker_race.json"]
    for i in range(len(src)):
        fr = open(src[i], 'r')
        component_data = json.load(fr)
        master_data.extend(component_data)
    fw = open('umauma_happy_app/fixtures/seed_faker.json', 'w')
    json.dump(master_data, fw, indent=2, ensure_ascii=False)
