from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import secrets
import uuid
import os
from django.utils import timezone


def user_profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"profile_{instance.id}.{ext}"
    return os.path.join('users', str(instance.id), 'profile_pictures', filename)

def user_export_path(instance, filename):
    return os.path.join('exports', f'user_{instance.user.id}', filename)

def user_thumbnail_path(instance, filename):

    return os.path.join('users', str(instance.user.id), 'thumbnails', filename)

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    models_count = models.IntegerField(default=0)
    last_model_created = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        return timezone.now() < self.expires_at
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Token for {self.user.username}"

class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    file_id = models.CharField(max_length=100, unique=True)
    
    title = models.CharField(max_length=255, default="New Project")
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    
    thumbnail = models.ImageField(upload_to=user_thumbnail_path, null=True, blank=True)
    camera_position = models.JSONField(default=dict, blank=True, null=True)
    thumbnail_updated = models.DateTimeField(null=True, blank=True)
    
    glb_file = models.FileField(upload_to=user_export_path, null=True, blank=True)
    glb_file_name = models.CharField(max_length=255, null=True, blank=True)
    has_glb_export = models.BooleanField(default=False)
    glb_export_time = models.DateTimeField(null=True, blank=True)
    
    total_elements = models.IntegerField(default=0)
    file_size_mb = models.FloatField(default=0.0)
    favorites = models.ManyToManyField(User, related_name='favorite_models',  blank=True)
    building_count = models.IntegerField(default=0)
    highway_count = models.IntegerField(default=0)
    water_count = models.IntegerField(default=0)
    natural_count = models.IntegerField(default=0)
    landuse_count = models.IntegerField(default=0)
    other_count = models.IntegerField(default=0)
    area_km2 = models.FloatField(default=0.0)
    
    public_view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0) 
    user_data = models.JSONField(default=dict, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.file_id})"

    def delete(self, *args, **kwargs):
        if self.glb_file and os.path.isfile(self.glb_file.path):
            os.remove(self.glb_file.path)
        if self.thumbnail and os.path.isfile(self.thumbnail.path):
            os.remove(self.thumbnail.path)
        super().delete(*args, **kwargs)
        
    def is_favorited_by(self, user):
        return self.favorites.filter(id=user.id).exists()
    
    def get_favorites_count(self):
        return self.favorites.count()