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
    else:
        return None


def feed_candle():
    directories = os.listdir('./helper/')
    for directory in directories:
        path = f'./helper/{directory}/'
        print(os.path.isdir(path), directory)
        if os.path.isdir(path):
            print(f'check {directory}')
            farsi_title = find_farsi_title(directory)
            print(farsi_title)
            if farsi_title is None:
                continue

            try:
                # symbol = models.Instrumentsel.objects.get(short_name__contains=directory)
                symbol = models.Instrumentsel.objects.get(short_name=farsi_title)
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
