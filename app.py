import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Streamlit Page Config ---
st.set_page_config(page_title="India Population Insights", layout="centered")

# --- Title Section ---
st.title("🇮🇳 India's Population Insights Dashboard")
st.markdown("This dashboard helps you explore population data by **year** and **age distribution**.")

# --- Section 1: Load year-wise population data ---
df = pd.read_csv("india_population_yearwise.csv")

# Dropdown for year
selected_year = st.selectbox("📅 Select a year:", sorted(df["Year"].unique()))

# Filter selected year
row = df[df["Year"] == selected_year].iloc[0]
population = row["Value"]

# Display results
st.subheader(f"🗓️ Year: {selected_year}")
st.success(f"📈 India's population in **{selected_year}** was **{population:,}** people.")

# Interpretation
st.markdown(f"""
India's population has experienced consistent growth over the decades.
In **{selected_year}**, the estimated population was approximately **{population:,}**.
This rise can be attributed to improvements in healthcare, education, and infrastructure.
""")

# --- Section 2: Dynamic Age Group Distribution ---
st.markdown("## 👶🧑👵 Age Group Distribution (Estimated for Selected Year)")

# Estimate percentages by year range
def get_age_group_percentages(year):
    if year <= 1979:
        return 0.45, 0.50, 0.05
    elif year <= 1999:
        return 0.42, 0.53, 0.05
    elif year <= 2010:
        return 0.38, 0.56, 0.06
    else:
        return 0.36, 0.57, 0.07

# Get percentages for the selected year
p_young, p_adult, p_old = get_age_group_percentages(selected_year)
pop_million = population / 1_000_000
age_group_values = [
    round(pop_million * p_young, 1),
    round(pop_million * p_adult, 1),
    round(pop_million * p_old, 1)
]

# Plot dynamic horizontal bar
age_groups = ["0–20 Years", "21–64 Years", "65+ Years"]
colors = ['#FFE600', '#1E90FF', '#FF69B4']

fig1, ax1 = plt.subplots(figsize=(8, 3.5))
ax1.barh(age_groups, age_group_values, color=colors)

for i, v in enumerate(age_group_values):
    ax1.text(v + 10, i, f"{v} Mn", va='center', fontsize=10, fontweight='bold')

ax1.set_xlabel("Estimated Population (in Millions)")
ax1.set_title(f"India's Age Group Distribution in {selected_year}")
st.pyplot(fig1)

# --- Section 3: Line Chart of Total Population Over Years ---
st.markdown("## 📈 India's Population Growth Over the Years")
st.line_chart(df.set_index("Year")["Value"])

# --- Section 4: Smooth Shape Distribution (Dummy Curve) ---
st.markdown("## 🌊 Estimated Age Distribution Curve (Shape Only)")

ages = np.arange(0, 101, 1)
population_curve = (
    np.piecewise(
        ages,
        [ages <= 20, (ages > 20) & (ages <= 64), ages > 64],
        [lambda x: 25 - 0.3 * abs(x - 15),
         lambda x: 30 - 0.4 * abs(x - 30),
         lambda x: 10 - 0.2 * abs(x - 70)]
    )
)
population_curve = np.clip(population_curve, 0, None)

fig2, ax2 = plt.subplots(figsize=(10, 4.5))
ax2.fill_between(ages, population_curve, color='skyblue', alpha=0.8)
ax2.axvline(x=28, color='black', linestyle='--', label='Median Age = 28')
ax2.set_xlabel("Age")
ax2.set_ylabel("Relative Population (Shape Only)")
ax2.set_title("India's Age Distribution Curve (Estimated)")
ax2.legend()
st.pyplot(fig2)
