from django.urls import path

from . import views


app_name = 'service'
urlpatterns = [
    path('', views.index, name='index'),

    path('candidates/', views.candidate_data, name='candidate'),
    path('candidates/test/<int:candidate_id>/<int:planet_id>/', views.test, name='test'),
    path('candidates/test/end/', views.test, name='end'),

    path('jedis/', views.jedi, name='jedis'),
    path('jedis/<int:jedi_id>/<int:planet_id>/', views.candidate_list, name='current_jedi'),
    path('jedis/test/<int:candidate_id>/', views.candidate_test, name='done_test'),
]

