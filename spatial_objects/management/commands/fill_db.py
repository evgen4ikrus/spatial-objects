import csv
import logging
import os

from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


def fill_type_land_table(cursor, land_types):
    for land_type in land_types:
        cursor.execute(
            f"""
            INSERT INTO type_land (gid, name)
            VALUES ({land_type.get('gid')}, '{land_type.get('name')}')
            """
        )


def fill_road_table(cursor, roads):
    for road in roads:
        gid = road.get('gid')
        name = road.get('name')
        status = road.get('status')
        geom = road.get('geom')
        cursor.execute(
            f"""
            INSERT INTO road (gid, name, status, geom, len)
            VALUES ({gid}, '{name}', {status}, '{geom}', ST_Length('{geom}')/1000)
            """
        )


def fill_land_plot_table(cursor, land_plots):
    for land_plot in land_plots:

        gid = land_plot.get('gid')
        name = land_plot.get('name')
        date_create = land_plot.get('date_create')
        description = land_plot.get('description')
        polygon = land_plot.get('polygon')
        type_land = land_plot.get('type_land')

        cursor.execute(f"SELECT road FROM road WHERE ST_Intersects(road.geom, '{polygon}');")
        crossing_roads = cursor.fetchall()
        status = True if crossing_roads else False

        cursor.execute(
            f"""
            INSERT INTO land_plot (gid, name, area, status, date_create, description, polygon, type_land)
            VALUES ({gid}, '{name}', ST_Area('{polygon}')*1000, {status}, '{date_create}', '{description}', 
                '{polygon}', {type_land})
            """
        )


def get_data_from_file(file_path):
    with open(file_path) as file:
        reader = csv.DictReader(file)
        data_from_file = [row for row in reader]
        return data_from_file


class Command(BaseCommand):
    @staticmethod
    def handle(*args, **kwargs):
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level=logging.DEBUG)

        land_types_file_path = os.path.join('db_data', 'type_land.csv')
        roads_file_path = os.path.join('db_data', 'road.csv')
        land_plots_file_path = os.path.join('db_data', 'land_plot.csv')

        land_types = get_data_from_file(land_types_file_path)
        roads = get_data_from_file(roads_file_path)
        land_plots = get_data_from_file(land_plots_file_path)

        with connection.cursor() as cursor:
            fill_type_land_table(cursor, land_types)
            fill_road_table(cursor, roads)
            fill_land_plot_table(cursor, land_plots)

            logger.info('Таблицы land_plot, road и type_land успешно наполнены данными из csv-файлов')
