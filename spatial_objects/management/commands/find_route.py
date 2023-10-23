import logging
import time

import requests
from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


def get_routes(coord_from, coord_to):
    payload = {
        'alternatives': 'true',
        'overview': 'false',
    }
    url = f'http://router.project-osrm.org/route/v1/driving/{coord_from};{coord_to}'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_time(seconds):
    beautiful_time = time.strftime("%Hч %Mмин", time.gmtime(seconds))
    return beautiful_time


def generate_message_about_routes(routes):
    waypoints = routes['waypoints']
    waypoints_message = ''
    for index, point in enumerate(waypoints, start=1):
        message = f'{index}. ключевая точка - ({round(point["distance"] / 1000, 2)}км)'
        waypoints_message += message + '\n'

    message = f"""
###Самый короткий маршрут
Расстояние - {round(routes['routes'][0]['distance'] / 1000, 1)}км
Время в пути - {get_time(int(routes['routes'][0]['duration']))}
Точки маршрута:
{waypoints_message}
    """
    return message


class Command(BaseCommand):
    help = 'Поиск маршрутов'

    def handle(self, *args, **options):
        land_plot_id = options['land_plot_id']
        coordinate = options['coordinate']
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level=logging.DEBUG)

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT ST_X(ST_AsText(ST_Centroid(polygon))), ST_Y(ST_AsText(ST_Centroid(polygon))) "
                           f"FROM land_plot WHERE gid={land_plot_id};")
            polygon_center = (cursor.fetchone())
        longitude, latitude = polygon_center
        routes = get_routes(f'{longitude},{latitude}', coordinate)
        message = generate_message_about_routes(routes)
        logger.info(message)

    def add_arguments(self, parser):
        parser.add_argument('land_plot_id', help='Id земельного участка;')
        parser.add_argument('coordinate', help='Координата.')
