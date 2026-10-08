# CSV Data Cleaning Tool

A Python-based data cleaning tool built with **Pandas** to clean, standardize, validate, and prepare CSV datasets for analysis.

This project simulates a common data analyst workflow where raw employee data contains missing values, duplicate records, inconsistent text formatting, invalid numerical values, and inconsistent salary formats.


## Project Overview

Raw datasets are rarely ready for analysis.

Before building dashboards or performing analysis, data needs to be checked for quality issues such as:

- Missing values
- Duplicate records
- Inconsistent text formatting
- Invalid numerical values
- Inconsistent salary formats
- Data quality issues that require investigation

This project automates several of these cleaning steps and saves the cleaned dataset as a new CSV file.


## Objectives

The tool was built to:

1. Load data from a CSV file
2. Identify missing values and affected records
3. Detect and remove exact duplicate records
4. Identify duplicate email addresses for review
5. Standardize names, emails, departments, and cities
6. Standardize salary values from different formats
7. Validate numerical values such as age and salary
8. Handle missing and invalid values
9. Add data-quality investigation flags
10. Export the cleaned dataset to a new CSV file


## Project Structure

```text
csv-data-cleaning-tool/
│
├── data/
│   ├── dirty_data.csv
│   └── cleaned_data.csv
│
├── src/
│   └── data_cleaner.py
│
└── README.md
````

## Technologies Used

* Python
* Pandas


## Data Cleaning Workflow

```text
Raw CSV Data
      ↓
Load Dataset
      ↓
Inspect Missing Values
      ↓
Remove Exact Duplicates
      ↓
Identify Duplicate Emails
      ↓
Standardize Text
      ↓
Standardize Salary Formats
      ↓
Validate Numerical Values
      ↓
Handle Missing / Invalid Values
      ↓
Final Data Quality Checks
      ↓
Export Cleaned CSV
```

## Key Cleaning Operations

### 1. Missing Data

The tool identifies missing values at both the column and row level.

It reports:

* Number of missing values per column
* Number of records containing missing data
* The affected records


### 2. Duplicate Records

The tool checks for:

* Exact duplicate rows
* Duplicate email addresses

Exact duplicate rows are automatically removed.

Duplicate email records are displayed for investigation rather than automatically deleted because the records may represent legitimate cases that require business review.


### 3. Text Standardization

Different text fields are standardized according to their purpose.

Examples include:

| Field              | Standardization     |
| ------------------ | ------------------- |
| Name               | Title Case          |
| Email              | Lowercase           |
| Department         | Uppercase           |
| City               | Title Case          |
| City abbreviations | Standard city names |

Example:

```text
john DOE              → John Doe
 JOHNDOE@EMAIL.COM    → johndoe@email.com
sales                 → SALES
ph                    → Philadelphia
```


### 4. Salary Standardization

The tool handles different salary representations such as:

```text
$50,000
50000
50k
```

These values are converted into consistent numerical values.

Invalid salary values are converted to missing values so they can be handled during the cleaning process.


### 5. Numerical Validation

Numerical fields are checked against reasonable business rules.

For example:

* Age should fall within a defined range.
* Salary should not be negative.

Invalid values are identified and treated as missing rather than being silently accepted.


### 6. Missing Value Handling

Different fields require different approaches.

| Column     | Approach                              |
| ---------- | ------------------------------------- |
| City       | Replace missing values with `Unknown` |
| Department | Use the most frequent value           |
| Salary     | Use the median salary                 |
| Name       | Flag for investigation                |
| Email      | Flag for investigation                |

The approach depends on the role of the column and whether replacing the value would introduce misleading information.


## Data Quality Flags

The tool creates an `Investigation_Flag` column to identify records requiring attention.

Examples include:

```text
OK
Missing Name
Missing Email
Missing Both
```

This allows potentially important records to be identified rather than silently changing critical information.


## Output

The cleaned dataset is exported to:

```text
data/cleaned_data.csv
```

The original raw dataset is preserved separately so that the cleaning process does not overwrite the source data.


## What I Learned

This project helped me practice several important data analyst skills:

* Working with CSV files using Pandas
* Detecting missing data
* Working with boolean conditions
* Removing duplicate records
* Standardizing categorical and text data
* Converting messy numerical data
* Validating data against business rules
* Handling missing values
* Thinking about when data should be corrected automatically versus flagged for investigation

One of the main lessons from this project is that **data cleaning is not simply about changing values**.

A good cleaning process should also preserve the context of the original data and identify records that require human or business review.


## Future Improvements

Planned improvements include:

* [ ] More robust multi-issue data-quality flags
* [ ] More comprehensive validation rules
* [ ] Cleaning summary report
* [ ] Configurable validation rules
* [ ] Command-line arguments for input and output files
* [ ] Logging of cleaning activities
* [ ] Unit tests
* [ ] Support for larger datasets


## Author

**Felix Asibor**

Data Analyst | Python | SQL | Power BI | Excel

This project is part of my data analytics portfolio and demonstrates practical data cleaning and data quality techniques using Python and Pandas.


