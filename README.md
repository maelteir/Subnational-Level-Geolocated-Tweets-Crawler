# Subnational-Level-Geolocated-Tweets-Crawler
This repository presents a crawler that queries Twitter backend to retrieve tweets geolocated at the subnational level.  The retrieved tweets are not only geotagged tweets, but also tweets whose user location belongs to the target subnational region. Generating such dataset is essential for building a surveillance system that provides national-level and subnational-level insights during crises and epidemics.

Applying this crawler to Kingdom of Saudi Arabia during COVID-19 epidemic, the generated dataset reaches 262,178 unique geolocated tweets compared to only 61,711 unique geotagged tweets i.e., 4.25 times as many tweets. Additionally, the dataset successfully predicted two COVID-19 outbreaks in June 2021 and January 2022. The Pearson correlation coefficient between WHO weekly reported cases and weekly returned tweets, with a one-week lag, is r = 0.733; p < 0.001 for Arabic tweets and r = 0.814; p < 0.001 when including English tweets, indicating a very strong correlation at the national level. At the subnational level, top-populated provinces show strong correlations (r = 0.64 to 0.74; p < 0.003).

Similar datasets can be generated for different regions and events by:
 - Changing the files in the Circles directory to represent the regions/ subregions of interest.
 - Changing the files in the Keywords directory to include the keywords representing the target event.
 
The dataset generated using this crawler can be accessed at [KSAGeoCOV](https://kaggle.com/datasets/5e2c333e22d6edca5ee813c84c964e00d682c4aabb3e04b53f85156ba1c52cc6).

# Publications
    @article{elteir2024ksadataset,  
      title =  {Cost-Effective Time-Efficient Subnational-Level Surveillance Using Twitter: Kingdom of Saudi Arabia Case Study},    
      author = {Marwa K. Elteir},
      journal = {Discover Applied Sciences},
      volume = {},
      number = {},
      pages = {},
      year = {2024},
      issn = {3004-9261},
      doi = {},
      url = {},
      publisher={Springer}
    }
