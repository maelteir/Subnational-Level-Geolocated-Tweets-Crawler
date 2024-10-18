from pyproj import CRS, Transformer
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.ops import transform
from shapely.geometry import mapping
import numpy as np
import math
from geopy.distance import geodesic, great_circle
from area import area

def geodesic_point_buffer(lat, lon, radius):
    """
    Creates circles from given latitude, longitude, and radius
    :param lat: latitude from original data
    :param lon: longitude from original data
    :param radius: radius from original data
    """
    # Azimuthal equidistant projection
    #aeqd_proj = CRS.from_proj4(('+proj=aea +lat_1=50 +lat_2=70 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs'))
    aeqd_proj = CRS.from_proj4(f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0")
    tfmr = Transformer.from_proj(aeqd_proj, aeqd_proj.geodetic_crs)
    buf = Point(0, 0).buffer(radius * 1609.34)  # distance in miles
    return Polygon(transform(tfmr.transform, buf).exterior.coords[:])

def circle_coverage_overlap(circles):
  """
  Calculates the total area covered by a list of circles and the overlapping area.

  Args:
    circles: A list of dictionaries, where each dictionary represents a circle
      with the following keys:
        - 'radius': The radius of the circle.
        - 'x': The x-coordinate of the circle's centroid.
        - 'y': The y-coordinate of the circle's centroid.

  Returns:
    A tuple containing three elements:
      - The total area covered by all circles.
      - The total area of overlap between all circles.
      - A list of dictionaries, where each dictionary represents an overlap area
        between two circles with the following keys:
          - 'circle1_idx': The index of the first circle in the original list.
          - 'circle2_idx': The index of the second circle in the original list.
          - 'area': The area of overlap between the two circles.
  """

  total_area = 0
  total_area2 = 0
  total_area3 = 0
  overlap_area = 0
  overlap_area2 = 0
  overlap_details = []

  # Earth's radius (example value)
  earth_radius = 6371  # kilo meters

  for i, circle1 in enumerate(circles):
    r1 = circle1['radius']
    x1, y1 = circle1['x'], circle1['y']

    poly = geodesic_point_buffer(y1, x1 , r1*0.621371) #This function takes distance in miles
    area_pyproj= area(mapping(poly))/1000/1000  #"km^2"

    total_area2 += np.pi * r1**2
    total_area += 4 * np.pi * r1**2  # Assuming spherical Earth
    total_area3 += area_pyproj

    #print("Circle ",i," Area: ", np.pi * r1**2, " Spherical area: ", 4 * np.pi * r1**2, "pyproj Area: (km2)",   area_pyproj)

    for j, circle2 in enumerate(circles[i + 1:]):  # Avoid self-overlap
      r2 = circle2['radius']
      x2, y2 = circle2['x'], circle2['y']

      # Convert latitudes and longitudes to radians
      lat1_rad = math.radians(y1)
      lon1_rad = math.radians(x1)
      lat2_rad = math.radians(y2)
      lon2_rad = math.radians(x2)
      # Calculate central angle using spherical law of cosines
      central_angle = math.acos(
          math.sin(lat1_rad) * math.sin(lat2_rad) +
          math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(math.fabs(lon1_rad - lon2_rad))
      )
      # Calculate distance using spherical law of cosines
      distance = earth_radius * central_angle
      distance2 = geodesic((y1,x1), (y2,x2)).km
      distance3 = great_circle((y1,x1), (y2,x2)).km
      #distance4 = np.sqrt((lon2_rad - lon1_rad)**2 + (lat2_rad - lat1_rad)**2)

      #print("distance between two centroids: ",distance, " r1+r2: ",str(r1+r2))
      #print("distance between two centroids2: ",distance2, " r1+r2: ",str(r1+r2))
      #print("distance between two centroids3: ",distance3, " r1+r2: ",str(r1+r2))
      #print("distance between two centroids - normal: ",distance4, " r1+r2: ",str(r1+r2))

      if distance2 < r1 + r2:
        # Overlap area based on circle intersection formula
        # overlap2 = np.pi * min(r1**2, r2**2) * (1 - 2 * np.arccos(distance2 / (2 * r1 * r2)))

        # Overlap area using formula for spherical triangles
        overlap = 2 * np.pi * r1 * r2 * np.sin(central_angle / 2) ** 2
        #print(" overlap: ", overlap)
        overlap_area += overlap
        #overlap_area2 += overlap2
        overlap_details.append({
            'circle1_idx': i,
            'circle2_idx': i + j + 1,  # Adjust for skipping self-overlap
            'area': overlap
        })

  return total_area3, total_area2, total_area, overlap_area, overlap_details

print("State  Total area covered PiProj  ", "Total area covered Pi*r^2  ", "Total overlapping area  ", "Overlap details  ")

with open('States', 'r') as states_file:
    	lines = states_file.readlines()
Totalcount=0
for line in lines:
  state= line.replace('\n','')
  circles = []
  with open(state+".txt", 'r') as file: #EasternRegion
    for line in file:
      # Split the line by space and convert values to numbers
      values = line.strip().split()
      y, x, radius = map(float, values)

      # Create a dictionary for the circle data
      circle = {
          'radius': radius,
          'x': x,
          'y': y
      }
      circles.append(circle)
    #print(circles)

    # Calculate coverage and overlap
    total_area3, total_area2, total_area, overlap_area, overlap_details = circle_coverage_overlap(circles)

    print(state,".txt","  ",total_area3,"  ", total_area2, "  ",overlap_area,"  ", overlap_details)
