"""
Investment URLs.
"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import InvestmentPlanViewSet, UserInvestmentViewSet

router = SimpleRouter()
router.register(r'plans', InvestmentPlanViewSet, basename='plan')
router.register(r'my-investments', UserInvestmentViewSet, basename='user-investment')

urlpatterns = [
    path('', include(router.urls)),
]
