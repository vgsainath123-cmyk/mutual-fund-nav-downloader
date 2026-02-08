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

from rolling_engine import calculate_lumpsum, calculate_sip
from datetime import datetime

from rolling_engine import (
    get_lumpsum_yearwise_growth,
    get_sip_yearwise_growth
)



from fastapi import FastAPI
from rolling_engine import (
    load_master_db,
    calculate_scheme_summary,
    get_all_schemes,
    calculate_lumpsum_return,
    calculate_sip_return
)

from fastapi import FastAPI
from rolling_engine import load_master_db

app = FastAPI(title="Mutual Fund Analytics API")

master_db = None
valid_master_db = None

@app.on_event("startup")
def startup_event():
    global master_db, valid_master_db
    print("📂 Loading Master NAV database...")

    from download_data import download_database
    download_database()

    master_db = load_master_db()

    scheme_counts = master_db.groupby("scheme_code").size()
    valid_scheme_codes = scheme_counts[scheme_counts >= 500].index.tolist()
    valid_master_db = master_db[master_db["scheme_code"].isin(valid_scheme_codes)]

    print("API Ready 🚀")

print("Checking valid schemes...")

scheme_counts = master_db.groupby("scheme_code").size()
valid_scheme_codes = scheme_counts[scheme_counts >= 500].index.tolist()
valid_master_db = master_db[master_db["scheme_code"].isin(valid_scheme_codes)]

print("Total schemes:", master_db['scheme_code'].nunique())
print("Valid schemes:", len(valid_scheme_codes))
print("API Ready 🚀")

# ---------------------------------------------------
# HOME ROUTE
# ---------------------------------------------------
@app.get("/")
def home():
    return {"message": "Mutual Fund API running 🚀"}

# ---------------------------------------------------
# GET ALL VALID SCHEMES
# ---------------------------------------------------
@app.get("/schemes")
def schemes():
    return get_all_schemes(valid_master_db)

# ---------------------------------------------------
# ROLLING RETURNS SUMMARY
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
# LUMPSUM CALCULATOR
# Example:
# /lumpsum/120377?amount=100000&start=2015-01-01&end=2024-01-01
# ---------------------------------------------------
@app.get("/lumpsum/{scheme_code}")
def lumpsum_return(
    scheme_code: int,
    amount: float,
    start: str = None,
    end: str = None
):
    try:
        result = calculate_lumpsum_return(
            valid_master_db,
            scheme_code,
            amount,
            start,
            end
        )
        return result

    except Exception as e:
        return {"error": str(e)}

# ---------------------------------------------------
# SIP CALCULATOR
# Example:
# /sip/120377?monthly=5000&start=2015-01-01&end=2024-01-01
# ---------------------------------------------------
@app.get("/sip/{scheme_code}")
def sip_return(
    scheme_code: int,
    monthly: float,
    start: str = None,
    end: str = None
):
    try:
        result = calculate_sip_return(
            valid_master_db,
            scheme_code,
            monthly,
            start,
            end
        )
        return result

    except Exception as e:
        return {"error": str(e)}


@app.get("/lumpsum/{scheme_code}")
def lumpsum(scheme_code:int, amount:float, start:str, end:str):
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)

        result = calculate_lumpsum(valid_master_db, scheme_code, amount, start_date, end_date)

        if result is None:
            return {"error":"Not enough data for selected period"}

        return result

    except Exception as e:
        return {"error":str(e)}

@app.get("/sip/{scheme_code}")
def sip(scheme_code:int, monthly:float, start:str, end:str):
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)

        result = calculate_sip(valid_master_db, scheme_code, monthly, start_date, end_date)

        if result is None:
            return {"error":"Not enough data for selected period"}

        return result

    except Exception as e:
        return {"error":str(e)}


@app.get("/lumpsum_yearly/{scheme_code}")
def lumpsum_yearly(
    scheme_code: int,
    amount: float,
    start_date: str,
    end_date: str
):
    try:
        result = get_lumpsum_yearwise_growth(
            valid_master_db,
            scheme_code,
            amount,
            start_date,
            end_date
        )

        if result is None:
            return {"error": "No data"}

        return result.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

@app.get("/sip_yearly/{scheme_code}")
def sip_yearly(
    scheme_code: int,
    monthly_amount: float,
    start_date: str,
    end_date: str
):
    try:
        result = get_sip_yearwise_growth(
            valid_master_db,
            scheme_code,
            monthly_amount,
            start_date,
            end_date
        )

        if result is None:
            return {"error": "No data"}

        return result.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
