"""
Support URLs.
"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import SupportTicketViewSet

router = SimpleRouter()
router.register(r'tickets', SupportTicketViewSet, basename='support-ticket')

urlpatterns = [
    path('', include(router.urls)),
]
