from django.urls import path
from .views import hello_world, greet, dashboard, edit_emp, statistics

urlpatterns = [
    path('hello-world/', hello_world),  # Added trailing slash
    path('greet/<str:name>/', greet, name='greet'),  # Added trailing slash
    path('dashboard/', dashboard, name='dashboard'),  # Added trailing slash
    path('edit_emp/', edit_emp),  # Added trailing slash
    path('statistics/', statistics, name='statistics'),
]
