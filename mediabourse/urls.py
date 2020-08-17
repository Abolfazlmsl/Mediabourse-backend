from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static

from mediabourse import settings

import private_storage.urls

schema_view = get_swagger_view(title='MediaBourse API')


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('user-panel/', include('user_panel.urls')),
    path('bourse/', include('bourse.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('', schema_view),

    path('private-media/', include(private_storage.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
