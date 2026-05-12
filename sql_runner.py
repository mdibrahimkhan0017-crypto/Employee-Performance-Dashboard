"""
sql_runner.py
-------------
Loads data/employees.csv into an in-memory SQLite database, executes all 12
HR analytics SQL queries from sql/hr_queries.sql, and saves each result set
as a CSV file under outputs/sql_results/.
"""

import os
import re
import sqlite3
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CSV_INPUT = os.path.join("data", "employees.csv")
SQL_FILE = os.path.join("sql", "hr_queries.sql")
OUTPUT_DIR = os.path.join("outputs", "sql_results")

# Mapping of query numbers to descriptive output filenames
QUERY_FILE_MAP = {
    1:  "query_01_salary_rank.csv",
    2:  "query_02_performance_rank.csv",
    3:  "query_03_top3_performers.csv",
    4:  "query_04_salary_percentile.csv",
    5:  "query_05_performance_quartile.csv",
    6:  "query_06_top_performer.csv",
    7:  "query_07_lowest_performer.csv",
    8:  "query_08_previous_month_hires.csv",
    9:  "query_09_next_month_hires.csv",
    10: "query_10_running_total_hires.csv",
    11: "query_11_moving_average_hires.csv",
    12: "query_12_department_salary_comparison.csv",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_queries(sql_text):
    """
    Split the SQL file into individual queries using the
    ``-- Query XX: <title>`` comment headers as delimiters.

    Returns a list of (query_number, title, sql) tuples.
    """
    header_pattern = re.compile(
        r"^--\s*Query\s+(\d+)\s*:\s*(.+)$", re.MULTILINE
    )

    headers = list(header_pattern.finditer(sql_text))
    queries = []

    for idx, match in enumerate(headers):
        query_num = int(match.group(1))
        title = match.group(2).strip()

        start = match.end()
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(sql_text)

        raw_sql = sql_text[start:end].strip()
        sql_lines = [
            line for line in raw_sql.splitlines()
            if not header_pattern.match(line)
        ]
        clean_sql = "\n".join(sql_lines).strip().rstrip(";")

        if clean_sql:
            queries.append((query_num, title, clean_sql))

    return queries


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_queries():
    """Execute all queries and persist results as CSV files."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Loading data from {CSV_INPUT}")
    df = pd.read_csv(CSV_INPUT)
    conn = sqlite3.connect(":memory:")
    df.to_sql("employees", conn, index=False, if_exists="replace")
    print(f"Loaded {len(df)} rows into SQLite table 'employees'.\n")

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_text = f.read()

    queries = _parse_queries(sql_text)
    print(f"Found {len(queries)} queries to execute.\n")

    success_count = 0
    fail_count = 0

    for query_num, title, sql in queries:
        filename = QUERY_FILE_MAP.get(query_num, f"query_{query_num:02d}.csv")
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            result = pd.read_sql_query(sql, conn)
            result.to_csv(output_path, index=False)
            print(f"  Query {query_num:02d}: {title}  ->  {output_path}  ({len(result)} rows)")
            success_count += 1
        except Exception as exc:
            print(f"  Query {query_num:02d}: {title}  ->  FAILED - {exc}")
            fail_count += 1

    conn.close()
    print(f"\n{'=' * 60}")
    print(f"Results: {success_count} succeeded, {fail_count} failed.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run_queries()
