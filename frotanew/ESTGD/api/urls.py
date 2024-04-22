from django.urls import path,  include
from .import views

urlpatterns = [
    path('veiculos/', views.ESTGDAPIView.as_view()),
    path('veiculos/<int:veiculo_id>/', views.ESTGDAPIView.as_view())
]