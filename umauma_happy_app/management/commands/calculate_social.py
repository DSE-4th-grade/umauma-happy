from django.core.management.base import BaseCommand, CommandError
import social_analysis.views as social_analysis
import umauma_happy_app.utils.analysis as utils_analysis

import datetime

class Command(BaseCommand):
    help = 'Calculate number of used factor in all users.'

    def add_arguments(self, parser):
        parser.add_argument('start_delta', nargs='+', type=int, help='Difference from calculation start time today')
        parser.add_argument('end_delta', nargs='+', type=int, help='Difference from calculation end time today')

    def handle(self, *args, **options):
            now = datetime.datetime.now()
            start_time = now + datetime.timedelta(days=options['start_delta'][0])
            end_time = now + datetime.timedelta(days=options['end_delta'][0])
            race_list = utils_analysis.get_race_by_period(start_time, end_time)
            social_analysis.count_factor_by_races(race_list)
            self.stdout.write(self.style.SUCCESS(f'{start_time}~{end_time}の{len(race_list)}件のレースに関して処理しました。'))