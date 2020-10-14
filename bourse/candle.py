import os
from . import models
import pandas as pd
from django.db import IntegrityError
import jdatetime
from shutil import copy2
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


def find_farsi_title(instrument):
    if instrument == 'saman':
        return 'سامان'
    # گروه:حمل ونقل، انبارداري و ارتباطات
    elif instrument == 'hkshti':
        return 'حکشتی'
    elif instrument == 'hfars':
        return 'حفارس'
    elif instrument == 'hsina':
        return 'حسینا'
    elif instrument == 'htied':
        return 'حتاید'
    elif instrument == 'hbandar':
        return 'حبندر'
    elif instrument == 'toril':
        return 'توریل'
    elif instrument == 'hril':
        return 'حریل'
    elif instrument == 'htoka':
        return 'حتوکا'
    elif instrument == 'hasa':
        return 'حآسا'
    elif instrument == 'hparsa':
        return 'حپارسا'
    elif instrument == 'hsir':
        return 'حسیر'
    elif instrument == 'hpetro':
        return 'حپترو'
    elif instrument == 'hrhsha':
        return 'حرهشا'
    # گروه:خودرو و ساخت قطعات
    elif instrument == 'Khodro':
        return 'خودرو'
    elif instrument == 'khsapa':
        return 'خساپا'
    elif instrument == 'khgostar':
        return 'خگستر'
    elif instrument == 'khpars':
        return 'خپارس'
    elif instrument == 'khmoharekeh':
        return 'خمحرکه'
    elif instrument == 'khbahman':
        return 'خبهمن'
    elif instrument == 'vrona':
        return 'ورنا'
    elif instrument == 'khtogha':
        return 'ختوقا'
    elif instrument == 'khzamia':
        return 'خزامیا'
    elif instrument == 'khazin':
        return 'خاذین'
    elif instrument == 'khmhr':
        return 'خمهر'
    elif instrument == 'khkerman':
        return 'خکرمان'
    elif instrument == 'khrikht':
        return 'خریخت'
    elif instrument == 'khtor':
        return 'ختور'
    elif instrument == 'khavar':
        return 'خاور'
    elif instrument == 'khkaveh':
        return 'خکاوه'
    elif instrument == 'khahn':
        return 'خاهن'
    elif instrument == 'khring':
        return 'خرینگ'
    elif instrument == 'khshargh':
        return 'خشرق'
    elif instrument == 'khfanar':
        return 'خفنر'
    elif instrument == 'khosaz':
        return 'خوساز'
    elif instrument == 'khdyzl':
        return 'خدیزل'
    elif instrument == 'khazar':
        return 'خزر'
    elif instrument == 'khkar':
        return 'خکار'
    elif instrument == 'khcharkhesh':
        return 'خچرخش'
    elif instrument == 'khkomak':
        return 'خکمک'
    elif instrument == 'khtrak':
        return 'ختراک'
    elif instrument == 'khnsir':
        return 'خنصیر'
    elif instrument == 'khmotor':
        return 'خموتور'
    elif instrument == 'khlent':
        return 'خلنت'
    elif instrument == 'khmehvar':
        return 'خمحور'
    elif instrument == 'khpoish':
        return 'خپویش'
    elif instrument == 'khamra':
        return 'خعمرا'
    elif instrument == 'tshtad':
        return 'تشتاد'
    elif instrument == 'khfanaor':
        return 'خفناور'
    elif instrument == 'khlibl':
        return 'خلیبل'
    #  گروه:مواد و محصولات دارويي
    elif instrument == 'dyran':
        return 'دیران'
    elif instrument == 'barkat':
        return 'برکت'
    elif instrument == 'valbr':
        return 'والبر'
    elif instrument == 'dtolid':
        return 'دتولید'
    elif instrument == 'dzahravi':
        return 'دزهراوی'
    elif instrument == 'rishmk':
        return 'ریشمک'
    elif instrument == 'dkoser':
        return 'دکوثر'
    elif instrument == 'dfara':
        return 'دفارا'
    elif instrument == 'dbalk':
        return 'دبالک'
    elif instrument == 'dtmad':
        return 'دتماد'
    elif instrument == 'tipiko':
        return 'تیپیکو'
    elif instrument == 'dsanko':
        return 'دسانکو'
    elif instrument == 'ddam':
        return 'ددام'
    elif instrument == 'drhaor':
        return 'درهآور'
    elif instrument == 'vpakhsh':
        return 'وپخش'
    elif instrument == 'drazk':
        return 'درازک'
    elif instrument == 'dabid':
        return 'دعبید'
    elif instrument == 'dsobhan':
        return 'دسبحان'
    elif instrument == 'Daro':
        return 'دارو'
    elif instrument == 'dabor':
        return 'دابور'
    elif instrument == 'dtozia':
        return 'دتوزیع'
    elif instrument == 'pakhsh':
        return 'پخش'
    elif instrument == 'dshimi':
        return 'دشیمی'
    elif instrument == 'djabr':
        return 'دجابر'
    elif instrument == 'dsobha':
        return 'دسبحا'
    elif instrument == 'daoh':
        return 'داوه'
    elif instrument == 'dlr':
        return 'دلر'
    elif instrument == 'dpars':
        return 'دپارس'
    elif instrument == 'dalbr':
        return 'دالبر'
    elif instrument == 'hejrat':
        return 'هجرت'
    elif instrument == 'damin':
        return 'دامین'
    elif instrument == 'kaspin':
        return 'کاسپین'
    elif instrument == 'dsina':
        return 'دسینا'
    elif instrument == 'dkimi':
        return 'دکیمی'
    elif instrument == 'dkpsol':
        return 'دکپسول'
    elif instrument == 'dasoh':
        return 'داسوه'
    elif instrument == 'ki_bi_si':
        return 'کی بی سی'
    elif instrument == 'shafa':
        return 'شفا'
    elif instrument == 'dloghma':
        return 'دلقما'
    elif instrument == 'dfara':
        return 'دفرا'
    elif instrument == 'droz':
        return 'دروز'
    elif instrument == 'dhaoi':
        return 'دحاوی'
    elif instrument == 'dghazi':
        return 'دقاضی'
    elif instrument == 'dshiri':
        return 'دشیری'
    elif instrument == 'shthran':
        return 'شتهران'
    elif instrument == 'dthran':
        return 'دتهران'
    # گروه:رايانه و فعاليت‌هاي وابسته به آن
    elif instrument == 'ap':
        return 'آپ'
    elif instrument == 'ranfor':
        return 'رانفور'
    elif instrument == 'tapkish':
        return 'تاپکیش'
    elif instrument == 'mrgham':
        return 'مرقام'
    elif instrument == 'sp':
        return 'سپ'
    elif instrument == 'rtap':
        return 'رتاپ'
    elif instrument == 'rafza':
        return 'رافزا'
    elif instrument == 'rkish':
        return 'رکیش'
    elif instrument == 'mdaran':
        return 'مداران'
    elif instrument == 'mfakhr':
        return 'مفاخر'
    elif instrument == 'system':
        return 'سیستم'
    elif instrument == 'aFara':
        return 'افرا'
    elif instrument == 'prdakht':
        return 'پرداخت'
    elif instrument == 'fanawa':
        return 'فن آوا'
    # گروه:زراعت و خدمات وابسته
    elif instrument == 'zkoser':
        return 'زکوثر'
    elif instrument == 'zmlard':
        return 'زملارد'
    elif instrument == 'zghiam':
        return 'زقیام'
    elif instrument == 'zbina':
        return 'زبینا'
    elif instrument == 'zmgsa':
        return 'زمگسا'
    elif instrument == 'zshgza':
        return 'زشگزا'
    elif instrument == 'zshrif':
        return 'زشریف'
    elif instrument == 'tlish':
        return 'تلیسه'
    elif instrument == 'zksht':
        return 'زکشت'
    elif instrument == 'zpars':
        return 'زپارس'
    elif instrument == 'zmahan':
        return 'زماهان'
    elif instrument == 'abin':
        return 'آبین'
    elif instrument == 'zdasht':
        return 'زدشت'
    elif instrument == 'simrgh':
        return 'سیمرغ'
    elif instrument == 'zgoldasht':
        return 'زگلدشت'
    elif instrument == 'aindh':
        return 'آینده'
    elif instrument == 'zfka':
        return 'زفکا'
    #گروه:سرمايه گذاريها
    elif instrument == 'vsobhan':
        return 'وسبحان'
    elif instrument == 'sba':
        return 'صبا'
    elif instrument == 'vkharzm':
        return 'وخارزم'
    elif instrument == 'vsepahr':
        return 'وسپهر'
    elif instrument == 'vtosa':
        return 'وتوصا'
    elif instrument == 'vpvia':
        return 'وپویا'
    elif instrument == 'vsapa':
        return 'وساپا'
    elif instrument == 'vSanat':
        return 'وصنعت'
    elif instrument == 'vniki':
        return 'ونیکی'
    elif instrument == 'vbrgh':
        return 'وبرق'
    elif instrument == 'vboali':
        return 'وبوعلی'
    elif instrument == 'vgostar':
        return 'وگستر'
    elif instrument == 'vsepah':
        return 'وسپه'
    elif instrument == 'vmhan':
        return 'ومهان'
    elif instrument == 'srchshmh':
        return 'سرچشمه'
    elif instrument == 'arian':
        return 'آریان'
    elif instrument == 'vskab':
        return 'وسکاب'
    elif instrument == 'vava':
        return 'وآوا'
    elif instrument == 'vbimeh':
        return 'وبیمه'
    elif instrument == 'vbahman':
        return 'وبهمن'
    elif instrument == 'vtoosm':
        return 'وتوسم'
    elif instrument == 'sdbir':
        return 'سدبیر'
    elif instrument == 'pardis':
        return 'پردیس'
    elif instrument == 'vati':
        return 'واتی'
    elif instrument == 'vkadv':
        return 'وکادو'
    elif instrument == 'vsana':
        return 'وصنا'
    elif instrument == 'aatla':
        return 'اعتلا'
    elif instrument == 'varin':
        return 'وآرین'
    elif instrument == 'vshomal':
        return 'وشمال'
    elif instrument == 'vjami':
        return 'وجامی'
    elif instrument == 'gohran':
        return 'گوهران'
    elif instrument == 'flat':
        return 'فلات'
    elif instrument == 'snovin':
        return 'سنوین'
    elif instrument == 'viera':
        return 'وایرا'
    elif instrument == 'vetebar':
        return 'واعتبار'
    elif instrument == 'maiar':
        return 'معیار'
    elif instrument == 'vskhraj':
        return 'وسخراج'
    elif instrument == 'vmellat':
        return 'وملت'
    elif instrument == 'vsghm':
        return 'وسقم'
    elif instrument == 'vsgolsta':
        return 'وسگلستا'
    elif instrument == 'vsilam':
        return 'وسیلام'
    elif instrument == 'vskhrash':
        return 'وسخراش'
    elif instrument == 'vsarbil':
        return 'وساربیل'
    elif instrument == 'vsznjan':
        return 'وسزنجان'
    elif instrument == 'vsmrkz':
        return 'وسمرکز'
    elif instrument == 'vskrsha':
        return 'وسکرشا'
    elif instrument == 'vadak':
        return 'وآداک'
    elif instrument == 'vsbvshahr':
        return 'وسبوشهر'
    elif instrument == 'vdana':
        return 'ودانا'
    # گروه:محصولات شيميايي
    elif instrument == 'shkolr':
        return 'شکلر'
    elif instrument == 'petrol':
        return 'پترول'
    elif instrument == 'shgoia':
        return 'شگویا'
    elif instrument == 'fars':
        return 'فارس'
    elif instrument == 'tapiko':
        return 'تاپیکو'
    elif instrument == 'aria':
        return 'آریا'
    elif instrument == 'shafars':
        return 'شفارس'
    elif instrument == 'shiran':
        return 'شیران'
    elif instrument == 'zagrs':
        return 'زاگرس'
    elif instrument == 'shlord':
        return 'شلرد'
    elif instrument == 'parsan':
        return 'پارسان'
    elif instrument == 'shghdyr':
        return 'شغدیر'
    elif instrument == 'sharak':
        return 'شاراک'
    elif instrument == 'nori':
        return 'نوری'
    elif instrument == 'kolr':
        return 'کلر'
    elif instrument == 'sharom':
        return 'شاروم'
    elif instrument == 'shekarbn':
        return 'شکربن'
    elif instrument == 'shpli':
        return 'شپلی'
    elif instrument == 'shpetro':
        return 'شپترو'
    elif instrument == 'paksho':
        return 'پاکشو'
    elif instrument == 'ghrn':
        return 'قرن'
    elif instrument == 'kermasha':
        return 'کرماشا'
    elif instrument == 'pars':
        return 'پارس'
    elif instrument == 'shsdf':
        return 'شصدف'
    elif instrument == 'shpaksa':
        return 'شپاکسا'
    elif instrument == 'siena':
        return 'ساینا'
    elif instrument == 'vpetro':
        return 'وپترو'
    elif instrument == 'shoindh':
        return 'شوینده'
    elif instrument == 'shkhark':
        return 'شخارک'
    elif instrument == 'maron':
        return 'مارون'
    elif instrument == 'jam_piln':
        return 'جم پیلن'
    elif instrument == 'shpdys':
        return 'شپدیس'
    elif instrument == 'jam':
        return 'جم'
    elif instrument == 'shpars':
        return 'شپارس'
    elif instrument == 'shfan':
        return 'شفن'
    elif instrument == 'shlaab':
        return 'شلعاب'
    elif instrument == 'znjan':
        return 'زنجان'
    elif instrument == 'shjam':
        return 'شجم'
    elif instrument == 'shiraz':
        return 'شیراز'
    elif instrument == 'shbsir':
        return 'شبصیر'
    elif instrument == 'shgol':
        return 'شگل'
    elif instrument == 'shsafha':
        return 'شصفها'
    elif instrument == 'shtoka':
        return 'شتوکا'
    elif instrument == 'shkaf':
        return 'شکف'
    elif instrument == 'shMavad':
        return 'شمواد'
    elif instrument == 'khorasan':
        return 'خراسان'
    elif instrument == 'shdos':
        return 'شدوص'
    elif instrument == 'shamla':
        return 'شاملا'
    elif instrument == 'shafara':
        return 'شفارا'
    elif instrument == 'jhrm':
        return 'جهرم'
    elif instrument == 'fasa':
        return 'فسا'
    elif instrument == 'darab':
        return 'داراب'
    elif instrument == 'shtoli':
        return 'شتولی'
    elif instrument == 'shkbir':
        return 'شکبیر'
    elif instrument == 'mmsni':
        return 'ممسنی'
    elif instrument == 'shsm':
        return 'شسم'
    elif instrument == 'shrngi':
        return 'شرنگی'
    elif instrument == 'dhdasht':
        return 'دهدشت'
    elif instrument == 'kazro':
        return 'کازرو'
    elif instrument == 'shstan':
        return 'شستان'
    elif instrument == 'shgamrn':
        return 'شگامرن'
    elif instrument == 'znjan':
        return 'زنجان'
    # گروه:محصولات غذايي و آشاميدني به جز قند و شكر
    elif instrument == 'ghoita':
        return 'غویتا'
    elif instrument == 'ghgol':
        return 'غگل'
    elif instrument == 'ghnosh':
        return 'غنوش'
    elif instrument == 'ghshahdab':
        return 'غشهداب'
    elif instrument == 'ghsalem':
        return 'غسالم'
    elif instrument == 'ghzr':
        return 'غزر'
    elif instrument == 'ghpino':
        return 'غپینو'
    elif instrument == 'ghmarag':
        return 'غمارگ'
    elif instrument == 'vbshahr':
        return 'وبشهر'
    elif instrument == 'ghbhnosh':
        return 'غبهنوش'
    elif instrument == 'ghshahd':
        return 'غشهد'
    elif instrument == 'tbrk':
        return 'تبرک'
    elif instrument == 'ghdam':
        return 'غدام'
    elif instrument == 'ghbshahr':
        return 'غبشهر'
    elif instrument == 'ghoita':
        return 'غویتا'
    elif instrument == 'ghpak':
        return 'غپاک'
    elif instrument == 'ghgorji':
        return 'غگرجی'
    elif instrument == 'ghmino':
        return 'غمینو'
    elif instrument == 'khodkafa':
        return 'خودکفا'
    elif instrument == 'ghgila':
        return 'غگیلا'
    elif instrument == 'ghazar':
        return 'غاذر'
    elif instrument == 'ghshazar':
        return 'غشاذر'
    elif instrument == 'ghalbr':
        return 'غالبر'
    elif instrument == 'ghgolsta':
        return 'غگلستا'
    elif instrument == 'ghshsfa':
        return 'غشصفا'
    elif instrument == 'ghchin':
        return 'غچین'
    elif instrument == 'ghfars':
        return 'غفارس'
    elif instrument == 'ghdasht':
        return 'غدشت'
    elif instrument == 'ghdys':
        return 'غدیس'
    elif instrument == 'bhpak':
        return 'بهپاک'
    elif instrument == 'ghgolpa':
        return 'غگلپا'
    elif instrument == 'ghmhra':
        return 'غمهرا'
    elif instrument == 'ghshan':
        return 'غشان'
    elif instrument == 'ghponh':
        return 'غپونه'
    elif instrument == 'ghshoko':
        return 'غشوکو'
    elif instrument == 'ghnili':
        return 'غنیلی'
    elif instrument == 'ghpazar':
        return 'غپآذر'
    elif instrument == 'ghgz':
        return 'غگز'
    elif instrument == 'ghbhar':
        return 'غبهار'
    elif instrument == 'ghioan':
        return 'غیوان'
    elif instrument == 'ghsino':
        return 'غصینو'
    # گروه:ساير محصولات كاني غيرفلزي
    elif instrument == 'kFara':
        return 'کفرا'
    elif instrument == 'kasra':
        return 'کسرا'
    elif instrument == 'kpshir':
        return 'کپشیر'
    elif instrument == 'kehamda':
        return 'کهمدا'
    elif instrument == 'krazi':
        return 'کرازی'
    elif instrument == 'kazar':
        return 'کاذر'
    elif instrument == 'kfaravar':
        return 'کفرآور'
    elif instrument == 'ktoka':
        return 'کتوکا'
    elif instrument == 'kmrjan':
        return 'کمرجان'
    elif instrument == 'kafpars':
        return 'کفپارس'
    elif instrument == 'kgaz':
        return 'کگاز'
    elif instrument == 'kkhak':
        return 'کخاک'
    elif instrument == 'sfarod':
        return 'سفارود'
    elif instrument == 'kasram':
        return 'کسرام'
    elif instrument == 'ksapa':
        return 'کساپا'
    elif instrument == 'sfasi':
        return 'سفاسی'
    elif instrument == 'kabgn':
        return 'کابگن'
    elif instrument == 'kbadh':
        return 'کباده'
    elif instrument == 'kghzoi':
        return 'کقزوی'
    elif instrument == 'sprmi':
        return 'سپرمی'
    elif instrument == 'kmina':
        return 'کمینا'
    elif instrument == 'korz':
        return 'کورز'
    elif instrument == 'kieta':
        return 'کایتا'
    elif instrument == 'Sayerea':
        return 'سایرا'
    elif instrument == 'sazari':
        return 'ساذری'
    # گروه:فراورده هاي نفتي، كك و سوخت هسته اي
    elif instrument == 'shapna':
        return 'شپنا'
    elif instrument == 'shbandar':
        return 'شبندر'
    elif instrument == 'shabriz':
        return 'شبریز'
    elif instrument == 'vnaft':
        return 'ونفت'
    elif instrument == 'shbehran':
        return 'شبهرن'
    elif instrument == 'shaspa':
        return 'شسپا'
    elif instrument == 'shpas':
        return 'شپاس'
    elif instrument == 'shranl':
        return 'شرانل'
    elif instrument == 'shaoan':
        return 'شاوان'
    elif instrument == 'shnaft':
        return 'شنفت'
    elif instrument == 'shraz':
        return 'شراز'
    elif instrument == 'shatran':
        return 'شتران'
    elif instrument == 'shzng':
        return 'شزنگ'
    # گروه:شرکتهاي چند رشته اي صنعتي
    elif instrument == 'shsta':
        return 'شستا'
    elif instrument == 'vghdyr':
        return 'وغدیر'
    elif instrument == 'vbank':
        return 'وبانک'
    elif instrument == 'vamid':
        return 'وامید'
    elif instrument == 'vsandogh':
        return 'وصندوق'
    # فعاليتهاي كمكي به نهادهاي مالي واسط
    elif instrument == 'amid':
        return 'امید'
    elif instrument == 'Bourse':
        return 'بورس'
    elif instrument == 'amin':
        return 'امین'
    elif instrument == 'kala':
        return 'کالا'
    elif instrument == 'FaraBourse':
        return 'فرابورس'
    elif instrument == 'tmellat':
        return 'تملت'
    elif instrument == 'tnovin':
        return 'تنوین'
    elif instrument == 'anrzhi3':
        return 'انرژی3'
    elif instrument == 'lvtoos':
        return 'لوتوس'
    elif instrument == 'tmaond':
        return 'تماوند'
    elif instrument == 'anrzhi1':
        return 'انرژی1'
    elif instrument == 'akala':
        return 'اکالا'
    elif instrument == 'anrzhi2':
        return 'انرژی2'
    elif instrument == 'kBourse':
        return 'کبورس'
    elif instrument == 'tkala':
        return 'تکالا'
    elif instrument == 'nkala':
        return 'نکالا'
    elif instrument == 'nBourse':
        return 'نبورس'

    elif instrument == '-----':
        return '---'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    elif instrument == '-----':
        return '-----'
    else:
        return None


def feed_candle():
    directories = os.listdir('./helper/')
    for directory in directories:
        path = f'./helper/{directory}/'
        print(os.path.isdir(path), directory)
        if os.path.isdir(path):
            print(f'check {directory}')
            # farsi_title = find_farsi_title(directory)
            # print(farsi_title)
            # if farsi_title is None:
            #     continue

            try:
                symbol = models.Instrumentsel.objects.get(short_name=directory)
                # symbol = models.Instrumentsel.objects.get(short_name=farsi_title)
                # symbol = models.Instrumentsel.objects.get(id=36094)
            except ObjectDoesNotExist:
                print('Instrument not found!')
                continue
            print(f'symbol: {symbol}')

            for file in os.listdir(path):
                print(file)
                df = pd.read_csv(path + file)  # read csv
                df = df.drop(columns=['<TICKER>', '<PER>', '<OPENINT>'])  # drop unused columns
                df.to_csv((path + file), index=False)  # write to file
                last_date = str(df['<DTYYYYMMDD>'].iloc[-1])
                jalali_date = jdatetime.date.fromgregorian(
                    day=int(last_date[6:8]),
                    month=int(last_date[4:6]),
                    year=int(last_date[:4])
                )
                jalali_date = str(jalali_date).replace('-', '')
                last_time = "{0:0=6d}".format(df[' <TIME>'].iloc[-1])
                date_time = str(jalali_date) + str(last_time)
                time_frame = file.split('.')[0].split('-')[1]

                # print(settings.MEDIA_ROOT)
                # continue
                # create directory for media
                url = settings.MEDIA_ROOT.replace('\\', '/')
                try:
                    os.mkdir(f'{url}/uploads/file/chart/{directory}')
                except FileExistsError:
                    pass

                # copy file to media
                copy2(path + file, f'{url}/uploads/file/chart/{directory}/')

                # create an object
                try:
                    models.Chart.objects.create(
                        last_candle_date=date_time,
                        instrument=symbol,
                        timeFrame=time_frame,
                        data=f'./uploads/file/chart/{directory}/' + file
                    )
                except IntegrityError:
                    pass
