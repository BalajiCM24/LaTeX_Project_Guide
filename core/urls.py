from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('note/latex2docx/', views.latex2docx_view, name='latex2docx'),
    path('note/uppreedit/', views.uppreedit_view, name='uppreedit'),
    path('note/uptypeset/', views.uptypeset_view, name='uptypeset'),
    path('note/olhtypeset/', views.olhtypeset_view, name='olhtypeset'),
    path('note/latextoxml/', views.latextoxml_view, name='latextoxml'),
    path('open-folder/', views.open_folder, name='open_folder'),
]
