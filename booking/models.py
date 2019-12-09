from django.db import models

# Create your models here.
from django.forms import ModelForm


class Movie(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    name = models.CharField(max_length=100,verbose_name='Movie Name',null=False,blank=False)
    tot_tickets = models.PositiveSmallIntegerField(default=50,verbose_name='Total Number of tickets')

    def __str__(self):
        return self.name


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields=['name','tot_tickets']


TICKET_STATUS_CHOICES =(
    (1,'AVAILABLE'),
    (2,'BOOKED'),
)

class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    ticket_num = models.PositiveSmallIntegerField(null=False,blank=False)
    movie = models.ForeignKey(Movie,null=False,on_delete=models.CASCADE)
    status= models.IntegerField(choices=TICKET_STATUS_CHOICES,default=2)

    class Meta:
        unique_together =('movie','ticket_num')

