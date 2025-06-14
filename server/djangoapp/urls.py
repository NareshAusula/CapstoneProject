from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "djangoapp"

urlpatterns = [
    # path for registration
    path(route="register", view=views.registration, name="register"),
    # path for login
    path(route="login", view=views.login_user, name="login"),
    path(route="logout", view=views.logout_request, name="logout"),
    path(route="get_cars", view=views.get_cars, name="get_cars"),
    # path for dealer reviews view
    path("get_dealers", views.get_dealerships, name="get_dealers"),
    path(
        "get_dealers/<str:state>/",
        views.get_dealerships,
        name="get_dealers_by_state",
    ),
    path(
        route="reviews/dealer/<int:dealer_id>/",
        view=views.get_dealer_reviews,
        name="dealer_details",
    ),
    # path for add a review view
    path(route="add_review", view=views.add_review, name="add_review"),
    path(
        route="postreview/<int:dealer_id>/",
        view=views.add_review,
        name="post_review",
    ),
    path(
        route="dealer/<int:dealer_id>/",
        view=views.get_dealer_details,
        name="dealer_detail",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
