# from django.contrib.postgres.fields import ArrayField
# from django.db import models

# # Create your models here.

# class Song(models.Model):
#     song_id = models.CharField(max_length=255)
#     song_name = models.CharField(max_length=255)
#     duration = models.DurationField() #stores periods of time


# class Person(models.Model):
#     person_id = models.IntegerField()
#     username = models.CharField(max_length=255)
#     spotify_username = models.CharField(max_length=255)
#     current_room = models.OneToOneField('Room', on_delete=models.CASCADE)

# class Room(models.Model):
#     room_name = models.CharField(max_length=255)
#     host = models.ForeignKey(Person, on_delete=models.CASCADE)
#     guests = models.ArrayField(
#                     models.OneToOneField(Person, on_delete=models.CASCADE)
#                     )

#     songs_in_queue = models.ArrayField(
#                     models.OneToOneField(Songs, on_delete=models.CASCADE)
#                     )
