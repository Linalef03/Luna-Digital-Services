from django.urls import path
from . import views

app_name = 'dashboard'  

urlpatterns = [
    
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/assign/<int:order_id>/', views.assign_order, name='assign_order'),
   
    path('admin/orders/', views.manage_orders, name='manage_orders'),


  
    path('admin/employees/', views.employees_list, name='employees_list'),
    path('admin/employees/add/', views.add_employee, name='add_employee'),
    path('admin/employees/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('admin/employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),

   
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/start/<int:order_id>/', views.start_order, name='start_order'),
    path('employee/complete/<int:order_id>/', views.complete_order, name='complete_order'),
   

]
