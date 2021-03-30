from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("<str:item_name>", views.view_item, name="item"),
    path("<str:item_name>/edit", views.edit, name="edit"),
    path("random", views.view_item, name="random")
    
]