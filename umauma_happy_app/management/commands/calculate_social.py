from django.core.management.base import BaseCommand, CommandError
import social_analysis.views as social_analysis
import umauma_happy_app.utils.analysis as utils_analysis

import datetime
import time

class Command(BaseCommand):
    """
    レースごとの全ユーザー要素別的中率(未来は使用率のみ)を計算する
    コマンド: python manage.py calculate_social [start_delta] [end_delta]
    start_delta: 計算開始時間の今日からの日数差(ex:1年前なら'-365')
    end_delta: 計算終了時間の今日からの日数差(ex:今日なら'0')
    """
    help = 'Calculate number of used factor in all users.'

    def add_arguments(self, parser):
        """
        引数を管理する.
        :param parser:
        """
        parser.add_argument('start_delta', nargs='+', type=int, help='Difference days from today calculation start time')
        parser.add_argument('end_delta', nargs='+', type=int, help='Difference days from today calculation end time')

    def handle(self, *args, **options):
        """
        実際にコマンドを入力されたときの処理
        :param args:
        :param options:
        """
        pre_time = time.time()
        today = datetime.date.today()
        start_time = today + datetime.timedelta(days=options['start_delta'][0])
        end_time = today + datetime.timedelta(days=options['end_delta'][0])
        race_list = utils_analysis.get_race_by_period(start_time, end_time)
        self.stdout.write(self.style.NOTICE(f'{datetime.datetime.now()} | '
                                             f'{start_time} ~ {end_time}の{len(race_list)}件のレースに関して処理を始めます.'))
        social_analysis.count_factor_by_races(race_list)
        self.stdout.write(self.style.SUCCESS(f'{datetime.datetime.now()} | '
                                             f'{start_time} ~ {end_time}の{len(race_list)}件のレースに関して処理しました.'
                                             f'処理時間：{time.time() - pre_time:.5}秒'))