# -*- coding: utf-8 -*-
"""Copy of Delivery Time Prediction Dataset - Final

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10P5VHKN7doqvEj5J4prxNpVo_NO_8LxT
"""

import pandas as pd

import pandas as pd
import requests
import io

file_id = '1jpxel4H432tANWQs1wWbr-MvKm6B-vpd'
url = f'https://drive.google.com/uc?id={file_id}'

# Download the contents of the CSV file
download = requests.get(url).content

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(io.StringIO(download.decode('utf-8')))

df

df.columns

#Fixing the data type of columns
numeric_columns = ["Delivery_person_Age", "Delivery_person_Ratings", "multiple_deliveries"]

for column in numeric_columns:
    df[column] = df[column].astype(float)

"""# Filtering the South Asian Restuarants"""

import math

# Define boundaries for South Asian region (these are approximate values and can be refined)
LAT_MIN, LAT_MAX = 5.0, 37.0
LON_MIN, LON_MAX = 67.0, 97.0

# Filter by region
south_asian_restaurants = df[
    (df['Restaurant_latitude'] >= LAT_MIN) & (df['Restaurant_latitude'] <= LAT_MAX) &
    (df['Restaurant_longitude'] >= LON_MIN) & (df['Restaurant_longitude'] <= LON_MAX) &
    (df['Delivery_location_longitude'] >= LON_MIN) & (df['Delivery_location_longitude'] <= LON_MAX) &
    (df['Delivery_location_latitude'] >= LAT_MIN) & (df['Delivery_location_latitude'] <= LAT_MAX)
]
def vincenty_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the Earth's surface
    using the Vincenty formula.

    Parameters:
    - lat1, lon1: Latitude and Longitude of the first point.
    - lat2, lon2: Latitude and Longitude of the second point.

    Returns:
    - Distance in kilometers between the two points.
    """

    # WGS-84 ellipsoidal parameters
    a = 6378137.0  # semi-major axis in meters
    f = 1 / 298.257223563  # flattening
    b = (1 - f) * a  # semi-minor axis

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    U1 = math.atan((1 - f) * math.tan(lat1))
    U2 = math.atan((1 - f) * math.tan(lat2))

    L = lon2 - lon1
    Lambda = L
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    # Iterate till change in lambda is insignificant
    for _ in range(1000):
        sinLambda = math.sin(Lambda)
        cosLambda = math.cos(Lambda)
        sinSigma = math.sqrt((cosU2 * sinLambda)**2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda)**2)
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cos2Alpha = 1 - sinAlpha**2
        cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cos2Alpha
        C = f / 16 * cos2Alpha * (4 + f * (4 - 3 * cos2Alpha))
        Lambda_prev = Lambda
        Lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM**2)))

        # Break if change in lambda is insignificant
        if abs(Lambda - Lambda_prev) < 1e-12:
            break

    u2 = cos2Alpha * (a**2 - b**2) / (b**2)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma * (-1 + 2 * cos2SigmaM**2) - B / 6 * cos2SigmaM * (-3 + 4 * sinSigma**2) * (-3 + 4 * cos2SigmaM**2)))

    # Distance in meters
    s = b * A * (sigma - deltaSigma)

    # Convert to kilometers
    return (s/1000)


# Add distance column
south_asian_restaurants['distance'] = south_asian_restaurants.apply(
    lambda row: vincenty_distance(
        row['Restaurant_latitude'], row['Restaurant_longitude'],
        row['Delivery_location_latitude'], row['Delivery_location_longitude']
    ),
    axis=1
)

# Define a threshold for implausible distances (e.g., 100 km) and filter out records exceeding this distance
MAX_DISTANCE = 30 # change accordingly
filtered_df = south_asian_restaurants[south_asian_restaurants['distance'] <= MAX_DISTANCE]

print(filtered_df)

filtered_df['distance']

filtered_df.shape

"""## Box plots of Restuarant longitude , latitude with delivery longitude and latitudes

> Indented block


"""

# Melt the DataFrame to long format

import matplotlib.pyplot as plt
import seaborn as sns

plot_loc = filtered_df.melt(value_vars=['Restaurant_latitude', 'Delivery_location_latitude', 'Restaurant_longitude', 'Delivery_location_longitude'])

plt.figure(figsize=(10, 6))  # Adjust the size based on your needs
sns.boxplot(x='variable', y='value', data= plot_loc)
plt.ylabel('Coordinates')
plt.xlabel('Locations')
plt.title('Distribution of Latitude and Longitude for Restaurants and Delivery')
plt.xticks(rotation=45)  # Rotate x-labels for better readability

plt.show()

"""# Handling Null values


"""

#Convert String 'NaN' to np.nan
import numpy as np
def convert_nan(df):
    df.replace('NaN', float(np.nan), regex=True,inplace=True)

convert_nan(filtered_df)


#Check null values

filtered_df.isnull().sum().sort_values(ascending=False)

null_rows = filtered_df[filtered_df.isnull().any(axis=1)].shape[0]
print(null_rows)

filtered_df.dropna(inplace=True)

#Rechecking for null values
filtered_df.isnull().sum().sort_values(ascending=False)

"""# Feature Extraction

## Calculating the Order Prepare Time ( order time - picked time )
"""

filtered_df.columns

import pandas as pd
import numpy as np

def calculate_time_diff(df):
    # Convert Order_Date to datetime object
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    # Find the difference between ordered time & picked time
    df['Time_Orderd'] = pd.to_timedelta(df['Time_Orderd'])
    df['Time_Order_picked'] = pd.to_timedelta(df['Time_Order_picked'])

    # Calculate Time_Order_picked_formatted
    offset = np.where(df['Time_Order_picked'] < df['Time_Orderd'], pd.DateOffset(days=1), pd.DateOffset(days=0))
    df['Time_Order_picked_formatted'] = df['Order_Date'] + offset + df['Time_Order_picked']
    df['Time_Ordered_formatted'] = df['Order_Date'] + df['Time_Orderd']

    df['order_prepare_time'] = (df['Time_Order_picked_formatted'] - df['Time_Ordered_formatted']).dt.total_seconds() / 60

    # Handle null values by filling with the median
    df['order_prepare_time'].fillna(df['order_prepare_time'].median(), inplace=True)

    # Drop all the time & date related columns
    df.drop(['Time_Orderd', 'Time_Order_picked', 'Time_Ordered_formatted', 'Time_Order_picked_formatted', 'Order_Date'], axis=1, inplace=True)

calculate_time_diff(filtered_df)

filtered_df[1:3]

"""## More feature extraction"""

# From Delivery_person_ID
filtered_df["delivery_city"] = filtered_df["Delivery_person_ID"].apply(lambda id: id.split("RES")[0])
filtered_df["person_id"] = "RES" + filtered_df["Delivery_person_ID"].apply(lambda id: id.split("RES")[1])

# Creating restaurant number and delivery number feature from person_id
#filtered_df["restaurant_num"] = filtered_df["person_id"].str[:5]
#filtered_df["delivery_num"] = filtered_df["person_id"].str[5:10]

# From weather conditions and time taken
filtered_df["weather_condition"] = filtered_df["Weatherconditions"].apply(lambda condition: condition.split(" ")[1])
filtered_df["delivery_time_taken_min"] = filtered_df["Time_taken(min)"].apply(lambda time_taken: float(time_taken.split(" ")[1]))

#DROPPING THE ORDER ID AND DELIVERY ID

filtered_df = filtered_df.drop(['ID', 'Delivery_person_ID','Time_taken(min)','Weatherconditions','Restaurant_latitude',
       'Restaurant_longitude', 'Delivery_location_latitude','Delivery_location_longitude'], axis=1)
filtered_df

"""# Advanced analysis

## Handling the categorical variables
"""

filtered_df.columns

filtered_df = pd.get_dummies(filtered_df, columns=['Type_of_order'])

filtered_df = pd.get_dummies(filtered_df, columns=['City'])

filtered_df = pd.get_dummies(filtered_df, columns=['weather_condition'])

filtered_df = pd.get_dummies(filtered_df, columns=['Type_of_vehicle'])

filtered_df = pd.get_dummies(filtered_df, columns=['delivery_city'])


#Vehicle condition is already encoded as 0,1,2

filtered_df = pd.get_dummies(filtered_df, columns =['Festival'])

mapping1 = {
    'Low ':1,
    'Medium ':2,
    'High ':3,
    'Jam ':4,
}
filtered_df['Road_traffic_density'] = filtered_df['Road_traffic_density'].map(mapping1)

filtered_df.columns

"""## Train test splitting"""

from sklearn.model_selection import train_test_split


X = filtered_df[['Delivery_person_Age', 'Delivery_person_Ratings',
       'Road_traffic_density', 'Vehicle_condition', 'multiple_deliveries',
       'distance', 'order_prepare_time', 'Type_of_order_Buffet ',
       'Type_of_order_Drinks ', 'Type_of_order_Meal ', 'Type_of_order_Snack ',
       'City_Metropolitian ', 'City_Semi-Urban ', 'City_Urban ',
       'weather_condition_Cloudy', 'weather_condition_Fog',
       'weather_condition_Sandstorms', 'weather_condition_Stormy',
       'weather_condition_Sunny', 'weather_condition_Windy',
       'Type_of_vehicle_electric_scooter ', 'Type_of_vehicle_motorcycle ',
       'Type_of_vehicle_scooter ', 'delivery_city_AGR', 'delivery_city_ALH',
       'delivery_city_AURG', 'delivery_city_BANG', 'delivery_city_BHP',
       'delivery_city_CHEN', 'delivery_city_COIMB', 'delivery_city_DEH',
       'delivery_city_GOA', 'delivery_city_HYD', 'delivery_city_INDO',
       'delivery_city_JAP', 'delivery_city_KNP', 'delivery_city_KOC',
       'delivery_city_KOL', 'delivery_city_LUDH', 'delivery_city_MUM',
       'delivery_city_MYS', 'delivery_city_PUNE', 'delivery_city_RANCHI',
       'delivery_city_SUR', 'delivery_city_VAD', 'Festival_No ',
       'Festival_Yes ']]

y = filtered_df['delivery_time_taken_min']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

"""# Fitting the final RF model - Using the important predictors identified by vip plot"""

#For the random forest best fit model
from sklearn.ensemble import RandomForestRegressor
rf_final = RandomForestRegressor(n_estimators= 150,
                            min_samples_split = 5,
                            min_samples_leaf = 4,
                            max_features = 'auto',
                            max_depth = 15,
                            bootstrap = True)

indices=[0,1,2,3,4,5,6,14,15,16,17,18,45,46]


rf_final.fit(X_train.iloc[:, indices],y_train)

X_train.iloc[:, indices].columns

X_train['multiple_deliveries'].unique()

import joblib

# Save the scikit-learn model to a file
joblib.dump(rf_final, 'model_file.pkl')