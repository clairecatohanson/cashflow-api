import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from cashflowapi.serializers import UserSerializer, UserSerializerEmbedded


@csrf_exempt
def register_user(request):
    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    if (
        not req_body["username"]
        or not req_body["password"]
        or not req_body["firstName"]
        or not req_body["lastName"]
    ):
        return HttpResponse(
            {
                "error": "Missing required fields: username, firstName, and lastName must be included in the request"
            },
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        new_user = User.objects.create_user(
            username=req_body["username"],
            password=req_body["password"],
            first_name=req_body["firstName"],
            last_name=req_body["lastName"],
        )
    except IntegrityError as e:
        return HttpResponse(
            {"error": e.args[0]},
            content_type="application/json",
            status=status.HTTP_409_CONFLICT,
        )

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps(
        {
            "token": token.key,
            "id": new_user.id,
            "valid": True,
            "username": new_user.username,
        }
    )
    return HttpResponse(
        data, content_type="application/json", status=status.HTTP_201_CREATED
    )


@csrf_exempt
def login_user(request):
    body = request.body.decode("utf-8")
    req_body = json.loads(body)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":

        # Use the built-in authenticate method to verify
        username = req_body["username"]
        password = req_body["password"]
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps(
                {
                    "valid": True,
                    "token": token.key,
                    "id": authenticated_user.id,
                    "username": authenticated_user.username,
                }
            )
            return HttpResponse(data, content_type="application/json")

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type="application/json")

    return HttpResponseNotAllowed(permitted_methods=["POST"])


class UserViewSet(viewsets.ModelViewSet):
    def list(self, request):
        users = User.objects.all()

        # Get optional query params
        username = request.query_params.get("username", None)
        if username is not None:
            users = users.filter(username=username)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)

        # get optional query params
        embed = request.query_params.get("_embed", None)

        if embed is not None:
            if embed == "userTeams":
                serializer = UserSerializerEmbedded(user, many=False)
                return Response(serializer.data)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)

        # Get keys from the request body
        username = request.data.get("username", None)
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)

        if not username and not first_name and not last_name:
            return Response(
                {
                    "error": "Missing required fields. Please include at least one of the following: username, first_name, last_name."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update and save the instance
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name

        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
