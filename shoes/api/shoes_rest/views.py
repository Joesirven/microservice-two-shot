from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from common.json import ModelEncoder
from .models import Shoe, BinVO

# Create your views here.

class BinVOEncoder(ModelEncoder):
    model = BinVO
    properties = [
        "closet_name",
        "bin_number",
        "import_href",
    ]

class ShoeEncoder(ModelEncoder):
    model = Shoe
    properties = [
        "id",
        "manufacturer",
        "model_name",
        "color",
        "picture",
        "bin",
    ]
    encoders = {
        "bin": BinVOEncoder()
    }



@require_http_methods(["GET", "POST"])
def api_shoes(request):
    """
    Collection RESTful API handler for Shoe objects in
    the wardrobe.

    GET:
    Returns a dictionary with a single key "shoes" which
    is a list of the manufacturer, model name, color, and picture, along with its href and id.

    {
        "shoes": [
            {
                "id": database id for the location,
                "manufacturer": shoe's manufacturer,
                "model_name": the model name of the shoe,
                "color": the color of the shoe,
                "picture": a url to a picture of the shoe,
                "href": URL to the shoe object,
            },
            ...
        ]
    }

    POST:
    Creates a location resource and returns its details.
    {
        "manufacturer": shoe's manufacturer,
        "model_name": the model name of the shoe,
        "color": the color of the shoe,
        "picture": url to a picture of the shoe,
    }
    """
    if request.method == "GET":
        shoes = Shoe.objects.all()
        return JsonResponse(
            {"shoes": shoes},
            encoder=ShoeEncoder,
        )
    else: #POST
        content = json.loads(request.body)

        try:
            id = content['bin']
            href = f"/api/bins/{id}/"
            binvo_object = BinVO.objects.get(import_href=href)
            content["bin"] = binvo_object
        except BinVO.DoesNotExist:
            return JsonResponse(
                {"message": "Bin object id does not exist"},
                status=400,
            )
        shoe = Shoe.objects.create(**content)
        return JsonResponse(
            shoe,
            encoder=ShoeEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_shoe(request, pk):
    """
    Single-object API for the Shoe resource.

    GET:
    Returns the information for a Shoe resource based
    on the value of pk
    {
        "id": database id for the location,
        "manufacturer": shoe's manufacturer,
        "model_name": the model name of the shoe,
        "color": the color of the shoe,
        "picture": a url to a picture of the shoe,
        "href": URL to the shoe object,
    }

    PUT:
    Updates the information for a Shoe resource based
    on the value of the pk
    {
        "manufacturer": shoe's manufacturer,
        "model_name": the model name of the shoe,
        "color": the color of the shoe,
        "picture": a url to a picture of the shoe,
    }

    DELETE:
    Removes the shoe resource from the application
    """
    if request.method == "GET":
        try:
            shoe = Shoe.objects.get(id=pk)
            return JsonResponse(
                shoe,
                encoder=ShoeEncoder,
                safe=False
            )
        except Shoe.DoesNotExist:
            response = JsonResponse({"message": "Does not exist"})
            response.status_code = 404
            return response
    elif request.method == "DELETE":
        try:
            shoe = Shoe.objects.get(id=pk)
            shoe.delete()
            return JsonResponse(
                shoe,
                encoder=ShoeEncoder,
                safe=False,
            )
        except Shoe.DoesNotExist:
            return JsonResponse({"message": "Does not exist"})
    else: # PUT
        try:
            content = json.loads(request.body)
            shoe = Shoe.objects.get(id=pk)

            props = ["manufacturer", "model_name", "color", "picture",]
            for prop in props:
                if prop in content:
                    setattr(shoe, prop, content[prop])
            shoe.save()
            return JsonResponse(
                shoe,
                encoder=ShoeEncoder,
                safe=False,
            )
        except Shoe.DoesNotExist:
            response = JsonResponse({"message": "Does not exist"})
            response.status_code = 404
            return response
