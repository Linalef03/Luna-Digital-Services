from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("new/", views.create_order, name="create_order"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
   
]
