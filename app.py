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
from datetime import datetime

from rolling_engine import (
    load_master_db,
    calculate_scheme_summary,
    get_all_schemes,
    calculate_lumpsum_return,
    calculate_sip_return,
    get_lumpsum_yearwise_growth,
    get_sip_yearwise_growth,
)

app = FastAPI(title="Mutual Fund Analytics API")

master_db = None
valid_master_db = None

# ---------------------------------------------------
# STARTUP
# ---------------------------------------------------
@app.on_event("startup")
def startup_event():
    global master_db, valid_master_db

    print("⬇️ Checking database...")
    from download_data import download_database
    ok = download_database()
    if not ok:
        raise RuntimeError("Database download failed")

    print("📂 Loading Master NAV database...")
    master_db = load_master_db()

    if master_db is None:
        raise RuntimeError("Database load failed")

    scheme_counts = master_db.groupby("scheme_code").size()
    valid_codes = scheme_counts[scheme_counts >= 500].index.tolist()
    valid_master_db = master_db[master_db["scheme_code"].isin(valid_codes)]

    print("API Ready 🚀")

# ---------------------------------------------------
# HOME
# ---------------------------------------------------
@app.get("/")
def home():
    return {"message": "Mutual Fund API running 🚀"}

# ---------------------------------------------------
# SCHEMES
# ---------------------------------------------------
@app.get("/schemes")
def schemes():
    return get_all_schemes(valid_master_db)

# ---------------------------------------------------
# ROLLING SUMMARY
# ---------------------------------------------------
@app.get("/scheme/{scheme_code}")
def scheme_summary(scheme_code: int):
    try:
        result = calculate_scheme_summary(valid_master_db, scheme_code)
        if result is None or result.empty:
            return {"error": "Not enough history"}
        return result.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ---------------------------------------------------
# LUMPSUM
# ---------------------------------------------------
@app.get("/lumpsum/{scheme_code}")
def lumpsum_return(scheme_code: int, amount: float, start: str, end: str):
    try:
        return calculate_lumpsum_return(
            valid_master_db, scheme_code, amount, start, end
        )
    except Exception as e:
        return {"error": str(e)}

# ---------------------------------------------------
# SIP
# ---------------------------------------------------
@app.get("/sip/{scheme_code}")
def sip_return(scheme_code: int, monthly: float, start: str, end: str):
    try:
        return calculate_sip_return(
            valid_master_db, scheme_code, monthly, start, end
        )
    except Exception as e:
        return {"error": str(e)}

# ---------------------------------------------------
# LUMPSUM YEARLY
# ---------------------------------------------------
@app.get("/lumpsum_yearly/{scheme_code}")
def lumpsum_yearly(scheme_code: int, amount: float, start_date: str, end_date: str):
    try:
        result = get_lumpsum_yearwise_growth(
            valid_master_db, scheme_code, amount, start_date, end_date
        )
        if result is None:
            return {"error": "No data"}
        return result.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ---------------------------------------------------
# SIP YEARLY
# ---------------------------------------------------
@app.get("/sip_yearly/{scheme_code}")
def sip_yearly(
    scheme_code: int, monthly_amount: float, start_date: str, end_date: str
):
    try:
        result = get_sip_yearwise_growth(
            valid_master_db, scheme_code, monthly_amount, start_date, end_date
        )
        if result is None:
            return {"error": "No data"}
        return result.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
