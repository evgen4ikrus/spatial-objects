import logging

from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


def create_land_plot_table(cursor):
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS land_plot (
            gid integer NOT NULL,
            name character varying,
            area double precision,
            status boolean,
            date_create timestamp with time zone, 
            description text,
            polygon geometry NOT NULL,
            type_land integer,
            CONSTRAINT land_plot_pk PRIMARY KEY (gid),
            CONSTRAINT type_land_fk
                FOREIGN KEY (type_land)
                REFERENCES type_land(gid)
        );
        '''
    )


def create_road_table(cursor):
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS road(
            gid integer,
            name character varying,
            len double precision,
            status boolean, 
            geom geometry NOT NULL,
            CONSTRAINT road_transport_pk PRIMARY KEY (gid) 
        );
        '''
    )


def create_type_land_table(cursor):
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS type_land (
            gid integer NOT NULL,
            name character varying, 
            CONSTRAINT type_land_pk PRIMARY KEY (gid)
        );
        '''
    )


class Command(BaseCommand):
    @staticmethod
    def handle(*args, **kwargs):
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level=logging.DEBUG)
        with connection.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
            create_road_table(cursor)
            create_type_land_table(cursor)
            create_land_plot_table(cursor)
            logger.info('Таблицы land_plot, road и type_land успешно созданы')
