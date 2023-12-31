from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from common.json import ModelEncoder
from .models import Hat, LocationVO

# Create your views here.


class LocationVOEncoder(ModelEncoder):
    model = LocationVO
    properties = [
        "closet_name",
        "section_number",
        "shelf_number",
        "import_href",
    ]


class HatEncoder(ModelEncoder):
    model = Hat
    properties = [
        "id",
        "fabric",
        "style",
        "color",
        "picture_url",
        "wardrobe_location",
    ]
    encoders = {
        "wardrobe_location": LocationVOEncoder()
    }


@require_http_methods(["GET", "POST"])
def api_hats(request):
    """
    Collection RESTful API handler for Hat objects in
    the wardrobe.

    GET:
    Returns a dictionary with a single key "hats" which
    is a list of the fabric, style, color, and picture, along with its href and id.

    {
        "hats": [
            {
                "id": database id for the location,
                "manufacturer": Hat's manufacturer,
                "model_name": the model name of the Hat,
                "color": the color of the Hat,
                "picture": a url to a picture of the Hat,
                "href": URL to the Hat object,
            },
            ...
        ]
    }

    POST:
    Creates a Hat resource and returns its details.
    {
        "manufacturer": Hat's manufacturer,
        "model_name": the model name of the Hat,
        "color": the color of the Hat,
        "picture": url to a picture of the Hat,
    }
    """
    if request.method == "GET":
        hats = Hat.objects.all()
        return JsonResponse(
            {"hats": hats},
            encoder=HatEncoder,
        )
    else:  #POST
        content = json.loads(request.body)
        locationvo = LocationVO.objects.all()
        print(locationvo)
        try:
            href = f"/api/locations/{content['wardrobe_location']}/"
            print(href)
            location_vo_object = LocationVO.objects.get(import_href=href)
            print(location_vo_object)
            content["wardrobe_location"] = location_vo_object
        except LocationVO.DoesNotExist:
            return JsonResponse(
                {"message": "Bin object does not exist"},
                status=400,
            )
        hat = Hat.objects.create(**content)
        return JsonResponse(
            hat,
            encoder=HatEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_hat(request, pk):
    """
    Single-object API for the Hat resource.

    GET:
    Returns the information for a Hat resource based
    on the value of pk
    {
        "id": database id for the location,
        "manufacturer": Hat's manufacturer,
        "model_name": the model name of the Hat,
        "color": the color of the Hat,
        "picture": a url to a picture of the Hat,
        "href": URL to the Hat object,
    }

    PUT:
    Updates the information for a Hat resource based
    on the value of the pk
    {
        "manufacturer": Hat's manufacturer,
        "model_name": the model name of the Hat,
        "color": the color of the Hat,
        "picture": a url to a picture of the Hat,
    }

    DELETE:
    Removes the Hat resource from the application
    """
    if request.method == "GET":
        try:
            hat = Hat.objects.get(id=pk)
            return JsonResponse(
                hat,
                encoder=HatEncoder,
                safe=False
            )
        except Hat.DoesNotExist:
            response = JsonResponse({"message": "Does not exist"})
            response.status_code = 404
            return response
    elif request.method == "DELETE":
        try:
            hat = Hat.objects.get(id=pk)
            hat.delete()
            return JsonResponse(
                hat,
                encoder=HatEncoder,
                safe=False,
            )
        except Hat.DoesNotExist:
            return JsonResponse({"message": "Does not exist"})
    else: # PUT
        try:
            content = json.loads(request.body)
            hat = Hat.objects.get(id=pk)

            props = ["manufacturer", "model_name", "color", "picture",]
            for prop in props:
                if prop in content:
                    setattr(hat, prop, content[prop])
            hat.save()
            return JsonResponse(
                hat,
                encoder=HatEncoder,
                safe=False,
            )
        except Hat.DoesNotExist:
            response = JsonResponse({"message": "Does not exist"})
            response.status_code = 404
            return response
