
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import io

# Use the application default credentials.
# cred = credentials.ApplicationDefault()
cred = credentials.Certificate('frcred.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

df = pd.read_csv('Dataset_v3.csv')
grouped = df.groupby('merchant_name')
aggregated = grouped['price'].agg(['min', 'max']).reset_index()

for d in aggregated.index:
    dmn = aggregated['merchant_name'][d]
    dmin = aggregated['min'][d]
    dmax = aggregated['max'][d]
    # dlat = aggregated['latitude'][d]
    # dlon = aggregated['longitude'][d]
    print(f"Inserting {dmn}....")
    # doc_ref = db.collection(u'restaurants').document(dmn)
    db.collection(u'restaurant_V3').add({
        u'name': dmn,
        u'min_price': dmin,
        u'max_price': dmax,
        # u'latitude': dlat,
        # u'longitude': dlon,
    })

# for d in aggregated.index:
#     dmn = aggregated['merchant_name'][d]
#     dmin = aggregated['min'][d]
#     dmax = aggregated['max'][d]
#     dlat = aggregated['latitude'][d]
#     dlot = aggregated['longtitude'][d]
#     print(f"Inserting {dmn}....")
#     # doc_ref = db.collection(u'restaurants').document(dmn)
#     db.collection(u'restaurant_V2').add({
#         u'name':dmn,
#         u'min_price': dmin,
#         u'max_price': dmax,
#         u'latitude': dlat,
#         u'longtitude': dlot,
#     })


# with open('gofood_dataset.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
    
#     for row in csv_reader:
#         print(row)
#         line_count+=1
        #
        # doc_ref = db.collection(u'restaurants').document(u'alovelace')
        # doc_ref.set({
        #     u'first': u'Ada',
        #     u'last': u'Lovelace',
        #     u'born': 1815
        # })

