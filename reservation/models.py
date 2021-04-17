from django.db import models


# Create your models here.


class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    projector_availability = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.capacity} {self.projector_availability}'

    def get_modify_url(self):
        return f'/modify_room/{self.id}/'

    def get_absolute_url(self):
        return f'/detail_room_view/{self.id}/'


class ReservationModel(models.Model):
    date = models.DateField()
    room = models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f'{self.date} {self.room} {self.comment}'

    class Meta:
        unique_together = ('date', 'room_id')