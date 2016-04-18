# README for pull\_from\_abstract.py


## Purpose
To extract datasets from the abstracts that were scraped by our scored api. 

[Example 1](https://github.com/dzhibas/SublimePrettyJson) [Example 2](https://podaac.jpl.nasa.gov/forum/viewtopic.php?f=7&t=335)

## Dependencies:

1. [NLTK Library](http://www.nltk.org/install.html)
For loading failures, open a python shell and type:
```
>>> import nltk
>>> nltk.download()
```
2. Python 2.7.X

## Running the extraction script
1. The 'jsonFiles' folder should be in the same directory as pull_from_abstract.py
and contain the raw jsonFiles that were extracted over Spring Break. 
2. Download the jsonFiles from the [Deliverable 4 Google Doc](https://docs.google.com/document/d/18IRD_CoqINE-x46510zMlA1BbJPu4tOiceeeREQIrRg/edit?usp=sharing) under the **Data** heading.
3. Download and place this [CSV File of Geographic Locations](https://github.com/ushahidi/geograpy/blob/master/geograpy/data/GeoLite2-City-Locations.csv) in the same directory.
4. Running `python pull_from_abstract.py` will execute the code if everything 
else is in place.

## Output
The code randomly selects a certain amount of json files (Can be changed in L85)
and extracts what it believes to be datasets based on a simple regex rule. The code is
commented to explain the regex as well as other checks. Entities containing 
Geographic locations are filtered out from these extracted datasets
	
As of now, outputs are printed to your terminal window, and are also dumped into a file
named "datasets.txt" in the same directory.

## TODOS

1. Make the regex and checks much more comprehensive; this script is very basic, and just to 
get things started. Think about sentence structure, flag words/phrases, and where datasets appear in sentences.

## Extra Resources
[SublimePrettyJson](https://github.com/dzhibas/SublimePrettyJson)

[NLTK Entity Extraction](http://www.nltk.org/book/ch07.html)

[List of POS Tags](http://nishutayaltech.blogspot.in/2015/02/penn-treebank-pos-tags-in-natural.html)

This Code includes GeoLite2 data created by MaxMind, available from
[Max Mind](https://dev.maxmind.com/geoip/geoip2/geoip2-csv-databases/)
