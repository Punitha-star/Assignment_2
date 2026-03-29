import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine

# 1️⃣ Load Dataset
df = pd.read_csv('C:\\Users\\Niresh\\Guvi\\ONINE_FOOD_DELIVERY_ANALYSIS.csv')

# 2️⃣ Strip column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

# 3️⃣ Drop unwanted 'Unnamed' columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# -------------------------------------------------------
# 4️⃣ HANDLE CATEGORICAL COLUMNS (Fill with MODE)
# -------------------------------------------------------

categorical_cols = df.select_dtypes(include='object').columns

for col in categorical_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Convert to category type
    df[col] = df[col].astype('category')

# -------------------------------------------------------
# 5️⃣ HANDLE NUMERICAL COLUMNS
# -------------------------------------------------------

numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns

for col in numerical_cols:
    if df[col].isnull().sum() > 0:

        # If column has outliers → use median
        if col in ['Final_Amount', 'Delivery_Time_Min', 'Order_Value', 'Discount_Applied']:
            df[col] = df[col].fillna(df[col].median())

        # Otherwise use mean
        else:
            df[col] = df[col].fillna(df[col].mean())
df['Distance_km'] = df['Distance_km'].round(2)
df['Delivery_Rating'] = df['Delivery_Rating'].round(2)

# -------------------------------------------------------
# 6️⃣ SPECIAL CASES
# -------------------------------------------------------

# Customer_Gender (27% null → Fill with Mode)
if 'Customer_Gender' in df.columns:
    df['Customer_Gender'] = df['Customer_Gender'].fillna(df['Customer_Gender'].mode()[0])
    df['Customer_Gender'] = df['Customer_Gender'].astype('category')

# Cancellation_Reason (96% null → Fill with Mode)
if 'Cancellation_Reason' in df.columns:
    df['Cancellation_Reason'] = df['Cancellation_Reason'].fillna(df['Cancellation_Reason'].mode()[0])
    df['Cancellation_Reason'] = df['Cancellation_Reason'].astype('category')

# -------------------------------------------------------
# 7️⃣ DATE & TIME CLEANING
# -------------------------------------------------------

if 'Order_Date' in df.columns:
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Order_Date'] = df['Order_Date'].fillna(method='ffill')

if 'Order_Time' in df.columns:
    df['Order_Time'] = pd.to_timedelta(df['Order_Time'].astype(str) + ':00', errors='coerce')
    df['Order_Time'] = df['Order_Time'].fillna(method='ffill')

# -------------------------------------------------------
# 8️⃣ FIX AGE COLUMN
# more then 50% null value i am using median also age is float and convert int
if 'Customer_Age' in df.columns:
    df['Customer_Age'] = df['Customer_Age'].fillna(df['Customer_Age'].median())
    df['Customer_Age'] = df['Customer_Age'].astype(int)

#Feature
# Convert date to datetime,Add Order Day Type (Weekday / Weekend)
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
# Create new column
df['Order_Day_Type'] = df['Order_Date'].dt.dayofweek.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
#2.Add Peak Hour Column
# Convert time
df['Order_Time'] = pd.to_datetime(df['Order_Time'], errors='coerce')
# Extract hour
df['Hour'] = df['Order_Time'].dt.hour
# Create Peak hour column
df['Order_Time'] = pd.to_datetime(df['Order_Time'], errors='coerce')
df['Hour'] = df['Order_Time'].dt.hour
#3-Add Profit Margin %
df['Profit_Margin_%'] = (df['Profit_Margin'] / df['Order_Value']) * 100
df['Profit_Margin_%'] = df['Profit_Margin_%'].round(2)
df['Peak_Hour'] = df['Hour'].apply(lambda x: 'Peak' if pd.notnull(x) and 18 <= x <= 21 else 'Non-Peak')
#4-Add Delivery Performance Category
def delivery_category(x):
    if x <= 30:
        return 'Fast'
    elif x <= 45:
        return 'Average'
    else:
        return 'Late'

df['Delivery_Performance'] = df['Delivery_Time_Min'].apply(delivery_category)
#5-Add Customer Age Group
def age_group(age):
    if age < 25:
        return 'Young'
    elif age < 40:
        return 'Adult'
    else:
        return 'Senior'

df['Age_Group'] = df['Customer_Age'].apply(age_group)
df.to_csv("cleaned_orders.csv", index=False)

# STEP 1: LOAD CSV DATA
# ==============================
print("Loading cleaned earthquake data...")
df = pd.read_csv(r"C:\Users\Niresh\Guvi\cleaned_orders.csv")
print(f"Loaded {len(df)} records\n")

# ==============================
# STEP 2: CREATE DATABASE ENGINE
# ==============================
print("Connecting to MySQL...")
engine = create_engine(
    "mysql+pymysql://root:12345@localhost/Project"
)
print("Connected to MySQL\n")

# ==============================
# STEP 3: INSERT DATA
# ==============================
print("Inserting data into food_delivery_orders table...")
try:
    df.to_sql(
        name="food_delivery_orders",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )
    print("Upload completed")
    #print("Data inserted successfully\n")
except Exception as e:
    print("Error inserting data:", e)

# ==============================