from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import bs4
import sqlite3
import re
import logging

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()



url = 'http://race.netkeiba.com/?pid=race_list'
soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read())
get = soup.find_all('div', class_="racename")
link = []
racelink = []
horselist = []
horse_link = []
horse_name = []
jockey_name = []
jockey_link = []
trainer_name = []
horse_birth = []
data_sex = []
data_handicap = []
data_odds = []
data_popularity = []
data_past_achievement = []


for i in range(0,len(get)):#イニシャルページからレースへのaタグを取る
    link.insert(0,get[i].find('a'))

list1=list()
for tag in link:#aタグのいらない部分を取る
    x = tag.get('href', None)
    list1.append(x)



for i in range(0,1):#リンクを使える形に直すlen(list1)
    racelink.append("http://race.netkeiba.com"+list1[i])

for i in range(0,len(racelink)):#レースごと
    data_sex = []
    data_handicap = []
    data_odds = []
    data_popularity = []
    racelink[i] = bs4.BeautifulSoup(urllib.request.urlopen(racelink[i]).read())
    horselink = racelink[i].find_all('a', href=re.compile('http://db.netkeiba.com/horse/'))
    jockeylink = racelink[i].find_all('a', href=re.compile('http://db.netkeiba.com/jockey/'))
    trainerlink = racelink[i].find_all('a', href=re.compile('http://db.netkeiba.com/trainer/'))
    raceval = racelink[i].find('div', class_='mainrace_data')
    raceval3 = racelink[i].find('table', class_='race_table_old')
    raceval4 = raceval3.find_all('td')
    for k in range(0,len(raceval4)):
        if k == 2+10*len(data_sex):
          data_sex.append(raceval4[k])
        if k == 3+10*len(data_handicap):
          data_handicap.append(raceval4[k])
        if k == 6+10*len(data_odds):
          data_odds.append(raceval4[k])
        if k == 7+10*len(data_popularity):
          data_popularity.append(raceval4[k])
    courseval = raceval.find('p').string
    courseval2 = raceval('p')[1].string
    course_value = courseval[0]
    distance_value = courseval[1:-3]
    groundcondition_value = re.compile('馬場：.*/').search(courseval2).string
    race_date = racelink[i].find('title').string[0:11]
    raceval2 = racelink[i].find('title').string.split(" ")
    race_number = raceval2[2]
    race_name = raceval2[3]
    race_arena = raceval2[1]
    race_head_count = len(horselink)
    for j in range(0,len(horselink)):#馬ページごと
        data_past_achievement = []
        horse_name.append(horselink[j].get('title'))
        jockey_name.append(jockeylink[j].get('title'))
        trainer_name.append(trainerlink[j].get('title'))
        horselink[j] = horselink[j].get('href', None)#馬ページへのリンク文字列
        jockeylink[j] = jockeylink[j].get('href', None)
        horse_link.append(horselink[j])
        jockey_link.append(jockeylink[j])
        gate = horselink[j]
        horselink[j] = bs4.BeautifulSoup(urllib.request.urlopen(horselink[j]).read())
        table = horselink[j].find('table', class_='db_prof_table')
        row = table.find('tr')
        horse_birth.append(row.find('td').string)
        table2 = horselink[j].find('table', class_='db_h_race_results')
        table2val = table2.find_all('td')
        for l in range(0, len(table2val)):
            if l == 11 + 28 * len(data_past_achievement):
                data_past_achievement.append(table2val[l])




    # horselink = bs4.BeautifulSoup(urllib.request.urlopen(racelink[i]).read())
   # horselist.insert()

#c.execute('insert into umauma_happy_app_horse(id, name, birth_year, link, created_at, updated_at) values (2,?,2,3,4,5)',(horsename,))

conn.commit()

def index(request):
    return HttpResponse(str(list1)+str(data_sex)+str(data_handicap)+str(data_odds)+str(data_popularity)+str(data_past_achievement)+str(race_date)+str(race_number)+str(race_name)+str(race_arena)+str(race_head_count)+str(groundcondition_value)+str(course_value)+str(distance_value)+str(jockey_name)+str(jockey_link)+str(trainer_name)+str(horse_name)+str(horse_birth)+str(horse_link))