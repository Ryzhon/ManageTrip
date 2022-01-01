from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from users.models import CustomUser
from django.core.signals import request_finished
from trips.models import Trip, Todo, ChatModel
from django.db.models import F



@receiver(pre_save, sender=Trip)
def add_slug_to_question(sender, instance, *args, **kwargs):

    if instance and not instance.slug:
        slug = slugify(instance.content)
        random_string = get_random_string(length=8)
        instance.slug = slug + "-" + random_string
        ChatModel(room_slug=instance.slug).save()

@receiver(post_save, sender=Todo)
def calc_total_charge(sender, instance, *args, **kwargs):

    print(instance.author)
    print(instance.charge)
    print(instance.From)
    from_name = instance.From
    a = 0
    print(sender.objects.filter(From=instance.From).values("charge"))
    for i in sender.objects.filter(From=instance.From).values("charge"):

        a += i["charge"]
    print(a)
        

    # print(sender.objects.filter(author=instance.author).values("From"))
    CustomUser.objects.filter(username=instance.From).values("total_charge").update(total_charge=a)

# @receiver(post_save, sender=CustomUser)
# def change_total_charge(sender, instance, *args, **kwargs):
#     print(instance.total_charge)
#     print()




