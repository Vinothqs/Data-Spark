import pandas as pd
import os

# List of all required CSV files
csv_files = {
    "customers": "Customers.csv",
    "data_dictionary": "Data_Dictionary.csv",
    "exchange_rates": "Exchange_Rates.csv",
    "products": "Products.csv",
    "sales": "Sales.csv",
    "stores": "Stores.csv",
}

# Function to clean each dataset
def clean_data(df, file_name):
    try:
        # Check for missing values and fill them using forward fill
        missing_values = df.isnull().sum()
        print(f"\n⚠️ Missing Values in {file_name}:\n{missing_values[missing_values > 0]}")
        df.ffill(inplace=True)

        # Handling Outliers (for numeric columns only)
        numeric_cols = df.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            q1 = df[numeric_cols].quantile(0.25)
            q3 = df[numeric_cols].quantile(0.75)
            iqr = q3 - q1
            outliers = ((df[numeric_cols] < (q1 - 1.5 * iqr)) | (df[numeric_cols] > (q3 + 1.5 * iqr))).sum()
            print(f"\n🚨 Outliers in {file_name}:\n{outliers[outliers > 0]}")

            # Removing outliers
            df = df[~((df[numeric_cols] < (q1 - 1.5 * iqr)) | (df[numeric_cols] > (q3 + 1.5 * iqr))).any(axis=1)]

        return df

    except Exception as e:
        print(f"\n❌ Error in cleaning {file_name}: {e}")
        return df  # Return the original dataframe if error occurs

# Process each file
for key, file_path in csv_files.items():
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, encoding="ISO-8859-1", low_memory=False)
            print(f"\n📂 Processing: {file_path}")
            cleaned_df = clean_data(df, file_path)

            # Save cleaned file
            cleaned_file_path = f"Cleaned_{file_path}"
            cleaned_df.to_csv(cleaned_file_path, index=False)
            print(f"✅ {file_path} cleaned and saved as '{cleaned_file_path}'")

        except Exception as e:
            print(f"\n❌ Error loading {file_path}: {e}")
    else:
        print(f"\n❌ Error: '{file_path}' not found. Please check the file path.")

print("\n🎯 All files are cleaned and ready for Power BI!")