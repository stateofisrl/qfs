"""
Withdrawals URLs.
"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import WithdrawalViewSet

router = SimpleRouter()
router.register(r'', WithdrawalViewSet, basename='withdrawal')

urlpatterns = [
    path('', include(router.urls)),
]
