from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, And
from math import radians, cos, sin, asin, sqrt, degrees, atan2

# Initialize Firebase app with credentials
cred = credentials.Certificate("frcredproject.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()


def validate_point(p):
    lat, lon = p
    assert -90 <= lat <= 90, "bad latitude"
    assert -180 <= lon <= 180, "bad longitude"


def distance_haversine(p1, p2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Haversine
    formula:
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
                        _   ____
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = R ⋅ c

    where   φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
            note that angles need to be in radians to pass to trig functions!
    """
    lat1, lon1 = p1
    lat2, lon2 = p2
    for p in [p1, p2]:
        validate_point(p)

    R = 6371  # km - earths's radius

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))  # 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c
    return d


class RestoItem(BaseModel):
    max: int
    min: int
    lat: float
    long: float
    radius: float


@app.get("/")
async def read_root():
    raise HTTPException(status_code=404)


@app.post("/get_resto/")
async def read_item(item: RestoItem):
    item_dict = item.dict()
    print(item.min, item.max)
    docs = db.collection("restaurant_V3")
    docs = docs.where(filter=FieldFilter("max_price", "<=", item.max))
    # docs.where(filter=FieldFilter('min_price','>=',item.min))
    dstream = docs.stream()
    ts = []
    for doc in dstream:
        dc = doc.to_dict()
        mp = dc["min_price"]
        loc = dc["location"].latitude, dc["location"].longitude
        currentloc = item.lat, item.long
        # this in KM
        distance = distance_haversine(currentloc, loc)
        # print(distance)
        if mp >= item.min:
            if distance <= item.radius:
                dc["distance"] = distance
                ts.append(dc)
    return {"status": "ok", "data": ts}
