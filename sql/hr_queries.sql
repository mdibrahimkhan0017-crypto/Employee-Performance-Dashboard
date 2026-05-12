-- =============================================================================
-- HR Analytics — SQL Window Function Queries (SQLite)
-- Table: employees
-- =============================================================================

-- Query 01: Salary Rank by Department
-- Assigns a unique sequential rank to each employee within their department
-- based on salary (highest first) using ROW_NUMBER().
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees
ORDER BY department, salary_rank;

-- Query 02: Performance Rank by Department
-- Ranks employees within each department by performance_score (highest first).
-- Employees with the same score receive the same rank; the next rank is skipped.
SELECT
    employee_id,
    employee_name,
    department,
    performance_score,
    performance_rating,
    RANK() OVER (
        PARTITION BY department
        ORDER BY performance_score DESC
    ) AS performance_rank
FROM employees
ORDER BY department, performance_rank;

-- Query 03: Top 3 Performers per Department
-- Uses DENSE_RANK() so that tied scores share the same rank and no ranks are
-- skipped. Only the top-3 dense ranks per department are returned.
SELECT *
FROM (
    SELECT
        employee_id,
        employee_name,
        department,
        performance_score,
        performance_rating,
        DENSE_RANK() OVER (
            PARTITION BY department
            ORDER BY performance_score DESC
        ) AS dense_rank
    FROM employees
)
WHERE dense_rank <= 3
ORDER BY department, dense_rank;

-- Query 04: Salary Percentile per Employee
-- Calculates the relative standing of each employee's salary within their
-- department using PERCENT_RANK() (0 = lowest, 1 = highest).
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    ROUND(
        PERCENT_RANK() OVER (
            PARTITION BY department
            ORDER BY salary
        ), 4
    ) AS salary_percentile
FROM employees
ORDER BY department, salary_percentile DESC;

-- Query 05: Performance Quartile
-- Splits employees into four roughly equal groups (quartiles) based on their
-- performance_score using NTILE(4).
SELECT
    employee_id,
    employee_name,
    department,
    performance_score,
    NTILE(4) OVER (
        ORDER BY performance_score
    ) AS performance_quartile
FROM employees
ORDER BY performance_quartile, performance_score;

-- Query 06: Top Performer per Department
-- Returns the name and score of the highest-performing employee in each
-- department using FIRST_VALUE().
SELECT DISTINCT
    department,
    FIRST_VALUE(employee_name) OVER (
        PARTITION BY department
        ORDER BY performance_score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS top_performer_name,
    FIRST_VALUE(performance_score) OVER (
        PARTITION BY department
        ORDER BY performance_score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS top_performer_score
FROM employees
ORDER BY department;

-- Query 07: Lowest Performer per Department
-- Returns the name and score of the lowest-performing employee in each
-- department using LAST_VALUE() with a full window frame.
SELECT DISTINCT
    department,
    LAST_VALUE(employee_name) OVER (
        PARTITION BY department
        ORDER BY performance_score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_performer_name,
    LAST_VALUE(performance_score) OVER (
        PARTITION BY department
        ORDER BY performance_score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_performer_score
FROM employees
ORDER BY department;

-- Query 08: Previous Month Hire Count
-- Aggregates hires by month and uses LAG() to show the previous month's
-- hire count alongside the current month.
SELECT
    hire_month,
    hire_count,
    LAG(hire_count, 1, 0) OVER (ORDER BY hire_month) AS prev_month_hires
FROM (
    SELECT
        strftime('%Y-%m', hire_date) AS hire_month,
        COUNT(*) AS hire_count
    FROM employees
    GROUP BY strftime('%Y-%m', hire_date)
)
ORDER BY hire_month;

-- Query 09: Next Month Hire Count
-- Aggregates hires by month and uses LEAD() to show the next month's
-- hire count alongside the current month.
SELECT
    hire_month,
    hire_count,
    LEAD(hire_count, 1, 0) OVER (ORDER BY hire_month) AS next_month_hires
FROM (
    SELECT
        strftime('%Y-%m', hire_date) AS hire_month,
        COUNT(*) AS hire_count
    FROM employees
    GROUP BY strftime('%Y-%m', hire_date)
)
ORDER BY hire_month;

-- Query 10: Running Total of Hires Over Time
-- Computes a cumulative (running) total of hires ordered chronologically
-- using SUM() OVER().
SELECT
    hire_month,
    hire_count,
    SUM(hire_count) OVER (
        ORDER BY hire_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_hires
FROM (
    SELECT
        strftime('%Y-%m', hire_date) AS hire_month,
        COUNT(*) AS hire_count
    FROM employees
    GROUP BY strftime('%Y-%m', hire_date)
)
ORDER BY hire_month;

-- Query 11: 3-Month Moving Average of Hires
-- Calculates a rolling 3-month average of monthly hire counts using
-- AVG() OVER() with a 3-row window.
SELECT
    hire_month,
    hire_count,
    ROUND(
        AVG(hire_count) OVER (
            ORDER BY hire_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2
    ) AS moving_avg_3m
FROM (
    SELECT
        strftime('%Y-%m', hire_date) AS hire_month,
        COUNT(*) AS hire_count
    FROM employees
    GROUP BY strftime('%Y-%m', hire_date)
)
ORDER BY hire_month;

-- Query 12: Department-Level Average Salary Comparison
-- Shows each employee's salary alongside their department's average salary,
-- the overall average salary, and the difference from the department average.
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS dept_avg_salary,
    ROUND(AVG(salary) OVER (), 2) AS overall_avg_salary,
    ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS diff_from_dept_avg
FROM employees
ORDER BY department, salary DESC;
