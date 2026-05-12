"""
hr_visualizations.py
--------------------
Generates 12 publication-quality charts from the HR dataset and saves them
as PNG files under the outputs/ directory.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_FILE = os.path.join("data", "employees.csv")
OUTPUT_DIR = "outputs"
FIGSIZE = (10, 6)

# Consistent colour palette
PALETTE = "Set2"
sns.set_theme(style="whitegrid", palette=PALETTE, font_scale=1.1)


def _save(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✅  Saved → {path}")


# ---------------------------------------------------------------------------
# Chart functions
# ---------------------------------------------------------------------------

def chart_01_department_headcount(df):
    """Bar chart of employee count per department."""
    counts = df["department"].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    colors = sns.color_palette(PALETTE, n_colors=len(counts))
    bars = ax.bar(counts.index, counts.values, color=colors)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                str(int(bar.get_height())), ha="center", va="bottom", fontweight="bold")
    ax.set_title("Employee Headcount by Department", fontsize=14, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Number of Employees")
    _save(fig, "department_headcount.png")


def chart_02_salary_distribution(df):
    """Histogram of salary with KDE and mean line."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.histplot(df["salary"], kde=True, bins=30, ax=ax, color="steelblue")
    mean_sal = df["salary"].mean()
    ax.axvline(mean_sal, color="red", linestyle="--", linewidth=2)
    ax.text(mean_sal + 1000, ax.get_ylim()[1] * 0.9,
            f"Mean: ${mean_sal:,.0f}", color="red", fontweight="bold")
    ax.set_title("Salary Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Salary ($)")
    ax.set_ylabel("Frequency")
    _save(fig, "salary_distribution.png")


def chart_03_salary_boxplot(df):
    """Boxplot of salary by department."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.boxplot(x="department", y="salary", data=df, ax=ax, palette=PALETTE)
    ax.set_title("Salary Distribution by Department", fontsize=14, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Salary ($)")
    plt.xticks(rotation=45, ha="right")
    _save(fig, "salary_boxplot.png")


def chart_04_performance_distribution(df):
    """Count plot of performance rating categories."""
    order = ["Poor", "Average", "Good", "Excellent"]
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.countplot(x="performance_rating", data=df, order=order, ax=ax, palette="RdYlGn")
    ax.set_title("Performance Rating Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Performance Rating")
    ax.set_ylabel("Count")
    _save(fig, "performance_distribution.png")


def chart_05_top_performers(df):
    """Average performance score per department (sorted desc)."""
    avg = df.groupby("department")["performance_score"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    colors = sns.color_palette("viridis", n_colors=len(avg))
    ax.barh(avg.index, avg.values, color=colors)
    ax.set_title("Avg Performance Score by Department", fontsize=14, fontweight="bold")
    ax.set_xlabel("Average Performance Score")
    ax.set_ylabel("Department")
    ax.invert_yaxis()
    _save(fig, "top_performers.png")


def chart_06_salary_by_dept_rating(df):
    """Grouped bar chart: department vs avg salary by performance rating."""
    fig, ax = plt.subplots(figsize=(12, 6))
    order = ["Poor", "Average", "Good", "Excellent"]
    pivot = df.pivot_table(values="salary", index="department",
                           columns="performance_rating", aggfunc="mean")
    pivot = pivot.reindex(columns=order)
    pivot.plot(kind="bar", ax=ax, colormap="RdYlGn")
    ax.set_title("Avg Salary by Department & Performance Rating", fontsize=14, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Salary ($)")
    plt.xticks(rotation=45, ha="right")
    ax.legend(title="Rating")
    _save(fig, "salary_by_dept_rating.png")


def chart_07_attrition_by_department(df):
    """Stacked bar chart of attrition risk per department."""
    ct = pd.crosstab(df["department"], df["attrition_risk"])
    ct = ct.reindex(columns=["High", "Medium", "Low"])
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ct.plot(kind="bar", stacked=True, ax=ax, color=["#e74c3c", "#f39c12", "#2ecc71"])
    ax.set_title("Attrition Risk by Department", fontsize=14, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Employee Count")
    plt.xticks(rotation=45, ha="right")
    ax.legend(title="Attrition Risk")
    _save(fig, "attrition_by_department.png")


def chart_08_attrition_by_satisfaction(df):
    """Boxplot of satisfaction score by attrition risk."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    order = ["High", "Medium", "Low"]
    sns.boxplot(x="attrition_risk", y="satisfaction_score", data=df,
                order=order, ax=ax, palette=["#e74c3c", "#f39c12", "#2ecc71"])
    ax.set_title("Satisfaction Score by Attrition Risk", fontsize=14, fontweight="bold")
    ax.set_xlabel("Attrition Risk")
    ax.set_ylabel("Satisfaction Score")
    _save(fig, "attrition_by_satisfaction.png")


def chart_09_satisfaction_vs_performance(df):
    """Scatter plot: satisfaction vs performance coloured by attrition risk."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    palette = {"High": "#e74c3c", "Medium": "#f39c12", "Low": "#2ecc71"}
    sns.scatterplot(x="satisfaction_score", y="performance_score", hue="attrition_risk",
                    data=df, ax=ax, palette=palette, alpha=0.7)
    ax.set_title("Satisfaction vs Performance", fontsize=14, fontweight="bold")
    ax.set_xlabel("Satisfaction Score")
    ax.set_ylabel("Performance Score")
    ax.legend(title="Attrition Risk")
    _save(fig, "satisfaction_vs_performance.png")


def chart_10_gender_pay_gap(df):
    """Grouped bar chart: avg salary by department and gender."""
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot = df.pivot_table(values="salary", index="department",
                           columns="gender", aggfunc="mean")
    pivot.plot(kind="bar", ax=ax, color=["#3498db", "#e91e63"])
    ax.set_title("Average Salary by Department & Gender", fontsize=14, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Salary ($)")
    plt.xticks(rotation=45, ha="right")
    ax.legend(title="Gender")
    _save(fig, "gender_pay_gap.png")


def chart_11_promotion_eligibility(df):
    """Pie chart of promotion eligibility."""
    counts = df["promotion_eligible"].value_counts()
    labels = ["Not Eligible", "Eligible"] if counts.index[0] == False else ["Eligible", "Not Eligible"]
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ["#e74c3c", "#2ecc71"] if counts.index[0] == False else ["#2ecc71", "#e74c3c"]
    ax.pie(counts.values, labels=labels, autopct="%1.1f%%", startangle=140,
           colors=colors, textprops={"fontsize": 12})
    ax.set_title("Promotion Eligibility", fontsize=14, fontweight="bold")
    _save(fig, "promotion_eligibility.png")


def chart_12_attrition_risk_heatmap(df):
    """Heatmap: department vs attrition risk (employee count)."""
    ct = pd.crosstab(df["department"], df["attrition_risk"])
    ct = ct.reindex(columns=["High", "Medium", "Low"])
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.heatmap(ct, annot=True, fmt="d", cmap="YlOrRd", linewidths=0.5, ax=ax)
    ax.set_title("Attrition Risk Heatmap by Department", fontsize=14, fontweight="bold")
    ax.set_xlabel("Attrition Risk")
    ax.set_ylabel("Department")
    _save(fig, "attrition_risk_map.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_all_charts():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📂  Loading data from {DATA_FILE} …")
    df = pd.read_csv(DATA_FILE)
    print(f"✅  Loaded {len(df)} rows.\n")
    print("📊  Generating charts …\n")

    chart_01_department_headcount(df)
    chart_02_salary_distribution(df)
    chart_03_salary_boxplot(df)
    chart_04_performance_distribution(df)
    chart_05_top_performers(df)
    chart_06_salary_by_dept_rating(df)
    chart_07_attrition_by_department(df)
    chart_08_attrition_by_satisfaction(df)
    chart_09_satisfaction_vs_performance(df)
    chart_10_gender_pay_gap(df)
    chart_11_promotion_eligibility(df)
    chart_12_attrition_risk_heatmap(df)

    print("\n🎉  All 12 charts generated successfully!")


if __name__ == "__main__":
    generate_all_charts()
