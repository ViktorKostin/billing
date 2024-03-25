from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WalletViewSet, WalletHolderViewSet, TransactionViewSet

app_name = 'wallet'

router = DefaultRouter()

router.register(r'holder', WalletHolderViewSet, basename='account')
router.register(r'wallets', WalletViewSet, basename='wallets')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('wallets/', include(router.urls)),
]
