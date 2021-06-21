from django.urls import path
from . import views 
urlpatterns = [
    path('login/',views.login),
    path('code_login/<code>/',views.code_login),
    path('users/',views.users),
    path('users/<user_id>/',views.users),
    path('register/',views.register),
    # ----------------------
    path('sections/',views.sections),
    path('sections/<int:user_id>/',views.sections),
    path('sections_create/',views.sections_create),
    path('sections_edit/',views.sections_edit),
    path('sections_delete/<section_id>/',views.sections_delete),
    #----------------------------
    path('boxes/',views.boxes),
    path('boxes/<section_id>/',views.boxes),
    path('boxes_create/',views.boxes_create),
    path('boxes_edit/',views.boxes_edit),
    path('boxes_delete/<sect_box_id>/',views.boxes_delete),
    path('boxes_detail/<sect_box_id>/',views.boxes_detail),
    #----------------------------
    path('files/',views.filesdoc),
    path('files/<box_id>/',views.filesdoc),
    path('files_create/',views.files_create),
    path('files_edit/',views.files_edit),
    path('files_delete/<file_id>/',views.files_delete),
]
