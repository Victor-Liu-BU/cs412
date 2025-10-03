# mini_insta/apps.py
# Ting Shing Liu, 9/26/25
# Making sure that the data gets registered to the database
from django.apps import AppConfig

#Register out mini_insta into the database with respective fields
class MiniInstaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_insta'
