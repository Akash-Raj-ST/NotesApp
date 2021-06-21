from django.urls import path
from . import views 

urlpatterns = [
    path('',views.index),
    path('code_login',views.code_login),
    path('register',views.register),
    path('home',views.home,name="home"),
    path('view/<int:box_id>/',views.view),

    path('section_edit/<int:section_id>',views.section_edit),
    path('section_create',views.section_create),
    path('section_delete/<int:section_id>',views.section_delete),

    path('box_edit/<int:box_id>',views.box_edit),
    path('box_create/<int:section_id>',views.box_create),
    path('box_delete/<int:box_id>',views.box_delete),

    path('view/<int:box_id>/file_edit/<int:file_id>',views.file_edit),
    path('view/<int:box_id>/file_create',views.file_create),
    path('view/<int:box_id>/file_delete/<int:file_id>',views.file_delete),

    path('logout',views.logout)
]
