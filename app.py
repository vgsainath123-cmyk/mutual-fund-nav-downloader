# from fastapi import FastAPI
# from rolling_engine import *
#
# app = FastAPI(title="Mutual Fund Analytics API")
#
# master_db = load_master_db()
#
# print("Checking valid schemes...")
#
# scheme_counts = master_db.groupby("scheme_code").size()
# valid_scheme_codes = scheme_counts[scheme_counts >= 500].index.tolist()
#
# valid_master_db = master_db[master_db["scheme_code"].isin(valid_scheme_codes)]
#
# print("Total schemes:", master_db['scheme_code'].nunique())
# print("Valid schemes:", len(valid_scheme_codes))
#
#
#
# # list all schemes
# @app.get("/schemes")
# def schemes():
#     return get_all_schemes(valid_master_db)
#
# # summary for a scheme
# @app.get("/scheme/{scheme_code}")
# def scheme_summary(scheme_code: int):
#     result = calculate_scheme_summary(valid_master_db, scheme_code)
#
#     if result is None:
#         return {"error": "Not enough history"}
#
#     return result.to_dict(orient="records")
#
# @app.get("/")
# def home():
#     return {"message": "Mutual Fund API is running 🚀"}
#

## Break - Up ##

# from fastapi import FastAPI
# from rolling_engine import load_master_db, calculate_scheme_summary, get_all_schemes
#
# app = FastAPI(title="Mutual Fund Analytics API")
#
# # ---------------------------------------------------
# # LOAD DATABASE ON STARTUP
# # ---------------------------------------------------
# print("📂 Loading Master NAV database...")
# master_db = load_master_db()
#
# print("Checking valid schemes...")
#
# scheme_counts = master_db.groupby("scheme_code").size()
# valid_scheme_codes = scheme_counts[scheme_counts >= 500].index.tolist()
#
# valid_master_db = master_db[master_db["scheme_code"].isin(valid_scheme_codes)]
#
# print("Total schemes:", master_db['scheme_code'].nunique())
# print("Valid schemes:", len(valid_scheme_codes))
# print("API Ready 🚀")
#
#
# # ---------------------------------------------------
# # HOME ROUTE
# # ---------------------------------------------------
# @app.get("/")
# def home():
#     return {"message": "Mutual Fund API is running 🚀"}
#
#
# # ---------------------------------------------------
# # GET ALL VALID SCHEMES
# # ---------------------------------------------------
# @app.get("/schemes")
# def schemes():
#     return get_all_schemes(valid_master_db)
#
#
# # ---------------------------------------------------
# # GET FULL SUMMARY FOR A SCHEME
# # ---------------------------------------------------
# @app.get("/scheme/{scheme_code}")
# def scheme_summary(scheme_code: int):
#
#     try:
#         result = calculate_scheme_summary(valid_master_db, scheme_code)
#
#         if result is None or result.empty:
#             return {"error": "Not enough history"}
#
#         # convert dataframe to JSON records
#         return result.to_dict(orient="records")
#
#     except Exception as e:
#         # THIS helps debugging inside Streamlit
#         return {"error": str(e)}

## Break up ##


## FINAL CODE ##

from fastapi import FastAPI
from download_data import download_database
from rolling_engine import *

app = FastAPI(title="Mutual Fund API")

master_db=None
valid_master_db=None
SCHEME_CACHE=None

@app.on_event("startup")
def startup():
    global master_db,valid_master_db,SCHEME_CACHE
    download_database()
    master_db = load_master_db()

    counts = master_db.groupby("scheme_code").size()
    valid_codes = counts[counts>=500].index
    valid_master_db = master_db[master_db["scheme_code"].isin(valid_codes)]

    SCHEME_CACHE = get_all_schemes(valid_master_db)

@app.get("/")
def home():
    return {"message":"API running"}

@app.get("/schemes")
def schemes():
    return SCHEME_CACHE

@app.get("/scheme/{scheme_code}")
def scheme(scheme_code:int):
    res = calculate_scheme_summary(valid_master_db,scheme_code)
    if res is None:
        return {"error":"Not enough history"}
    return res.to_dict("records")

@app.get("/lumpsum/{scheme_code}")
def lumpsum(scheme_code:int, amount:float, start:str=None, end:str=None):
    return calculate_lumpsum_return(valid_master_db,scheme_code,amount,start,end)

@app.get("/sip/{scheme_code}")
def sip(scheme_code:int, monthly:float, start:str=None, end:str=None):
    return calculate_sip_return(valid_master_db,scheme_code,monthly,start,end)

@app.get("/lumpsum_yearly/{scheme_code}")
def lumpsum_yearly(scheme_code:int, amount:float, start_date:str, end_date:str):
    return get_lumpsum_yearwise_growth(valid_master_db,scheme_code,amount,start_date,end_date).to_dict("records")

@app.get("/sip_yearly/{scheme_code}")
def sip_yearly(scheme_code:int, monthly_amount:float, start_date:str, end_date:str):
    return get_sip_yearwise_growth(valid_master_db,scheme_code,monthly_amount,start_date,end_date).to_dict("records")
