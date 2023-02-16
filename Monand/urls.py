from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from .api import router
from customer import ulr
from pyclick import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include(ulr)),
    path('click/', include(urls))
]

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

