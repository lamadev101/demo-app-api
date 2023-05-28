from django.urls import path
from .views import ItineraryPackageView,HomeView,LayTravllerPostView,LayTravellerPlaceView,LayTravelerUniquePackageNamePackagePostView,PackageInformationView,UserItineraryInformationView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('itenary', LayTravllerPostView.as_view(), name="itenary"),
    path('place-list',LayTravellerPlaceView.as_view(),name="place-list"),
    path('packages',PackageInformationView.as_view(),name="packages"),
    path('itinerary-package',ItineraryPackageView.as_view(),name="itinerary-package"),
    path('user-itinerary',UserItineraryInformationView.as_view(),name="user-itinerary"),
    path('itinerary-unique-package',LayTravelerUniquePackageNamePackagePostView.as_view(),name="itinerary-unique-package")

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


