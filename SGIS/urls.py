"""
URL configuration for SGIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from seguridad import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    
    
    path('users/',views.users_list,name='users_list'),
    path('users/upper_level/',views.users_upper_level,name='users_upper_level'),
    path('users/meddium_level/',views.users_medium_level,name='users_medium_level'),
    path('users/low_level/',views.users_low_level,name='users_low_level'),
    path('users/<int:id>/',views.users_detail,name='users_detail'),
    path('users/<int:id>/delete/',views.users_delete,name='users_delete'),
    
    
    path('sign_in/',views.sign_in,name='sign_in'),
    path('signup/',views.signup,name='signup'),
    path('loguot/',views.sign_out,name='loguot'),
    
    
    path('incedent/create/',views.create_incident,name='create_incident'),
    path('incidents/' , views.incidents_list,name='incidents_list'),
    path('incidents/<int:id>/',views.incidents_detail,name='incident_detail'),
    path('incidents/new/',views.incidents_new,name='incident_new'),
    path('incidents/<int:id>/delete',views.incidents_delete , name='incidents_delete'),
    path('incidents/in_progress/',views.incidents_in_progress,name='incident_in_progress'),
    path('incidents/resolver/',views.incidents_resolver,name='incident_resolver'),
    path('incidents/closed/',views.incidents_closed,name='incident_closed'),
    
    path('incidents/<int:id>/add_comment',views.add_comments, name='add_comment'),
]
