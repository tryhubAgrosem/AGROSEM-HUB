from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('nomenclatures/(?P<type>agm|as)/update/', views.update, name='update'),
    re_path('nomenclatures/(?P<type>agm|as)/', views.NomenclatureListView_edited.as_view(), name='nomenclatures'),
]