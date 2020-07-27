from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.utils import timezone

###################################################
SYMBOL_TYPE_CHOICES = (
    ('0', "شاخص کل"),
    ('1', "نماد"),
    ('2', "شاخص صنعت"),
)
###################################################


class Category(models.Model): #ModelMeta
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='گروه بورسی')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    # _metadata = {
    #     'title': 'title',
    #     'description': 'description',
    #     'image': 'get_meta_image',
    # }

    class Meta:
        ordering = ["createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:category-detail", kwargs={'category_id': self.pk})

    # def get_meta_image(self):
    #     if self.pic:
    #         return self.pic.url


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='گروه')
    symbol = models.CharField(max_length=120, null=True, blank=True, help_text='نماد')
    fullName = models.CharField(max_length=120, null=True, blank=True, help_text='نام شرکت')
    alias = models.CharField(max_length=120, null=True, blank=True, help_text='نام معادل انگلیسی')
    type = models.CharField(max_length=20, help_text='نوع نماد', choices=SYMBOL_TYPE_CHOICES, default='1')
    bourseType = models.CharField(max_length=120, null=True, blank=True, help_text='بازار بورس')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    tse = models.URLField(null=True, blank=True, help_text='لینک tse')
    site = models.URLField(null=True, blank=True, help_text='وبسایت')
    isTarget = models.BooleanField(default=False, help_text='تحت نظر')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    hit_count = models.BigIntegerField(default=0)
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:company-detail", kwargs={'company_id': self.pk})


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    s = send_mail(
        # title
        "Password Reset for {title}".format(title="Media Bource"),
        # message:
        email_plaintext_message,
        # from:
        "amir.amiri2730567@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    print(s)
