from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils import timezone
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import File, SharedLink
from .serializers import FileSerializer, User, RegisterSerializer
from .permission import IsOwnerOrAdmin

# ________________________ API VIEWS ________________________

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return File.objects.none()
        if user.role == 'admin':
            return File.objects.all()
        return File.objects.filter(owner=user)

    def perform_create(self, serializer):
        file_handle = self.request.FILES.get('file')
        size_kb = file_handle.size / 1024
        serializer.save(owner=self.request.user, size=size_kb)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        file_obj = self.get_object()
        token = uuid.uuid4().hex[:20]
        shared_link, created = SharedLink.objects.update_or_create(
            file=file_obj,
            defaults={
                'token': token,
                'is_active': True,
                'created_at': timezone.now()
            }
        )
        full_link = request.build_absolute_uri(f"/api/public/{token}/")
        return Response({
            'share_url': full_link,
            'token': token,
            'message': "Havola muvaffaqiyatli yaratildi!"
        })

class PublicDownloadView(APIView):
    permission_classes = []

    def get(self, request, token):
        link = get_object_or_404(SharedLink, token=token, is_active=True)
        if link.expire_date and link.expire_date < timezone.now():
            link.is_active = False
            link.save()
            return Response({"error": "Havola muddati tugagan!"}, status=status.HTTP_403_FORBIDDEN)

        file_obj = link.file
        file_obj.views += 1
        file_obj.save()

        return Response({
            "title": file_obj.title,
            "owner": file_obj.owner.username,
            "size": f"{file_obj.size:.2f} KB",
            "download_url": request.build_absolute_uri(file_obj.file.url),
            "uploaded_at": file_obj.created_at,
            "total_views": file_obj.views
        })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer




@login_required
def dashboard(request):
    if request.user.role == 'admin':
        files = File.objects.all()
    else:
        files = File.objects.filter(owner=request.user)
    return render(request, 'storage_app/dashboard.html', {'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        uploaded_file = request.FILES.get('file')
        is_public = request.POST.get('is_public') == 'on'

        if uploaded_file:
            File.objects.create(
                title=title,
                file=uploaded_file,
                owner=request.user,
                size=uploaded_file.size / 1024,
                is_public=is_public
            )
            return redirect('dashboard')

    return render(request, 'storage_app/upload.html')

def file_detail(request, pk):
    file_obj = get_object_or_404(File, pk=pk)
    if not file_obj.is_public and file_obj.owner != request.user and request.user.role != 'admin':
        return render(request, '403.html', status=403)

    return render(request, 'storage_app/detail.html', {'file': file_obj})


def delete_file(request, pk):
    file_obj = get_object_or_404(File, pk=pk)

    if file_obj.owner == request.user or request.user.role == 'admin':
        file_obj.file.delete()
        file_obj.delete()
    return redirect('dashboard')


def toggle_public(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    file.is_public = not file.is_public
    file.save()
    return redirect("file_detail", id=file_id)



def admin_all_files(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    files = File.objects.all()
    return render(request,"storage_app/dashboard.html", {'files': files})