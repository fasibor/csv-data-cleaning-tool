import pandas as pd

city_map = {
    "Ph": "Philadelphia",
    "Ny": "New York"
}

# ==========================================
# 1. LOAD THE DATA
# ==========================================
raw_data = r"C:\Users\FELIX\Documents\csv-data-cleaning-tool\data\dirty_data.csv"
output_file = r"C:\Users\FELIX\Documents\csv-data-cleaning-tool\data\cleaned_data.csv"

df = pd.read_csv(raw_data, on_bad_lines="skip")
print("Welcome to CSV Data Cleaner")
print("="*40)
print(f"Successfully Loaded: {len(df)} Data")


# ==========================================
# 2. CHECK FOR MISSING DATA
# ==========================================
def missing_values(df):
    print("\nMissing Values")
    print("="*40)

    #Column Level Missing Data
    print("\n Missing Column")
    print("="*20)
    missing_data_column = df.isna().sum()
    print(missing_data_column)

    #Identify rows with NA
    rows_with_NA = df[df.isna().any(axis = 1)]


    #Want to see the total missing rows
    total_missing_rows = df.isna().any(axis = 1).sum()
    print("\nMissing Rows")
    print("="*20)
    print(f"\nRows with Missing Data: {total_missing_rows}")
    print(rows_with_NA)
    return rows_with_NA


# ==========================================
# 3. REMOVE DUPLICATES
# ==========================================
def remove_duplicates(df):
    print("\n Remove Duplicates")
    print("="*40)
    #count exact duplicates
    duplicate_count = df.duplicated().sum()

    #Email based duplicates
    duplicate_count2 = df.duplicated(subset = ["Email"]).sum()
    email_duplicates = df[df.duplicated(subset=["Email"], keep=False)]

    print(f"Number of Exact Duplicates Found: {duplicate_count}")
    print(f"Number of Duplicates Found Via Email: {duplicate_count2}")
    print("\n Records with Duplicate Emails")
    print("="*40)
    print(email_duplicates)

    #remove duplicates
    df = df.drop_duplicates()
    print(f"Exact Duplicates Removed: {duplicate_count}")

    #Flag Email Duplicates
    print(f"Duplicate Emails Flagged: {duplicate_count2}")
    return df




# ==========================================
# 4. STANDARDIZE TEXT
# ==========================================
def standardize_text(df):
    print("\n Stanadardize Text")
    print("="*40)
    #clean names
    df["Name"] = df["Name"].str.strip().str.title()
    #clean emails
    df["Email"] = df["Email"].str.strip().str.lower()

    #clean department
    df["Department"] = df["Department"].str.strip().str.upper()

    #Clean City
    df["City"] = df["City"].str.strip().str.title()
    df["City"] = df["City"].replace(city_map)

    return df

# ==========================================
# 5. STANDARDIZE SALARY
# ==========================================
def standardize_salary(df):
      # 1. Convert to string, clean whitespace/case, and remove symbols like '$' or commas
      s = (
          df["Salary"]
          .astype(str)
          .str.strip()
          .str.lower()
          .str.replace("$", "", regex=False)
          .str.replace(",", "", regex=False)
      )

      # 2. Parse values: handle 'k' multiplier or standard numbers
      def parse_val(val):
        if val in ["nan", "none", "", "nat"]:
          return pd.NA

        try:
          if "k" in val:
            # Remove 'k' and multiply by 1000
            return float(val.replace("k", "")) * 1000
          else:
            return float(val)
        except ValueError:
          # Catches "abc" or other non-numeric garbage and turns it into NaN
          return pd.NA

      df["Salary"] = s.apply(parse_val)
      return df




# ==========================================
# 6. FIX NUMERICAL DATA
# ==========================================
def numerical_data(df):
    print("\n Numerical Cleaning")
    print("="*40)
    # 1. Force the Age column to be numeric, turning text/strings into NaN
    df["Age"] = pd.to_numeric(df["Age"], errors='coerce')

    invalid_age = (df["Age"] < 0) | (df["Age"]>100)
    invalid_salary = df["Salary"] < 0
    print(f"Invalid Ages: {invalid_age.sum()}")
    print(f"Invalid Salary: {invalid_salary.sum()}")

    #fix the invalid age and salary
    df.loc[invalid_age,"Age"] = pd.NA
    df.loc[invalid_salary, "Salary"] = pd.NA

    return df

# ==========================================
# 6. FIX MISSING NAME, EMAIL, DEPARTMENT
# ==========================================
def fix_missing_data(df):
    print("\n Fix Missing Data")
    print("="*40)

    # Create an initial clean status
    df["Investigation_Flag"] = "OK"

    # Flag specific issues
    df.loc[df["Name"].isna(), "Investigation_Flag"] = "Missing Name"
    df.loc[df["Email"].isna(), "Investigation_Flag"] = "Missing Email"
    df.loc[df["Name"].isna() & df["Email"].isna(), "Investigation_Flag"] = "Missing Both"


    #Fix Missing City
    df["City"] = df["City"].fillna("Unknown")

    #Fix missing department using mode(most frequent occurrence)
    dept_mode = df["Department"].mode()[0]
    df["Department"] = df["Department"].fillna(dept_mode)

    #Fill Missing Salary
    salary_median = df["Salary"].median()
    df["Salary"] = pd.to_numeric(df["Salary"], errors='coerce').fillna(salary_median)

    return df



# ==========================================
# 7. RUN CLEANING PROGRAM
# ==========================================
missing_values(df)
df = remove_duplicates(df)
df = standardize_text(df)
df = standardize_salary(df)
df = numerical_data(df)
df = fix_missing_data(df)


# ==========================================
# 8. SAVE TO CSV
# ==========================================
df.to_csv(output_file, index=False)
print("\n Data Cleaning Complete")
print("="*40)
print(f"Final Clean Records: {len(df)}")
print(f"File Successfully Saved to: {output_file}")
