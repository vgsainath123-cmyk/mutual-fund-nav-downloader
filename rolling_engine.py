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

ROLLING_YEARS = [1,3,5,7,10]

# ============================================================
# LOAD MASTER DATABASE
# ============================================================

DATA_PATH = "data/processed/master_nav_database.csv"
def load_master_db():
    print("🔎 Looking for DB at:", os.path.abspath(DATA_PATH))

    if not os.path.exists(DATA_PATH):
        print("❌ Database file NOT found at:", os.path.abspath(DATA_PATH))
        print("📁 Current folder:", os.getcwd())
        print("📂 Files here:", os.listdir())
        return None

    print("📂 Found DB, loading:", DATA_PATH)
    return pd.read_csv(DATA_PATH)
# ============================================================
# ROLLING RETURN ENGINE
# ============================================================
def calculate_scheme_summary(master_db, scheme_code):

    scheme_df = master_db[master_db['scheme_code'] == scheme_code].copy()

    if scheme_df.empty:
        return None

    scheme_name = scheme_df['scheme_name'].iloc[0]
    df = scheme_df[['date','nav']].sort_values('date').reset_index(drop=True)
    base_df = df.copy()

    # Rolling Returns Calculation
    for yr in ROLLING_YEARS:

        base_df[f"date_{yr}Y_back"] = base_df['date'] - pd.DateOffset(years=yr)

        base_df = pd.merge_asof(
            base_df,
            df.rename(columns={'date':f'match_date_{yr}Y','nav':f'nav_{yr}Y_back'}),
            left_on=f"date_{yr}Y_back",
            right_on=f"match_date_{yr}Y",
            direction="backward"
        )

        base_df[f"Rolling_{yr}Y"] = (
            (base_df['nav'] / base_df[f'nav_{yr}Y_back'])**(1/yr) - 1
        ) * 100

    rolling_cols = [c for c in base_df.columns if c.startswith("Rolling_")]

    # Stats
    stats_df = base_df[rolling_cols].agg(['mean','median','max','min','std']).T
    stats_df.columns = ['Average','Median','Maximum','Minimum','Std_Dev']

    last_row = base_df.tail(1)[rolling_cols].T
    last_row.columns = ['Last_Value']

    final_stats = stats_df.join(last_row)

    # ============================================================
    # DISTRIBUTION %
    # ============================================================
    ranges = {
        "Pct_0_8": (0, 8),
        "Pct_8_12": (8, 12),
        "Pct_12_15": (12, 15),
        "Pct_15_20": (15, 20),
        "Pct_Greater_20": (20, np.inf)
    }

    for label, (low, high) in ranges.items():
        pct_values = []
        for col in rolling_cols:
            col_data = base_df[col].dropna()
            pct = ((col_data >= low) & (col_data < high)).mean() * 100
            pct_values.append(round(pct, 2))
        final_stats[label] = pct_values

    final_stats = final_stats[
        [
            'Last_Value','Average','Median','Maximum','Minimum','Std_Dev',
            'Pct_0_8','Pct_8_12','Pct_12_15','Pct_15_20','Pct_Greater_20'
        ]
    ]

    final_stats.reset_index(inplace=True)
    final_stats.rename(columns={'index': 'Period'}, inplace=True)
    final_stats.insert(0, 'Scheme_Name', scheme_name)

    return final_stats


# ============================================================
# GET SCHEME LIST
# ============================================================
def get_all_schemes(master_db):
    return master_db[['scheme_code','scheme_name']].drop_duplicates().to_dict("records")


# ============================================================
# 💰 LUMPSUM CALCULATOR (DATE RANGE BASED)
# ============================================================
def calculate_lumpsum(master_db, scheme_code, amount, start_date, end_date):

    scheme_df = master_db[master_db["scheme_code"] == scheme_code].copy()
    scheme_df = scheme_df.sort_values("date")

    start_row = scheme_df[scheme_df["date"] >= start_date].head(1)
    end_row   = scheme_df[scheme_df["date"] <= end_date].tail(1)

    if start_row.empty or end_row.empty:
        return None

    start_nav = start_row["nav"].iloc[0]
    end_nav   = end_row["nav"].iloc[0]

    actual_start = start_row["date"].iloc[0]
    actual_end   = end_row["date"].iloc[0]

    units = amount / start_nav
    final_value = units * end_nav

    years = (actual_end - actual_start).days / 365.25
    cagr = ((final_value/amount)**(1/years)-1)*100
    abs_return = ((final_value/amount)-1)*100

    return {
        "Start_Date": str(actual_start.date()),
        "End_Date": str(actual_end.date()),
        "Start_NAV": round(start_nav,2),
        "End_NAV": round(end_nav,2),
        "Units": round(units,2),
        "Investment": amount,
        "Final_Value": round(final_value,2),
        "Absolute_Return_%": round(abs_return,2),
        "CAGR_%": round(cagr,2)
    }


# ============================================================
# 📅 SIP CALCULATOR (DATE RANGE BASED)
# ============================================================
def calculate_sip(master_db, scheme_code, monthly_amount, start_date, end_date):

    scheme_df = master_db[master_db["scheme_code"] == scheme_code].copy()
    scheme_df = scheme_df.sort_values("date")

    sip_dates = pd.date_range(start=start_date, end=end_date, freq="MS")

    total_units = 0
    total_investment = 0

    for dt in sip_dates:
        nav_row = scheme_df[scheme_df["date"] >= dt].head(1)
        if nav_row.empty:
            continue

        nav = nav_row["nav"].iloc[0]
        units = monthly_amount / nav

        total_units += units
        total_investment += monthly_amount

    end_row = scheme_df[scheme_df["date"] <= end_date].tail(1)
    if end_row.empty:
        return None

    end_nav = end_row["nav"].iloc[0]
    final_value = total_units * end_nav

    years = len(sip_dates)/12
    xirr = ((final_value/total_investment)**(1/years)-1)*100
    abs_return = ((final_value/total_investment)-1)*100

    return {
        "Start_Date": str(start_date.date()),
        "End_Date": str(end_date.date()),
        "Total_Investment": round(total_investment,2),
        "Units_Accumulated": round(total_units,2),
        "Final_Value": round(final_value,2),
        "Absolute_Return_%": round(abs_return,2),
        "XIRR_%": round(xirr,2)
    }

# =====================================================
# LUMPSUM RETURN CALCULATOR
# =====================================================
def calculate_lumpsum_return(master_db, scheme_code, amount, start=None, end=None):

    df = master_db[master_db['scheme_code'] == scheme_code].copy()
    df = df.sort_values("date")

    if start:
        df = df[df['date'] >= pd.to_datetime(start)]
    if end:
        df = df[df['date'] <= pd.to_datetime(end)]

    if df.empty:
        return {"error": "No data in selected period"}

    start_nav = df.iloc[0]['nav']
    end_nav = df.iloc[-1]['nav']

    units = amount / start_nav
    final_value = units * end_nav

    years = (df.iloc[-1]['date'] - df.iloc[0]['date']).days / 365
    cagr = ((final_value/amount)**(1/years) - 1) * 100 if years > 0 else 0

    return {
        "Start_Date": str(df.iloc[0]['date'].date()),
        "End_Date": str(df.iloc[-1]['date'].date()),
        "Invested_Amount": round(amount,2),
        "Final_Value": round(final_value,2),
        "CAGR %": round(cagr,2)
    }


# =====================================================
# SIP RETURN CALCULATOR
# =====================================================
def calculate_sip_return(master_db, scheme_code, monthly, start=None, end=None):

    df = master_db[master_db['scheme_code'] == scheme_code].copy()
    df = df.sort_values("date")

    if start:
        df = df[df['date'] >= pd.to_datetime(start)]
    if end:
        df = df[df['date'] <= pd.to_datetime(end)]

    if df.empty:
        return {"error": "No data in selected period"}

    df['month'] = df['date'].dt.to_period("M")
    sip_dates = df.groupby("month").first().reset_index()

    total_units = 0
    invested = 0

    for _, row in sip_dates.iterrows():
        nav = row['nav']
        units = monthly / nav
        total_units += units
        invested += monthly

    final_nav = df.iloc[-1]['nav']
    final_value = total_units * final_nav

    years = (df.iloc[-1]['date'] - df.iloc[0]['date']).days / 365
    cagr = ((final_value/invested)**(1/years) - 1) * 100 if years > 0 else 0

    return {
        "Start_Date": str(df.iloc[0]['date'].date()),
        "End_Date": str(df.iloc[-1]['date'].date()),
        "Invested_Amount": round(invested,2),
        "Final_Value": round(final_value,2),
        "CAGR %": round(cagr,2)
    }


# ============================================================
# 💰 LUMPSUM RETURN CALCULATOR
# ============================================================
def calculate_lumpsum(master_db, scheme_code, amount, start_date, end_date):

    df = master_db[master_db["scheme_code"] == scheme_code].copy()
    df = df.sort_values("date")

    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    if len(df) < 2:
        return None

    start_nav = df.iloc[0]["nav"]
    end_nav = df.iloc[-1]["nav"]

    units = amount / start_nav
    final_value = units * end_nav

    days = (df.iloc[-1]["date"] - df.iloc[0]["date"]).days
    years = days / 365

    cagr = ((final_value / amount) ** (1/years) - 1) * 100
    abs_return = ((final_value/amount) - 1) * 100

    # growth series for chart
    df["value"] = units * df["nav"]
    growth = df[["date","value"]].to_dict("records")

    return {
        "invested": round(amount,2),
        "final_value": round(final_value,2),
        "abs_return": round(abs_return,2),
        "cagr": round(cagr,2),
        "growth": growth
    }

# ============================================================
# 📅 SIP RETURN CALCULATOR
# ============================================================
def calculate_sip(master_db, scheme_code, monthly, start_date, end_date):

    df = master_db[master_db["scheme_code"] == scheme_code].copy()
    df = df.sort_values("date")
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    if len(df) < 60:
        return None

    df["month"] = df["date"].dt.to_period("M")
    sip_dates = df.groupby("month").first().reset_index()

    total_units = 0
    invested = 0
    growth_series = []

    for _, row in sip_dates.iterrows():
        nav = row["nav"]
        units = monthly / nav

        total_units += units
        invested += monthly

        value = total_units * nav
        growth_series.append({"date": row["date"], "value": value})

    final_nav = sip_dates.iloc[-1]["nav"]
    final_value = total_units * final_nav
    abs_return = ((final_value/invested)-1)*100

    # ---------- XIRR ----------
    cashflows = [-monthly]*len(sip_dates)
    cashflows[-1] += final_value

    def xirr(cashflows, guess=0.1):
        rate = guess
        for _ in range(100):
            npv = sum(cf/(1+rate)**i for i,cf in enumerate(cashflows))
            d_npv = sum(-i*cf/(1+rate)**(i+1) for i,cf in enumerate(cashflows))
            rate -= npv/d_npv
        return rate*100

    xirr_value = xirr(cashflows)

    return {
        "invested": round(invested,2),
        "final_value": round(final_value,2),
        "abs_return": round(abs_return,2),
        "xirr": round(xirr_value,2),
        "growth": growth_series
    }



import pandas as pd
import numpy as np

# ---------------------------------------------------
# YEAR WISE LUMPSUM GROWTH
# ---------------------------------------------------
def get_lumpsum_yearwise_growth(df, scheme_code, amount, start_date, end_date):

    data = df[df["scheme_code"] == scheme_code].copy()
    data = data.sort_values("date")

    data = data[(data["date"] >= start_date) & (data["date"] <= end_date)]
    if data.empty:
        return None

    start_nav = data.iloc[0]["nav"]
    units = amount / start_nav

    data["portfolio_value"] = units * data["nav"]

    # year end value
    yearly = data.resample("Y", on="date").last().reset_index()
    yearly["Year"] = yearly["date"].dt.year

    return yearly[["Year", "portfolio_value"]]


# ---------------------------------------------------
# YEAR WISE SIP GROWTH
# ---------------------------------------------------
def get_sip_yearwise_growth(df, scheme_code, monthly_amt, start_date, end_date):

    data = df[df["scheme_code"] == scheme_code].copy()
    data = data.sort_values("date")
    data = data[(data["date"] >= start_date) & (data["date"] <= end_date)]

    if data.empty:
        return None

    sip_dates = pd.date_range(start=start_date, end=end_date, freq="MS")

    total_units = 0
    portfolio = []

    for d in sip_dates:
        # nearest NAV for SIP date
        nav_row = data[data["date"] >= d].head(1)
        if nav_row.empty:
            continue

        nav = nav_row.iloc[0]["nav"]
        units_bought = monthly_amt / nav
        total_units += units_bought

        # portfolio value at that date
        value = total_units * nav_row.iloc[0]["nav"]
        portfolio.append([nav_row.iloc[0]["date"], value])

    sip_df = pd.DataFrame(portfolio, columns=["date", "value"])

    yearly = sip_df.resample("Y", on="date").last().reset_index()
    yearly["Year"] = yearly["date"].dt.year

    return yearly[["Year", "value"]]



