from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()


def upload_item_image(instance, filename):
    new_id = None
    try:
        new_id = Item.objects.all().last().id + 1
    except:
        new_id = 1
    try:
        if instance.id:
            new_id = instance.id
    except:
        pass

    return "{}/{}/{}".format("item", new_id, filename)


class Item(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_item_image)

    def __str__(self):
        return self.name


class UserItemRelation(models.Model):

    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)

    def __str__(self):
        return "{} bought {}".format(self.user.username, self.item.name)


class Buy(models.Model):

    user_item_relation = models.ForeignKey(UserItemRelation)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_item_relation)

    class Meta():
        verbose_name_plural = "Buy"


class IntegerRangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value':self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Rating(models.Model):

    user_item_relation = models.OneToOneField(UserItemRelation, related_name='rating')
    rate = IntegerRangeField(min_value=1, max_value=5)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_item_relation)

    class Meta():
        verbose_name_plural = "Rating"
