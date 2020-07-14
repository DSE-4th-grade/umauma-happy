from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import bs4
import sqlite3
import re
import datetime
import logging

#from .scraping_view import list1, data_sex, data_handicap, data_odds, data_popularity, data_past_achievement,

#レース情報までの入れ子
#   1 レース一覧ページのトップページ
#       2 特定の日付ごとのレース一覧ページ
#           3 個別のレースページ
#               4 馬情報ページや調教師情報ページ


def find_initialize():
    #URLを受け取って、適切な形に直したりする
    url = 'http://race.netkeiba.com/?pid=race_list' #レース一覧ページのリンク
    racedate_url = [] #
    soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser") #レース一覧ページをsoupで取得
    for i in range(0, len(soup.find('div', class_='DateList_Box').find_all('a'))):
        racedate_url.append(soup.find('div', class_='DateList_Box')('a')[i].get('href', None))#racedate_urlに特定の日付のレース一覧のURLを配列形式で保存
    return racedate_url


def race_link_conversion(racedate_url):#特定の日付のレース一覧を受け取り、個別のレースのリンクの一覧として返す
    url = "http://race.netkeiba.com" + racedate_url  # URL
    race_list = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")  # 2 特定の日付ごとのレース一覧ページ
    get = race_list.find_all('div', class_="racename")  # 個別のレースのリンクの一覧(使える形に修正する前)
    individual_race_list = []
    for i in range(0, len(get)):  # イニシャルページからレースへのaタグを取る
        individual_race_url = get[i].find('a')
        individual_race_url = "http://race.netkeiba.com" + individual_race_url.get('href', None)
        individual_race_list.append(individual_race_url)  # 個別のレースのリンクの一覧(修正後)
    return individual_race_list


def find_horse_data(individual_race_url):
    #horse_name, horse_birth, horse_link
    #全て配列
    horse_name = []
    horse_link = []
    horse_birth = []
    url = individual_race_url
    individual_race_contents = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")  #個別レースページを展開
    horselink = individual_race_contents.find_all('a', href=re.compile('http://db.netkeiba.com/horse/'))
    for j in range(0, len(horselink)):
        horse_name.append(horselink[j].get('title'))
        horselink[j] = horselink[j].get('href', None)
        horse_link.append(horselink[j])
        horselink[j] = bs4.BeautifulSoup(urllib.request.urlopen(horselink[j]).read(), "html.parser")
        table = horselink[j].find('table', class_='db_prof_table')
        row = table.find('tr')
        horse_birth.append(row.find('td').string)
    return 0


def find_jockey_data(individual_race_url):
    #jockey_name, jockey_link
    #全て配列
    url = individual_race_url
    individual_race_contents = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")#2 特定の日付ごとのレース一覧ページ
    jockey_name = []
    jockey_link = []
    jockeylink = individual_race_contents.find_all('a', href=re.compile('http://db.netkeiba.com/jockey/'))
    for j in range(0, len(jockeylink)):  # ジョッキーページごと
        jockey_name.append(jockeylink[j].get('title'))
        jockeylink[j] = jockeylink[j].get('href', None)
        jockey_link.append(jockeylink[j])
    return 0


def find_trainer_data(individual_race_url):
    #trainer_name, trainer_link
    #全て配列
    trainer_name = []
    trainer_link = []
    url = individual_race_url  # URL
    individual_race_contents = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")#2 特定の日付ごとのレース一覧ページ
    trainerlink = individual_race_contents.find_all('a', href=re.compile('http://db.netkeiba.com/trainer/'))
    for j in range(0, len(trainerlink)):  # 馬ページごと
        trainer_name.append(trainerlink[j].get('title'))
        trainerlink[j] = trainerlink[j].get('href', None)
        trainer_link.append(trainerlink[j])
    return 0


def find_stable_data(individual_race_url):
    #stable_name, stable_link
    #stable_nameは配列、stable_linkは使われていない
    stable_name = []
    stable_link = []
    url = individual_race_url  # URL
    individual_race_contents = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")#2 特定の日付ごとのレース一覧ページ
    trainerlink = individual_race_contents.find_all('a', href=re.compile('http://db.netkeiba.com/trainer/'))
    for j in range(0, len(trainerlink)):  # 馬ページごと
        stable_name.append(trainerlink[j].get('title'))
    return 0


def find_race_data(individual_race_url):
    #race_number, race_name, race_arena, groundcondition_value, course_value, distance_value, race_head_count
    url = individual_race_url  # URL
    individual_race_contents = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")#2 特定の日付ごとのレース一覧ページ
    raceval = individual_race_contents.find('div', class_='mainrace_data')
    courseval = raceval.find('p').string
    courseval2 = raceval('p')[1].string
    course_value = courseval[0]
    distance_value = courseval[1:-3]
    groundcondition_value = re.compile('馬場：.*/').search(courseval2).string
    race_date = individual_race_contents.find('title').string[0:11]
    raceval2 = individual_race_contents.find('title').string.split(" ")
    race_number = raceval2[2]
    race_name = raceval2[3]
    race_arena = raceval2[1]
    horselink = individual_race_contents.find_all('a', href=re.compile('http://db.netkeiba.com/horse/'))
    race_head_count = len(horselink)
    return 0


conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

ddate = []
url = 'http://race.netkeiba.com/?pid=race_list'
#url = 'http://race.netkeiba.com/?pid=race_list&id=p0714'
soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
for i in range(0,len(soup.find('div', class_='DateList_Box').find_all('a'))):
    ddate.append(soup.find('div', class_='DateList_Box')('a')[i].get('href', None))

for so in range(0,len(ddate)):#一日ごとにスクレイピング
    url = "http://race.netkeiba.com"+ddate[so] #URL
    soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    get = soup.find_all('div', class_="racename")
    link = []
    racelink = []
    horselist = []
    horse_link = []
    horse_name = []
    jockey_name = []
    jockey_link = []
    stable_name = []
    trainer_link = []
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

    for i in range(0,len(racelink)):#レースごとにスクレイピング

        data_sex = []
        data_handicap = []
        data_odds = []
        data_popularity = []
        racelink[i] = bs4.BeautifulSoup(urllib.request.urlopen(racelink[i]).read(), "html.parser")
        horselink = racelink[i].find_all('a', href=re.compile('http://db.netkeiba.com/horse/'))
        jockeylink = racelink[i].find_all('a', href=re.compile('http://db.netkeiba.com/jockey/'))
        trainerlink = racelink[i].find_all('a', href=re.compile('http://db.netkeiba.com/trainer/'))
        dt_now = datetime.datetime.now()

        if int(ddate[so][-4:]) < int(dt_now.month)*100+int(dt_now.day):#もう終わったレース結果のみを取る
            # 結果ページから取得する
            racevl = racelink[i].find('table', class_='race_table_01')
            data_rank = []
            data_horse_order = []
            data_horse_id = []
            data_popularity = []
            data_odds = []
            for p in range(0, len(racevl.find_all('tr')) - 1):
                data_rank.append(p + 1)
                data_horse_order.append(racevl('td', class_=re.compile('waku'))[p].string)
                data_horse_id.append(racevl('a', href=re.compile('http://db.netkeiba.com/horse/'))[p].get('href',None))
                data_popularity.append(racevl('td', class_=re.compile('r*ml'))[p * 2].string)
                data_odds.append(racevl('td', class_=re.compile('txt_r'))[p].string)
        else:   # まだ始まっていないレース
            raceval = racelink[i].find('div', class_='mainrace_data')
            raceval3 = racelink[i].find('table', class_='race_table_old')
            raceval4 = raceval3.find_all('td')
            for k in range(0,len(raceval4)):
                if k == 2+10*len(data_sex):
                  data_sex.append(raceval4[k].get_text()[:1])
                if k == 3+10*len(data_handicap):
                  data_handicap.append(raceval4[k].get_text()[:2])
                if k == 6+10*len(data_odds):
                  data_odds.append(raceval4[k].get_text())
                if k == 7+10*len(data_popularity):
                  data_popularity.append(raceval4[k].get_text())
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
                stable_name.append(trainerlink[j].get('title'))
                horselink[j] = horselink[j].get('href', None)#馬ページへのリンク文字列
                jockeylink[j] = jockeylink[j].get('href', None)
                trainerlink[j] = trainerlink[j].get('href', None)
                horse_link.append(horselink[j])
                jockey_link.append(jockeylink[j])
                trainer_link.append(trainerlink[j])
                gate = horselink[j]
                horselink[j] = bs4.BeautifulSoup(urllib.request.urlopen(horselink[j]).read(), "html.parser")
                trainerlink[j] = bs4.BeautifulSoup(urllib.request.urlopen(trainerlink[j]).read(), "html.parser")
                table = horselink[j].find('table', class_='db_prof_table')
                row = table.find('tr')
                horse_birth.append(row.find('td').string)
                table2 = horselink[j].find('table', class_='db_h_race_results')
                table2val = table2.find_all('td')
                for l in range(0, len(table2val)):
                    if l == 11 + 28 * len(data_past_achievement):
                        data_past_achievement.append(table2val[l])


conn.commit()


def index(request):
    return HttpResponse("flasd")

