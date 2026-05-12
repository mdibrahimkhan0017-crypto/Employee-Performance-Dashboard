# Employee Performance Dashboard

A comprehensive HR analytics project that generates synthetic employee data, runs advanced SQL window-function queries against it, and produces publication-quality visualisation charts — all from a single command.

---

## Features

- 🗃️ **Synthetic Data Generation** — 1,000 realistic employee records created with Faker & NumPy
- 🔍 **12 SQL Window-Function Queries** — ROW_NUMBER, RANK, DENSE_RANK, PERCENT_RANK, NTILE, FIRST_VALUE, LAST_VALUE, LAG, LEAD, SUM OVER, AVG OVER, PARTITION BY
- 📊 **12 Professional Charts** — Bar, histogram, boxplot, scatter, pie, and heatmap visualisations
- 🗄️ **SQLite In-Memory Database** — No external database setup required
- 📁 **Organised Output** — SQL results as CSVs, charts as PNGs
- 🚀 **One-Command Pipeline** — `python run_all.py` runs everything end-to-end
- 🔄 **Reproducible** — Fixed random seed ensures identical results on every run
- ✅ **Beginner-Friendly** — Clean code with docstrings, comments, and clear folder structure

---

## Folder Structure

```
employee_dashboard/
├── data/
│   └── employees.csv              # Generated dataset
├── outputs/
│   ├── sql_results/               # 12 query result CSVs
│   │   ├── query_01_salary_rank.csv
│   │   ├── query_02_performance_rank.csv
│   │   ├── ...
│   │   └── query_12_department_salary_comparison.csv
│   ├── department_headcount.png
│   ├── salary_distribution.png
│   ├── salary_boxplot.png
│   ├── performance_distribution.png
│   ├── top_performers.png
│   ├── salary_by_dept_rating.png
│   ├── attrition_by_department.png
│   ├── attrition_by_satisfaction.png
│   ├── satisfaction_vs_performance.png
│   ├── gender_pay_gap.png
│   ├── promotion_eligibility.png
│   └── attrition_risk_map.png
├── sql/
│   └── hr_queries.sql             # 12 SQL window-function queries
├── generate_hr_data.py            # Data generation script
├── sql_runner.py                  # SQL execution engine
├── hr_visualizations.py           # Chart generation script
├── run_all.py                     # Master pipeline runner
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Requirements

- **Python** 3.9 or higher
- **Libraries**: pandas, numpy, matplotlib, seaborn, faker
- **Built-in**: sqlite3 (ships with Python)

---

## Setup Instructions

### Windows

```bash
# 1. Create a virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python run_all.py
```

### macOS / Linux

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python run_all.py
```

---

## How to Run

```bash
python run_all.py
```

This single command will:

1. **Generate** 1,000 synthetic employee records → `data/employees.csv`
2. **Execute** 12 SQL window-function queries → `outputs/sql_results/*.csv`
3. **Create** 12 visualisation charts → `outputs/*.png`

---

## Output Files

### SQL Result CSVs (`outputs/sql_results/`)

| File | Description |
|------|-------------|
| `query_01_salary_rank.csv` | Salary rank within each department |
| `query_02_performance_rank.csv` | Performance rank within each department |
| `query_03_top3_performers.csv` | Top 3 performers per department |
| `query_04_salary_percentile.csv` | Salary percentile per employee |
| `query_05_performance_quartile.csv` | Performance quartile assignment |
| `query_06_top_performer.csv` | Top performer per department |
| `query_07_lowest_performer.csv` | Lowest performer per department |
| `query_08_previous_month_hires.csv` | Previous month hire count (LAG) |
| `query_09_next_month_hires.csv` | Next month hire count (LEAD) |
| `query_10_running_total_hires.csv` | Running total of hires |
| `query_11_moving_average_hires.csv` | 3-month moving average of hires |
| `query_12_department_salary_comparison.csv` | Department-level salary comparison |

### Charts (`outputs/`)

| File | Type |
|------|------|
| `department_headcount.png` | Bar chart |
| `salary_distribution.png` | Histogram + KDE |
| `salary_boxplot.png` | Boxplot |
| `performance_distribution.png` | Count plot |
| `top_performers.png` | Horizontal bar chart |
| `salary_by_dept_rating.png` | Grouped bar chart |
| `attrition_by_department.png` | Stacked bar chart |
| `attrition_by_satisfaction.png` | Boxplot |
| `satisfaction_vs_performance.png` | Scatter plot |
| `gender_pay_gap.png` | Grouped bar chart |
| `promotion_eligibility.png` | Pie chart |
| `attrition_risk_map.png` | Heatmap |

---

## SQL Window Functions Used

| # | Window Function | Purpose |
|---|----------------|---------|
| 1 | `ROW_NUMBER()` | Unique sequential rank per partition |
| 2 | `RANK()` | Rank with gaps for ties |
| 3 | `DENSE_RANK()` | Rank without gaps for ties |
| 4 | `PERCENT_RANK()` | Relative position as a percentage |
| 5 | `NTILE(4)` | Split into quartiles |
| 6 | `FIRST_VALUE()` | First row value in window frame |
| 7 | `LAST_VALUE()` | Last row value in window frame |
| 8 | `LAG()` | Access previous row's value |
| 9 | `LEAD()` | Access next row's value |
| 10 | `SUM() OVER()` | Running total |
| 11 | `AVG() OVER()` | Moving average |
| 12 | `PARTITION BY` | Segment-level aggregation |

---

## Sample Business Insights

This project helps answer questions like:

- Which department has the highest average salary?
- Who are the top 3 performers in each department?
- Is there a correlation between satisfaction and attrition risk?
- Does a gender pay gap exist across departments?
- Which departments have the highest attrition risk?
- How has the hiring trend changed over time?
- What percentage of employees are promotion-eligible?
- How does performance vary across salary quartiles?

---

## Future Enhancements

- 📈 Add an interactive Streamlit or Dash dashboard
- 🤖 Integrate ML models for attrition prediction
- 🗂️ Support PostgreSQL / MySQL backends
- 📬 Automated email reports with charts
- 🧪 Add unit tests for data generation and SQL queries
- 📅 Time-series analysis of hiring and attrition trends

---

> Built with ❤️ using Python, SQLite, Matplotlib & Seaborn
# Employee-Performance-Dashboard
