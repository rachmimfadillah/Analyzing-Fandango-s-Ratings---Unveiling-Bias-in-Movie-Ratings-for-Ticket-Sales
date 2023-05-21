#!/usr/bin/env python
# coding: utf-8

# 
# <center><em>Copyright by Pierian Data Inc.</em></center>
# <center><em>For more information, visit us at <a href='http://www.pieriandata.com'>www.pieriandata.com</a></em></center>

# # Capstone Project
# ## Overview
# 
# If you are planning on going out to see a movie, how well can you trust online reviews and ratings? *Especially* if the same company showing the rating *also* makes money by selling movie tickets. Do they have a bias towards rating movies higher than they should be rated?
# 
# ### Goal:
# 
# **Your goal is to complete the tasks below based off the 538 article and see if you reach a similar conclusion. You will need to use your pandas and visualization skills to determine if Fandango's ratings in 2015 had a bias towards rating movies better to sell more tickets.**
# 
# ---
# ---
# 
# **Complete the tasks written in bold.**
# 
# ---
# ----
# 
# ## Part One: Understanding the Background and Data
# 
# 
# **TASK: Read this article: [Be Suspicious Of Online Movie Ratings, Especially Fandango’s](http://fivethirtyeight.com/features/fandango-movies-ratings/)**

# ----
# 
# **TASK: After reading the article, read these two tables giving an overview of the two .csv files we will be working with:**
# 
# ### The Data
# 
# This is the data behind the story [Be Suspicious Of Online Movie Ratings, Especially Fandango’s](http://fivethirtyeight.com/features/fandango-movies-ratings/) openly available on 538's github: https://github.com/fivethirtyeight/data. There are two csv files, one with Fandango Stars and Displayed Ratings, and the other with aggregate data for movie ratings from other sites, like Metacritic,IMDB, and Rotten Tomatoes.
# 
# #### all_sites_scores.csv

# -----
# 
# `all_sites_scores.csv` contains every film that has a Rotten Tomatoes rating, a RT User rating, a Metacritic score, a Metacritic User score, and IMDb score, and at least 30 fan reviews on Fandango. The data from Fandango was pulled on Aug. 24, 2015.

# Column | Definition
# --- | -----------
# FILM | The film in question
# RottenTomatoes | The Rotten Tomatoes Tomatometer score  for the film
# RottenTomatoes_User | The Rotten Tomatoes user score for the film
# Metacritic | The Metacritic critic score for the film
# Metacritic_User | The Metacritic user score for the film
# IMDB | The IMDb user score for the film
# Metacritic_user_vote_count | The number of user votes the film had on Metacritic
# IMDB_user_vote_count | The number of user votes the film had on IMDb

# ----
# ----
# 
# #### fandango_scape.csv

# `fandango_scrape.csv` contains every film 538 pulled from Fandango.
# 
# Column | Definiton
# --- | ---------
# FILM | The movie
# STARS | Number of stars presented on Fandango.com
# RATING |  The Fandango ratingValue for the film, as pulled from the HTML of each page. This is the actual average score the movie obtained.
# VOTES | number of people who had reviewed the film at the time we pulled it.

# ----
# 
# **TASK: Import any libraries you think you will use:**

# In[1]:


# IMPORT HERE!
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[174]:





# ## Part Two: Exploring Fandango Displayed Scores versus True User Ratings
# 
# Let's first explore the Fandango ratings to see if our analysis agrees with the article's conclusion.
# 
# **TASK: Run the cell below to read in the fandango_scrape.csv file**

# In[2]:


fandango = pd.read_csv("fandango_scrape.csv")


# **TASK: Explore the DataFrame Properties and Head.**

# In[3]:


fandango.head()


# In[4]:


fandango.info()


# In[5]:


fandango.describe()


# **TASK: Let's explore the relationship between popularity of a film and its rating. Create a scatterplot showing the relationship between rating and votes. Feel free to edit visual styling to your preference.**

# In[7]:


# CODE HERE
plt.figure(figsize=(10,5), dpi=200)
sns.scatterplot(x = 'RATING', y = 'VOTES', data = fandango)


# **TASK: Calculate the correlation between the columns:**

# In[8]:


# CODE HERE
fandango.corr()


# **TASK: Assuming that every row in the FILM title column has the same format:**
# 
#     Film Title Name (Year)
#     
# **Create a new column that is able to strip the year from the title strings and set this new column as YEAR**

# In[14]:


# CODE HERE
fandango['YEAR'] = fandango['FILM'].str.strip(')').str.split('(').str[-1]
fandango.head()


# **TASK: How many movies are in the Fandango DataFrame per year?**

# In[15]:


#CODE HERE
movie_counts = fandango.groupby(['YEAR']).size().sort_values(ascending=False)
movie_counts


# **TASK: Visualize the count of movies per year with a plot:**

# In[16]:


#CODE HERE
plt.figure(figsize=(10,5), dpi=200)
plt.bar(movie_counts.index, movie_counts.values)
plt.xlabel('YEAR')
plt.ylabel('count')
plt.title('Total Movies per Year')


# **TASK: What are the 10 movies with the highest number of votes?**

# In[17]:


#CODE HERE
fandango.nlargest(10, 'VOTES')


# **TASK: How many movies have zero votes?**

# In[18]:


len(fandango[fandango['VOTES'] == 0])


# **TASK: Create DataFrame of only reviewed films by removing any films that have zero votes.**

# In[19]:


#CODE HERE
df = fandango[fandango['VOTES'] > 0]
df.info()


# ----
# 
# **As noted in the article, due to HTML and star rating displays, the true user rating may be slightly different than the rating shown to a user. Let's visualize this difference in distributions.**
# 
# **TASK: Create a KDE plot (or multiple kdeplots) that displays the distribution of ratings that are displayed (STARS) versus what the true rating was from votes (RATING). Clip the KDEs to 0-5.**

# In[126]:


#CODE HERE
plt.figure(figsize=(10,5), dpi=200)
sns.kdeplot(data = df, x = 'RATING', fill=True, label = 'True Rating', clip = (0,5))
sns.kdeplot(data = df, x = 'STARS', fill=True, label = 'Star Displayed', clip = (0,5))
plt.legend(bbox_to_anchor=(1.25, 1))


# **TASK: Let's now actually quantify this discrepancy. Create a new column of the different between STARS displayed versus true RATING. Calculate this difference with STARS-RATING and round these differences to the nearest decimal point.**

# In[21]:


#CODE HERE
df['STARS_DIFF'] = df['STARS'].astype(float) - df['RATING'].astype(float)
df['STARS_DIFF'] = df['STARS_DIFF'].round(1)
df


# **TASK: Create a count plot to display the number of times a certain difference occurs:**

# In[22]:


#CODE HERE
plt.figure(figsize=(10,5), dpi = 200)
sns.countplot(data = df, x = 'STARS_DIFF')


# **TASK: We can see from the plot that one movie was displaying over a 1 star difference than its true rating! What movie had this close to 1 star differential?**

# In[23]:


#CODE HERE
df[df['STARS_DIFF'] == 1.0]


# ## Part Three: Comparison of Fandango Ratings to Other Sites
# 
# Let's now compare the scores from Fandango to other movies sites and see how they compare.
# 
# **TASK: Read in the "all_sites_scores.csv" file by running the cell below**

# In[25]:


all_sites = pd.read_csv("all_sites_scores.csv")


# **TASK: Explore the DataFrame columns, info, description.**

# In[26]:


all_sites.head()


# In[27]:


all_sites.info()


# In[28]:


all_sites.describe()


# ### Rotten Tomatoes
# 
# Let's first take a look at Rotten Tomatoes. RT has two sets of reviews, their critics reviews (ratings published by official critics) and user reviews. 
# 
# **TASK: Create a scatterplot exploring the relationship between RT Critic reviews and RT User reviews.**

# In[127]:


# CODE HERE
plt.figure(figsize=(10,5), dpi=200)
sns.scatterplot(x = 'RottenTomatoes', y = 'RottenTomatoes_User', data = all_sites)
plt.xlim(0,100)
plt.ylim(0,100)


# Let's quantify this difference by comparing the critics ratings and the RT User ratings. We will calculate this with RottenTomatoes-RottenTomatoes_User. Note: Rotten_Diff here is Critics - User Score. So values closer to 0 means aggrement between Critics and Users. Larger positive values means critics rated much higher than users. Larger negative values means users rated much higher than critics.
# 
# **TASK: Create a new column based off the difference between critics ratings and users ratings for Rotten Tomatoes. Calculate this with RottenTomatoes-RottenTomatoes_User**

# In[33]:


#CODE HERE
all_sites['Rotten_Diff'] = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']


# In[34]:


all_sites.head()


# Let's now compare the overall mean difference. Since we're dealing with differences that could be negative or positive, first take the absolute value of all the differences, then take the mean. This would report back on average to absolute difference between the critics rating versus the user rating.

# **TASK: Calculate the Mean Absolute Difference between RT scores and RT User scores as described above.**

# In[37]:


# CODE HERE
all_sites['Rotten_Diff'].abs().mean()


# **TASK: Plot the distribution of the differences between RT Critics Score and RT User Score. There should be negative values in this distribution plot. Feel free to use KDE or Histograms to display this distribution.**

# In[128]:


#CODE HERE
plt.figure(figsize=(10, 5), dpi=200)
sns.displot(data = all_sites, x = 'Rotten_Diff', bins = 25, color = 'maroon',
            edgecolor = 'black', kde = True)
plt.title('RT Critics Score Minus RT Users Score')


# **TASK: Now create a distribution showing the *absolute value* difference between Critics and Users on Rotten Tomatoes.**

# In[129]:


#CODE HERE
plt.figure(figsize=(10, 5), dpi=200)
sns.displot(data = all_sites, x = all_sites['Rotten_Diff'].abs(), bins = 25, color = 'maroon',
            edgecolor = 'black', kde = True)
plt.title('Abs Difference between RT Critics Score and RT Users Score')


# **Let's find out which movies are causing the largest differences. First, show the top 5 movies with the largest *negative* difference between Users and RT critics. Since we calculated the difference as Critics Rating - Users Rating, then large negative values imply the users rated the movie much higher on average than the critics did.**

# **TASK: What are the top 5 movies users rated higher than critics on average:**

# In[130]:


# CODE HERE
print('Users Love, Critics Hate')
all_sites.nsmallest(5, 'Rotten_Diff')[['FILM', 'Rotten_Diff']]


# **TASK: Now show the top 5 movies critics scores higher than users on average.**

# In[131]:


# CODE HERE
print('Critics Love, Users Hate')
all_sites.nlargest(5, 'Rotten_Diff')[['FILM', 'Rotten_Diff']]


# ## MetaCritic
# 
# Now let's take a quick look at the ratings from MetaCritic. Metacritic also shows an average user rating versus their official displayed rating.

# **TASK: Display a scatterplot of the Metacritic Rating versus the Metacritic User rating.**

# In[134]:


# CODE HERE
plt.figure(figsize=(10,5), dpi=200)
sns.scatterplot(x = 'Metacritic', y = 'Metacritic_User', data = all_sites)
plt.xlim(0,100)
plt.ylim(0,10)


# ## IMDB
# 
# Finally let's explore IMDB. Notice that both Metacritic and IMDB report back vote counts. Let's analyze the most popular movies.
# 
# **TASK: Create a scatterplot for the relationship between vote counts on MetaCritic versus vote counts on IMDB.**

# In[54]:


#CODE HERE
plt.figure(figsize=(10,5), dpi=200)
sns.scatterplot(x = 'Metacritic_user_vote_count', y = 'IMDB_user_vote_count', data = all_sites)


# **Notice there are two outliers here. The movie with the highest vote count on IMDB only has about 500 Metacritic ratings. What is this movie?**
# 
# **TASK: What movie has the highest IMDB user vote count?**

# In[55]:


#CODE HERE
all_sites.nlargest(1, 'IMDB_user_vote_count')


# **TASK: What movie has the highest Metacritic User Vote count?**

# In[56]:


#CODE HERE
all_sites.nlargest(1, 'Metacritic_user_vote_count')


# ## Fandago Scores vs. All Sites
# 
# Finally let's begin to explore whether or not Fandango artificially displays higher ratings than warranted to boost ticket sales.

# **TASK: Combine the Fandango Table with the All Sites table. Not every movie in the Fandango table is in the All Sites table, since some Fandango movies have very little or no reviews. We only want to compare movies that are in both DataFrames, so do an *inner* merge to merge together both DataFrames based on the FILM columns.**

# In[73]:


#CODE HERE
fandango_vs_all = pd.merge(fandango, all_sites, on='FILM', how='inner')
fandango_vs_all.head()


# In[74]:


fandango_vs_all.info()


# ### Normalize columns to Fandango STARS and RATINGS 0-5 
# 
# Notice that RT,Metacritic, and IMDB don't use a score between 0-5 stars like Fandango does. In order to do a fair comparison, we need to *normalize* these values so they all fall between 0-5 stars and the relationship between reviews stays the same.
# 
# **TASK: Create new normalized columns for all ratings so they match up within the 0-5 star range shown on Fandango. There are many ways to do this.**
# 
# Hint link: https://stackoverflow.com/questions/26414913/normalize-columns-of-pandas-data-frame
# 
# 
# Easier Hint:
# 
# Keep in mind, a simple way to convert ratings:
# * 100/20 = 5 
# * 10/2 = 5

# In[84]:


# CODE HERE
# RottenTomatoes = 100/20
# Metacritic = 100/20
# IMDB = 10/2
fandango_vs_all['RottenTomatoes_normalized'] = fandango_vs_all['RottenTomatoes'] * 5 / 100
fandango_vs_all['RT_U_normalized'] = fandango_vs_all['RottenTomatoes_User'] * 5 / 100
fandango_vs_all['Metacritic_normalized'] = fandango_vs_all['Metacritic'] * 5 / 100
fandango_vs_all['Meta_U_normalized'] = fandango_vs_all['Metacritic_User'] * 5 / 10
fandango_vs_all['IMDB_normalized'] = fandango_vs_all['IMDB'] * 5 / 10
fandango_vs_all.head()


# **TASK: Now create a norm_scores DataFrame that only contains the normalizes ratings. Include both STARS and RATING from the original Fandango table.**

# In[85]:


#CODE HERE
norm_scores = fandango_vs_all[['STARS', 'RATING', 'RottenTomatoes_normalized', 'RT_U_normalized',
                               'Metacritic_normalized', 'Meta_U_normalized', 'IMDB_normalized']]


# In[86]:


norm_scores.head()


# ### Comparing Distribution of Scores Across Sites
# 
# 
# Now the moment of truth! Does Fandango display abnormally high ratings? We already know it pushs displayed RATING higher than STARS, but are the ratings themselves higher than average?
# 
# 
# **TASK: Create a plot comparing the distributions of normalized ratings across all sites. There are many ways to do this, but explore the Seaborn KDEplot docs for some simple ways to quickly show this. Don't worry if your plot format does not look exactly the same as ours, as long as the differences in distribution are clear.**
# 
# Quick Note if you have issues moving the legend for a seaborn kdeplot: https://github.com/mwaskom/seaborn/issues/2280

# In[88]:


#CODE HERE
plt.figure(figsize=(10,5), dpi=200)
sns.kdeplot(data = norm_scores, x = 'STARS', fill=True, label = 'STARS', clip = (0,5))
sns.kdeplot(data = norm_scores, x = 'RATING', fill=True, label = 'RATING', clip = (0,5))
sns.kdeplot(data = norm_scores, x = 'RottenTomatoes_normalized', fill=True, label = 'RT_Norm', clip = (0,5))
sns.kdeplot(data = norm_scores, x = 'RT_U_normalized', fill=True, label = 'RTU_Norm', clip = (0,5))
sns.kdeplot(data = norm_scores, x = 'Metacritic_normalized', fill=True, label = 'Meta_Norm', clip = (0,5))
sns.kdeplot(data = norm_scores, x = 'Meta_U_normalized', fill=True, label = 'Meta_U_Norm', clip = (0,5))
sns.kdeplot(data = norm_scores, x = 'IMDB_normalized', fill=True, label = 'IMDB_Norm', clip = (0,5))
plt.legend(bbox_to_anchor=(1.5, 1))


# **Clearly Fandango has an uneven distribution. We can also see that RT critics have the most uniform distribution. Let's directly compare these two.** 
# 
# **TASK: Create a KDE plot that compare the distribution of RT critic ratings against the STARS displayed by Fandango.**

# In[89]:


#CODE HERE
plt.figure(figsize=(10,5), dpi=200)
sns.kdeplot(data = norm_scores, x = 'RottenTomatoes_normalized', fill=True, label = 'RT_Norm', clip = (0,5))
sns.kdeplot(data = norm_scores, x = 'STARS', fill=True, label = 'STARS', clip = (0,5))
plt.legend(bbox_to_anchor=(1.5, 1))


# **OPTIONAL TASK: Create a histplot comparing all normalized scores.**

# In[135]:


plt.figure(figsize=(10, 5), dpi=200)
sns.histplot(norm_scores, bins = 50)

# Add labels and title
plt.xlabel('Normalized Ratings')
plt.ylabel('Count')
plt.title('Distribution of Normalized Ratings')

# Show the plot
plt.show()


# 
# ### How are the worst movies rated across all platforms?
# 
# **TASK: Create a clustermap visualization of all normalized scores. Note the differences in ratings, highly rated movies should be clustered together versus poorly rated movies. Note: This clustermap does not need to have the FILM titles as the index, feel free to drop it for the clustermap.**

# In[101]:


# CODE HERE
plt.figure(figsize = (10, 5), dpi = 200)
sns.clustermap(norm_scores, col_cluster = False)


# **TASK: Clearly Fandango is rating movies much higher than other sites, especially considering that it is then displaying a rounded up version of the rating. Let's examine the top 10 worst movies. Based off the Rotten Tomatoes Critic Ratings, what are the top 10 lowest rated movies? What are the normalized scores across all platforms for these movies? You may need to add the FILM column back in to your DataFrame of normalized scores to see the results.**

# In[103]:


# CODE HERE
norm_scores = fandango_vs_all[['STARS', 'RATING', 'RottenTomatoes_normalized', 'RT_U_normalized',
                               'Metacritic_normalized', 'Meta_U_normalized', 'IMDB_normalized', 'FILM']]


# In[106]:


top_10_RT_worst = norm_scores.nsmallest(10, 'RottenTomatoes_normalized')
top_10_RT_worst


# **FINAL TASK: Visualize the distribution of ratings across all sites for the top 10 worst movies.**

# In[107]:


# CODE HERE
plt.figure(figsize=(10, 5), dpi=200)
sns.kdeplot(data=top_10_RT_worst, x='STARS', fill=True, label='STARS', clip=(0, 5))
sns.kdeplot(data=top_10_RT_worst, x='RATING', fill=True, label='RATING', clip=(0, 5))
sns.kdeplot(data=top_10_RT_worst, x='RottenTomatoes_normalized', fill=True, label='RT_Norm', clip=(0, 5))
sns.kdeplot(data=top_10_RT_worst, x='RT_U_normalized', fill=True, label='RTU_Norm', clip=(0, 5))
sns.kdeplot(data=top_10_RT_worst, x='Metacritic_normalized', fill=True, label='Meta_Norm', clip=(0, 5))
sns.kdeplot(data=top_10_RT_worst, x='Meta_U_normalized', fill=True, label='Meta_U_Norm', clip=(0, 5))
sns.kdeplot(data=top_10_RT_worst, x='IMDB_normalized', fill=True, label='IMDB_Norm', clip=(0, 5))
plt.legend(bbox_to_anchor=(1.5, 1))


# ---
# ----
# 
# <img src="https://upload.wikimedia.org/wikipedia/en/6/6f/Taken_3_poster.jpg">
# 
# **Final thoughts: Wow! Fandango is showing around 3-4 star ratings for films that are clearly bad! Notice the biggest offender, [Taken 3!](https://www.youtube.com/watch?v=tJrfImRCHJ0). Fandango is displaying 4.5 stars on their site for a film with an [average rating of 1.86](https://en.wikipedia.org/wiki/Taken_3#Critical_response) across the other platforms!**

# In[114]:


norm_scores[norm_scores['FILM'] == 'Taken 3 (2015)']


# In[115]:


0.4+2.3+1.3+2.3+3


# In[116]:


9.3/5


# ----
