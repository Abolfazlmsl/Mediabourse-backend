import os
from . import models
import pandas as pd
from django.db import IntegrityError
import jdatetime
from shutil import copy2
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
import requests



def find_farsi_title(instrument):
    if instrument == 'saman':
        return 'سامان'
    elif instrument == 'dara_ikm':
        return 'دارا یکم'
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
    elif instrument == 'dFara':
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
    # گروه:سرمايه گذاريها
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
    elif instrument == 'shsina':
        return 'شسینا'
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
    #  گروه:بانكها و موسسات اعتباري
    elif instrument == 'vbmellat':
        return 'وبملت'
    elif instrument == 'dy':
        return 'دی'
    elif instrument == 'vtejarat':
        return 'وتجارت'
    elif instrument == 'vbsader':
        return 'وبصادر'
    elif instrument == 'vpars':
        return 'وپارس'
    elif instrument == 'vpasar':
        return 'وپاسار'
    elif instrument == 'vnovin':
        return 'ونوین'
    elif instrument == 'vshahr':
        return 'وشهر'
    elif instrument == 'vgrdsh':
        return 'وگردش'
    elif instrument == 'vpost':
        return 'وپست'
    elif instrument == 'vsina':
        return 'وسینا'
    elif instrument == 'saman':
        return 'سامان'
    elif instrument == 'vkar':
        return 'وکار'
    elif instrument == 'vsalt':
        return 'وسالت'
    elif instrument == 'vaind':
        return 'وآیند'
    elif instrument == 'vmll':
        return 'وملل'
    elif instrument == 'vkhavar':
        return 'وخاور'
    elif instrument == 'vansar':
        return 'وانصار'
    elif instrument == 'vzmin':
        return 'وزمین'
    elif instrument == 'smieh':
        return 'سمایه'
    elif instrument == 'hkmt':
        return 'حکمت'
    elif instrument == 'vghvam':
        return 'وقوام'
    elif instrument == 'vkvser':
        return 'وکوثر'
    elif instrument == 'tosah':
        return 'توسعه'
    elif instrument == 'vmhr':
        return 'ومهر'
    elif instrument == 'vseamn':
        return 'وثامن'
    #  گروه:فلزات اساسي
    elif instrument == 'fmeli':
        return 'فملی'
    elif instrument == 'folad':
        return 'فولاد'
    elif instrument == 'zob':
        return 'ذوب'
    elif instrument == 'fkhoz':
        return 'فخوز'
    elif instrument == 'kaveh':
        return 'کاوه'
    elif instrument == 'arfa':
        return 'ارفع'
    elif instrument == 'fasmin':
        return 'فاسمین'
    elif instrument == 'floleh':
        return 'فلوله'
    elif instrument == 'kavir':
        return 'کویر'
    elif instrument == 'fsorb':
        return 'فسرب'
    elif instrument == 'hrmz':
        return 'هرمز'
    elif instrument == 'midko':
        return 'میدکو'
    elif instrument == 'fbahonar':
        return 'فباهنر'
    elif instrument == 'vtoka':
        return 'وتوکا'
    elif instrument == 'fros':
        return 'فروس'
    elif instrument == 'fayera':
        return 'فایرا'
    elif instrument == 'folazh':
        return 'فولاژ'
    elif instrument == 'kimia':
        return 'کیمیا'
    elif instrument == 'fspa':
        return 'فسپا'
    elif instrument == 'faravar':
        return 'فرآور'
    elif instrument == 'fajr':
        return 'فجر'
    elif instrument == 'fnavard':
        return 'فنورد'
    elif instrument == 'vsadid':
        return 'وسدید'
    elif instrument == 'folie':
        return 'فولای'
    elif instrument == 'fpanta':
        return 'فپنتا'
    elif instrument == 'fanoal':
        return 'فنوال'
    elif instrument == 'fkhas':
        return 'فخاس'
    elif instrument == 'fmrad':
        return 'فمراد'
    elif instrument == 'falom':
        return 'فالوم'
    elif instrument == 'fsadid':
        return 'فسدید'
    elif instrument == 'froi':
        return 'فروی'
    elif instrument == 'fafza':
        return 'فافزا'
    elif instrument == 'fzrin':
        return 'فزرین'
    elif instrument == 'fmak':
        return 'فماک'
    elif instrument == 'fasazan':
        return 'فسازان'
    elif instrument == 'fahwaz':
        return 'فاهواز'
    elif instrument == 'fnaft':
        return 'فنفت'
    elif instrument == 'foka':
        return 'فوکا'
    elif instrument == 'zngan':
        return 'زنگان'
    # خرده فروشي،باستثناي وسايل نقليه موتوري
    elif instrument == 'ghasm':
        return 'قاسم'
    elif instrument == 'afgh':
        return 'افق'
    elif instrument == 'rfah':
        return 'رفاه'
    # گروه:محصولات كاغذي
    elif instrument == 'chkapa':
        return 'چکاپا'
    elif instrument == 'chkarn':
        return 'چکارن'
    elif instrument == 'chkaveh':
        return 'چکاوه'
    elif instrument == 'chkarm':
        return 'چکارم'
    elif instrument == 'chbspa':
        return 'چبسپا'
    # گروه:ماشين آلات و تجهيزات
    elif instrument == 'tkomba':
        return 'تکمبا'
    elif instrument == 'tksha':
        return 'تکشا'
    elif instrument == 'tiera':
        return 'تایرا'
    elif instrument == 'tpompi':
        return 'تپمپی'
    elif instrument == 'vtosheh':
        return 'وتوشه'
    elif instrument == 'labsa':
        return 'لابسا'
    elif instrument == 'lbotan':
        return 'لبوتان'
    elif instrument == 'lsrma':
        return 'لسرما'
    elif instrument == 'tkno':
        return 'تکنو'
    elif instrument == 'lkhazar':
        return 'لخزر'
    elif instrument == 'lazma':
        return 'لازما'
    elif instrument == 'tpko':
        return 'تپکو'
    elif instrument == 'tfiro':
        return 'تفیرو'
    elif instrument == 'lkhanh':
        return 'لخانه'
    elif instrument == 'trak':
        return 'تراک'
    # گروه:انبوه سازي، املاك و مستغلات
    elif instrument == 'seshahed':
        return 'ثشاهد'
    elif instrument == 'kerman':
        return 'کرمان'
    elif instrument == 'seakht':
        return 'ثاخت'
    elif instrument == 'sefars':
        return 'ثفارس'
    elif instrument == 'senosa':
        return 'ثنوسا'
    elif instrument == 'vazar':
        return 'وآذر'
    elif instrument == 'vsakht':
        return 'وساخت'
    elif instrument == 'vtoos':
        return 'وتوس'
    elif instrument == 'seamra':
        return 'ثعمرا'
    elif instrument == 'sebagh':
        return 'ثباغ'
    elif instrument == 'semaskan':
        return 'ثمسکن'
    elif instrument == 'setran':
        return 'ثتران'
    elif instrument == 'separdis':
        return 'ثپردیس'
    elif instrument == 'kison':
        return 'کیسون'
    elif instrument == 'seshargh':
        return 'ثشرق'
    elif instrument == 'seghzoi':
        return 'ثقزوی'
    elif instrument == 'sealond':
        return 'ثالوند'
    elif instrument == 'a_s_p':
        return 'آ س پ'
    elif instrument == 'segharb':
        return 'ثغرب'
    elif instrument == 'sejoan':
        return 'ثجوان'
    elif instrument == 'senor':
        return 'ثنور'
    elif instrument == 'setosa':
        return 'ثتوسا'
    elif instrument == 'senzam':
        return 'ثنظام'
    elif instrument == 'seaman':
        return 'ثامان'
    elif instrument == 'seatma':
        return 'ثعتما'
    elif instrument == 'serod':
        return 'ثرود'
    elif instrument == 'seabad':
        return 'ثاباد'
    elif instrument == 'vsekhoz':
        return 'وثخوز'
    elif instrument == 'sezagrs':
        return 'ثزاگرس'
    elif instrument == 'senam':
        return 'ثنام'
    elif instrument == 'sebhsaz':
        return 'ثبهساز'
    elif instrument == 'seamid':
        return 'ثامید'
    elif instrument == 'seasfa':
        return 'ثاصفا'
    elif instrument == 'seazhn':
        return 'ثاژن'
    # گروه:عرضه برق، گاز، بخاروآب گرم
    elif instrument == 'bpiond':
        return 'بپیوند'
    elif instrument == 'damaond':
        return 'دماوند'
    elif instrument == 'bjhrm':
        return 'بجهرم'
    elif instrument == 'vniro':
        return 'ونیرو'
    elif instrument == 'bgilan':
        return 'بگیلان'
    elif instrument == 'bzagrs':
        return 'بزاگرس'
    elif instrument == 'vhvr':
        return 'وهور'
    elif instrument == 'abada':
        return 'آبادا'
    elif instrument == 'bfajr':
        return 'بفجر'
    elif instrument == 'mobin':
        return 'مبین'
    elif instrument == 'bmpna':
        return 'بمپنا'
    elif instrument == 'bkhnoj':
        return 'بکهنوج'
    # گروه:بيمه وصندوق بازنشستگي به جزتامين اجتماعي
    elif instrument == 'vdy':
        return 'ودی'
    elif instrument == 'asia':
        return 'آسیا'
    elif instrument == 'bpas':
        return 'بپاس'
    elif instrument == 'ma':
        return 'ما'
    elif instrument == 'dana':
        return 'دانا'
    elif instrument == 'bsama':
        return 'بساما'
    elif instrument == 'mihn':
        return 'میهن'
    elif instrument == 'mellat':
        return 'ملت'
    elif instrument == 'atkam':
        return 'اتکام'
    elif instrument == 'parsian':
        return 'پارسیان'
    elif instrument == 'vsin':
        return 'وسین'
    elif instrument == 'albrz':
        return 'البرز'
    elif instrument == 'arman':
        return 'آرمان'
    elif instrument == 'vtaavn':
        return 'وتعاون'
    elif instrument == 'novin':
        return 'نوین'
    elif instrument == 'bno':
        return 'بنو'
    elif instrument == 'vhkmt':
        return 'وحکمت'
    elif instrument == 'atkie':
        return 'اتکای'
    elif instrument == 'koser':
        return 'کوثر'
    elif instrument == 'vrazi':
        return 'ورازی'
    elif instrument == 'bkhavar':
        return 'بخاور'
    elif instrument == 'vmalm':
        return 'ومعلم'
    elif instrument == 'vhafez':
        return 'وحافظ'
    elif instrument == 'vsrmd':
        return 'وسرمد'
    elif instrument == 'vafri':
        return 'وآفری'
    elif instrument == 'tejarat':
        return 'تجارت'
    elif instrument == 'baran':
        return 'باران'
    # گروه:مخابرات
    elif instrument == 'akhabr':
        return 'اخابر'
    elif instrument == 'hamrah':
        return 'همراه'
    # گروه:ماشين آلات و دستگاه‌هاي برقي
    elif instrument == 'bshhab':
        return 'بشهاب'
    elif instrument == 'bkam':
        return 'بکام'
    elif instrument == 'btrans':
        return 'بترانس'
    elif instrument == 'bmoto':
        return 'بموتو'
    elif instrument == 'bkab':
        return 'بکاب'
    elif instrument == 'bniro':
        return 'بنیرو'
    elif instrument == 'bsoich':
        return 'بسویچ'
    elif instrument == 'niro':
        return 'نیرو'
    elif instrument == 'balbr':
        return 'بالبر'
    elif instrument == 'bieka':
        return 'بایکا'
    elif instrument == 'btk':
        return 'بتک'
    # گروه:پيمانكاري صنعتي
    elif instrument == 'balas':
        return 'بالاس'
    elif instrument == 'khsadra':
        return 'خصدرا'
    elif instrument == 'vpsa':
        return 'وپسا'
    # گروه:لاستيك و پلاستيك
    elif instrument == 'pkavir':
        return 'پکویر'
    elif instrument == 'pkerman':
        return 'پکرمان'
    elif instrument == 'pasa':
        return 'پاسا'
    elif instrument == 'ptier':
        return 'پتایر'
    elif instrument == 'plask':
        return 'پلاسک'
    elif instrument == 'psahand':
        return 'پسهند'
    elif instrument == 'pdrakhsh':
        return 'پدرخش'
    elif instrument == 'pizd':
        return 'پیزد'
    elif instrument == 'ploleh':
        return 'پلوله'
    elif instrument == 'parta':
        return 'پارتا'
    elif instrument == 'plast':
        return 'پلاست'
    elif instrument == 'pshahn':
        return 'پشاهن'
    # گروه:خدمات فني و مهندسي
    elif instrument == 'rmpna':
        return 'رمپنا'
    elif instrument == 'rnik':
        return 'رنیک'
    elif instrument == 'khfola':
        return 'خفولا'
    elif instrument == 'rtko':
        return 'رتکو'
    elif instrument == 'tpola':
        return 'تپولا'
    elif instrument == 'taba':
        return 'تابا'
    # گروه:سيمان، آهك و گچ
    elif instrument == 'sfars':
        return 'سفارس'
    elif instrument == 'stran':
        return 'ستران'
    elif instrument == 'sshargh':
        return 'سشرق'
    elif instrument == 'sbzoa':
        return 'سبزوا'
    elif instrument == 'spaha':
        return 'سپاها'
    elif instrument == 'ssofi':
        return 'سصوفی'
    elif instrument == 'smazn':
        return 'سمازن'
    elif instrument == 'sidko':
        return 'سیدکو'
    elif instrument == 'sarab':
        return 'ساراب'
    elif instrument == 'sbaghr':
        return 'سباقر'
    elif instrument == 'sarom':
        return 'ساروم'
    elif instrument == 'skord':
        return 'سکرد'
    elif instrument == 'ssafha':
        return 'سصفها'
    elif instrument == 'shegmat':
        return 'سهگمت'
    elif instrument == 'skhoz':
        return 'سخوز'
    elif instrument == 'sdor':
        return 'سدور'
    elif instrument == 'sarbil':
        return 'ساربیل'
    elif instrument == 'silam':
        return 'سیلام'
    elif instrument == 'srod':
        return 'سرود'
    elif instrument == 'skhoaf':
        return 'سخواف'
    elif instrument == 'skhazar':
        return 'سخزر'
    elif instrument == 'sbhan':
        return 'سبهان'
    elif instrument == 'sshomal':
        return 'سشمال'
    elif instrument == 'skerma':
        return 'سکرما'
    elif instrument == 'sfano':
        return 'سفانو'
    elif instrument == 'snir':
        return 'سنیر'
    elif instrument == 'sgharb':
        return 'سغرب'
    elif instrument == 'sjam':
        return 'سجام'
    elif instrument == 'sfar':
        return 'سفار'
    elif instrument == 'sehormoz':
        return 'سهرمز'
    elif instrument == 'sbjno':
        return 'سبجنو'
    elif instrument == 'skhash':
        return 'سخاش'
    elif instrument == 'skaron':
        return 'سکارون'
    elif instrument == 'sghaien':
        return 'سقاین'
    elif instrument == 'sdasht':
        return 'سدشت'
    elif instrument == 'sita':
        return 'سیتا'
    elif instrument == 'saveh':
        return 'ساوه'
    elif instrument == 'saroj':
        return 'ساروج'
    elif instrument == 'slar':
        return 'سلار'
    elif instrument == 'smtaz':
        return 'سمتاز'
    # گروه:ساخت محصولات فلزي
    elif instrument == 'chodan':
        return 'چدن'
    elif instrument == 'farak':
        return 'فاراک'
    elif instrument == 'fama':
        return 'فاما'
    elif instrument == 'fazar':
        return 'فاذر'
    elif instrument == 'fjam':
        return 'فجام'
    elif instrument == 'flami':
        return 'فلامی'
    elif instrument == 'fbstm':
        return 'فبستم'
    elif instrument == 'fbira':
        return 'فبیرا'
    elif instrument == 'kia':
        return 'کیا'
    elif instrument == 'fslir':
        return 'فسلیر'
    elif instrument == 'fanarzhi':
        return 'فنرژی'
    elif instrument == 'fjosh':
        return 'فجوش'
    # گروه:قند و شكر
    elif instrument == 'ghsabet':
        return 'قثابت'
    elif instrument == 'ghazvin':
        return 'قزوین'
    elif instrument == 'ghnisha':
        return 'قنیشا'
    elif instrument == 'ghsafha':
        return 'قصفها'
    elif instrument == 'ghshekar':
        return 'قشکر'
    elif instrument == 'ghchar':
        return 'قچار'
    elif instrument == 'ghlorest':
        return 'قلرست'
    elif instrument == 'ghpira':
        return 'قپیرا'
    elif instrument == 'ghshir':
        return 'قشیر'
    elif instrument == 'ghhkmt':
        return 'قهکمت'
    elif instrument == 'ghshahd':
        return 'قشهد'
    elif instrument == 'ghshrin':
        return 'قشرین'
    elif instrument == 'ghmro':
        return 'قمرو'
    elif instrument == 'ghjam':
        return 'قجام'
    elif instrument == 'ghnghsh':
        return 'قنقش'
    elif instrument == 'gharom':
        return 'قاروم'
    elif instrument == 'ghisto':
        return 'قیستو'
    # گروه:كاشي و سراميك
    elif instrument == 'kehafez':
        return 'کحافظ'
    elif instrument == 'ktram':
        return 'کترام'
    elif instrument == 'ksady':
        return 'کسعدی'
    elif instrument == 'kpars':
        return 'کپارس'
    elif instrument == 'kolond':
        return 'کلوند'
    elif instrument == 'ksaveh':
        return 'کساوه'
    elif instrument == 'khram':
        return 'کهرام'
    elif instrument == 'ksdf':
        return 'کصدف'
    elif instrument == 'knilo':
        return 'کنیلو'
    elif instrument == 'kasfa':
        return 'کاصفا'
    elif instrument == 'kchini':
        return 'کچینی'
    # گروه:هتل و رستوران
    elif instrument == 'smga':
        return 'سمگا'
    elif instrument == 'gshan':
        return 'گشان'
    elif instrument == 'gkoser':
        return 'گکوثر'
    elif instrument == 'gdna':
        return 'گدنا'
    elif instrument == 'gpars':
        return 'گپارس'
    elif instrument == 'gkish':
        return 'گکیش'
    # گروه:توليد محصولات كامپيوتري الكترونيكي ونوري
    elif instrument == 'madyra':
        return 'مادیرا'
    # گروه:استخراج ساير معادن
    elif instrument == 'kmash':
        return 'کماسه'
    # گروه:دباغي، پرداخت چرم و ساخت انواع پاپوش
    elif instrument == 'vmeli':
        return 'وملی'
    # گروه:استخراج نفت گاز و خدمات جنبي جز اکتشاف
    elif instrument == 'hfari':
        return 'حفاری'
    elif instrument == 'shsakht':
        return 'شساخت'
    elif instrument == 'prshia':
        return 'پرشیا'
    # گروه:واسطه‌گري‌هاي مالي و پولي
    elif instrument == 'vlshargh':
        return 'ولشرق'
    elif instrument == 'vsenv':
        return 'وثنو'
    elif instrument == 'vars':
        return 'وارس'
    elif instrument == 'vlana':
        return 'ولانا'
    elif instrument == 'vsevgh':
        return 'وثوق'
    elif instrument == 'vahsa':
        return 'واحصا'
    elif instrument == 'vsna':
        return 'وسنا'
    elif instrument == 'vltjar':
        return 'ولتجار'
    elif instrument == 'vatvs':
        return 'وآتوس'
    elif instrument == 'vlraz':
        return 'ولراز'
    elif instrument == 'vmshan':
        return 'ومشان'
    elif instrument == 'vahia':
        return 'واحیا'
    elif instrument == 'arian':
        return 'آریان'
    elif instrument == 'vkvser':
        return 'وکوثر'
    # گروه:ساخت دستگاه‌ها و وسايل ارتباطي
    elif instrument == 'lpars':
        return 'لپارس'
    elif instrument == 'lpiam':
        return 'لپیام'
    elif instrument == 'lkma':
        return 'لکما'
    # گروه:استخراج زغال سنگ
    elif instrument == 'kshargh':
        return 'کشرق'
    elif instrument == 'ktbs':
        return 'کطبس'
    elif instrument == 'kpror':
        return 'کپرور'
    # گروه:حمل و نقل آبي
    elif instrument == 'haria':
        return 'حاریا'
    elif instrument == 'hkhazar':
        return 'حخزر'
    # گروه:ساير واسطه گريهاي مالي
    elif instrument == 'vlsapa':
        return 'ولساپا'
    elif instrument == 'vliz':
        return 'ولیز'
    elif instrument == 'vlbahman':
        return 'ولبهمن'
    elif instrument == 'viran':
        return 'وایران'
    elif instrument == 'vlghdr':
        return 'ولغدر'
    elif instrument == 'vlsanam':
        return 'ولصنم'
    elif instrument == 'vlmellat':
        return 'ولملت'
    elif instrument == 'vlpars':
        return 'ولپارس'
    # گروه:منسوجات
    elif instrument == 'ntrin':
        return 'نطرین'
    elif instrument == 'nmrino':
        return 'نمرینو'
    elif instrument == 'ntos':
        return 'نتوس'
    # گروه:استخراج کانه هاي فلزي
    elif instrument == 'kama':
        return 'کاما'
    elif instrument == 'kroi':
        return 'کروی'
    elif instrument == 'kgol':
        return 'کگل'
    elif instrument == 'kchad':
        return 'کچاد'
    elif instrument == 'kdama':
        return 'کدما'
    elif instrument == 'vmaaden':
        return 'ومعادن'
    elif instrument == 'tasiko':
        return 'تاصیکو'
    elif instrument == 'kbafgh':
        return 'کبافق'
    elif instrument == 'kmangenez':
        return 'کمنگنز'
    elif instrument == 'kghr':
        return 'کگهر'
    elif instrument == 'tknar':
        return 'تکنار'
    elif instrument == 'knor':
        return 'کنور'
    # گروه:محصولات چوبي
    elif instrument == 'chfibr':
        return 'چفیبر'
    elif instrument == 'chnopa':
        return 'چنوپا'
    # گروه:انتشار، چاپ و تکثير
    elif instrument == 'chafst':
        return 'چافست'
    # گروه:اطلاعات و ارتباطات
    elif instrument == 'aprdaz':
        return 'اپرداز'
    elif instrument == 'hie_web':
        return 'های وب'
    elif instrument == 'aoan':
        return 'اوان'
    # گروه:فعاليت هاي هنري، سرگرمي و خلاقانه
    elif instrument == 'vhnr':
        return 'وهنر'
    # گروه:تجارت عمده فروشي به جز وسايل نقليه موتور
    elif instrument == 'bmila':
        return 'بمیلا'
    # گروه:فعاليت مهندسي، تجزيه، تحليل و آزمايش فني
    elif instrument == 'khbazrs':
        return 'خبازرس'
    # گروه:ابزارپزشکي، اپتيکي و اندازه‌گيري
    elif instrument == 'akntor':
        return 'آکنتور'
    # شاخص ها
    elif instrument == 'Bazar_Dovom_FaraBourse6':
        return 'بازار دوم فرابورس6'
    elif instrument == 'Shakhes_kol_FaraBourse6':
        return 'شاخص کل فرابورس6'
    elif instrument == 'Bazar_Aval_FaraBourse6':
        return 'بازار اول فرابورس6'
    elif instrument == '34-Khodro6':
        return '34-خودرو6'
    elif instrument == '36-Mobloman6':
        return '36-مبلمان6'
    elif instrument == '21-Mahsolat_kaghz6':
        return '21-محصولات کاغذ6'
    elif instrument == 'bazdh_nghdy_o_Gheymat6':
        return 'بازده نقدی و قیمت6'
    elif instrument == '44-Shimiaee6':
        return '44-شیمیایی6'
    elif instrument == '31-Dastgahhie_brghi6':
        return '31-دستگاههای برقی6'
    elif instrument == '56-Sarmaye_gzariha6':
        return '56-سرمایه گذاریها6'
    elif instrument == '01-Zeraat6':
        return '01-زراعت6'
    elif instrument == 'TEPIX':
        return 'شاخص کل6'
    elif instrument == '27-Felezat_asasi6':
        return '27-فلزات اساسی6'
    elif instrument == '39-Chand_Reshteh_ie_s6':
        return '39-چند رشته ای ص6'
    elif instrument == 'Shakhes_Sanat6':
        return 'شاخص صنعت6'
    elif instrument == '64-radyoii6':
        return '64-رادیویی6'
    elif instrument == '45-pimankari6':
        return '45-پیمانکاری6'
    elif instrument == 'Shakhes50Sherkat_Faaltar6':
        return 'شاخص50شرکت فعالتر6'
    elif instrument == '74-Fani_Mohandesi6':
        return '74-فنی مهندسی6'
    elif instrument == '26-kani_GheyreFelezi6':
        return '26-کانی غیرفلزی6'
    elif instrument == '25-lastik6':
        return '25-لاستیک6'
    elif instrument == 'Shakhes_azad_Shenavar6':
        return 'شاخص آزاد شناور6'
    elif instrument == '33-abzar_Pezeshki6':
        return '33-ابزار پزشکی6'
    elif instrument == '65-mali6':
        return '65-مالی6'
    elif instrument == '49-kashi_o_sramik6':
        return '49-کاشی و سرامیک6'
    elif instrument == '14-Sayere_maaden6':
        return '14-سایر معادن6'
    elif instrument == 'Shakhes_Bazar_Aval6':
        return 'شاخص بازار اول6'
    elif instrument == '35-Haml_o_Naghl6':
        return '35-حمل و نقل6'
    elif instrument == '20-Mahsolat_chobi6':
        return '20-محصولات چوبی6'
    elif instrument == '17-Mansojat6':
        return '17-منسوجات6'
    elif instrument == '19-Mahsolat_Charmi6':
        return '19-محصولات چرمی6'
    elif instrument == 'Shakhes_Gheymat_50_Sherkat6':
        return 'شاخص قیمت 50 شرکت6'
    elif instrument == '53-siman6':
        return '53-سیمان6'
    elif instrument == 'Shakhes_Bazar_Dovom6':
        return 'شاخص بازار دوم6'
    elif instrument == '57-bankha6':
        return '57-بانکها6'
    elif instrument == 'Estekhraj_naft_jzkshf6':
        return 'استخراج نفت جزکشف6'
    elif instrument == 'bimeh_o_baznshsth666':
        return 'بیمه و بازنشسته666'
    elif instrument == 'Shakhes_30_Sherkat_Bozorg6':
        return 'شاخص قیمت 30 شرکت6'
    elif instrument == '58-Sayeremali6':
        return '58-سایرمالی6'
    elif instrument == '32-Vasayel_Ertebati6':
        return '32-وسایل ارتباطی6'
    elif instrument == '60-Haml_o_Naghl6':
        return '60-حمل و نقل6'
    elif instrument == '54-kani_GheyreFelezi6':
        return '54-کانی غیرفلزی6'
    elif instrument == '10-zghal_sng6':
        return '10-ذغال سنگ6'
    elif instrument == '28-Mahsolat_Felezi6':
        return '28-محصولات فلزی6'
    elif instrument == '38-Ghand_o_shekar6':
        return '38-قند و شکر6'
    elif instrument == '22-Enteshar_o_chap6':
        return '22-انتشار و چاپ6'
    elif instrument == '42-Ghazaii_Ghand_Ghand6':
        return '42-غذایی بجز قند6'
    elif instrument == '40-tamin_ab،brgh،g6':
        return '40-تامین آب،برق،گ6'
    elif instrument == 'Shakhes_kol_(ham_Vazn)6':
        return 'شاخص کل (هم وزن)6'
    elif instrument == 'Shakhes_Gheymat6':
        return 'شاخص قیمت6'
    elif instrument == 'Shakhes_Gheymat(ham_Vazn6)':
        return 'شاخص قیمت(هم وزن6)'


    else:
        return None


def feed_candle():

    # instruments = models.Instrumentsel.objects.all().filter(type='warrant')
    # print(instruments.count())
    # for itm in instruments:
    #     print(f'{itm}-{itm.id}')
    #     print(f'\'{itm}\',')
    # return

    #-----------------------------------------------------------
    # check empty instruments
    # instruments_chart = models.Chart.objects.all().values('instrument').distinct()
    # instruments = models.Instrumentsel.objects.all()
    # # instruments = models.Instrumentsel.objects.filter(type='index').distinct()
    # print(instruments_chart.count())
    #
    # for itm in instruments:
    #     # print(f'{itm}')
    #     # continue
    #     res = instruments_chart.filter(instrument=itm.id)
    #     if res.count() > 0:
    #         # print(f'{itm}-{itm.id} exist')
    #         pass
    #     else:
    #         # print(f'{itm}-{itm.id} dose not exist')
    #         print(f'{itm}')
    #         continue
    #         url = f'http://mediadrive.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/tradedetails?instrument.id={itm.id}'
    #
    #         req = requests.get(url)
    #         data1 = req.json()
    #         print(len(data1['data']))
    #         #  check next pagination
    #         if len(data1['data']) == 0:
    #             print(f"remove: {itm}")
    #             itm.delete()
    # return
    #-----------------------------------------------------------

    is_haghtaghadom = False  #True #

    directories = os.listdir('./helper/')
    for directory in directories:
        path = f'./helper/{directory}/'
        # print(os.path.isdir(path), directory)
        if os.path.isdir(path):
            print(f'----------check {directory}')
            if is_haghtaghadom is True:
                directory2 = directory[0:len(directory) - 1]
                # print(f'check2 {directory2}')
                farsi_title = find_farsi_title(directory2)
            else:
                farsi_title = find_farsi_title(directory)
            print(farsi_title)
            if farsi_title is None:
                continue

            if is_haghtaghadom is True:
                farsi_title = farsi_title + 'ح'
                print(farsi_title)

            try:
                # symbol = models.Instrumentsel.objects.get(short_name=directory)
                symbol = models.Instrumentsel.objects.get(short_name=farsi_title)
                # symbol = models.Instrumentsel.objects.get(id=1931)
            except ObjectDoesNotExist:
                print(f'{directory}-{farsi_title}- Instrument not found!')
                continue
            except MultipleObjectsReturned:
                print(f'{directory}-{farsi_title}- multiple Instrument found!')
                continue
            print(f'symbol: {symbol}')

            for file in os.listdir(path):
                # print(file)
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
