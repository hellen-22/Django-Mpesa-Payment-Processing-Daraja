from django.urls import path

from . import views

urlpatterns = [
    path("stk/", views.SendSTKPushView.as_view(), name="stk"),
    path('callback/<uuid:order_id>/', views.MpesaCallbackView.as_view(), name='callback'),
]