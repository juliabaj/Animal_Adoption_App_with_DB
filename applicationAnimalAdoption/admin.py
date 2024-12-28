from django.contrib import admin
from .models import Animals, Owners

@admin.register(Animals)
class AnimalsAdmin(admin.ModelAdmin):
    list_display = ('animal_name', 'species', 'birth_date', 'adoption_status', 'owner')
    search_fields = ('animal_name', 'species', 'adoption_status')

@admin.register(Owners)
class OwnersAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'user', 'is_verified')
    list_filter = ('is_verified',)  # Add a filter for status
    search_fields = ('owner_name', 'email', 'user_username', 'is_verified')  # Enable searching by name and email