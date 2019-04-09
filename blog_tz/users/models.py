from django.db import models
from django.conf import settings
from PIL import Image
from django.utils import timezone

# from django.db.models.signals import post_save
# from django.dispatch import receiver



def save_image_path(instance, filename):
    filename = instance.image
    return 'profile_pics/{}/{}'.format(instance.user.username, filename)



class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name = 'subscriber')
    city = models.CharField(max_length = 25)
    country = models.CharField(max_length = 25)
    birthday = models.CharField(max_length = 25)
    image = models.ImageField(default='default.jpg', upload_to=save_image_path, blank = True)

    # email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # resize of image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']

#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Subscriber.objects.create(user=instance)
#     instance.profile.save()