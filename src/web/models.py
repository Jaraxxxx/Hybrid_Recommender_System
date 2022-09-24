from time import timezone
from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.validators import RegexValidator

class Movie(models.Model):
	id = models.CharField(primary_key=True,max_length=4, validators=[RegexValidator(r'^\d{1,10}$')],default="0.0")
	movie_logo  = models.FileField(max_length=500,default="NA") 
	title   	= models.CharField(max_length=200,default="NA")
	released_year = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$')],default="NA")
	certificate = models.CharField(max_length=10,default="NA")
	runtime = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$')],default="0")
	genre = models.CharField(max_length=100,default="NA")
	imdb_ratings = models.FloatField(max_length=3,default="0.0")
	overview = models.CharField(max_length=5000,default="NA")
	score = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$')],default="0.0")
	director = models.CharField(max_length=100,default="NA")
	stars = models.CharField(max_length=400,default="NA")
	no_of_votes  = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{1,10}$')],default="0")

	def __str__(self):
		return self.title

class Myrating(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE) 
	movie 	= models.ForeignKey(Movie,on_delete=models.CASCADE)
	rating 	= models.IntegerField(default=0,validators=[MaxValueValidator(5),MinValueValidator(0)])
		