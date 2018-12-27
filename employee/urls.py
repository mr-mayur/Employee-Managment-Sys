from django.contrib import admin
from django.urls import path
from .views import (employee_list, employee_add, employee_delete, employee_details, employee_edit, MyProfile,ProfileUpdate)


urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('add/', employee_add, name="employee_add"),

    path('<int:id>/details/', employee_details, name='employee_details'),
    path('<int:id>/edit', employee_edit, name='employee_edit'),
    path('<int:id>/delete', employee_delete, name="employee_delete"),

    path('profile/', MyProfile.as_view(), name='my_profile'),
    path('profile/update/', ProfileUpdate.as_view(), name='update_profile'),

]

