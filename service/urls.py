from django.urls import path

from . import views


app_name = 'service'
urlpatterns = [
    path('', views.index, name='index'),

    path('candidates/', views.candidate_data, name='candidate'),
    path('candidates/test/<int:candidate_id>/<int:planet_id>/', views.test, name='test_list'),
    # path('candidates/test/end/', views.test),

    path('jedis/', views.jedi, name='jedis'),
    path('jedis/<int:jedi_id>/', views.detail, name='current_jedi'),


]

