from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="shopHome"),
    path("about/",views.about,name="aboutus"),
    path("contact/",views.contact,name="contactus"),
    path("tracker/",views.tracker,name="TrackingStatus"),
    path("products/<int:myid>",views.prodView,name="ProductView"),
    path("checkout/",views.checkout,name="CheckOut"),
    path("search/",views.search,name="Search"),
]