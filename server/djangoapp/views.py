from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
# import os
# Get an instance of a logger
logger = logging.getLogger(__name__)


# sample_data_dir = os.path.dirname(os.path.realpath(__file__))
# sample_data_file_path = os.path.join(sample_data_dir, '../sample.json')
#
# with open(sample_data_file_path) as f:
#   sample_data = json.load(f)

# Create your views here.


# Create an `about` view to render a static about page
def about(request):
  context = {}
  if request.method == "GET":
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
  context = {}
  if request.method == "GET":
    return render(request, 'djangoapp/contact_us.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
  context = {}
  if request.method == "POST":
    # Get username and password from request.POST dictionary
    username = request.POST['username']
    password = request.POST['psw']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    if user is not None:
      # If user is valid, call login method to login current user
      login(request, user)
      return redirect('djangoapp:index')
    else:
      # If not, return to login page again
      return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
  if request.method == "GET":
    logout(request)
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
  context = {}
  # If it is a GET request, just render the registration page
  if request.method == 'GET':
    return render(request, 'djangoapp/registration.html', context)
  # If it is a POST request
  elif request.method == 'POST':
    # Get user information from request.POST
    username = request.POST['username']
    password = request.POST['psw']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    user_exist = False
    try:
      # Check if user already exists
      User.objects.get(username=username)
      user_exist = True
    except:
      # If not, simply log this is a new user
      logger.debug("{} is new user".format(username))
      # If it is a new user
    if not user_exist:
      # Create user in auth_user table
      user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                      password=password)
      # Login the user and redirect to course list page
      login(request, user)
      return redirect("djangoapp:index")
    else:
      return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
  context = {}
  if request.method == "GET":
    url = "https://jp-tok.functions.appdomain.cloud/api/v1/web/8767a390-c1a2-4465-adee-608645d9cc2b/dealership-package/get-dealership"
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url)
    # Concat all dealer's short name
    # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
    context['dealership_list'] = dealerships
    # context['dealership_list'] = sample_data['dealerships']['body']
    # Return a list of dealer short name
    return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
  if request.method == "GET":
    context = {}
    dealer_url = "https://jp-tok.functions.appdomain.cloud/api/v1/web/8767a390-c1a2-4465-adee-608645d9cc2b/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    # context["dealer"] = sample_data['dealerships']['body'][14]
    review_url = "https://jp-tok.functions.appdomain.cloud/api/v1/web/8767a390-c1a2-4465-adee-608645d9cc2b/dealership-package/get-review"
    reviews = get_dealer_reviews_from_cf(review_url, id=id)
    context["reviews"] = reviews
    # context["reviews"] = sample_data['review']['body']

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, id):
  context = {}
  dealer_url = "https://jp-tok.functions.appdomain.cloud/api/v1/web/2e1cc6b1-4125-4ddf-983a-23203b79e5e7/dealership-package/get-dealership"
  dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
  context["dealer"] = dealer
  # context["dealer"] = sample_data['dealerships']['body'][14]
  if request.method == 'GET':
    # Get cars for the dealer
    cars = CarModel.objects.all()
    print(cars)
    context["cars"] = cars

    return render(request, 'djangoapp/add_review.html', context)
  elif request.method == 'POST':
    if request.user.is_authenticated:
      username = request.user.username
      print(request.POST)
      payload = dict()
      car_id = request.POST["car"]
      car = CarModel.objects.get(pk=car_id)
      payload["time"] = datetime.utcnow().isoformat()
      payload["name"] = username
      payload["dealership"] = id
      payload["id"] = id
      payload["review"] = request.POST["content"]
      payload["purchase"] = False
      if "purchasecheck" in request.POST:
        if request.POST["purchasecheck"] == 'on':
          payload["purchase"] = True
          payload["purchase_date"] = request.POST["purchasedate"]
          payload["car_make"] = car.make.name
          payload["car_model"] = car.name
          payload["car_year"] = int(car.year)

      new_payload = {}
      new_payload["review"] = payload
      review_post_url = "https://jp-tok.functions.appdomain.cloud/api/v1/web/8767a390-c1a2-4465-adee-608645d9cc2b/dealership-package/post-review"
      post_request(review_post_url, new_payload, id=id)
    return redirect("djangoapp:dealer_details", id=id)
