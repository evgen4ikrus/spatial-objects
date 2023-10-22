from django.urls import path

from .views import land_plot_detail, land_plot_list

urlpatterns = [
    path('', land_plot_list, name="land-plot-list"),
    path('land-plot/<int:pk>/', land_plot_detail, name="land-plot-detail"),
]
