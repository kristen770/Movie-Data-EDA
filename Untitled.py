#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Install Libraries 
import pandas as pd 
import numpy as np   


# In[ ]:


#Read in IMDB Name Basics 
imdb_title = pd.read_csv('imdb.name.basics.csv.gz', compression='gzip', header=0, sep=',', quotechar='"') 

imdb_title 


# In[ ]:


#Read in IMDB title akas 
imdb_akas = pd.read_csv('imdb.title.akas.csv.gz', compression='gzip', header=0, sep=',', quotechar='"') 

imdb_akas 


# In[ ]:


#Read in IMDB title basics 
imdb_basics = pd.read_csv('imdb.title.basics.csv.gz', compression='gzip', header=0, sep=',', quotechar='"') 

imdb_basics 


# In[ ]:


#Read in IMDB title crew
imdb_crew = pd.read_csv('imdb.title.crew.csv.gz', compression='gzip', header=0, sep=',', quotechar='"') 

imdb_crew 


# In[ ]:


#Read in IMDB title principals 
imdb_principals = pd.read_csv('imdb.title.principals.csv.gz', compression='gzip', header=0, sep=',', quotechar='"') 

imdb_principals


# In[ ]:


#Read in IMDB title ratings 
imdb_ratings = pd.read_csv('imdb.title.ratings.csv.gz', compression='gzip', header=0, sep=',', quotechar='"') 

imdb_ratings 


# In[ ]:


#Merging the dataframes 
imdb_rating_principal = pd.merge(imdb_principals, imdb_ratings, on='tconst', how='outer') 
imdb_rating_principal_crew = pd.merge(imdb_rating_principal, imdb_crew, on='tconst', how='outer') 
imdb_rating_principal_crew_basics = pd.merge(imdb_rating_principal_crew, imdb_basics, on='tconst', how='outer') 
imdb_rating_principal_crew_basics_akas = pd.merge(imdb_rating_principal_crew_basics, imdb_akas,
                                                  left_on="tconst", right_on="title_id", how='outer')
imdb_rating_principal_crew_basics_akas_title = pd.merge(imdb_rating_principal_crew_basics_akas, imdb_title, 
                                                       on="nconst", how='outer')
imdb_rating_principal_crew_basics_akas_title


# In[70]:


#Resetting the DF name for brevity and to preserve orignial df 
df = imdb_rating_principal_crew_basics_akas_title


# In[ ]:


df.head()


# In[72]:


#DF shape view 
df.shape


# In[73]:


#Viewing NaN values
df.isna().sum()


# In[74]:


#Dropping columns with high NaN values 

#langauge- over 87% of the column is Nan   
#attributes - over 95% of the column is Nan  
#death_year - over 98% of the column is Nan 
#birth_year - over 61% of the column is Nan 
#The job - over 74% of the column is Nan  
#characters - over 61% of the column is Nan
df.drop(["language", "attributes", "death_year","birth_year", "job", "characters"], axis =1, inplace=True) 

#directors and writers columns - they are a repeat of the nconstant 
#title_id - a repeat of the tconstant 
df.drop(["title_id", "directors", "writers"], axis =1, inplace=True)


# # Question 1: What is the correlation between runtime & genre?

# In[75]:


#Creating a new df to isolate the genre/ runtime data 
runtime_genres =  df.drop(["nconst", "tconst", "ordering_x", "category", "averagerating", "numvotes", "primary_title", 
        "original_title", "start_year", "ordering_y", "title", "region", "types",
       "is_original_title", "primary_name", "primary_profession", "known_for_titles"], axis =1) 


# In[76]:


runtime_genres.shape


# In[83]:


runtime_genres.isna().sum()


# In[78]:


#Drop the genre rows that have nan values - with more time you could look at the occurance of each genre and then replace
#it with a random genre
runtime_genres.dropna(subset= ['genres'], inplace= True)


# In[80]:


#Calculating Runtime Mean
runtime_genres['runtime_minutes'].mean() 
#97.96914147492264


# In[81]:


#Calculating Runtime Median 
runtime_genres['runtime_minutes'].median()  
#95.0


# In[ ]:


#Replacing NaN values with Runtime Mean based on calculations ^  
median=95
runtime_genres.fillna(median, inplace=True)


# In[ ]:


#Calculation Correlation 
runtime_genres.apply(lambda x: x.factorize()[0]).corr()


# In[ ]:


#Visualizing the correlation
fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
fig.show()

