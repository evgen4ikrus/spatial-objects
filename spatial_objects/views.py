from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.http import Http404
from django.shortcuts import render


@login_required(login_url='/accounts/login/')
def land_plot_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT description, area, gid FROM land_plot ORDER BY land_plot.gid;')
        records = cursor.fetchall()
    land_plots = []
    for land_plot in records:
        description, area, gid = land_plot
        land_plots.append({
            'description': description,
            'area': round(area, 2),
            'gid': gid,
        })
    paginator = Paginator(land_plots, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, template_name='land_plot_list.html', context={"page_obj": page_obj})


@login_required(login_url='/accounts/login/')
def land_plot_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            WITH distance as(
                SELECT MIN(ST_Distance(polygon, geom)) min_distance
                FROM road, land_plot 
                WHERE land_plot.gid={pk}
            ),
            nearest_road as(
                SELECT ST_Distance(polygon, geom) as min_dis, 
                       road.name,
                       land_plot.gid
                FROM road, land_plot
                WHERE land_plot.gid={pk} and ST_Distance(polygon, geom) = (SELECT min_distance FROM distance)
            ),
            current_land_plot as(
                SELECT land_plot.gid, area, status, date_create, description, polygon, type_land.name
                FROM land_plot JOIN type_land
                ON land_plot.type_land = type_land.gid
                WHERE land_plot.gid={pk}
            )
            SELECT current_land_plot.gid, area, status, date_create,
                   description, polygon, current_land_plot.name, nearest_road.name,
                   CASE WHEN min_dis < 1
                   THEN CAST(min_dis * 1000 AS CHAR(15)) || ' м'
                   ELSE CAST(min_dis AS CHAR(15)) || ' км'
                   END
            FROM current_land_plot, nearest_road; 
            """
        )
        record = cursor.fetchone()
    if record:
        gid, area, status, date_create, description, polygon, type_land, rout_name, min_distance = record
        min_distance, length_measure = min_distance.split()
        land_plot = {
            'gid': gid,
            'area': round(area, 2),
            'status': status,
            'date_create': date_create,
            'description': description,
            'polygon': polygon,
            'type_land': type_land,
            'rout_name': rout_name,
            'min_distance': f'{round(float(min_distance), 1)}{length_measure}'
        }
        context = {'land_plot': land_plot}
        return render(request, template_name='land_plot_detail.html', context=context)
    raise Http404("Poll does not exist")
