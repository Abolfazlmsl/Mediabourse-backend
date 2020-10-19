import pyautogui
import pyperclip

# print('test')
# pos = pyautogui.position()  # current mouse x and y
# print(pos)
# size = pyautogui.size()  # current screen resolution width and height
# print(size)
# pyautogui.PAUSE = 2.5  # Set up a 2.5 second pause after each PyAutoGUI call
# pyautogui.sleep(2)
# check = pyautogui.onScreen(20, 3000)  # True if x & y are within the screen.
# print(check)

# pyautogui.moveTo(10, 300, duration=1)  # move mouse to XY coordinates over num_second seconds
# pyautogui.moveRel(10, 300, duration=1)  # move mouse relative to its current position
# pyautogui.dragTo(100, 300, duration=1)  # drag mouse to XY
# pyautogui.dragRel(100, 300, duration=0.1)  # drag mouse relative to its current position
# pyautogui.click(x=100, y=300, clicks=1, interval=1, button='left')  # The button keyword argument can be 'left', 'middle', or 'right'.

# pyautogui.typewrite('Hello world!\n', interval=0.1)  # useful for entering text, newline is Enter
# pyautogui.typewrite(['a', 'b', 'c', 'left', 'backspace', 'enter', 'f1'], interval=1)
# pyautogui.alert('This displays some text with an OK button.')
# pyautogui.confirm('This displays text and has an OK and Cancel button.')
# pyautogui.prompt('This lets the user type in a string and press OK.')

# pyautogui.screenshot('foo.png')  # returns a Pillow/PIL Image object, and saves it to a file
# loc = pyautogui.locateOnScreen('loc.png')  # returns (left, top, width, height) of first place it is found
# print(loc)
# loc = pyautogui.locateCenterOnScreen('loc.png')  # returns center x and y
# print(loc)
# pyautogui.leftClick(loc)

# show desktop
# loc = pyautogui.locateCenterOnScreen('./pyautoPics/showDesktop.png')  # returns center x and y
# pyautogui.leftClick(loc)
# pyautogui.sleep(0.2)

# run mofidtrader
# loc = pyautogui.locateCenterOnScreen('./pyautoPics/mofidapp.png')  # returns center x and y
# pyautogui.doubleClick(loc)
# if loc is None:
#     pyautogui.alert('can not find mofidtrader icon')

# pyautogui.sleep(3)

ins_list2 = {
    'اعتلاح',
    'افراح',
    'حسیناح',
    'وشهرح',
    'کنورح',
    'ثعتماح',
    'شلردح',
    'سجامح',
    'میدکوح',
    'معیارح',
    'وپاسارح',
    'وانصارح',
    'ثباغح',
    'وشمالح',
    'حکمتح',
    'کرماشاح',
    'وداناح',
    'بمیلاح',
    'ملتح',
    'بساماح',
    'پلاستح',
    'چبسپاح',
    'لازماح',
    'پشاهنح',
    'سنوینح',
    'وخارزمح',
    'چکارمح',
    'غیوانح',
    'لپیامح',
    'بایکاح',
    'غنابح',
    'فسدیدح',
    'قجامح',
    'کابگنح',
    'کقزویح',
    'خصدراح',
    'ممسنیح',
    'فزرینح',
    'فولاژح',
    'دهدشتح',
    'لکماح',
    'سلارح',
    'فبیراح',
    'وآوینح',
    'تشتادح',
    'شزنگح',
    'کایتاح',
    'لخانهح',
    'ثترانح',
    'نیروح',
    'پارتاح',
    'رتاپح',
    'آرمانح',
    'فن آواح',
    'کسراح',
    'غشصفاح',
    'وتوصاح',
    'شبهرنح',
    'قشکرح',
    'سفارسح',
    'کفراح',
    'کرویح',
    'بکابح',
    'ددامح',
    'خاهنح',
    'غگلح',
    'کگازح',
    'وغدیرح',
    'شفارسح',
    'شکلرح',
    'فلامیح',
    'سهرمزح',
    'وپتروح',
    'فنوالح',
    'ثابادح',
    'چکارنح',
    'ولیزح',
    'پاساح',
    'دابورح',
    'شدوصح',
    'سمازنح',
    'فولادح',
    'خمحرکهح',
    'سترانح',
    'خزامیاح',
    'درازکح',
    'فباهنرح',
    'والبرح',
    'دفاراح',
    'غبهنوشح',
    'بشهابح',
    'ثفارسح',
    'وصندوقح',
    'کبافقح',
    'سصفهاح',
    'کچادح',
    'دکیمیح',
    'وصنعتح',
    'خکارح',
    'زمگساح',
    'فرآورح',
    'سقاینح',
    'دامینح',
    'کرازیح',
    'ختراکح',
    'فجامح',
    'قپیراح',
    'دلرح',
    'حتوکاح',
    'قشهدح',
    'لابساح',
    'رانفورح',
    'کلوندح',
    'اخابرح',
    'پدرخشح',
    'شگلح',
    'وتوسح',
    'بنیروح',
    'سبجنوح',
    'قلرستح',
    'غدامح',
    'بترانسح',
    'تپمپیح',
    'سفارح',
    'وسپهح',
    'سدورح',
    'دسیناح',
    'غگرجیح',
    'سنیرح',
    'چفیبرح',
    'دزهراویح',
    'غسالمح',
    'دفراح',
    'وآذرح',
    'سیلامح',
    'قزوینح',
    'قنیشاح',
    'ورناح',
    'غالبرح',
    'کهمداح',
    'کترامح',
    'خلنتح',
    'وامیدح',
    'فایراح',
    'خشرقح',
    'غشهدح',
    'سپاهاح',
    'قثابتح',
    'رمپناح',
    'قهکمتح',
    'ثامانح',
    'خمهرح',
    'غمارگح',
    'دسبحاح',
    'شفنح',
    'وبیمهح',
    'غدشتح',
    'ولساپاح',
    'ختوقاح',
    'کخاکح',
    'وکارح',
    'واتیح',
    'قمروح',
    'خفنرح',
    'آکنتورح',
    'خموتورح',
    'وبشهرح',
    'کپارسح',
    'ساربیلح',
    'کگلح',
    'وبهمنح',
    'فلولهح',
    'کاماح',
    'شاراکح',
    'ونیروح',
    'ولغدرح',
    'سخزرح',
    'دروزح',
    'غمهراح',
    'وتوشهح',
    'بکامح',
    'فاسمینح',
    'کفپارسح',
    'کماسهح',
    'سغربح',
    'شلعابح',
    'تکشاح',
    'حتایدح',
    'ومعادنح',
    'مرقامح',
    'کمنگنزح',
    'دلقماح',
    'فاراکح',
    'پسهندح',
    'شخارکح',
    'سکردح',
    'وپخشح',
    'سارابح',
    'شپاکساح',
    'فاذرح',
    'ثاختح',
    'لخزرح',
    'تایراح',
    'تکمباح',
    'لبوتانح',
    'ونوینح',
    'شپناح',
    'خمحورح',
    'ودیح',
    'وبملتح',
    'وتجارتح',
    'پترو گچسارانح',
    'آرینح',
    'البرزح',
    'سمگاح',
    'دیح',
    'شکبیرح',
    'وپارسح',
    'حپتروح',
    'خزرح',
    'فپنتاح',
    'خوسازح',
    'کحافظح',
    'بسویچح',
    'سشمالح',
    'کدماح',
    'ثشاهدح',
    'ثمسکنح',
    'چافستح',
    'دکوثرح',
    'وساپاح',
    'خرینگح',
    'ونیکیح',
    'خچرخشح',
    'پردیسح',
    'حکشتیح',
    'شاملاح',
    'قصفهاح',
    'خگسترح',
    'ولصنمح',
    'شیرازح',
    'غپاکح',
    'خپویشح',
    'سهگمتح',
    'پتایرح',
    'دعبیدح',
    'واعتبارح',
    'فنوردح',
    'وبانکح',
    'خاذینح',
    'لسرماح',
    'خساپاح',
    'کسعدیح',
    'رتکوح',
    'خکمکح',
    'شسیناح',
    'بموتوح',
    'فمرادح',
    'سبهانح',
    'تکنوح',
    'دپارسح',
    'غاذرح',
    'وتوکاح',
    'خپارسح',
    'شنفتح',
    'وبوعلیح',
    'دیرانح',
    'کساپاح',
    'کاذرح',
    'سارومح',
    'وصناح',
    'سخاشح',
    'بالبرح',
    'غشانح',
    'سدشتح',
    'غبشهرح',
    'دتمادح',
    'فسپاح',
    'دشیمیح',
    'دجابرح',
    'فولایح',
    'آ س پح',
    'وسکابح',
    'بپاسح',
    'پارسانح',
    'فالومح',
    'وقوامح',
    'پارسیانح',
    'آریانح',
    'سباقرح',
    'تکنارح',
    'کازروح',
    'پخشح',
    'گکیشح',
    'زنگانح',
    'رکیشح',
    'سدبیرح',
    'دتولیدح',
    'وسناح',
    'سخوافح',
    'وکادوح',
    'کفرآورح',
    'سخرمح',
    'توریلح',
    'شجمح',
    'بدکوح',
    'کی بی سیح',
    'فسلیرح',
    'سامانح',
    'دارابح',
    'فساح',
    'جهرمح',
    'ورازیح',
    'وهورح',
    'دشیریح',
    'کتوکاح',
    'وثوقح',
    'وحافظح',
    'سرچشمهح',
    'قشیرح',
    'پاکشوح',
    'کاصفاح',
    'ومللح',
    'دسانکوح',
    'وخاورح',
    'بکهنوجح',
    'فاهوازح',
    'بصباح',
    'اتکامح',
    'اتکایح',
    'شرانلح',
    'همراهح',
    'سیدکوح',
    'شپاسح',
    'حپارساح',
    'کوثرح',
    'ارفعح',
    'وآیندح',
    'ثپردیسح',
    'ولبهمنح',
    'حخزرح',
    'فافزاح',
    'ثغربح',
    'ثشرقح',
    'وآفریح',
    'شبریزح',
    'شپدیسح',
    'ثرودح',
    'وآرینح',
    'وکوثرح',
    'قاسمح',
    'شکفح',
    'حقشمح',
    'دبالکح',
    'زنجانح',
    'پکویرح',
    'وسرمدح',
    'شصفهاح',
    'ثعمراح',
    'وسینح',
    'ثقزویح',
    'کمرجانح',
    'فلاتح',
    'ثنورح',
    'کیسونح',
    'میهنح',
    'داناح',
    'غشهدابح',
    'تاپیکوح',
    'ماح',
    'حبندرح',
    'شپلیح',
    'رنیکح',
    'زقیامح',
    'گوهرانح',
    'مادیراح',
    'کاسپینح',
    'ولرازح',
    'شپتروح',
    'لوتوسح',
    'کویرح',
    'شصدفح',
    'تاصیکوح',
    'تیپیکوح',
    'ساروجح',
    'غشوکوح',
    'پترولح',
    'کگهرح',
    'افقح',
    'بزاگرسح',
    'کمیناح',
    'وملتح',
    'خفناورح',
    'پرداختح',
    'ثالوندح',
    'خاورح',
    'نوینح',
    'خکاوهح',
    'حفاریح',
    'تلیسهح',
    'قنقشح',
    'سمایهح',
    'امیدح',
    'کهرامح',
    'شفاراح',
    'جمح',
    'وتعاونح',
    'کاوهح',
    'وگردشح',
    'سفانوح',
    'برکتح',
    'ولشرقح',
    'دقاضیح',
    'اوانح',
    'غویتاح',
    'سخوزح',
    'خفولاح',
    'کنیلوح',
    'صباح',
    'بنوح',
    'آباداح',
    'تاپکیشح',
    'ساذریح',
    'فماکح',
}

ins_list_shakhes = [
    'بازار دوم فرابورس6'
    , 'شاخص کل فرابورس6'
    , 'بازار اول فرابورس6'
    , '34-خودرو6'
    , '36-مبلمان6'
    , '21-محصولات کاغذ6'
    , 'بازده نقدی و قیمت6'
    , '44-شیمیایی6'
    , '31-دستگاههای برقی6'
    , '56-سرمایه گذاریها6'
    , '01-زراعت6'
    , 'شاخص کل6'
    , '27-فلزات اساسی6'
    , '39-چند رشته ای ص6'
    , 'شاخص صنعت6'
    , '64-رادیویی6'
    , '45-پیمانکاری6'
    , 'شاخص50شرکت فعالتر6'
    , '74-فنی مهندسی6'
    , '26-کانی غیرفلزی6'
    , '25-لاستیک6'
    , 'شاخص آزاد شناور6'
    , '33-ابزار پزشکی6'
    , '65-مالی6'
    , '49-کاشی و سرامیک6'
    , '14-سایر معادن6'
    , 'شاخص بازار اول6'
    , '35-حمل و نقل6'
    , '20-محصولات چوبی6'
    , '17-منسوجات6'
    , '19-محصولات چرمی6'
    , 'شاخص قیمت 50 شرکت6'
    , '53-سیمان6'
    , 'شاخص بازار دوم6'
    , '57-بانکها6'
    , 'استخراج نفت جزکشف6'
    , 'بیمه و بازنشسته666'
    , 'شاخص 30 شرکت بزرگ6'
    , 'شاخص قیمت 30 شرکت6'
    , '58-سایرمالی6'
    , '32-وسایل ارتباطی6'
    , '60-حمل و نقل6'
    , '54-کانی غیرفلزی6'
    , '10-ذغال سنگ6'
    , '28-محصولات فلزی6'
    , '38-قند و شکر6'
    , '22-انتشار و چاپ6'
    , '42-غذایی بجز قند6'
    , '40-تامین آب،برق،گ6'
    , 'شاخص کل (هم وزن)6'
    , 'شاخص قیمت6'
    , 'شاخص قیمت(هم وزن6)'
]

ins_list = [
    'ملتح',
    'بساماح',
    'سهرمزح',
    'دفراح',
    'وآذرح',
    'کدماح',
    'واعتبارح',
    'ساروجح',
    'غشوکوح',
    'پترولح',
    'کگهرح',
    'افقح',
    'بزاگرسح',
    'پرداختح',
    'جوین',
    'ثالوندح',
    'حفاریح',
    'تلیسهح',
    'امیدح',
    'جمح',
    'وتعاونح',
    'کاوهح',
    'وگردشح',
    'سفانوح',
    'برکتح',
    'ولشرقح',
    'دقاضیح',
    'اوانح',
    'سخوزح',
    'خفولاح',
    'صباح',
    'تاپکیشح',
    'فماکح'
]

# sleep
def sleep(num):
    pyautogui.sleep(num)


# find exporter window
def find_exporter_win():
    loc = pyautogui.locateCenterOnScreen('./pyautoPics/exporter.png')  # returns center x and y
    # print(loc)
    if loc is not None:
        # print("exporter finded")
        pyautogui.moveTo(loc)
        # pyautogui.click()
        pyautogui.dragRel(200, 0, duration=0.2)
        # delay to open window
        pyautogui.sleep(0.3)
        return True
    else:
        print('can not find exporter')
        return False


# find exporter checkbox1
def find_exporter_checks_okbtn(is_find_checkbox=False):
    if is_find_checkbox is False:
        pyautogui.move(500, -160, duration=0.1)
        pyautogui.leftClick()
        pyautogui.move(0, 25, duration=0.1)
        pyautogui.leftClick()
        pyautogui.move(220, 50, duration=0.1)
        pyautogui.leftClick()
        return True
    else:
        loc = pyautogui.locateCenterOnScreen('./pyautoPics/exporter_chec1.png')  # returns center x and y
        print(loc)
        if loc is not None:
            print(f"exporter finded {loc}-{loc.x},{loc.y}")
            pyautogui.moveTo(loc)
            pyautogui.leftClick()
            pyautogui.move(0, 20, duration=0.1)
            pyautogui.leftClick()
            pyautogui.move(220, 50, duration=0.1)
            pyautogui.leftClick()
            return True
        else:
            print('can not find exporter check1')
            return False


# find symbol tab
def find_symboltab(loc_symbolTab=None):
    if loc_symbolTab is None:
        loc_symbolTab = pyautogui.locateCenterOnScreen('./pyautoPics/symbolsTab.png')  # returns center x and y
    # print(loc)
    if loc_symbolTab is not None:
        # print("finded tab")
        pyautogui.click(loc_symbolTab)
        # scroll down to show 'click to add' link
        pyautogui.move(0, -150)
        pyautogui.click()
        pyautogui.hotkey("end")
        # Hide all symbols
        # pyautogui.rightClick()
        # pyautogui.move(10, 200)
        # pyautogui.leftClick()
        return True
    else:
        print('can not find symbol tab')
        return False


# type instrument, language must be english in system
def find_addsymbol_type(instrumnet):
    loc = pyautogui.locateCenterOnScreen('./pyautoPics/addSymbol.png')  # returns center x and y
    if loc is not None:
        pyautogui.doubleClick(loc)
        pyperclip.copy(instrumnet)
        pyautogui.sleep(0.5)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.sleep(0.5)
        pyautogui.hotkey("enter")
        pyautogui.sleep(1)
        # open menu
        pyautogui.rightClick()
        pyautogui.move(10, 30, duration=0.1)
        # click on open chart window
        pyautogui.leftClick()
        # sleep(5)
        return True
    else:
        print("can not locate add symbol")
        return False


loc_symbolTab = None
for ins in ins_list:

    print(f'check {ins} ...')
    flag = True
    if find_symboltab(loc_symbolTab) is False:
        flag = False
    if flag and find_addsymbol_type(ins) is False:
        flag = False
    if flag and find_exporter_win() is False:
        flag = False
    if flag and find_exporter_checks_okbtn() is False:
        flag = False
    print(f'prosecc of {ins} completed')
    # sleep(5)
