"""
generate_hr_data.py
-------------------
Generates a synthetic HR dataset with 1,000 employee records using Faker and
NumPy.  The output CSV is saved to data/employees.csv.
"""

import os
import numpy as np
import pandas as pd
from faker import Faker

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SEED = 42
NUM_EMPLOYEES = 1000
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "employees.csv")

DEPARTMENTS = [
    "Engineering", "Marketing", "Sales", "HR",
    "Finance", "Operations", "IT", "Legal",
]

# Salary ranges per department (min, max)
SALARY_RANGES = {
    "Engineering": (70000, 150000),
    "Marketing":   (45000, 120000),
    "Sales":       (40000, 130000),
    "HR":          (40000, 100000),
    "Finance":     (55000, 140000),
    "Operations":  (35000, 95000),
    "IT":          (60000, 145000),
    "Legal":       (55000, 135000),
}

JOB_ROLES = {
    "Engineering": ["Software Engineer", "Data Engineer", "DevOps Engineer", "ML Engineer", "QA Engineer"],
    "Marketing":   ["Marketing Analyst", "Content Strategist", "SEO Specialist", "Brand Manager", "Campaign Lead"],
    "Sales":       ["Account Executive", "Sales Manager", "BDR", "Sales Analyst", "Regional Lead"],
    "HR":          ["HR Generalist", "Recruiter", "HR Manager", "Compensation Analyst", "Training Lead"],
    "Finance":     ["Financial Analyst", "Accountant", "Controller", "Audit Specialist", "Finance Manager"],
    "Operations":  ["Operations Analyst", "Logistics Coordinator", "Supply Chain Lead", "Process Engineer", "Operations Manager"],
    "IT":          ["System Administrator", "Network Engineer", "IT Support", "Security Analyst", "Cloud Architect"],
    "Legal":       ["Legal Counsel", "Compliance Officer", "Paralegal", "Contract Specialist", "Legal Analyst"],
}

LOCATIONS = [
    "New York", "San Francisco", "Chicago", "Austin", "Seattle",
    "Boston", "Denver", "Atlanta", "Los Angeles", "Miami",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _performance_rating(score: float) -> str:
    """Map a numeric performance score to a categorical rating."""
    if score < 2.0:
        return "Poor"
    elif score < 3.0:
        return "Average"
    elif score < 4.0:
        return "Good"
    else:
        return "Excellent"


def _attrition_risk(satisfaction: float, performance: float) -> str:
    """Derive attrition risk from satisfaction and performance scores."""
    if satisfaction < 2.0 or (satisfaction < 3.0 and performance < 2.5):
        return "High"
    elif satisfaction < 3.5 or performance < 3.0:
        return "Medium"
    else:
        return "Low"


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_hr_data() -> pd.DataFrame:
    """Create and return a DataFrame of synthetic HR data."""
    fake = Faker()
    Faker.seed(SEED)
    np.random.seed(SEED)

    records = []

    for emp_id in range(1, NUM_EMPLOYEES + 1):
        gender = np.random.choice(["Male", "Female"])
        employee_name = (
            fake.name_male() if gender == "Male" else fake.name_female()
        )

        department = np.random.choice(DEPARTMENTS)
        job_role = np.random.choice(JOB_ROLES[department])

        sal_min, sal_max = SALARY_RANGES[department]
        salary = round(np.random.uniform(sal_min, sal_max), 2)

        performance_score = round(np.random.uniform(1.0, 5.0), 2)
        performance_rating = _performance_rating(performance_score)

        satisfaction_score = round(np.random.uniform(1.0, 5.0), 2)

        years_at_company = int(np.random.randint(1, 21))  # 1-20

        last_promotion_year = int(
            np.random.randint(
                max(2005, 2023 - years_at_company), 2024
            )
        )

        promotion_eligible = (
            performance_score > 4.0 and years_at_company >= 3
        )

        attrition_risk = _attrition_risk(satisfaction_score, performance_score)

        hire_date = fake.date_between(
            start_date="-18y", end_date="-1y"
        ).strftime("%Y-%m-%d")

        manager_id = np.random.randint(1001, 1051)  # 50 possible managers

        location = np.random.choice(LOCATIONS)

        records.append(
            {
                "employee_id": emp_id,
                "employee_name": employee_name,
                "gender": gender,
                "department": department,
                "job_role": job_role,
                "salary": salary,
                "performance_score": performance_score,
                "performance_rating": performance_rating,
                "satisfaction_score": satisfaction_score,
                "years_at_company": years_at_company,
                "last_promotion_year": last_promotion_year,
                "promotion_eligible": promotion_eligible,
                "attrition_risk": attrition_risk,
                "hire_date": hire_date,
                "manager_id": manager_id,
                "location": location,
            }
        )

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_hr_data()
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅  Generated {len(df)} employee records → {OUTPUT_FILE}")
