from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Sum

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from product.models import Item, Rating, Buy, UserItemRelation
from product.serializers import ItemSerializer, ItemListSerializer
from . import messages
# Create your views here.


User = get_user_model()



class ItemView(ListAPIView):
    """
    ### GET

    #### Response:
    ```
    [
        {
            "id": Integer,
            "name": String,
            "description": String,
            "price": Float,
            "image": URL,
            "rating": Integer
        },
    ]
    ```
    """
    serializer_class = ItemListSerializer
    queryset = Item.objects.all()




class BuyItemView(APIView):

    def post(self, request, *args, **kwargs):
        """
        #### URL:
        Send item id through url.
        __url = "/buy/{item_id}/"__

        Data to be sent:

        #### Header:
        ```
        {
            "Authorization": "Token String"
        }
        ```

        #### Success:
        __status:__ 200
        ```
        {
            "detail": "Item is successfully purchased."
        }
        ```
        """
        try:
            user_id = request.auth.user_id
            user = User.objects.get(id=user_id)
        except:
            return Response(messages.USER_NOT_FOUND, status=status.HTTP_401_UNAUTHORIZED)

        item_id = int(kwargs['pk'])

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response(messages.ITEM_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_item_relation = UserItemRelation.objects.get(user=user, item=item)
        except UserItemRelation.DoesNotExist:
            user_item_relation = UserItemRelation.objects.create(user=user, item=item)
        except:
            return Response(messages.ERROR, status=status.HTTP_400_BAD_REQUEST)

        try:
            buy= Buy.objects.create(user_item_relation=user_item_relation)
        except:
            return Response(messages.ERROR, status=status.HTTP_400_BAD_REQUEST)

        return Response(messages.BUY_ITEM_SUCCESS, status=status.HTTP_200_OK)



class ProductRateView(APIView):

    def post(self, request, *args, **kwargs):
        """
        Data to be sent:

        #### Header:
        ```
        {
            "Authorization": "Token String"
        }
        ```

        #### Body:
        ```
        {
            "rate": Integer
        }
        ```

        #### URL:
        Send item id through url.
        __url = "/buy/{item_id}/"__


        ### Response:
        __Success:__ status:201
        ```
        {
            "detail": "Product has been successfully rated."
        }
        ```


        """
        data = request.data.copy()
        try:
            user_id = request.auth.user_id
            user = User.objects.get(id=user_id)
        except:
            return Response(messages.USER_NOT_FOUND, status=status.HTTP_401_UNAUTHORIZED)


        try:
            item_id = int(kwargs["pk"])
            item = Item.objects.get(id=item_id)
        except:
            return Response(messages.ITEM_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)


        try:
            rate = data["rate"]
        except KeyError:
            return Response(messages.RATING_NOT_SUPPLIED, status=status.HTTP_400_BAD_REQUEST)


        user_item = UserItemRelation.objects.filter(user=user, item=item)
        if user_item:
            user_item_relation = user_item.first()
            buy = Buy.objects.filter(user_item_relation=user_item_relation)
        else:
            return Response(messages.CANNOT_RATE, status=status.HTTP_400_BAD_REQUEST)


        if buy:
            check_rating = Rating.objects.filter(user_item_relation=user_item_relation).exists()
            print(check_rating)
            if not check_rating:
                rating = Rating.objects.create(user_item_relation=user_item_relation, rate=rate)
                return Response(messages.PRODUCT_RATED, status=status.HTTP_201_CREATED)
            else:
                return Response(messages.ERROR, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(messages.CANNOT_RATE, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        """
        Data to be sent:

        #### Header:
        ```
        {
            "Authorization": "Token String"
        }
        ```

        #### Body:
        ```
        {
            "rate": Integer
        }
        ```

        #### URL:
        Send item id through url.
        __url = "/buy/{item_id}/"__


        ### Response:
        __Success:__ status:201
        ```
        {
            "detail": "Product has been successfully rated."
        }
        ```


        """
        data = request.data.copy()
        try:
            user_id = request.auth.user_id
            user = User.objects.get(id=user_id)
        except:
            return Response(messages.USER_NOT_FOUND, status=status.HTTP_401_UNAUTHORIZED)


        try:
            item_id = int(kwargs["pk"])
            item = Item.objects.get(id=item_id)
        except:
            return Response(messages.ITEM_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)


        try:
            rate = data["rate"]
        except KeyError:
            return Response(messages.RATING_NOT_SUPPLIED, status=status.HTTP_400_BAD_REQUEST)


        user_item = UserItemRelation.objects.filter(user=user, item=item)
        if user_item:
            user_item_relation = user_item.first()
        else:
            return Response(messages.ERROR, status=status.HTTP_400_BAD_REQUEST)


        try:
            rating = Rating.objects.filter(user_item_relation=user_item_relation)
            if rating:
                rating = rating.first()
                rating.rate = rate
                rating.save()
                return Response(messages.PRODUCT_RATE_UPDATED, status=status.HTTP_200_OK)
            else:
                return Response(messages.CANNOT_RATE, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(messages.ERROR, status=status.HTTP_400_BAD_REQUEST)
