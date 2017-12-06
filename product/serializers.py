from rest_framework import serializers

from django.db.models import Sum

from product.models import Item, Rating, UserItemRelation



class ItemSerializer(serializers.ModelSerializer):

    class Meta():
        model = Item
        fields = ["id", "name", "description", "price", "image"]


class ItemListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta():
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "rating",
        ]

    def get_rating(self, obj):
        user_items = UserItemRelation.objects.filter(item=obj.id)

        _sum = 0
        count = 0
        ratings = Rating.objects.all()

        if user_items:
            for user_item in user_items:
                rating = ratings.filter(user_item_relation=user_item)
                _sum += rating.first().rate
                count += 1
            try:
                average_rating = _sum / count
            except:
                average_rating = None
            return average_rating
        else:
            return None
