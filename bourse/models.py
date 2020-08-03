import jsonfield as jsonfield
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from ckeditor.fields import RichTextField
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if value and is_number(value) and\
            is_valid_phone_number(value) and\
            len(value) == 11:
        return value
    else:
        raise ValidationError("یک شماره تلفن معتبر وارد کنید.")


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_valid_phone_number(number):
    if number[0] == '0' and number[1] == '9':
        return True
    else:
        return False


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password, email=None,
                    **extra_fields):
        """Create and save a new user"""
        if phone_number and \
                is_number(phone_number) and \
                is_valid_phone_number(phone_number) and \
                len(phone_number) == 11:
            pass
        else:
            raise ValueError('Phone number is invalid!')
        if email:
            email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password):
        """create and save new super user"""
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support email instead of username"""
    name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(
        validators=[validate_phone_number],
        max_length=11,
        unique=True,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    generated_token = models.IntegerField(
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    title = models.CharField(
        max_length=255,
        help_text='گروه بورسی'
    )
    created_on = models.DateField(auto_now_add=True,)
    logo = models.ImageField(
        upload_to='uploads/category/',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    description = models.TextField(null=True, blank=True, help_text='توضیحات')

    def __str__(self):
        return self.title


class Company(models.Model):

    SYMBOL_TYPE_CHOICES = (
        ('0', "شاخص کل"),
        ('1', "نماد"),
        ('2', "شاخص صنعت"),
    )
    BOURSE_TYPE_CHOICES = (
        ('0', "تابلو اصلی بازار اول بورس"),
        ('1', "تابلو فرعی بازار اول بورس"),
        ('2', "بازار دوم بورس"),
        ('3', "بازار اول فرابورس"),
        ('4', "بازار دوم فرابورس"),
        ('5', "بازار پایه زرد فرابورس"),
        ('6', "بازار پایه نارنجی فرابورس"),
        ('7', "بازار پایه قرمز فرابورس"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='گروه'
    )
    symbol = models.CharField(
        max_length=255,
        unique=True,
        help_text='نماد'
    )
    name = models.CharField(
        max_length=255,
        help_text='نام شرکت'
    )
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='نام معادل انگلیسی'
    )
    type = models.CharField(
        max_length=255,
        help_text='نوع نماد',
        choices=SYMBOL_TYPE_CHOICES,
        default='1'
    )
    bourse_type = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        choices=BOURSE_TYPE_CHOICES,
        help_text='بازار بورس'
    )
    image = models.ImageField(
        upload_to='uploads/company/',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    created_on = models.DateField(auto_now_add=True)
    tse = models.URLField(help_text='لینک tse')
    site = models.URLField(null=True, blank=True, help_text='وبسایت')
    # isTarget = models.BooleanField(default=False, help_text='تحت نظر')
    hit_count = models.BigIntegerField(default=0)
    description = models.TextField(null=True, blank=True, help_text='توضیحات')

    def __str__(self):
        return self.symbol


class RequestSymbol(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        help_text='نماد'
    )
    is_analyzed = models.BooleanField(
        default=False,
        help_text='آیا تحلیل برای این نماد انجام گرفته'
    )
    analyzed_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ تحلیل'
    )
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )


class WatchList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text='نام دیده بان'
    )


class WatchListItem(models.Model):
    watch_list = models.ForeignKey(
        WatchList,
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )


class News(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='در صورت اختصاص خبر برای گروه انتخاب شود'
    )
    company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='در صورت اختصاص خبر برای نماد انتخاب شود'
    )
    title = models.CharField(
        max_length=255,
        help_text='عنوان'
    )
    reference = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text='مرجع'
    )
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    pic = models.ImageField(
        upload_to='uploads/news/',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    tag = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text='برچسب'
    )
    is_approved = models.BooleanField(default=False, help_text='تایید خبر')
    is_important = models.BooleanField(default=False, help_text='خبر مهم')
    hit_count = models.BigIntegerField(default=0)
    short_description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        help_text='توضیحات کوتاه'
    )
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

# kharabe, bayad doros she

class Technical(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    video = models.FileField(upload_to='videos/', null=True, blank=True, help_text='فایل ویدیو')
    audio = models.FileField(upload_to='audio/', null=True, blank=True, help_text='فایل صوتی')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:technical-detail", kwargs={'technical_id': self.pk})


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_user', on_delete=models.CASCADE, null=True, blank=True,
                             help_text='فرستنده')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver_user', on_delete=models.CASCADE, null=True, blank=True,
                             help_text='گیرنده')
    createAt = models.DateTimeField(default=timezone.now, help_text='تاریخ ایجاد')
    isSeen = models.BooleanField(default=False, help_text='مشاهده شده')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return str(self.sender)

    @property
    def owner(self):
        return self.sender


class Webinar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:webinar-detail", kwargs={'webinar_id': self.pk})


class MapBazaar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __unicode__(self):
        return self.createAt

    @property
    def owner(self):
        return self.user


class Fundamental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:fundamental-detail", kwargs={'fundamental_id': self.pk})


class Bazaar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:bazaar-detail", kwargs={'bazaar_id': self.pk})


TIME_FRAME_CHOICES = (
    ('M1', "1 دقیقه"),
    ('M5', "5 دقیقه"),
    ('M15', "15 دقیقه"),
    ('M30', "30 دقیقه"),
    ('H1', "۱ ساعت"),
    ('H4', "4 ساعت"),
    ('D1', "1 روز"),
    ('W1', "1 هفته"),
    ('MN1', "1 ماه"),
)


class Chart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    lastCandleDate = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    timeFrame = models.CharField(max_length=20, help_text='تایم فریم', choices=TIME_FRAME_CHOICES, default='D1')
    data = models.FileField('uploaded chart file', upload_to='charts/', null=True, blank=True, help_text='فایل csv,  prn, txt چارت نماد')

    class Meta:
        ordering = ["-lastCandleDate"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class TechnicalUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    created_on = models.DateTimeField(auto_now_add=True, help_text='تاریخ ایجاد')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='نام فایل')
    isShare = models.BooleanField(default=False, help_text='اجازه اشتراک گذاریا')
    # data = models.TextField(null=True, blank=True, help_text='فایل متنی شده json')
    data = jsonfield.JSONField(help_text='فایل متنی شده json')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class TutorialCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextField(null=True, blank=True, help_text='توضیحات')
    createAt = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


CATEGORY_LEVEL_CHOICES = (
    ('0', "مقدماتی"),
    ('1', "پیشرفته"),
)


class TutorialSubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE, null=True, blank=True, help_text='دسته بندی')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextField(null=True, blank=True, help_text='توضیحات')
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    categoryLevel = models.CharField(max_length=20, help_text='سطح آموزش', choices=CATEGORY_LEVEL_CHOICES,
                                default='0')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


class Tutorial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    file = models.FileField('uploaded file', null=True, blank=True, help_text='فایل')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    # category = models.CharField(max_length=120, null=True, blank=True, help_text='دسته آموزش', choices=CATEGORY_CHOICES,
    #                             default='تحلیل بازار')
    subCategory = models.ForeignKey(TutorialSubCategory, on_delete=models.CASCADE, null=True, blank=True, help_text='زیر دسته بندی')
    externalLink = models.URLField(null=True, blank=True, help_text='لینک آموزش')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    description = RichTextField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:tutorial-detail", kwargs={'tutorial_id': self.pk})


class CompanyFinancial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    file = models.FileField(upload_to='CompanyFinancial/', null=True, blank=True, help_text='فایل')
    previousFinancialPeriodProfitability = models.IntegerField(default=0, help_text='سودآوری-دوره مالی قبل')
    previousFinancialPeriodSell = models.IntegerField(default=0, help_text='فروش-دوره مالی قبل')
    previousFinancialPeriodProduction = models.IntegerField(default=0, help_text='تولی-دوره مالی قبلد')
    previousFinancialPeriodAccumulatedProfits = models.IntegerField(default=0, help_text='سود انباشته-دوره مالی قبل')
    previousFinancialPeriodSymbolPrice = models.IntegerField(default=0, help_text='قیمت سهم-دوره مالی قبل')
    newFinancialPeriodProfitability = models.IntegerField(default=0, help_text='سودآوری-دوره مالی جدید')
    newFinancialPeriodSell = models.IntegerField(default=0, help_text='فروش-دوره مالی جدید')
    newFinancialPeriodProduction = models.IntegerField(default=0, help_text='تولید-دوره مالی جدید')
    newFinancialPeriodAccumulatedProfits = models.IntegerField(default=0, help_text='سود انباشته-دوره مالی جدید')
    newFinancialPeriodSymbolPrice = models.IntegerField(default=0, help_text='قیمت سهم-دوره مالی جدید')
    forecastProfitability = models.IntegerField(default=0, help_text='سودآوری-پیشبینی')
    forecastSell = models.IntegerField(default=0, help_text='فروش-پیشبینی')
    forecastProduction = models.IntegerField(default=0, help_text='تولید-پیشبینی')
    forecastAccumulatedProfits = models.IntegerField(default=0, help_text='سود انباشته-پیشبینی')
    forecastSymbolPrice = models.IntegerField(default=0, help_text='قیمت سهم-پیشبینی')

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class FileRepository(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    file = models.FileField('uploaded file', upload_to='files/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    fileTag = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ["-createAt"]

    @property
    def owner(self):
        return self.user


##################################################################################################
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

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
