## Code without Lumpsup and SIP ##

# import pandas as pd
# import numpy as np
#
# ROLLING_YEARS = [1,3,5,7,10]
#
# def load_master_db():
#     df = pd.read_csv("data/processed/master_nav_database.csv")
#     df['date'] = pd.to_datetime(df['date'])
#     return df
#
#
# def calculate_scheme_summary(master_db, scheme_code):
#     scheme_df = master_db[master_db['scheme_code'] == scheme_code].copy()
#
#     scheme_name = scheme_df['scheme_name'].iloc[0]
#     df = scheme_df[['date','nav']].sort_values('date').reset_index(drop=True)
#     base_df = df.copy()
#
#     # rolling returns
#     for yr in ROLLING_YEARS:
#         base_df[f"date_{yr}Y_back"] = base_df['date'] - pd.DateOffset(years=yr)
#
#         base_df = pd.merge_asof(
#             base_df,
#             df.rename(columns={'date':f'match_date_{yr}Y','nav':f'nav_{yr}Y_back'}),
#             left_on=f"date_{yr}Y_back",
#             right_on=f"match_date_{yr}Y",
#             direction="backward"
#         )
#
#         base_df[f"Rolling_{yr}Y"] = ((base_df['nav'] / base_df[f'nav_{yr}Y_back'])**(1/yr)-1)*100
#
#     rolling_cols = [c for c in base_df.columns if c.startswith("Rolling_")]
#
#     stats_df = base_df[rolling_cols].agg(['mean','median','max','min','std']).T
#     stats_df.columns = ['Average','Median','Maximum','Minimum','Std_Dev']
#
#     last_row = base_df.tail(1)[rolling_cols].T
#     last_row.columns = ['Last_Value']
#
#     final_stats = stats_df.join(last_row)
#
#     # ======================================
#     # DISTRIBUTION %
#     # ======================================
#     ranges = {
#         "Pct_0_8": (0, 8),
#         "Pct_8_12": (8, 12),
#         "Pct_12_15": (12, 15),
#         "Pct_15_20": (15, 20),
#         "Pct_Greater_20": (20, np.inf)
#     }
#
#     for label, (low, high) in ranges.items():
#         pct_values = []
#         for col in rolling_cols:
#             col_data = base_df[col].dropna()
#             pct = ((col_data >= low) & (col_data < high)).mean() * 100
#             pct_values.append(round(pct, 2))
#         final_stats[label] = pct_values
#
#     # reorder columns
#     final_stats = final_stats[
#         [
#             'Last_Value', 'Average', 'Median', 'Maximum', 'Minimum', 'Std_Dev',
#             'Pct_0_8', 'Pct_8_12', 'Pct_12_15', 'Pct_15_20', 'Pct_Greater_20'
#         ]
#     ]
#
#     final_stats.reset_index(inplace=True)
#     final_stats.rename(columns={'index': 'Period'}, inplace=True)
#     final_stats.insert(0, 'Scheme_Name', scheme_name)
#
#     return final_stats
#
#
# def get_all_schemes(master_db):
#     return master_db[['scheme_code','scheme_name']].drop_duplicates().to_dict("records")


## Code with Lumpsum and SIP - FINAL CODE ##


import os
import pandas as pd
import numpy as np

DATA_PATH = "data/processed/master_nav_database.csv"
ROLLING_YEARS = [1,3,5,7,10]

# ---------------- LOAD DB ----------------
def load_master_db():
    if not os.path.exists(DATA_PATH):
        return None

    df = pd.read_csv(DATA_PATH)

    # normalize
    df.columns = [c.lower() for c in df.columns]
    if "date" not in df.columns or "nav" not in df.columns:
        return None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date","nav"])

    return df

# ---------------- ROLLING SUMMARY ----------------
def calculate_scheme_summary(master_db, scheme_code):

    df = master_db[master_db["scheme_code"] == scheme_code].copy()
    if len(df) < 1000:
        return None

    scheme_name = df["scheme_name"].iloc[0]
    df = df.sort_values("date")[["date","nav"]].reset_index(drop=True)
    base = df.copy()

    for yr in ROLLING_YEARS:
        base[f"date_{yr}"] = base["date"] - pd.DateOffset(years=yr)

        base = pd.merge_asof(
            base,
            df.rename(columns={"date":f"match_{yr}","nav":f"nav_{yr}"}),
            left_on=f"date_{yr}",
            right_on=f"match_{yr}",
            direction="backward"
        )

        base[f"Rolling_{yr}Y"] = ((base["nav"]/base[f"nav_{yr}"])**(1/yr)-1)*100

    roll_cols = [c for c in base.columns if c.startswith("Rolling_")]

    stats = base[roll_cols].agg(["mean","median","max","min","std"]).T
    stats.columns = ["Average","Median","Maximum","Minimum","Std_Dev"]

    last = base[roll_cols].tail(1).T
    last.columns = ["Last_Value"]

    final = stats.join(last)

    ranges = {
        "Pct_0_8": (0,8),
        "Pct_8_12": (8,12),
        "Pct_12_15": (12,15),
        "Pct_15_20": (15,20),
        "Pct_Greater_20": (20,np.inf)
    }

    for label,(lo,hi) in ranges.items():
        final[label] = [
            ((base[c]>=lo)&(base[c]<hi)).mean()*100
            for c in roll_cols
        ]

    final.reset_index(inplace=True)
    final.rename(columns={"index":"Period"}, inplace=True)
    final.insert(0,"Scheme_Name",scheme_name)

    return final.round(2)

# ---------------- LIST ----------------
def get_all_schemes(master_db):
    return (
        master_db[["scheme_code","scheme_name"]]
        .drop_duplicates()
        .sort_values("scheme_name")
        .to_dict("records")
    )

# ---------------- LUMPSUM ----------------
def calculate_lumpsum_return(df, scheme_code, amount, start=None, end=None):

    data = df[df["scheme_code"]==scheme_code].copy()
    if start: data = data[data["date"]>=pd.to_datetime(start)]
    if end:   data = data[data["date"]<=pd.to_datetime(end)]
    if len(data)<2:
        return {"error":"Not enough data"}

    data = data.sort_values("date")
    units = amount/data.iloc[0]["nav"]
    final = units*data.iloc[-1]["nav"]
    years = (data.iloc[-1]["date"]-data.iloc[0]["date"]).days/365

    return {
        "Invested_Amount": round(amount,2),
        "Final_Value": round(final,2),
        "CAGR %": round(((final/amount)**(1/years)-1)*100,2)
    }

def calculate_sip_return(df, scheme_code, monthly, start=None, end=None):

    data = df[df["scheme_code"]==scheme_code].copy()
    if start: data = data[data["date"]>=pd.to_datetime(start)]
    if end:   data = data[data["date"]<=pd.to_datetime(end)]
    if len(data)<60:
        return {"error":"Not enough data"}

    data["month"] = data["date"].dt.to_period("M")
    sip = data.groupby("month").first().reset_index()

    units=0; invested=0
    for _,r in sip.iterrows():
        units += monthly/r["nav"]
        invested += monthly

    final = units*data.iloc[-1]["nav"]
    years = (data.iloc[-1]["date"]-data.iloc[0]["date"]).days/365

    return {
        "Invested_Amount": round(invested,2),
        "Final_Value": round(final,2),
        "CAGR %": round(((final/invested)**(1/years)-1)*100,2)
    }

# ---------------- YEARLY ----------------
def get_lumpsum_yearwise_growth(df, scheme_code, amount, start_date, end_date):

    data = df[df["scheme_code"]==scheme_code].copy()
    data = data[(data["date"]>=pd.to_datetime(start_date))&(data["date"]<=pd.to_datetime(end_date))]
    if data.empty: return None

    units = amount/data.iloc[0]["nav"]
    data["portfolio_value"] = units*data["nav"]

    y = data.resample("Y",on="date").last().reset_index()
    y["Year"] = y["date"].dt.year
    return y[["Year","portfolio_value"]]

def get_sip_yearwise_growth(df, scheme_code, monthly_amt, start_date, end_date):

    data = df[df["scheme_code"]==scheme_code].copy()
    data = data[(data["date"]>=pd.to_datetime(start_date))&(data["date"]<=pd.to_datetime(end_date))]
    if data.empty: return None

    sip_dates = pd.date_range(start=start_date,end=end_date,freq="MS")
    units=0; rows=[]

    for d in sip_dates:
        r = data[data["date"]>=d].head(1)
        if r.empty: continue
        nav = r.iloc[0]["nav"]
        units += monthly_amt/nav
        rows.append({"date":r.iloc[0]["date"],"value":units*nav})

    df2 = pd.DataFrame(rows)
    y = df2.resample("Y",on="date").last().reset_index()
    y["Year"] = y["date"].dt.year
    return y[["Year","value"]]
