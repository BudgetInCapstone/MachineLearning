# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import pandas as pd

# # Initialize Firebase app with credentials
# cred = credentials.Certificate('frcred.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# df = pd.read_csv('Dataset_v3.csv')
# grouped = df.groupby('merchant_name')
# aggregated = grouped.agg({'price': ['min', 'max']}).reset_index()

# for _, row in aggregated.iterrows():
#     dmn = row['merchant_name']
#     # dmr = row[('merchant_area', 'first')]
#     dmin = row[('price', 'min')]
#     dmax = row[('price', 'max')]
#     # dlat = row.get(('latitude'))  # Replace 'latitude' with the actual column name if present
#     # dlon = row.get(('longitude'))  # Replace 'longitude' with the actual column name if present

#     print(f"Inserting {dmn}....")
#     data = {
#         u'name': dmn,
#         u'min_price': dmin,
#         u'max_price': dmax,
#         # u'area': dmr,
#     }
#     # if dlat is not None and dlon is not None:
#     #     # Convert latitude and longitude to Firestore GeoPoint
#     #     data[u'location'] = firestore.GeoPoint(dlat, dlon)

#     try:
#         db.collection(u'restaurant_V3').add(data)
#     except Exception as e:
#         print(f"Error inserting {dmn}: {e}")
 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Initialize Firebase app with credentials
cred = credentials.Certificate('frcred.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

df = pd.read_csv('Dataset_v3.csv')
grouped = df.groupby('merchant_name')
aggregated = grouped.agg({'price': ['min', 'max']}).reset_index()


for _, row in aggregated.iterrows():
    dmn = row['merchant_name']
    # dmr = row['merchant_area']
    dmin = row[('price', 'min')]
    dmax = row[('price', 'max')]
    # dmin = row['min']
    # dmax = row['max']
    dlat = row['latitude']  # Replace 'latitude' with the actual column name
    dlon = row['longitude']  # Replace 'longitude' with the actual column name

    print(f"Inserting {dmn}....")
    data = {
        u'name': dmn,
        u'min_price': dmin,
        u'max_price': dmax,
        # u'merchant_area': dmr,
    }
    if not pd.isnull(dlat) and not pd.isnull(dlon):
        # Convert latitude and longitude to Firestore GeoPoint
        data[u'location'] = firestore.GeoPoint(float(dlat), float(dlon))

    try:
        db.collection(u'restaurant_V3').add(data)
    except Exception as e:
        print(f"Error inserting {dmn}: {e}")
