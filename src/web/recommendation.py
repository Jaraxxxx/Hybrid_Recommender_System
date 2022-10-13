import numpy as np 
import pandas as pd
from web.models import Myrating,Movie
import scipy.optimize 


def Myrecommend():
	ratings_df=pd.DataFrame(list(Myrating.objects.all().values()))
	movie_df=pd.DataFrame(list(Movie.objects.all().values()))
	user_movie_df = movie_df.merge(ratings_df, how="right", on="movie_id")
	user_movie_df = user_movie_df.pivot_table(index=["user_id"], columns=["title"], values="rating")
	return user_movie_df
	







