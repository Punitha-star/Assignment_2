import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Food Delivery Dashboard", layout="wide")
st.title("🍔 Food Delivery 🚚 Dashboard")

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
engine = create_engine("mysql+pymysql://root:12345@localhost/Project")

# -------------------------------
# LOAD FULL DATA (EDA)
# -------------------------------
eda_df = pd.read_sql("SELECT * FROM food_delivery_orders", engine)

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
option = st.sidebar.radio("Select Module", ["SQL Analysis", "EDA Analysis"])

# =========================================================
# 🔹 SQL ANALYSIS (15 QUERIES)
# =========================================================
if option == "SQL Analysis":

    st.header("📊 SQL Analysis")

    TASKS = {
        "1.Top 10 Customers": """
            SELECT Customer_ID,SUM(Order_Value) AS Total_Spending
            FROM food_delivery_orders
            GROUP BY Customer_ID
            ORDER BY Total_Spending DESC
            LIMIT 10;
        """,

        "2.Age-wise Purchase": """
            SELECT Customer_Age,ROUND(AVG(Order_Value),2) AS Avg_Order_Value
            FROM food_delivery_orders
            GROUP BY Customer_Age;
        """,

        "3.Weekend vs Weekday": """
            SELECT Order_Day_Type,COUNT(*) AS Total_Orders
            FROM food_delivery_orders
            GROUP BY Order_Day_Type;
        """,

        "4.Monthly Revenue": """
            SELECT MONTHNAME(Order_Date) AS Month,
            ROUND(SUM(Order_Value),2) AS Revenue
            FROM food_delivery_orders
            GROUP BY Month;
        """,

        "5.Discount vs Profit": """
            SELECT Discount_Applied,ROUND(AVG(Profit_Margin),2) AS Profit
            FROM food_delivery_orders
            GROUP BY Discount_Applied;
        """,

        "6.City & Cuisine Revenue": """
            SELECT City,Cuisine_Type,ROUND(AVG(Order_Value),2) AS Revenue
            FROM food_delivery_orders
            GROUP BY City,Cuisine_Type;
        """,

        "7.City Delivery Time": """
            SELECT City,ROUND(AVG(Delivery_Time_Min),2) AS Avg_Time
            FROM food_delivery_orders
            GROUP BY City;
        """,

        "8.Distance vs Delivery": """
            SELECT ROUND(Distance_km,1) AS Distance,
            ROUND(AVG(Delivery_Time_Min),2) AS Avg_Time
            FROM food_delivery_orders
            GROUP BY Distance;
        """,

        "9.Rating vs Time": """
            SELECT ROUND(Delivery_Rating,1) AS Rating,
            ROUND(AVG(Delivery_Time_Min),2) AS Avg_Time
            FROM food_delivery_orders
            GROUP BY Rating;
        """,

        "10.Top Restaurants": """
            SELECT Restaurant_Name,
            ROUND(AVG(Delivery_Rating),2) AS Rating,
            COUNT(*) AS Orders
            FROM food_delivery_orders
            GROUP BY Restaurant_Name
            ORDER BY Rating DESC
            LIMIT 10;
        """,

        "11.Restaurant Cancellation": """
            SELECT Restaurant_Name,COUNT(*) AS Cancel
            FROM food_delivery_orders
            WHERE Cancellation_Reason != 'None'
            GROUP BY Restaurant_Name;
        """,

        "12.Cuisine Performance": """
            SELECT Cuisine_Type,COUNT(*) AS Orders,
            ROUND(SUM(Order_Value),2) AS Revenue
            FROM food_delivery_orders
            GROUP BY Cuisine_Type;
        """,

        "13.Peak Hour": """
            SELECT Peak_Hour,COUNT(*) AS Orders
            FROM food_delivery_orders
            GROUP BY Peak_Hour;
        """,

        "14.Payment Mode": """
            SELECT Payment_Mode,COUNT(*) AS Orders
            FROM food_delivery_orders
            GROUP BY Payment_Mode;
        """,

        "15.Cancellation Reason": """
            SELECT Cancellation_Reason,COUNT(*) AS Cancel
            FROM food_delivery_orders
            WHERE Order_Status='Cancelled'
            GROUP BY Cancellation_Reason;
        """
    }

    selected_task = st.selectbox("Select Task", list(TASKS.keys()))

    if st.button("Run SQL Task"):

        df = pd.read_sql(TASKS[selected_task], engine)

        st.dataframe(df, use_container_width=True)

        # -------------------------------
        # AUTO CHART
        # -------------------------------
        if len(df.columns) >= 2:
            fig, ax = plt.subplots(figsize=(10,5))

            x_col = df.columns[0]
            y_col = df.columns[1]

            # Smart chart selection
            if "Distance" in x_col or "Rating" in x_col:
                sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
            else:
                sns.barplot(data=df, x=x_col, y=y_col, ax=ax)

            plt.xticks(rotation=45)
            st.pyplot(fig)

# =========================================================
# 🔹 EDA ANALYSIS (6 TYPES)
# =========================================================
elif option == "EDA Analysis":

    st.header("📊 Exploratory Data Analysis")

    eda_option = st.selectbox(
        "Select EDA Task",
        [
            "Order Value Distribution",
            "City & Cuisine",
            "Weekend vs Weekday",
            "Distance vs Delivery Time",
            "Cancellation Analysis",
            "Correlation Heatmap"
        ]
    )
         # ✅ RUN BUTTON
    
    if st.button("Run EDA Task"):

            df = pd.read_sql("SELECT * FROM food_delivery_orders", engine)

       
    # -------------------------------
    # EDA VISUALS
    # -------------------------------

    if eda_option == "Order Value Distribution":
            fig, ax = plt.subplots()
            sns.histplot(eda_df['Order_Value'], kde=True, ax=ax)
            st.pyplot(fig)


    elif eda_option == "City & Cuisine":
        city_cuisine = eda_df.groupby(['City','Cuisine_Type']).size().reset_index(name='Orders')
        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(data=city_cuisine, x='City', y='Orders', hue='Cuisine_Type', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif eda_option == "Weekend vs Weekday":
        fig, ax = plt.subplots()
        sns.countplot(data=eda_df, x='Order_Day_Type', ax=ax)
        st.pyplot(fig)

    elif eda_option == "Distance vs Delivery Time":
        fig, ax = plt.subplots()
        sns.scatterplot(data=eda_df, x='Distance_km', y='Delivery_Time_Min', ax=ax)
        st.pyplot(fig)

    elif eda_option == "Cancellation Analysis":
        cancel_df = eda_df[eda_df['Order_Status']=='Cancelled']
        fig, ax = plt.subplots()
        sns.countplot(data=cancel_df, x='Cancellation_Reason', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif eda_option == "Correlation Heatmap":
        numeric_df = eda_df.select_dtypes(include=['int64','float64'])
        fig, ax = plt.subplots(figsize=(10,6))
        sns.heatmap(numeric_df.corr(), annot=True, ax=ax)
        st.pyplot(fig)