import makefixtures
import json

if __name__ == '__main__':
    makefixtures.cource()
    makefixtures.distance()
    makefixtures.distancesuitability()
    makefixtures.factor()
    makefixtures.legquality()
    makefixtures.groundcondition()

    component_data = []
    master_data = []
    src = ["umauma_happy_app/fixtures/components/faker_course.json",
           "umauma_happy_app/fixtures/components/faker_distance.json",
           "umauma_happy_app/fixtures/components/faker_distancesuitability.json",
           "umauma_happy_app/fixtures/components/faker_factor.json",
           "umauma_happy_app/fixtures/components/faker_legquality.json",
           "umauma_happy_app/fixtures/components/faker_groundcondition.json"]
    for i in range(len(src)):
        fr = open(src[i], 'r')
        component_data = json.load(fr)
        master_data.extend(component_data)
    fw = open('umauma_happy_app/fixtures/seed_default.json', 'w')
    json.dump(master_data, fw, indent=2, ensure_ascii=False)
