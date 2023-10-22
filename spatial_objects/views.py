from django.core.paginator import Paginator
from django.db import connection
from django.http import Http404
from django.shortcuts import render


def land_plot_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT description, area, gid FROM land_plot;')
        records = cursor.fetchall()
    land_plots = []
    for serial_number, land_plot in enumerate(records, start=1):
        description, area, gid = land_plot
        land_plots.append({
            'description': description,
            'area': round(area, 1),
            'serial_number': serial_number,
            'gid': gid,
        })
    paginator = Paginator(land_plots, 20)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, template_name='land_plot_list.html', context={"page_obj": page_obj})


def land_plot_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT land_plot.gid, area, status, date_create, description, polygon, type_land.name '
                       f'FROM land_plot JOIN type_land ON land_plot.type_land = type_land.gid '
                       f'WHERE land_plot.gid={pk};')
        records = cursor.fetchall()
    if records:
        gid, area, status, date_create, description, polygon, type_land = records[0]
        land_plot = {
            'gid': gid,
            'area': round(area, 1),
            'status': status,
            'date_create': date_create,
            'description': description,
            'polygon': polygon,
            'type_land': type_land,
        }
        context = {'land_plot': land_plot}
        return render(request, template_name='land_plot_detail.html', context=context)
    raise Http404("Poll does not exist")
