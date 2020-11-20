import os

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from ckeditor.fields import RichTextField
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import jsonfield

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

    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
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

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'


# class Category(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         help_text='کاربر'
#     )
#     title = models.CharField(
#         max_length=255,
#         help_text='گروه بورسی'
#     )
#     created_on = models.DateField(auto_now_add=True)
#     logo = models.ImageField(
#         upload_to='uploads/images/category/',
#         null=True,
#         blank=True,
#         help_text='تصویر'
#     )
#     description = models.TextField(
#         null=True,
#         blank=True,
#         help_text='توضیحات'
#     )
# 
#     def __str__(self):
#         return self.title


class Meta(models.Model):
    version = models.BigIntegerField(primary_key=True, help_text='نسخه فیلد')
    state = models.CharField(max_length=255, null=True, blank=True, help_text='وضعیت')
    insert_date_time = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ درج اطلاعات')
    update_date_time = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ به روز رسانی')
    type = models.CharField(max_length=255, null=True, blank=True, help_text='نوع')

    def __str__(self):
        return str(self.version)


#   انواع وضعیت دارایی‌ها
class Assetstate(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    english_title = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')

    def __str__(self):
        return self.title


#  انواع دارایی
class Assettype(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    english_title = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد شاخص')
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')

    def __str__(self):
        return self.title


# دسته بندی‌های اوراق مشارکت
class Category(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='اطلاعات رکورد')
    parent_id = models.CharField(max_length=255, null=True, blank=True, help_text='دسته بندی مادر')
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد دسته بندی')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='نام دسته بندی')
    english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه دسته بندی')
    english_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه انگلیسی دسته بندی')

    def __str__(self):
        return self.name


# شاخص ها
class Index(models.Model):
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد شاخص')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='نام فارسی')
    english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام فارسی خلاصه')
    english_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی خلاصه')
    fingilish_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام فینگلیش')
    fingilish_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام فینگلیش خلاصه')
    id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name


#  بازارها
class Exchange(models.Model):
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد شاخص')
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    english_title = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.title


#  صندوق‌های سرمایه گذاری
class Fund(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد صندوق')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='نام صندوق')
    english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی صندوق')
    short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه صندوق')
    english_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه انگلیسی صندوق')
    trade_symbol = models.CharField(max_length=255, null=True, blank=True, help_text='نماد معاملاتی')
    website = models.CharField(max_length=255, null=True, blank=True, help_text='وبسایت')
    inception_date = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ شروع به کار صندوق')
    manager_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام مدیر صندوق')
    manager_english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی مدیر صندوق')
    investment_manager_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام مدیر سرمایه گذاری صندوق')
    investment_manager_english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی مدیر سرمایه گذاری صندوق')
    custodian_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام متولی صندوق')
    custodian_english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی متولی صندوق')
    liquidity_guarantor_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام ضامن نقد شوندگی صندوق')
    liquidity_guarantor_english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی ضامن نقد شوندگی صندوق')

    state = models.ForeignKey(Assetstate, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')

    def __str__(self):
        return self.name


#   انواع وضعیت شرکت ها
class Companystate(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')

    def __str__(self):
        return self.title


# دسته بندی‌های اوراق مشارکت
class Company(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False, help_text='نام دسته بندی')
    english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه دسته بندی')
    english_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه انگلیسی شرکت')
    trade_symbol = models.CharField(max_length=255, null=True, blank=True, help_text='نماد معاملاتی')
    english_trade_symbol = models.CharField(max_length=255, null=True, blank=True, help_text='نماد معاملاتی انگلیسی')
    description = models.TextField(null=True, blank=True, help_text='توصیحات')
    fiscalyear = models.CharField(max_length=255, null=True, blank=True, help_text='سال مالی')

    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='اطلاعات رکورد')
    state = models.ForeignKey(Companystate, on_delete=models.CASCADE, null=True, blank=True, help_text='وضعیت شرکت')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار معاملاتی')

    def __str__(self):
        return self.name


# دارایی‌ها
class Asset(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    trade_symbol = models.CharField(max_length=255, null=True, blank=True, help_text='نماد معاملاتی')
    english_trade_symbol = models.CharField(max_length=255, null=True, blank=True, help_text='نماد معاملاتی انگلیسی')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='نام دسته بندی')
    english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه دسته بندی')
    english_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه انگلیسی شرکت')
    fingilish_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام فینگیلیش')
    fingilish_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه فینگیلیش')
    fingilish_trade_symbol = models.CharField(max_length=255, null=True, blank=True, help_text='نام نماد معاملاتی فینگیلیش')
    state_change_date = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ اعمال وضعیت')
    state_description = models.TextField(null=True, blank=True, help_text='دلایل تغییر وضعیت')
    english_state_description = models.TextField(null=True, blank=True, help_text='دلایل تغییر وضعیت انگلیسی')

    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='اطلاعات رکورد')
    assetType = models.ForeignKey(Assettype, on_delete=models.CASCADE, null=True, blank=True, help_text='نوع دارایی')
    state = models.ForeignKey(Assetstate, on_delete=models.CASCADE, null=True, blank=True, help_text='وضعیت دارایی')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار معاملاتی')
    # stock = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, help_text='سهام')
    entity = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, help_text='موجودی')
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, null=True, blank=True, help_text='صندوق')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, help_text='گروه‌ها')

    def __str__(self):
        return self.name


#  مارکت
class Market(models.Model):
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد شاخص')
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    english_title = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.title


#  تابلو
class Board(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد شاخص')
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    english_title = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')

    def __str__(self):
        return self.title


#  گروه‌های نماد
class Instrumentgroup(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد شاخص')
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    english_title = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')

    def __str__(self):
        return self.title


#  انواع گروه‌های نماد
class Instrumentexchangestate(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True, help_text='نام')
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='meta info.')

    def __str__(self):
        return self.title


# نمادها
class Instrument(models.Model):
    id = models.CharField(max_length=255, primary_key=True, help_text='کد رکورد')
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد بورسی')
    bbs_code = models.CharField(max_length=255, null=True, blank=True, help_text='کد BBS')
    isin = models.CharField(max_length=255, null=True, blank=True, help_text='کد ISIN')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='نام دسته بندی')
    english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه دسته بندی')
    english_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه انگلیسی شرکت')
    # share: سهام
    # warrant: حق تقدم
    # index: شاخص
    # bond: اوراق مشارکت
    # future: آتی
    # option: اختیار فروش تبعی
    # energy: انرژی
    # energy2: انرژی۲
    # intellectual_property: دارایی فکری
    # commodity: کالا
    # currency: ارز
    type = models.CharField(max_length=255, null=True, blank=True, help_text='نوع نماد')
    # price: ریالی
    # percent: درصدی
    value_type = models.CharField(max_length=255, null=True, blank=True, help_text='نوع قیمت نماد')
    base_volume = models.BigIntegerField(null=True, blank=True, help_text='حجم مبنای نماد')
    nominal_price = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, help_text='قیمت اسمی نماد')
    price_tick = models.IntegerField(null=True, blank=True, help_text='حداقل تغییر قیمت نماد')
    trade_tick = models.IntegerField(null=True, blank=True, help_text='حداقل تغییر معاملات نماد')
    payment_delay = models.IntegerField(null=True, blank=True, help_text='دوره زمانی تسویه معاملات نماد')
    minimum_volume_permit = models.BigIntegerField(null=True, blank=True, help_text='حداقل حجم معاملات نماد در یک سفارش')
    maximum_volume_permit = models.BigIntegerField(null=True, blank=True, help_text='حداکثر حجم معاملات نماد در یک سفارش')
    listing_date = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ ایجاد نماد')
    image = models.ImageField(
                upload_to='uploads/images/instrument/',
                null=True,
                blank=True,
                help_text='تصویر'
    )
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='اطلاعات رکورد')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار معاملاتی')
    exchange_state = models.ForeignKey(Instrumentexchangestate, on_delete=models.CASCADE, null=True, blank=True, help_text='وضعیت نماد در بورس')
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار')
    group = models.ForeignKey(Instrumentgroup, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True, help_text='تابلوی معاملاتی نماد')
    index = models.ForeignKey(Index, on_delete=models.CASCADE, null=True, blank=True, help_text='شاخص')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True, help_text='دارایی')
    stock = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, help_text='شرکت')

    def __str__(self):
        return self.name


# نمادهای منتخب
class Instrumentsel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, help_text='کد رکورد')
    code = models.CharField(max_length=255, null=True, blank=True, help_text='کد بورسی')
    bbs_code = models.CharField(max_length=255, null=True, blank=True, help_text='کد BBS')
    isin = models.CharField(max_length=255, null=True, blank=True, help_text='کد ISIN')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='نام ')
    english_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام انگلیسی')
    short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه دسته بندی')
    english_short_name = models.CharField(max_length=255, null=True, blank=True, help_text='نام کوتاه انگلیسی شرکت')
    # share: سهام
    # warrant: حق تقدم
    # index: شاخص
    # bond: اوراق مشارکت
    # future: آتی
    # option: اختیار فروش تبعی
    # energy: انرژی
    # energy2: انرژی۲
    # intellectual_property: دارایی فکری
    # commodity: کالا
    # currency: ارز
    type = models.CharField(max_length=255, null=True, blank=True, help_text='نوع نماد')
    # price: ریالی
    # percent: درصدی
    value_type = models.CharField(max_length=255, null=True, blank=True, help_text='نوع قیمت نماد')
    base_volume = models.BigIntegerField(null=True, blank=True, help_text='حجم مبنای نماد')
    nominal_price = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, help_text='قیمت اسمی نماد')
    price_tick = models.IntegerField(null=True, blank=True, help_text='حداقل تغییر قیمت نماد')
    trade_tick = models.IntegerField(null=True, blank=True, help_text='حداقل تغییر معاملات نماد')
    payment_delay = models.IntegerField(null=True, blank=True, help_text='دوره زمانی تسویه معاملات نماد')
    minimum_volume_permit = models.BigIntegerField(null=True, blank=True, help_text='حداقل حجم معاملات نماد در یک سفارش')
    maximum_volume_permit = models.BigIntegerField(null=True, blank=True, help_text='حداکثر حجم معاملات نماد در یک سفارش')
    listing_date = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ ایجاد نماد')

    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='اطلاعات رکورد')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار معاملاتی')
    exchange_state = models.ForeignKey(Instrumentexchangestate, on_delete=models.CASCADE, null=True, blank=True, help_text='وضعیت نماد در بورس')
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار')
    group = models.ForeignKey(Instrumentgroup, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True, help_text='تابلوی معاملاتی نماد')
    index = models.ForeignKey(Index, on_delete=models.CASCADE, null=True, blank=True, help_text='شاخص')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True, help_text='دارایی')
    stock = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, help_text='شرکت')

    def __str__(self):
        if self.short_name is not None:
            return self.short_name
        return str(self.meta.version)


# معاملات روزانه
class Trade(models.Model):
    id = models.CharField(max_length=255, primary_key=True, help_text='کد رکورد')
    date_time = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ و زمان معامله انجام شده')
    open_price = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='اولین قیمت معاملاتی')
    high_price = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='بیشترین قیمت معاملاتی')
    low_price = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='کمترین قیمت معاملاتی')
    close_price = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='آخرین قیمت معاملاتی')
    close_price_change = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='تفاوت آخرین قیمت با قیمت پایانی روز قبل')
    real_close_price = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='قیمت پایانی معاملات با احتساب حجم مبنا')
    real_close_price_change = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='تغییر قیمت پایانی نسبت به قیمت پایانی روز قبل')
    value = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='ارزش ریالی معاملات')
    buyer_count = models.IntegerField(null=True, blank=True, help_text='تعداد خریداران')
    volume = models.BigIntegerField(null=True, blank=True, help_text='تعداد معامله شده')
    trade_count = models.IntegerField(null=True, blank=True, help_text='تعداد معامله')
    adjusted_close_price = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, help_text='')

    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True, blank=True, help_text='اطلاعات رکورد')
    instrument = models.ForeignKey(Instrumentsel, on_delete=models.CASCADE, null=True, blank=True, help_text='بازار معاملاتی')

    def __str__(self):
        return self.instrument.name


# جزعیات معاملات روزانه
class Tradedetail(models.Model):
    date_time = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ و زمان معامله انجام شده')
    value = models.CharField(max_length=255, null=True, blank=True, help_text='اطلاعات کندل')
    #  open_price, high_price, low_price, close_price, close_price_change, real_close_price
    #  , real_close_price_change, buyer_count, trade_count, volume, value
    #  person_buyer_count, company_buyer_count, person_buy_volume, company_buy_volume, person_seller_count
    #  , company_seller_count, person_sell_volume, company_sell_volume
    version = models.BigIntegerField(primary_key=True, help_text='نسخه فیلد')
    instrument = models.ForeignKey(Instrumentsel, on_delete=models.CASCADE, null=True, blank=True, help_text='نماد معاملاتی')

    def __str__(self):
        if self.instrument is not None:
            return self.instrument.name
        return self.version


class Trademidday(models.Model):
    date_time = models.CharField(max_length=255, null=True, blank=True, help_text='تاریخ و زمان معامله انجام شده')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrumentsel, on_delete=models.CASCADE, null=True, blank=True, help_text='نماد معاملاتی')
    value = models.CharField(max_length=255, null=True, blank=True, help_text='اطلاعات کندل')
    version = models.BigIntegerField(primary_key=True, help_text='نسخه فیلد')

    def __str__(self):
        if self.company is not None:
            return self.instrument.name
        return self.version


# class Company(models.Model):
#     SYMBOL_TYPE_CHOICES = (
#         ('0', "شاخص کل"),
#         ('1', "نماد"),
#         ('2', "شاخص صنعت"),
#     )
#     BOURSE_TYPE_CHOICES = (
#         ('0', "تابلو اصلی بازار اول بورس"),
#         ('1', "تابلو فرعی بازار اول بورس"),
#         ('2', "بازار دوم بورس"),
#         ('3', "بازار اول فرابورس"),
#         ('4', "بازار دوم فرابورس"),
#         ('5', "بازار پایه زرد فرابورس"),
#         ('6', "بازار پایه نارنجی فرابورس"),
#         ('7', "بازار پایه قرمز فرابورس"),
#     )
# 
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         help_text='کاربر'
#     )
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         help_text='گروه'
#     )
#     symbol = models.CharField(
#         max_length=255,
#         unique=True,
#         help_text='نماد'
#     )
#     name = models.CharField(
#         max_length=255,
#         help_text='نام شرکت'
#     )
#     alias = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
#         help_text='نام معادل انگلیسی'
#     )
#     type = models.CharField(
#         max_length=255,
#         help_text='نوع نماد',
#         choices=SYMBOL_TYPE_CHOICES,
#         default='1'
#     )
#     bourse_type = models.CharField(
#         max_length=120,
#         null=True,
#         blank=True,
#         choices=BOURSE_TYPE_CHOICES,
#         help_text='بازار بورس'
#     )
#     image = models.ImageField(
#         upload_to='uploads/images/company/',
#         null=True,
#         blank=True,
#         help_text='تصویر'
#     )
#     created_on = models.DateField(auto_now_add=True)
#     tse = models.URLField(help_text='لینک tse')
#     site = models.URLField(
#         null=True,
#         blank=True,
#         help_text='وبسایت'
#     )
#     # isTarget = models.BooleanField(default=False, help_text='تحت نظر')
#     hit_count = models.BigIntegerField(default=0)
#     description = models.TextField(
#         null=True,
#         blank=True,
#         help_text='توضیحات'
#     )
# 
#     def __str__(self):
#         return self.symbol
# 
#     @property
#     def news(self):
#         return self.news_set.all()


class RequestSymbol(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    company = models.ForeignKey(
        Instrumentsel,
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
        Instrumentsel,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('watch_list', 'company',)

    def __str__(self):
        return f'{self.watch_list.name}, {self.company.short_name}'

    def get_short_name(self):
        return self.company.short_name

    def get_short_english_name(self):
        return self.company.english_short_name

    def get_name(self):
        return self.company.name


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Instrumentsel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user}, {self.company.name}'


class News(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='کاربر'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='در صورت اختصاص خبر برای گروه انتخاب شود'
    )
    instrument = models.ForeignKey(
        Instrumentsel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='در صورت اختصاص خبر برای نماد انتخاب شود'
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        help_text='عنوان'
    )
    reference = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text='مرجع'
    )
    date = models.CharField(
        max_length=255,
        help_text='تاریخ ایجاد'
    )
    pic = models.ImageField(
        upload_to='uploads/images/news/',
        max_length=300,
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

    @property
    def pic_url(self):
        return self.pic


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
    instrument = models.ForeignKey(
        Instrumentsel,
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
    thumbnail = models.ImageField(
        upload_to='upload/thumbnail/technical',
        help_text='تصویر'
    )

    def __str__(self):
        return str(self.id)


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
    instrument = models.ForeignKey(
        Instrumentsel,
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
        return self.instrument.name


class Fundamental(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    instrument = models.ForeignKey(
        Instrumentsel,
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
        return self.instrument.name


class Bazaar(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    instrument = models.ForeignKey(
        Instrumentsel,
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
        return self.instrument.name


class Chart(models.Model):

    def file_path(self, filename):
        return os.path.join('uploads/file/chart/', str(self.instrument.english_short_name), filename)

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
    last_candle_date = models.CharField(max_length=255, help_text='تاریخ آخرین کندل')
    instrument = models.ForeignKey(
        Instrumentsel,
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
        upload_to=file_path,
        null=True,
        blank=True,
        help_text='فایل csv,  prn, txt چارت نماد'
    )

    def __str__(self):
        return self.instrument.short_name

    class Meta:
        unique_together = ('instrument', 'timeFrame')


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
    instrument = models.ForeignKey(
        Instrumentsel,
        on_delete=models.CASCADE,
        help_text='نماد'
    )
    title = models.CharField(
        max_length=255,
        help_text='نام فایل'
    )
    poster = models.ImageField(
        'uploads/image/user-technical',
        null=True,
        blank=True,
        help_text='تصویر'
    )
    is_share = models.BooleanField(default=False, help_text='اجازه اشتراک گذاری')
    short_description = models.CharField(max_length=255, null=True, blank=True)
    data = models.TextField(help_text='فایل متنی شده json')

    def __str__(self):
        return self.instrument.name


class TechnicalJSONUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    created_on = models.DateField(auto_now_add=True, help_text='تاریخ ایجاد')
    instrument = models.ForeignKey(Instrumentsel, on_delete=models.CASCADE, help_text='نماد')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='نام فایل')
    isShare = models.BooleanField(default=False, help_text='اجازه اشتراک گذاریا')
    # data = models.TextField(null=True, blank=True, help_text='فایل متنی شده json')
    data = jsonfield.JSONField(help_text='فایل متنی شده json')

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.instrument.short_name

    @property
    def owner(self):
        return self.user


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
    free = models.BooleanField(default=True)
    description = RichTextField(null=True, blank=True, help_text='توضیحات')
    thumbnail = models.ImageField(
        upload_to='uploads/thumbnail/tutorial',
        help_text='تصویر'
    )

    @property
    def tutorial_files(self):
        if self.free:
            return self.tutorialfreefile_set.all()
        return self.tutorialfile_set

    def __str__(self):
        return self.title


class TutorialFile(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    file = PrivateFileField("File")

    def __str__(self):
        return self.tutorial.title


class TutorialFreeFile(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/file/free-tutorial')

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


class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(
        upload_to='uploads/thumbnail/article',
        help_text='تصویر'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='در صورت اختصاص مقاله برای گروه انتخاب شود'
    )
    instrument = models.ForeignKey(
        Instrumentsel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='در صورت اختصاص مقاله برای نماد انتخاب شود'
    )
    date = models.DateField(
        auto_now_add=True,
        help_text=
        'تاریخ ایجاد')
    author = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text='نویسنده'
    )
    tag = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text='برچسب'
    )
    hit_count = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.author}, {self.title}'


class CompanyFinancial(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    company = models.ForeignKey(
        Instrumentsel,
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
        return self.company.name


class UserComment(models.Model):
    COMMENT_FOR = (
        ('0', 'تحلیل تکنیکال'),
        ('1', 'تحلیل بنیادی'),
        ('2', 'وبینار'),
        ('3', 'اخبار'),
        ('4', 'نماد')
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
    company = models.ForeignKey(
        Instrumentsel,
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
    like = models.PositiveIntegerField(default=0)

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


class Software(models.Model):
    software = models.FileField(
        upload_to='uploads/file/software',
    )
    version = models.CharField(
        max_length=128,
        null=False,
        blank=False
    )


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
    instrument = models.ForeignKey(
        Instrumentsel,
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
    article = models.ForeignKey(
        Article,
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


class Notification(models.Model):
    title = models.CharField(max_length=255)
    text = RichTextField()
    instrument = models.ForeignKey(
        Instrumentsel,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    thumbnail = models.ImageField(
        upload_to='uploads/thumbnail/notification',
        help_text='تصویر'
    )
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}, {self.title}'

    @property
    def company_name(self):
        if self.instrument:
            return self.instrument.name
        else:
            return ''


class BugReport(models.Model):
    STATUS_CHOICES = (
        ('0', "گزارش شده"),
        ('1', "در حال بررسی"),
        ('2', "رفع باگ"),
    )
    status = models.CharField(
        max_length=255,
        help_text='وضعیت باگ',
        choices=STATUS_CHOICES,
        default='0'
    )

    text = models.TextField(
        null=False,
        blank=False
    )
    email = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    fixed_on = models.DateTimeField(null=True, blank=True, help_text="زمان رفع باگ")

    def __str__(self):
        return f'{self.email}, {self.text}'


class NewsPodcast(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(
        upload_to='uploads/thumbnail/news-podcast',
        help_text='تصویر'
    )
    file = models.FileField(
        upload_to='uploads/file/news-podcast',
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class InstrumentInfo(models.Model):
    instrument = models.ForeignKey(Instrumentsel, on_delete=models.CASCADE)
    volAvg1M = models.PositiveIntegerField(default=0, help_text='میانگین ماهانه')
    volAvg3M = models.PositiveIntegerField(default=0, help_text='میانگین 3 ماه')
    volAvg12M = models.PositiveIntegerField(default=0, help_text='میانگین 12 ماهه')
    created_on = models.DateField(null=True, blank=True, help_text="آخرین روز محاسبه")

    def __str__(self):
        return self.instrument.short_name
