from django.conf import settings


def findCsvFileUrl(candle_url, host):
    # find candle file url
    url = settings.MEDIA_ROOT.replace('\\', '/')
    parts = url.split('/')
    parts = parts[:-1]
    url = '/'.join(parts)
    url2 = url + candle_url
    print(url2)
    # url2 = 'http://127.0.0.1:8000' + candle.url
    if host != '127.0.0.1:8000':
        url2 = url2.replace('/media/media/', '/media/')
    return url2