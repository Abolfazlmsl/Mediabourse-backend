import os
from . import models
import pandas as pd
from django.db import IntegrityError


def feed_candle():
    directories = os.listdir('./helper/')
    for directory in directories:
        path = f'./helper/{directory}/'
        if os.path.isdir(path):
            symbol = models.Instrumentsel.objects.get(short_name__contains=directory)
            for file in os.listdir(path):
                df = pd.read_csv(path + file)
                df = df.drop(columns=['<TICKER>', '<PER>', '<OPENINT>'])
                last_date = df['<DTYYYYMMDD>'].iloc[-1]
                last_time = "{0:0=6d}".format(df[' <TIME>'].iloc[-1])
                date_time = str(last_date) + str(last_time)
                des_path = './uploads/file/chart/'
                time_frame = file.split('.')[0].split('-')[1]
                try:
                    models.Chart.objects.create(
                        last_candle_date=date_time,
                        company=symbol,
                        timeFrame=time_frame,
                        data=des_path + file
                    )
                except IntegrityError:
                    pass
