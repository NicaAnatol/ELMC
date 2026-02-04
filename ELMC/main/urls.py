from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.Intro, name='intro'),
    path('view-3d/<str:file_id>/', views.view_3d, name='view_3d'),
    path('home/', views.home, name='home'),
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/profile/', views.get_user_profile, name='profile'),
    path('api/data/<str:file_id>/', views.get_building_data, name='get_building_data'),
    path('api/save-data/', views.save_building_data, name='save_building_data'),
    path('api/download-data/<str:file_id>/', views.download_building_data, name='download_building_data'),
    path('api/export/<str:file_id>/', views.export_glb, name='export_glb'),
    path('api/download/<str:filename>/', views.download_file, name='download_file'),
    path('api/clear-data/', views.clear_building_data, name='clear_building_data'),
    path('api/session-info/', views.get_session_info, name='session_info'),
    path('health/', views.health_check, name='health_check'),
    path('api/docs/', views.api_docs, name='api_docs'),
    path('auth/', views.auth_page, name='auth_page'),
    path('api/element-texture/', views.element_texture, name='element_texture'),
    path('api/available-textures/', views.available_textures, name='available_textures'),
    path('account/', views.account_page, name='account_page'),
    path('api/account/profile/', views.update_profile, name='update_profile'),
    path('api/account/password/', views.change_password, name='change_password'),
    path('api/account/models/', views.get_user_models, name='get_user_models'),
    path('api/account/stats/', views.get_account_stats, name='get_account_stats'),
    path('api/account/models/detailed/', views.get_user_models_detailed, name='get_user_models_detailed'),
    path('api/save-export/', views.save_export, name='save_export'),
    path('api/download-export/<str:file_id>/', views.download_export, name='download_export'),
    path('api/glb-file/<str:file_id>/', views.get_glb_file, name='get_glb_file'),
    path('api/download-model-archive/<str:file_id>/', views.download_model_archive, name='download_model_archive'),
    path('api/project/<str:file_id>/thumbnail/', views.update_project_thumbnail, name='update_project_thumbnail'),
    path('api/project/<str:file_id>/thumbnail/image/', views.get_project_thumbnail, name='get_project_thumbnail'),
    path('api/project/<str:file_id>/camera-position/', views.get_project_camera_position, name='get_project_camera_position'),
    path('api/account/model/<str:file_id>/update/', views.update_model, name='update_model'),
    path('api/account/model/<str:file_id>/delete/', views.delete_model, name='delete_model'),
    path('api/account/model/<str:file_id>/stats/', views.get_model_stats, name='get_model_stats'),
    path('api/account/model/<str:file_id>/toggle-visibility/', views.toggle_model_visibility, name='toggle_model_visibility'),
    path('workshop/', views.workshop_page, name='workshop_page'),
    path('api/public-models/', views.get_public_models, name='get_public_models'),
    path('api/public-model/<str:file_id>/view/', views.increment_model_view, name='increment_model_view'),
    path('api/favorite/<str:file_id>/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('api/account/favorites/', views.get_user_favorites, name='get_user_favorites'),
    path('api/workshop-stats/', views.get_workshop_stats, name='workshop_stats'),
    path('api/featured-models/', views.get_featured_models, name='featured_models'),
    path('api/account/delete/', views.delete_account, name='delete_account'),
    path('sw.js', views.service_worker_root, name='service_worker_root'),
    path('manifest.json', views.manifest_json, name='manifest_json'),
    path('offline/', views.offline_view, name='offline'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)