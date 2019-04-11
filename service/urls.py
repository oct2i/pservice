from django.urls import path, include

from . import views


app_name = 'service'

urlpatterns = [
    path('', views.index, name='index'),
    path('candidates/', include([
        path('', views.candidate_registration, name='candidates'),
        path('test/', include([
            path('<int:candidate_id>/<int:planet_id>/', views.test_trial, name='test'),
            path('end/', views.test_trial),
        ])),
    ])),

    path('jedis/', include([
        path('', views.jedi_list, name='jedis'),
        path('<int:jedi_id>/<int:planet_id>/', include([
            path('', views.candidate_list, name='jedi'),
            path('test/<int:candidate_id>/', views.test_trial_results, name='test_results'),
        ])),
    ])),
]
