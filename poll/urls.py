from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='polls_list'),
    path('<int:id>/details/', details, name='polls_details'),
    path('<int:id>/', poll, name='single_poll'),

    #path('<int:id>/', vote_poll, name="poll_vote")
    path('add/', PollView.as_view(), name='poll_add'),
    path('<int:id>/edit/', PollView.as_view(), name='poll_edit'),
    path('<int:id>/delete/', PollView.as_view(), name='poll_delete'),

]
