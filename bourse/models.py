from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from ckeditor.fields import RichTextField
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from private_storage.fields import PrivateFileField


def validate_phone_number(value):
    if value and is_number(value) and \
            is_valid_phone_number(value) and \
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


def validate_image(image):
    min_height = 200
    min_width = 200
    height = image.height
    width = image.width
    if width < min_width or height < min_height:
        raise ValidationError("سایز عکس باید از 200 * 200 بیشتر باشد!")


def validate_watchlist_items(watchlist):
    if WatchListItem.objects.filter(watch_list_id=watchlist).count() >= 20:
        raise ValidationError('شما نمی توانید بیش از 20 نماد در یک دیده بان ذخیره نمایید.')


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
            raise ValueError('شماره موبایل معتبر نسیت.')
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
    """
    Custom user model that support phone number instead of username
    """

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
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
    picture = models.ImageField(
        upload_to='uploads/image/user',
        null=True,
        blank=True,
        validators=[validate_image]
    )
    national_code = models.IntegerField(
        null=True,
        blank=True
    )
    father_name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    birth_date = models.DateField(null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True, unique=True)
    address = models.TextField(null=True, blank=True)
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
    created_on = models.DateField(auto_now_add=True, )
    logo = models.ImageField(
        upload_to='uploads/images/category/',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

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
        upload_to='uploads/images/company/',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    created_on = models.DateField(auto_now_add=True)
    tse = models.URLField(help_text='لینک tse')
    site = models.URLField(
        null=True,
        blank=True,
        help_text='وبسایت'
    )
    # isTarget = models.BooleanField(default=False, help_text='تحت نظر')
    hit_count = models.BigIntegerField(default=0)
    description = models.TextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

    def __str__(self):
        return self.symbol

    @property
    def news(self):
        return self.news_set.all()


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

    def __str__(self):
        return f'{self.user}, {self.name}'

    @property
    def item(self):
        return self.watchlistitem_set.all()


class WatchListItem(models.Model):
    watch_list = models.ForeignKey(
        WatchList,
        on_delete=models.CASCADE,
        validators=(validate_watchlist_items,)
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('watch_list', 'company',)

    def __str__(self):
        return f'{self.watch_list.name}, {self.company.symbol}'


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user}, {self.company.name}'


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
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    pic = models.ImageField(
        upload_to='uploads/images/news/',
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
    is_approved = models.BooleanField(
        default=False,
        help_text='تایید خبر'
    )
    is_important = models.BooleanField(
        default=False,
        help_text='خبر مهم'
    )
    hit_count = models.BigIntegerField(default=0)
    short_description = models.TextField(
        help_text='توضیحات کوتاه'
    )
    description = RichTextField(
        help_text='توضیحات'
    )

    def __str__(self):
        return self.title


class Filter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    filter_content = models.TextField(
        null=False,
        blank=False
    )

    def __str__(self):
        return f'{self.user}, {self.name}'


class Technical(models.Model):
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
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    video = models.FileField(
        upload_to='uploads/videos/technical/',
        null=True,
        blank=True,
        help_text='فایل ویدیو'
    )
    audio = models.FileField(
        upload_to='upload/audio/technical',
        null=True,
        blank=True,
        help_text='فایل صوتی'
    )
    image = models.ImageField(
        upload_to='upload/image/technical',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    title = models.CharField(
        max_length=255,
        help_text='عنوان'
    )
    aparat_embed_code = models.TextField(
        null=True,
        blank=True,
        help_text='کد امبد آپارات'
    )
    hit_count = models.BigIntegerField(default=0)
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

    def __str__(self):
        return self.company.symbol


class ChatMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sender_user',
        on_delete=models.CASCADE,
        help_text='فرستنده'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='receiver_user',
        on_delete=models.CASCADE,
        help_text='گیرنده'
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    is_seen = models.BooleanField(
        default=False,
        help_text='مشاهده شده'
    )
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

    def __str__(self):
        return str(self.sender)


class Webinar(models.Model):
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
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    video = models.FileField(
        upload_to='uploads/videos/webinar/',
        null=True,
        blank=True,
        help_text='فایل ویدیو'
    )
    audio = models.FileField(
        upload_to='upload/audio/webinar',
        null=True,
        blank=True,
        help_text='فایل صوتی'
    )
    image = models.ImageField(
        upload_to='upload/image/webinar',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    title = models.CharField(
        max_length=120,
        help_text='عنوان'
    )
    aparat_embed_code = models.TextField(
        null=True,
        blank=True,
        help_text='کد امبد آپارات'
    )
    hit_count = models.BigIntegerField(default=0)
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

    def __str__(self):
        return self.company.symbol


class Fundamental(models.Model):
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
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    image = models.ImageField(
        upload_to='uploads/image/fundamental',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    title = models.CharField(
        max_length=255,
        help_text='عنوان'
    )
    hit_count = models.BigIntegerField(default=0)
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

    def __str__(self):
        return self.company.symbol


class Bazaar(models.Model):
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
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    image = models.ImageField(
        upload_to='uploads/image/bazaar',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    title = models.CharField(
        max_length=255,
        help_text='عنوان'
    )
    aparat_embed_code = models.TextField(
        null=True,
        blank=True,
        help_text='کد امبد آپارات'
    )
    hit_count = models.BigIntegerField(default=0)
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )

    def __str__(self):
        return self.company.symbol


class Chart(models.Model):
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    last_candle_date = models.DateField(help_text='تاریخ ایجاد')
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        help_text='نماد'
    )
    timeFrame = models.CharField(
        max_length=20,
        help_text='تایم فریم',
        choices=TIME_FRAME_CHOICES,
        default='D1'
    )
    data = models.FileField(
        upload_to='uploads/file/chart/',
        null=True,
        blank=True,
        help_text='فایل csv,  prn, txt چارت نماد'
    )

    def __str__(self):
        return self.company.symbol


class UserTechnical(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        help_text='نماد'
    )
    title = models.CharField(
        max_length=255,
        help_text='نام فایل'
    )
    is_share = models.BooleanField(default=False, help_text='اجازه اشتراک گذاری')
    data = models.TextField(help_text='فایل متنی شده json')

    def __str__(self):
        return self.company.symbol


class TutorialCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    title = models.CharField(
        max_length=255,
        help_text='عنوان'
    )
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    image = models.ImageField(
        'uploads/image/tutorial-category',
        null=True,
        blank=True,
        help_text='تصویر'
    )

    def __str__(self):
        return self.title


class TutorialSubCategory(models.Model):
    CATEGORY_LEVEL_CHOICES = (
        ('0', "مقدماتی"),
        ('1', "پیشرفته"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    category = models.ForeignKey(
        TutorialCategory,
        on_delete=models.CASCADE,
        help_text='دسته بندی'
    )
    title = models.CharField(
        max_length=255,
        help_text='عنوان'
     )
    description = RichTextField(
        null=True,
        blank=True,
        help_text='توضیحات'
    )
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    category_level = models.CharField(
        max_length=20,
        help_text='سطح آموزش',
        choices=CATEGORY_LEVEL_CHOICES,
        default='0'
    )
    image = models.ImageField(
        upload_to='uploads/image/tutorial-subcategory',
        null=True,
        blank=True,
        help_text='تصویر'
    )

    def __str__(self):
        return self.title


class Tutorial(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    title = models.CharField(max_length=255, help_text='عنوان')
    sub_category = models.ForeignKey(
        TutorialSubCategory,
        on_delete=models.CASCADE,
        help_text='زیر دسته بندی'
    )
    external_link = models.URLField(
        null=True,
        blank=True,
        help_text='لینک آموزش'
    )
    aparat_embed_code = models.TextField(
        null=True,
        blank=True,
        help_text='کد امبد آپارات'
    )
    hit_count = models.BigIntegerField(default=0)
    description = RichTextField(null=True, blank=True, help_text='توضیحات')

    @property
    def tutorial_files(self):
        return self.tutorialfile_set.all()

    def __str__(self):
        return self.title


class TutorialFile(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    file = PrivateFileField("File")

    def __str__(self):
        return self.tutorial.title


class TutorialOwner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    tutorial = models.ForeignKey(
        Tutorial,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user}, {self.tutorial.title}'


class CompanyFinancial(models.Model):
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
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    file = models.FileField(
        upload_to='uploads/file/company-financial/',
        null=True,
        blank=True,
        help_text='فایل'
    )
    previousFinancialPeriodProfitability = models.IntegerField(
        default=0,
        help_text='سودآوری-دوره مالی قبل'
    )
    previousFinancialPeriodSell = models.IntegerField(
        default=0,
        help_text='فروش-دوره مالی قبل'
    )
    previousFinancialPeriodProduction = models.IntegerField(
        default=0,
        help_text='تولی-دوره مالی قبلد'
    )
    previousFinancialPeriodAccumulatedProfits = models.IntegerField(
        default=0,
        help_text='سود انباشته-دوره مالی قبل'
    )
    previousFinancialPeriodSymbolPrice = models.IntegerField(
        default=0,
        help_text='قیمت سهم-دوره مالی قبل'
    )
    newFinancialPeriodProfitability = models.IntegerField(
        default=0,
        help_text='سودآوری-دوره مالی جدید'
    )
    newFinancialPeriodSell = models.IntegerField(
        default=0,
        help_text='فروش-دوره مالی جدید'
    )
    newFinancialPeriodProduction = models.IntegerField(
        default=0,
        help_text='تولید-دوره مالی جدید'
    )
    newFinancialPeriodAccumulatedProfits = models.IntegerField(
        default=0,
        help_text='سود انباشته-دوره مالی جدید'
    )
    newFinancialPeriodSymbolPrice = models.IntegerField(
        default=0,
        help_text='قیمت سهم-دوره مالی جدید'
    )
    forecastProfitability = models.IntegerField(
        default=0,
        help_text='سودآوری-پیشبینی'
    )
    forecastSell = models.IntegerField(
        default=0,
        help_text='فروش-پیشبینی'
    )
    forecastProduction = models.IntegerField(
        default=0,
        help_text='تولید-پیشبینی'
    )
    forecastAccumulatedProfits = models.IntegerField(
        default=0,
        help_text='سود انباشته-پیشبینی'
    )
    forecastSymbolPrice = models.IntegerField(
        default=0,
        help_text='قیمت سهم-پیشبینی'
    )

    def __str__(self):
        return self.company.symbol


class UserComment(models.Model):
    COMMENT_FOR = (
        ('0', 'تحلیل تکنیکال'),
        ('1', 'تحلیل بنیادی'),
        ('2', 'وبینار'),
        ('3', 'اخبار'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'UserComment',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    technical = models.ForeignKey(
        Technical,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fundamental = models.ForeignKey(
        Fundamental,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    comment_for = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        choices=COMMENT_FOR
    )
    text = models.TextField(
        null=False,
        blank=False
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.text}, {self.comment_for}'


class FileRepository(models.Model):
    TYPE_CHOICES = (
        ('1', 'آموزش'),
        ('2', 'وبینار'),
        ('3', 'تبلیغات'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    file = models.FileField(
        upload_to='uploads/file/file-repository',
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    file_tag = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    type = models.CharField(null=False, choices=TYPE_CHOICES, max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class Note(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    technical = models.ForeignKey(
        Technical,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fundamental = models.ForeignKey(
        Fundamental,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    text = models.TextField(
        null=False,
        blank=False
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.text}'


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    technical = models.ForeignKey(
        Technical,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fundamental = models.ForeignKey(
        Fundamental,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class HitCount(models.Model):
    ip = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    technical = models.ForeignKey(
        Technical,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fundamental = models.ForeignKey(
        Fundamental,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    bazaar = models.ForeignKey(
        Bazaar,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    tutorial = models.ForeignKey(
        Tutorial,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ip
