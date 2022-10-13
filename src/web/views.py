from math import radians
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.http import Http404
from .models import Movie,Myrating
from django.contrib import messages
from .forms import UserForm
from django.db.models import Case, When
from .recommendation import Myrecommend
import numpy as np 
import pandas as pd
import random


# for recommendation version3
def recommend(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    ratings_df=pd.DataFrame(list(Myrating.objects.all().values()))
    movie_df=pd.DataFrame(list(Movie.objects.all().values()))
    nu=ratings_df.user_id.unique().shape[0]
    print(nu)
    current_user_id= request.user.id
    # if new user not rated any movie
    if current_user_id>nu:
        movie=Movie.objects.get(movie_id=random.randint(0,999))
        q=Myrating(user=request.user,movie=movie,rating=0)
        q.save()
    print("Current user id: ",current_user_id)
    user_movie_df = Myrecommend
    movie_df.certificate.fillna('',inplace = True)
    movie_df.score.fillna(0,inplace = True)
    # First let's make a copy of the movies_df.
    movies_with_genres = movie_df.copy(deep=True)
    movies_with_genres = movies_with_genres.drop(['movie_logo','released_year','certificate','runtime','imdb_ratings','overview','score','director','stars','no_of_votes'],1)
    movies_with_genres_list = movies_with_genres.genre.str.get_dummies(sep = ", ")
    movies_with_genres_list = movies_with_genres_list.multiply(1.0)
    movies_with_genres = pd.concat([movies_with_genres,movies_with_genres_list],axis=1)
    random_user_df = ratings_df[ratings_df['user_id'] == current_user_id]
    random_user_movie_df = random_user_df.merge(movie_df,how="left",on="movie_id")
    random_user_movie_df_ratings = random_user_movie_df.drop(['id','user_id','genre','imdb_ratings','score','director','stars','no_of_votes','movie_logo','released_year','certificate','runtime','overview'],1)
    # random_user_movie_df_genres = movies_with_genres[movies_with_genres.movie_id.isin(random_user_movie_df_ratings.movie_id.unique())]
    random_user_movie_df_genres = movies_with_genres.merge(random_user_movie_df_ratings,how='inner',on=['movie_id','title'])
    random_user_movie_df_genres.reset_index(drop = True,inplace = True)
    random_user_movie_df_genres.drop(['movie_id','title','genre','rating'],axis = 1,inplace = True)
    random_user_profile = random_user_movie_df_genres.T.dot(random_user_movie_df_ratings.rating)
    movies_with_genres = movies_with_genres.set_index(movies_with_genres.movie_id)
    movies_with_genres.drop(['movie_id','title','genre'], axis=1, inplace=True)
    random_user_recommendation_table = (movies_with_genres.dot(random_user_profile))/random_user_profile.sum() 
    random_user_recommendation_table.sort_values(ascending = False,inplace = True)
    top_12_index = random_user_recommendation_table.index[:12].tolist()
    print(top_12_index)
    recommended_movies = movie_df.loc[top_12_index, : ]
    print(recommended_movies[['movie_id','title','genre']])
    recommended_movies = list(Movie.objects.filter(movie_id__in = (recommended_movies['movie_id']-1)))
    return render(request,'web/recommend.html',{'movie_list':recommended_movies})


# # for recommendation
# def recommend(request):
# 	if not request.user.is_authenticated:
# 		return redirect("login")
# 	if not request.user.is_active:
# 		raise Http404
# 	df=pd.DataFrame(list(Myrating.objects.all().values()))
# 	nu=df.user_id.unique().shape[0]
# 	print(nu)
# 	current_user_id= request.user.id
# 	# if new user not rated any movie
# 	if current_user_id>nu:
# 		movie=Movie.objects.get(id=20)
# 		q=Myrating(user=request.user,movie=movie,rating=0)
# 		q.save()

# 	print("Current user id: ",current_user_id)
# 	prediction_matrix,Ymean = Myrecommend()
# 	my_predictions = prediction_matrix[:,current_user_id-1]+Ymean.flatten()
# 	pred_idxs_sorted = np.argsort(my_predictions)
# 	pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
# 	pred_idxs_sorted=pred_idxs_sorted+1
# 	# print(pred_idxs_sorted)
# 	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
# 	movie_list=list(Movie.objects.filter(id__in = pred_idxs_sorted,).order_by(preserved)[:10])
# 	return render(request,'web/recommend.html',{'movie_list':movie_list})


# List view
def index(request):
	movies = Movie.objects.all()
	query  = request.GET.get('q')
	if query:
		movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
		return render(request,'web/list.html',{'movies':movies})
	return render(request,'web/list.html',{'movies':movies})


# detail view
def detail(request,movie_id):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404
	movies = get_object_or_404(Movie,movie_id=movie_id)
	#for rating
	if request.method == "POST":
		rate = request.POST['rating']
		ratingObject = Myrating()
		ratingObject.user   = request.user
		ratingObject.movie  = movies
		ratingObject.rating = rate
		ratingObject.save()
		messages.success(request,"Your Rating is submited ")
		return redirect("index")
	return render(request,'web/detail.html',{'movies':movies})


# Register user
def signUp(request):
	form =UserForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		username  =	form.cleaned_data['username']
		password  = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("index")
	context ={
		'form':form
	}
	return render(request,'web/signUp.html',context)				


# Login User
def Login(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("index")
			else:
				return render(request,'web/login.html',{'error_message':'Your account disable'})
		else:
			return render(request,'web/login.html',{'error_message': 'Invalid Login'})
	return render(request,'web/login.html')

#Logout user
def Logout(request):
	logout(request)
	return redirect("login")




