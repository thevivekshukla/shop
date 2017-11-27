from rest_framework import serializers

from product.models import Item, Rating



class ItemSerializer(serializers.ModelSerializer):

    class Meta():
        model = Item
        fields = ["id", "name", "description", "price", "image"]
