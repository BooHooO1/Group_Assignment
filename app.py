# app.py
# code snippet assisted by ChatGPT

import streamlit as st
import pandas as pd
import altair as alt

st.title("Deadlier Than Expected: Clinic 1’s Shocking Numbers")

st.markdown(
    """
In the early 1840s, Dr. Ignaz Semmelweis noticed that **Clinic 1** had far more maternal deaths
than **Clinic 2**, even though both clinics were part of the same hospital.

Use the slider below to explore how deadly each clinic was across different year ranges.
"""
)

# ---------- LOAD & PREP DATA ----------
df = pd.read_csv("yearly_deaths_by_clinic.csv")

# Rename columns to simpler lowercase names
df = df.rename(columns={
    "Year": "year",
    "Birth": "births",
    "Deaths": "deaths",
    "Clinic": "clinic"
})

# Calculate mortality rate
df["mortality_rate"] = df["deaths"] / df["births"]

# ---------- YEAR SLIDER FILTER ----------
# find min and max years from the data
min_year = int(df["year"].min())
max_year = int(df["year"].max())

# slider lets user choose any range between min and max
year_range = st.slider(
    "Select year range:",
    min_value=min_year,
    max_value=max_year,
    value=(1841, 1846)  # default range you used before
)

# filter dataframe based on slider selection
filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# show filtered raw data
st.subheader(f"Yearly Data for Selected Range: {year_range[0]}–{year_range[1]}")
st.dataframe(filtered)

# ---------- BAR CHART: AVERAGE MORTALITY RATE BY CLINIC ----------
st.markdown(
    "<h3 style='font-size:20px; font-weight:600;'>Clinic 1 vs Clinic 2: How Deadly Were They?</h3>",
    unsafe_allow_html=True
)

# group by clinic within the selected year range
clinic_summary = (
    filtered
    .groupby("clinic", as_index=False)
    .agg(
        total_births=("births", "sum"),
        total_deaths=("deaths", "sum")
    )
)

clinic_summary["mortality_rate"] = (
    clinic_summary["total_deaths"] / clinic_summary["total_births"]
)

bar_chart = (
    alt.Chart(clinic_summary)
    .mark_bar()
    .encode(
        x=alt.X("clinic:N", title="Clinic"),
        y=alt.Y("mortality_rate:Q",
                title="Average mortality rate (deaths / births)"),
        tooltip=["clinic", "total_births", "total_deaths", "mortality_rate"]
    )
    .properties(height=400)
)

st.altair_chart(bar_chart, use_container_width=True)

# ---------- LINE CHART: DEATHS OVER TIME ----------
st.subheader("Deaths Over Time in Selected Years")

line_chart = (
    alt.Chart(filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("deaths:Q", title="Number of deaths"),
        color=alt.Color("clinic:N", title="Clinic"),
        tooltip=["year", "clinic", "births", "deaths", "mortality_rate"]
    )
    .properties(height=400)
)

st.altair_chart(line_chart, use_container_width=True)

# ---------- EXPLANATION / FINDINGS ----------
st.markdown(
    """
### What do we learn from this?

- For most year ranges, **Clinic 1** shows a **higher mortality rate** than **Clinic 2**.
- This is striking because both clinics served similar patients, but **Clinic 1** had doctors
  who often moved from autopsies straight to deliveries **without washing their hands**.
- The ability to slide across years helps us see that this pattern is **not** just one bad year,
  but a consistent problem that Semmelweis used as evidence for **hand hygiene**.
"""
)
