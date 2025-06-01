# Uncomment the required imports before adding the code


from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Handle sign in request."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:

        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    """Handle sign out request."""
    logout(request)
    data = {"username": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    """Handle sign up request."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    try:
        # Check if user already exists
        User.objects.get(username=username)
        return JsonResponse(
            {"userName": username, "error": "Already Registered"})
    except User.DoesNotExist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        # Login the user and redirect to list page
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})


def get_cars(request):
    """Return list of cars."""
    count = CarMake.objects.filter().count()

    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """Return list of dealerships."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Return reviews for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail["review"])
        review_detail["sentiment"] = response["sentiment"]
    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    """Return details for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse(
        {
            "status": 200,
            "dealer": dealership,
            "dealer_id": dealer_id,
        }
    )


def add_review(request):
    """Submit a review."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    try:
        data = json.loads(request.body)
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as e:
        logger.error(f"Error posting review: {str(e)}")
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"})
