# Analyzing-Fandango-s-Ratings---Unveiling-Bias-in-Movie-Ratings-for-Ticket-Sales
This data analysis project examines the trustworthiness of online movie ratings, particularly focusing on Fandango. The goal is to investigate whether Fandango's ratings in 2015 were influenced by a bias towards higher ratings, potentially driven by their ticket sales interests. Using pandas and visualization techniques, this project aims to uncover any patterns suggesting a bias and determine if Fandango's ratings were inflated to boost ticket sales.

# Data Source
This is the data behind the story Be Suspicious Of Online Movie Ratings, Especially Fandango’s openly available on 538's github: https://github.com/fivethirtyeight/data. There are two csv files, one with Fandango Stars and Displayed Ratings, and the other with aggregate data for movie ratings from other sites, like Metacritic,IMDB, and Rotten Tomatoes.

# Data Analysis
The data analysis was conducted using Python and various data analysis libraries such as pandas, numpy, matplotlib, and seaborn. The analysis includes data cleaning and preprocessing and exploratory data analysis. The results of the analysis are presented in Jupyter notebooks, which can be found in the notebooks directory.

# Repository Structure
Analyzing Fandango's Ratings - Unveiling Bias in Movie Ratings for Ticket Sales.ipynb = contains the Jupyter notebooks used for data analysis, including data cleaning and preprocessing and exploratory data analysis.
all_sites_scores.csv = contains every film that has a Rotten Tomatoes rating, a RT User rating, a Metacritic score, a Metacritic User score, and IMDb score, and at least 30 fan reviews on Fandango. The data from Fandango was pulled on Aug. 24, 2015.
fandango_scrape.csv = contains every film 538 pulled from Fandango.
