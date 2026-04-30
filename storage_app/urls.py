from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'files', views.FileViewSet, basename='file-api')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('file/<int:pk>/', views.file_detail, name='file_detail'),

    path('api/', include(router.urls)),
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/public/<str:token>/', views.PublicDownloadView.as_view(), name='public_api'),
    path('file/delete/<int:pk>/', views.delete_file, name='delete_file'),
    path("file/<int:file_id>/toggle/", views.toggle_public, name="toggle_public"),
    path('admin-dashboard/all-files/', views.admin_all_files, name='admin_files')
]