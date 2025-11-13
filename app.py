import streamlit as st
import pandas as pd
import altair as alt

# ---------- TITLE & INTRO ----------
st.title("Deadlier Than Expected: Clinic 1’s Shocking Numbers")

st.markdown(
    """
In the early 1840s, Dr. Ignaz Semmelweis noticed that **Clinic 1** had far more maternal deaths
than **Clinic 2**, even though both clinics were part of the same hospital.

This app focuses on the years **1841–1846**, before handwashing was introduced, to show how
dangerous unsanitary medical routines were for mothers.
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

# Focus only on the years 1841–1846 (before handwashing)
pre_handwashing = df[(df["year"] >= 1841) & (df["year"] <= 1846)]

st.subheader("Raw Data: 1841–1846 (Before Handwashing)")
st.dataframe(pre_handwashing)

# ---------- BAR CHART: MORTALITY RATE BY CLINIC ----------
st.subheader("Average Mortality Rate by Clinic (1841–1846)")

clinic_summary = (
    pre_handwashing
    .groupby("clinic", as_index=False)
    .agg(
        total_births=("births", "sum"),
        total_deaths=("deaths", "sum")
    )
)

clinic_summary["mortality_rate"] = (
    clinic_summary["total_deaths"] / clinic_summary["total_births"]
)

st.subheader("Clinic 1 vs Clinic 2: How Deadly Were They?")

bar_chart = (
    alt.Chart(clinic_summary)
    .mark_bar()
    .encode(
        x=alt.X("clinic:N", title="Clinic"),
        y=alt.Y("mortality_rate:Q", title="Average mortality rate (deaths / births)"),
        tooltip=["clinic", "total_births", "total_deaths", "mortality_rate"]
    )
    .properties(height=400)  # optional, gives it some breathing room
)

st.altair_chart(bar_chart, use_container_width=True)

# ---------- LINE CHART: DEATHS OVER TIME ----------
st.subheader("Deaths Over Time (1841–1846)")

line_chart = (
    alt.Chart(pre_handwashing)
    .mark_line(point=True)
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("deaths:Q", title="Number of deaths"),
        color=alt.Color("clinic:N", title="Clinic"),
        tooltip=["year", "clinic", "births", "deaths", "mortality_rate"]
    )
    .properties(title="Yearly Deaths in Clinic 1 vs Clinic 2")
)

st.altair_chart(line_chart, use_container_width=True)
