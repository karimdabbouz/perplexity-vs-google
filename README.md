# Comparison of Sources Used in Google vs. Perplexity for German Searches

There's a lot of speculation surrounding Perplexity's search index. Perplexity itself says that they keep their own index, but many users have noticed that the sources used in Perplexity are often very similar to those used in Google. I wanted to know how similar the sources are for German search terms. I therefore compiled 1800 searches over 18 hand-chosen categories, collected the sources and did some analysis on it.

I started with 18 hand-chosen categories, created 10 base queries for each of them and then randomly selected 10 similar queries from Google Keyword Planner and answerthepublic.com. This gave me 1800 queries in total. The queries used are listed in the queries.txt.

I have refactored the code to collect sources from Google and Perplexity into a Docker image in `/perplexity-google-script`. The code to collect similar queries from base queries has not been refactored but can be found in `perplexity-google-data-collection.ipynb`. All code for data cleaning and analysis can be found in `perplexity-google-analysis.ipynb` including pre-written code to visualize results for the different categories.

I plan on extending this experiment using a larger data set and to possibly include other search engines like Bing or Google SGE once it's available in Germany.