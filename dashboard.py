# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
#
# def highlight_best(row):
#     return ['background-color: #90EE90' if v == row.max() else '' for v in row]
#
#
#
# API = "http://127.0.0.1:8000"
#
# st.title("📊 Mutual Fund Rolling Returns Dashboard")
#
# # load schemes
# schemes = requests.get(f"{API}/schemes").json()
# scheme_names = {s['scheme_name']: s['scheme_code'] for s in schemes}
#
# selected_scheme = st.multiselect(
#     "🔎 Search and select funds to compare",
#     list(scheme_names.keys())
# )
#
#
#
# if st.button("🚀 Compare Funds"):
#
#     if len(selected_scheme) == 0:
#         st.warning("Please select at least one fund")
#         st.stop()
#
#     all_results = []
#
#     progress = st.progress(0)
#
#     for i, scheme_name in enumerate(selected_scheme):
#         code = scheme_names[scheme_name]
#         data = requests.get(f"{API}/scheme/{code}").json()
#
#         df = pd.DataFrame(data)
#         all_results.append(df)
#
#         progress.progress((i + 1) / len(selected_scheme))
#
#     final_df = pd.concat(all_results, ignore_index=True)
#
#     st.success("Comparison ready 🎉")
#
#     # ===============================
#     # PART 4 — SHOW COMPARISON TABLE
#     # ===============================
#     st.subheader("📊 Comparison Table")
#     st.dataframe(final_df)
#
#     # =========================================
#     # PART 5 — LATEST ROLLING RETURN CHART
#     # =========================================
#     st.subheader("📈 Latest Rolling Returns Comparison")
#
#     chart_df = final_df[["Scheme_Name", "Period", "Last_Value"]]
#
#     fig = px.bar(
#         chart_df,
#         x="Period",
#         y="Last_Value",
#         color="Scheme_Name",
#         barmode="group",
#         title="Rolling Returns Comparison"
#     )
#
#     st.plotly_chart(fig, use_container_width=True)
#
#

   # """ Break up """

# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
#
# API = "http://127.0.0.1:8000"
#
#
# # --------------------------------------------------
# # Highlight best fund in each row
# # --------------------------------------------------
# def highlight_best(row):
#     return ['background-color: #90EE90' if v == row.max() else '' for v in row]
#
#
#
# st.title("📊 Mutual Fund Rolling Returns Dashboard")
#
# # --------------------------------------------------
# # Load scheme list
# # --------------------------------------------------
# schemes = requests.get(f"{API}/schemes").json()
# scheme_names = {s['scheme_name']: s['scheme_code'] for s in schemes}
#
# selected_scheme = st.multiselect(
#     "🔎 Search and select funds to compare",
#     list(scheme_names.keys())
# )
#
# # --------------------------------------------------
# # FETCH DATA FROM API
# # --------------------------------------------------
# if st.button("🚀 Compare Funds"):
#
#     if len(selected_scheme) == 0:
#         st.warning("Please select at least one fund")
#         st.stop()
#
#     all_results = []
#     progress = st.progress(0)
#
#     for i, scheme_name in enumerate(selected_scheme):
#         code = scheme_names[scheme_name]
#         data = requests.get(f"{API}/scheme/{code}").json()
#
#         # skip funds with errors
#         if isinstance(data, dict) and "error" in data:
#             st.warning(f"{scheme_name} → Not enough history")
#             continue
#
#         df = pd.DataFrame(data)
#         all_results.append(df)
#
#         progress.progress((i + 1) / len(selected_scheme))
#
#     if len(all_results) == 0:
#         st.error("No valid funds returned rolling data")
#         st.stop()
#
#     final_df = pd.concat(all_results, ignore_index=True)
#     st.success("Comparison ready 🎉")
#
#
#     # =========================================================
#     # 1️⃣ SHOW RAW FULL DATA
#     # =========================================================
#     st.subheader("📋 Full Data Returned From API")
#     st.dataframe(final_df, use_container_width=True)
#
#
#     # =========================================================
#     # 2️⃣ CREATE PROFESSIONAL TABLES PER ROLLING YEAR
#     # =========================================================
#     st.header("📊 Rolling Return Comparison Tables")
#
#     rolling_periods = final_df["Period"].unique()
#
#     for period in rolling_periods:
#
#         st.subheader(f"🏆 {period} Comparison")
#
#         temp = final_df[final_df["Period"] == period]
#
#         # pivot → schemes as columns
#         pivot = temp.set_index("Scheme_Name")[
#             ["Last_Value","Average","Median","Maximum","Minimum","Std_Dev"]
#         ].T
#
#         styled = pivot.style.apply(highlight_best, axis=1).format("{:.2f}")
#
#         st.dataframe(styled, use_container_width=True)
#
#
#     # =========================================================
#     # 3️⃣ DISTRIBUTION TABLES
#     # =========================================================
#     st.header("📈 Rolling Return Distribution %")
#
#     for period in rolling_periods:
#
#         st.subheader(f"📊 Return Distribution → {period}")
#
#         temp = final_df[final_df["Period"] == period]
#
#         dist = temp.set_index("Scheme_Name")[
#             ["Pct_0_8","Pct_8_12","Pct_12_15","Pct_15_20","Pct_Greater_20"]
#         ].T
#
#         styled = dist.style.apply(highlight_best, axis=1).format("{:.2f}")
#
#         st.dataframe(styled, use_container_width=True)
#
#
#     # =========================================================
#     # 4️⃣ KEEP YOUR CHARTS (Latest Rolling Returns)
#     # =========================================================
#     st.header("📊 Latest Rolling Returns Chart")
#
#     chart_df = final_df[["Scheme_Name","Period","Last_Value"]]
#
#     fig = px.bar(
#         chart_df,
#         x="Period",
#         y="Last_Value",
#         color="Scheme_Name",
#         barmode="group",
#         title="Latest Rolling Returns Comparison"
#     )
#
#     st.plotly_chart(fig, use_container_width=True)


 ## Break - up - 2 ###

### Break  ###
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
#
# API = "http://127.0.0.1:8000"
#
# # --------------------------------------------------
# # Highlight best fund in each row (old logic kept)
# # --------------------------------------------------
# def highlight_best(row):
#     return ['background-color: #90EE90' if v == row.max() else '' for v in row]
#
# # --------------------------------------------------
# # ⭐ FIND OVERALL WINNER FUND
# # --------------------------------------------------
# def find_winner(final_df):
#     score = {}
#     periods = final_df["Period"].unique()
#
#     for period in periods:
#         temp = final_df[final_df["Period"] == period]
#
#         pivot = temp.set_index("Scheme_Name")[
#             ["Last_Value","Average","Median","Maximum","Minimum","Std_Dev"]
#         ].T
#
#         # count winners in each metric row
#         for _, row in pivot.iterrows():
#             winner = row.idxmax()
#             score[winner] = score.get(winner, 0) + 1
#
#     if len(score) == 0:
#         return None, None
#
#     winner = max(score, key=score.get)
#     return winner, score[winner]
#
# # --------------------------------------------------
# # ⭐ Highlight ENTIRE WINNER COLUMN
# # --------------------------------------------------
# def highlight_winner_column(df, winner):
#     def style(col):
#         if col.name == winner:
#             return ['background-color: #00FF7F'] * len(col)
#         return [''] * len(col)
#     return df.style.apply(style, axis=0).format("{:.2f}")
#
#
# st.title("📊 Mutual Fund Rolling Returns Dashboard")
#
# # --------------------------------------------------
# # Load schemes
# # --------------------------------------------------
# schemes = requests.get(f"{API}/schemes").json()
# scheme_names = {s['scheme_name']: s['scheme_code'] for s in schemes}
#
# selected_scheme = st.multiselect(
#     "🔎 Search and select funds to compare",
#     list(scheme_names.keys())
# )
#
# # --------------------------------------------------
# # FETCH DATA FROM API
# # --------------------------------------------------
# if st.button("🚀 Compare Funds"):
#
#     if len(selected_scheme) == 0:
#         st.warning("Please select at least one fund")
#         st.stop()
#
#     all_results = []
#     progress = st.progress(0)
#
#     for i, scheme_name in enumerate(selected_scheme):
#         code = scheme_names[scheme_name]
#         data = requests.get(f"{API}/scheme/{code}").json()
#
#         if isinstance(data, dict) and "error" in data:
#             st.warning(f"{scheme_name} → Not enough history")
#             continue
#
#         df = pd.DataFrame(data)
#         all_results.append(df)
#         progress.progress((i + 1) / len(selected_scheme))
#
#     if len(all_results) == 0:
#         st.error("No valid funds returned rolling data")
#         st.stop()
#
#     final_df = pd.concat(all_results, ignore_index=True)
#     st.success("Comparison ready 🎉")
#
#     # ⭐ FIND WINNER FUND
#     winner_fund, win_count = find_winner(final_df)
#
#     # =========================================================
#     # 1️⃣ RAW DATA
#     # =========================================================
#     st.subheader("📋 Full Data Returned From API")
#     st.dataframe(final_df, use_container_width=True)
#
#     # =========================================================
#     # 2️⃣ PERFORMANCE TABLES
#     # =========================================================
#     st.header("📊 Rolling Return Comparison Tables")
#
#     rolling_periods = final_df["Period"].unique()
#
#     for period in rolling_periods:
#         st.subheader(f"🏆 {period} Comparison")
#
#         temp = final_df[final_df["Period"] == period]
#
#         pivot = temp.set_index("Scheme_Name")[
#             ["Last_Value","Average","Median","Maximum","Minimum","Std_Dev"]
#         ].T
#
#         # ⭐ Apply winner column highlight
#         if winner_fund:
#             styled = highlight_winner_column(pivot, winner_fund)
#         else:
#             styled = pivot.style.format("{:.2f}")
#
#         st.dataframe(styled, use_container_width=True)
#
#     # =========================================================
#     # 3️⃣ DISTRIBUTION TABLES
#     # =========================================================
#     st.header("📈 Rolling Return Distribution %")
#
#     for period in rolling_periods:
#         st.subheader(f"📊 Return Distribution → {period}")
#
#         temp = final_df[final_df["Period"] == period]
#
#         dist = temp.set_index("Scheme_Name")[
#             ["Pct_0_8","Pct_8_12","Pct_12_15","Pct_15_20","Pct_Greater_20"]
#         ].T
#
#         if winner_fund:
#             styled = highlight_winner_column(dist, winner_fund)
#         else:
#             styled = dist.style.format("{:.2f}")
#
#         st.dataframe(styled, use_container_width=True)
#
#     # =========================================================
#     # 4️⃣ CHARTS (UNCHANGED)
#     # =========================================================
#     st.header("📊 Latest Rolling Returns Chart")
#
#     chart_df = final_df[["Scheme_Name","Period","Last_Value"]]
#
#     fig = px.bar(
#         chart_df,
#         x="Period",
#         y="Last_Value",
#         color="Scheme_Name",
#         barmode="group",
#         title="Latest Rolling Returns Comparison"
#     )
#
#     st.plotly_chart(fig, use_container_width=True)
#
#     # =========================================================
#     # 🏆 WINNER MESSAGE
#     # =========================================================
#     if winner_fund:
#         st.markdown("---")
#         st.success(f"🏆 Overall Best Performing Fund: **{winner_fund}**")
#         st.caption(f"Won {win_count} performance metrics across rolling periods")

### Break ###



#
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# from datetime import date
#
#
# # --------------------------------------------------
# # 📈 Growth Chart Helper
# # --------------------------------------------------
# def show_growth_chart(values, title):
#     df = pd.DataFrame(values)
#     df["date"] = pd.to_datetime(df["date"])
#
#     fig = px.line(df, x="date", y="value", title=title)
#     st.plotly_chart(fig, use_container_width=True)
#
#
#
#
#
# API = "http://127.0.0.1:8000"
#
# schemes = requests.get(f"{API}/schemes").json()
# schemes_df = pd.DataFrame(schemes)
#
# # --------------------------------------------------
# # Highlight best fund
# # --------------------------------------------------
# def find_winner(final_df):
#     score = {}
#     periods = final_df["Period"].unique()
#
#     for period in periods:
#         temp = final_df[final_df["Period"] == period]
#         pivot = temp.set_index("Scheme_Name")[["Last_Value","Average","Median","Maximum","Minimum","Std_Dev"]].T
#
#         for _, row in pivot.iterrows():
#             winner = row.idxmax()
#             score[winner] = score.get(winner, 0) + 1
#
#     if len(score) == 0:
#         return None, None
#
#     winner = max(score, key=score.get)
#     return winner, score[winner]
#
# def highlight_winner_column(df, winner):
#     def style(col):
#         if col.name == winner:
#             return ['background-color: #00FF7F'] * len(col)
#         return [''] * len(col)
#     return df.style.apply(style, axis=0).format("{:.2f}")
#
# # --------------------------------------------------
# # PAGE TITLE
# # --------------------------------------------------
# st.title("📊 Mutual Fund Analytics Dashboard")
#
# # --------------------------------------------------
# # LOAD SCHEMES
# # --------------------------------------------------
# schemes = requests.get(f"{API}/schemes").json()
# scheme_names = {s['scheme_name']: s['scheme_code'] for s in schemes}
#
# selected_scheme = st.multiselect(
#     "🔎 Select funds to compare",
#     list(scheme_names.keys())
# )
#
# # --------------------------------------------------
# # DATE FILTER
# # --------------------------------------------------
# st.sidebar.header("📅 Investment Period")
# start_date = st.sidebar.date_input("Start Date", date(2015,1,1))
# end_date = st.sidebar.date_input("End Date", date.today())
#
# # =========================================================
# # 🚀 ROLLING RETURNS COMPARISON
# # =========================================================
# if st.button("🚀 Compare Funds"):
#
#     if len(selected_scheme) == 0:
#         st.warning("Select at least one fund")
#         st.stop()
#
#     all_results = []
#     progress = st.progress(0)
#
#     for i, scheme_name in enumerate(selected_scheme):
#         code = scheme_names[scheme_name]
#         data = requests.get(f"{API}/scheme/{code}").json()
#
#         if isinstance(data, dict) and "error" in data:
#             st.warning(f"{scheme_name} → Not enough history")
#             continue
#
#         df = pd.DataFrame(data)
#         all_results.append(df)
#         progress.progress((i+1)/len(selected_scheme))
#
#     if len(all_results) == 0:
#         st.error("No valid funds returned rolling data")
#         st.stop()
#
#     final_df = pd.concat(all_results, ignore_index=True)
#     winner_fund, win_count = find_winner(final_df)
#
#     # ======================================================
#     # 📊 PERFORMANCE TABLES
#     # ======================================================
#     st.header("📊 Rolling Return Comparison")
#     periods = final_df["Period"].unique()
#
#     for period in periods:
#         st.subheader(period)
#
#         temp = final_df[final_df["Period"] == period]
#         pivot = temp.set_index("Scheme_Name")[["Last_Value","Average","Median","Maximum","Minimum","Std_Dev"]].T
#
#         if winner_fund:
#             styled = highlight_winner_column(pivot, winner_fund)
#         else:
#             styled = pivot.style.format("{:.2f}")
#
#         st.dataframe(styled, use_container_width=True)
#
#     # ======================================================
#     # ⭐ DISTRIBUTION TABLES (ADDED BACK)
#     # ======================================================
#     st.header("📈 Rolling Return Distribution %")
#
#     for period in periods:
#         st.subheader(f"Distribution → {period}")
#
#         temp = final_df[final_df["Period"] == period]
#
#         dist = temp.set_index("Scheme_Name")[
#             ["Pct_0_8","Pct_8_12","Pct_12_15","Pct_15_20","Pct_Greater_20"]
#         ].T
#
#         if winner_fund:
#             styled = highlight_winner_column(dist, winner_fund)
#         else:
#             styled = dist.style.format("{:.2f}")
#
#         st.dataframe(styled, use_container_width=True)
#
#     # ======================================================
#     # 📈 CHART
#     # ======================================================
#     st.header("📈 Latest Rolling Returns Chart")
#     chart_df = final_df[["Scheme_Name","Period","Last_Value"]]
#
#     fig = px.bar(chart_df, x="Period", y="Last_Value", color="Scheme_Name", barmode="group")
#     st.plotly_chart(fig, use_container_width=True)
#
#     if winner_fund:
#         st.success(f"🏆 Overall Best Fund: {winner_fund}  (won {win_count} metrics)")
#
# # =========================================================
# # 💰 LUMPSUM CALCULATOR (UPGRADED UI)
# # =========================================================
# st.header("💰 Lumpsum Calculator")
#
# lump_scheme = st.selectbox("Select fund for Lumpsum", list(scheme_names.keys()), key="lump")
# lump_amount = st.number_input("Investment Amount", 1000, 10000000, 100000)
#
# if st.button("Calculate Lumpsum Return"):
#     code = scheme_names[lump_scheme]
#
#     url = f"{API}/lumpsum/{code}?amount={lump_amount}&start={start_date}&end={end_date}"
#     result = requests.get(url).json()
#
#     if "error" in result:
#         st.error(result["error"])
#     else:
#         st.subheader("📊 Lumpsum Result")
#
#         c1, c2, c3 = st.columns(3)
#
#         c1.metric("💰 Invested Amount", f"₹{result['Invested_Amount']:,.0f}")
#         c2.metric("📈 Final Value", f"₹{result['Final_Value']:,.0f}")
#         c3.metric("🚀 CAGR", f"{result['CAGR %']} %")
#
#         # growth chart
#         growth_df = pd.DataFrame({
#             "Stage":["Invested","Final"],
#             "Amount":[result["Invested_Amount"], result["Final_Value"]]
#         })
#
#         fig = px.bar(growth_df, x="Stage", y="Amount", title="Investment Growth")
#         st.plotly_chart(fig, use_container_width=True)
#
#
# # =========================================================
# # 📅 SIP CALCULATOR (UPGRADED UI)
# # =========================================================
# st.header("📅 SIP Calculator")
#
# sip_scheme = st.selectbox("Select fund for SIP", list(scheme_names.keys()), key="sip")
# sip_amount = st.number_input("Monthly SIP Amount", 500, 100000, 5000)
#
# if st.button("Calculate SIP Return"):
#     code = scheme_names[sip_scheme]
#
#     url = f"{API}/sip/{code}?monthly={sip_amount}&start={start_date}&end={end_date}"
#     result = requests.get(url).json()
#
#     if "error" in result:
#         st.error(result["error"])
#     else:
#         st.subheader("📊 SIP Result")
#
#         c1, c2, c3 = st.columns(3)
#
#         c1.metric("💰 Invested Amount", f"₹{result['Invested_Amount']:,.0f}")
#         c2.metric("📈 Final Value", f"₹{result['Final_Value']:,.0f}")
#         c3.metric("🚀 CAGR", f"{result['CAGR %']} %")
#
#         growth_df = pd.DataFrame({
#             "Stage":["Invested","Final"],
#             "Amount":[result["Invested_Amount"], result["Final_Value"]]
#         })
#
#         fig = px.bar(growth_df, x="Stage", y="Amount", title="SIP Growth")
#         st.plotly_chart(fig, use_container_width=True)
#
#
#
# st.subheader("📈 Lumpsum Growth")
#
# url = f"http://127.0.0.1:8000/lumpsum_yearly/{scheme_code}?amount={amount}&start_date={start}&end_date={end}"
# yearly = requests.get(url).json()
#
# if isinstance(yearly, list):
#     df = pd.DataFrame(yearly)
#     df = df.set_index("Year")
#     st.line_chart(df)
#
#
# st.subheader("📈 SIP Growth")
#
# url = f"http://127.0.0.1:8000/sip_yearly/{scheme_code}?monthly_amount={sip_amt}&start_date={start}&end_date={end}"
# yearly = requests.get(url).json()
#
# if isinstance(yearly, list):
#     df = pd.DataFrame(yearly)
#     df = df.set_index("Year")
#     st.line_chart(df)


## Break- above code is error code ##


#####   FINAL CODE ###


import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date

API = "http://127.0.0.1:8000"

# --------------------------------------------------
# Load schemes once
# --------------------------------------------------
schemes = requests.get(f"{API}/schemes").json()
schemes_df = pd.DataFrame(schemes)
scheme_names = {s['scheme_name']: s['scheme_code'] for s in schemes}

# --------------------------------------------------
# Highlight best fund
# --------------------------------------------------
def find_winner(final_df):
    score = {}
    periods = final_df["Period"].unique()

    for period in periods:
        temp = final_df[final_df["Period"] == period]
        pivot = temp.set_index("Scheme_Name")[["Last_Value","Average","Median","Maximum","Minimum","Std_Dev"]].T

        for _, row in pivot.iterrows():
            winner = row.idxmax()
            score[winner] = score.get(winner, 0) + 1

    if len(score) == 0:
        return None, None

    winner = max(score, key=score.get)
    return winner, score[winner]

def highlight_winner_column(df, winner):
    def style(col):
        if col.name == winner:
            return ['background-color: #00FF7F'] * len(col)
        return [''] * len(col)
    return df.style.apply(style, axis=0).format("{:.2f}")

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------
st.title("📊 Mutual Fund Analytics Dashboard")

# --------------------------------------------------
# DATE FILTER
# --------------------------------------------------
st.sidebar.header("📅 Investment Period")
start_date = st.sidebar.date_input("Start Date", date(2015,1,1))
end_date = st.sidebar.date_input("End Date", date.today())

# =========================================================
# 🚀 ROLLING RETURNS COMPARISON
# =========================================================
selected_scheme = st.multiselect(
    "🔎 Select funds to compare",
    list(scheme_names.keys())
)

if st.button("🚀 Compare Funds"):

    if len(selected_scheme) == 0:
        st.warning("Select at least one fund")
        st.stop()

    all_results = []
    progress = st.progress(0)

    for i, scheme_name in enumerate(selected_scheme):
        code = scheme_names[scheme_name]
        data = requests.get(f"{API}/scheme/{code}").json()

        if isinstance(data, dict) and "error" in data:
            st.warning(f"{scheme_name} → Not enough history")
            continue

        df = pd.DataFrame(data)
        all_results.append(df)
        progress.progress((i+1)/len(selected_scheme))

    final_df = pd.concat(all_results, ignore_index=True)
    winner_fund, win_count = find_winner(final_df)

    st.header("📊 Rolling Return Comparison")
    periods = final_df["Period"].unique()

    for period in periods:
        st.subheader(period)
        temp = final_df[final_df["Period"] == period]
        pivot = temp.set_index("Scheme_Name")[["Last_Value","Average","Median","Maximum","Minimum","Std_Dev"]].T

        styled = highlight_winner_column(pivot, winner_fund) if winner_fund else pivot.style
        st.dataframe(styled, use_container_width=True)

    # Distribution tables
    st.header("📈 Rolling Return Distribution %")
    for period in periods:
        st.subheader(f"Distribution → {period}")
        temp = final_df[final_df["Period"] == period]
        dist = temp.set_index("Scheme_Name")[["Pct_0_8","Pct_8_12","Pct_12_15","Pct_15_20","Pct_Greater_20"]].T
        styled = highlight_winner_column(dist, winner_fund) if winner_fund else dist.style
        st.dataframe(styled, use_container_width=True)

    if winner_fund:
        st.success(f"🏆 Overall Best Fund: {winner_fund} (won {win_count} metrics)")

# =========================================================
# 💰 LUMPSUM CALCULATOR + YEARLY CHART
# =========================================================
st.header("💰 Lumpsum Calculator")

lump_scheme = st.selectbox("Select fund", list(scheme_names.keys()), key="lump")
lump_amount = st.number_input("Investment Amount", 1000, 10000000, 100000)

if st.button("Calculate Lumpsum"):

    code = scheme_names[lump_scheme]

    url = f"{API}/lumpsum/{code}?amount={lump_amount}&start={start_date}&end={end_date}"
    result = requests.get(url).json()

    if "error" in result:
        st.error(result["error"])
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Invested", f"₹{result['Invested_Amount']:,.0f}")
        c2.metric("Final Value", f"₹{result['Final_Value']:,.0f}")
        c3.metric("CAGR", f"{result['CAGR %']} %")

        # 🎯 YEARLY CHART
        st.subheader("📈 Year-wise Growth")
        yearly = requests.get(
            f"{API}/lumpsum_yearly/{code}?amount={lump_amount}&start_date={start_date}&end_date={end_date}"
        ).json()

        if isinstance(yearly, list) and len(yearly) > 0:
            df = pd.DataFrame(yearly)

            fig = px.bar(
                df,
                x="Year",
                y="portfolio_value",
                text="portfolio_value",
                title="Year-wise Lumpsum Growth"
            )

            fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            fig.update_layout(
                yaxis_title="Portfolio Value",
                xaxis_title="Year"
            )

            st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 📅 SIP CALCULATOR + YEARLY CHART
# =========================================================
st.header("📅 SIP Calculator")

sip_scheme = st.selectbox("Select fund ", list(scheme_names.keys()), key="sip")
sip_amount = st.number_input("Monthly SIP", 500, 100000, 5000)

if st.button("Calculate SIP"):

    code = scheme_names[sip_scheme]

    url = f"{API}/sip/{code}?monthly={sip_amount}&start={start_date}&end={end_date}"
    result = requests.get(url).json()

    if "error" in result:
        st.error(result["error"])
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Invested", f"₹{result['Invested_Amount']:,.0f}")
        c2.metric("Final Value", f"₹{result['Final_Value']:,.0f}")
        c3.metric("CAGR", f"{result['CAGR %']} %")

        # 🎯 YEARLY CHART
        st.subheader("📈 Year-wise Growth")
        yearly = requests.get(
            f"{API}/sip_yearly/{code}?monthly_amount={sip_amount}&start_date={start_date}&end_date={end_date}"
        ).json()

        if isinstance(yearly, list) and len(yearly) > 0:
            df = pd.DataFrame(yearly)

            fig = px.bar(
                df,
                x="Year",
                y="value",  # ⭐ FIXED HERE
                text="value",
                title="Year-wise SIP Growth"
            )

            fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            fig.update_layout(
                yaxis_title="Portfolio Value",
                xaxis_title="Year"
            )

            st.plotly_chart(fig, use_container_width=True)





