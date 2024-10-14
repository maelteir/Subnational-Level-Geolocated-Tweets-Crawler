# Subnational-Level-Geolocated-Tweets-Crawler
This repository presents a crawler that queries Twitter backend to retrieve tweets geolocated at subnational level.  The retrieved tweets are not only geotagged tweets, but also tweets whose user location belongs to the target subnational region. Generating such dataset is essential for building a surveillance system that provides national-level and subnational-level insights during crises and epidemics.

Applying this crawler to Kingdom of Saudi Arabia during COVID-19 epidemic, the generated dataset reaches 262,178 unique geolocated tweets compared to only 61,711 unique geotagged tweets i.e., 4.25 times as many tweets.

Similar datasets can be generated for different events and regions by:
 - Changing the files in the Cirlces directlory to represent the regions/ subregions of intereset.
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
