from django.urls import path, include

from . import views
# from .views import set_webhook
from .views import ViberUserView, set_webhook

urlpatterns = [
    path('callback/', views.callback),
    path('hi/', ViberUserView.as_view()),
    # path('send_message/', send_message_for_user),
    path('set_webhook/', set_webhook),

]
