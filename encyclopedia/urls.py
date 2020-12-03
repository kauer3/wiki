from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/",views.search_page, name="search"),
    path("new/", views.create_new_page, name="new"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("wiki/", views.get_random_page, name="random"),
]
