from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SellerSignup.as_view(), name="seller_signup"),
    path("store/", CreateStoreView.as_view(), name="create_store"),
    path("inventory/", UploadInventoryView.as_view(), name="upload_inventory"),
    path("store/<str:store_link>/", StoreDetailsView.as_view(), name="store_details"),
    path(
        "store/<str:store_link>/catalog/",
        StoreCatalogView.as_view(),
        name="store_catalog",
    ),
    path("cart/", CartView.as_view(), name="cart"),
    path("order/", PlaceOrderView.as_view(), name="place_order"),
]
