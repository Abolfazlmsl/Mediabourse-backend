import os
from . import models
import pandas as pd
from django.db import IntegrityError
import jdatetime
from shutil import copy2


def feed_candle():
    directories = os.listdir('./helper/')
    for directory in directories:
        path = f'./helper/{directory}/'
        if os.path.isdir(path):
            symbol = models.Instrumentsel.objects.get(short_name__contains=directory)
            for file in os.listdir(path):
                df = pd.read_csv(path + file)
                df = df.drop(columns=['<TICKER>', '<PER>', '<OPENINT>'])
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

                # create directory for media
                try:
                    os.mkdir(f'./media/uploads/file/chart/{directory}')
                except FileExistsError:
                    pass

                # copy file to media
                copy2(path + file, f'./media/uploads/file/chart/{directory}/')

                # create an object
                try:
                    models.Chart.objects.create(
                        last_candle_date=date_time,
                        company=symbol,
                        timeFrame=time_frame,
                        data=f'./uploads/file/chart/{directory}/' + file
                    )
                except IntegrityError:
                    pass
