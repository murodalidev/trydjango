import random
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

from articles.models import Article


def article_pre_save(instance, sender, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)
        article_slugs = [i[0] for i in sender.objects.values_list('slug')]
        if instance.slug in article_slugs:
            randon_numbers = random.randint(1000, 9999)
            instance.slug += str(randon_numbers)
    return instance


# def article_post_save(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.slug = slugify(instance.title)
#         instance.save()
#     return instance


pre_save.connect(article_pre_save, sender=Article)
# post_save.connect(article_post_save, sender=Article)
