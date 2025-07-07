from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import CityViewSet, BusOperatorViewSet, BusViewSet, RouteViewSet, SeatViewSet, BookingViewSet, RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'operators', BusOperatorViewSet)
router.register(r'buses', BusViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
]