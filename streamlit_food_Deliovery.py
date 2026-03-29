import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Food Delivery Dashboard",
    layout="wide"
)

st.title("🍔 Food Delivery 🚚 Dashboard")

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
print("Connecting to MySQL...")
engine = create_engine(
    "mysql+pymysql://root:12345@localhost/Project"
)
print("Connected to MySQL\n")

# SQL TASKS (DROPDOWN)
# -------------------------------
TASKS = {
    "1.Top 10 - Spending customers Analysis": {
        "query": """
            SELECT Customer_ID,SUM(Order_Value) AS Total_Spending
            FROM food_delivery_orders
            GROUP BY Customer_ID
            ORDER BY Total_Spending DESC
            LIMIT 10;
        """,
        "title": "Top 10 - Spending customers Analysis"
    },

    "2.Age - wise Purchases Value Insights": {
        "query": """
            SELECT Customer_Age,
            ROUND(AVG(Order_Value), 2) AS Avg_Order_Value
            FROM food_delivery_orders
            GROUP BY Customer_Age;
        """,
        "title": "Age - wise Purchases Value Insights"
    },

    "3.Weekend vs weekday order patterns Analysis": {
        "query": """
            SELECT Order_Day_Type,
            COUNT(*) AS Total_Orders
            FROM food_delivery_orders
            GROUP BY Order_Day_Type;
        """,
        "title": "Weekend vs weekday order patterns Analysis"
    },

    "4.Monthly revenue Analysis": {
        "query": """
            SELECT MONTHNAME(Order_Date) AS Month,
            ROUND(SUM(Order_Value),2) AS Total_Revenue
            FROM food_delivery_orders
            GROUP BY Month
            ORDER BY MONTH;
        """,
        "title": "Monthly revenue Analysis"
    },

    "5. Discounts vs profit Analysis": {
        "query": """
            SELECT Discount_Applied,
            ROUND(AVG(Profit_Margin),2) AS Avg_Profit
            FROM food_delivery_orders
            GROUP BY Discount_Applied
            ORDER BY Discount_Applied;
        """,
        "title": "Discounts vs profit Analysis"
    },

    "6.High-revenue cities and cuisines Analysis": {
        "query": """
            select City,Cuisine_Type,Round(Avg(Order_Value),2) AS Total_Revenue
            from food_delivery_orders
            group by City,Cuisine_Type
            order by Total_Revenue desc;
        """,
        "title": "High-revenue cities and cuisines Analysis"
    },

    "7.City-wise Delivery Time Analysis": {
        "query": """
            select City,Round(Avg(Delivery_Time_Min),2) As Average_Delivery_Time
            from food_delivery_orders
            group by City
            ORDER BY Average_Delivery_Time;
        """,
        "title": "City-wise Delivery Time Analysis"
    },

    "8.Distance vs delivery delay Analysis": {
        "query": """
            SELECT ROUND(Distance_km,1) AS Distance,
            ROUND(AVG(Delivery_Time_Min),2) AS Avg_Delivery_Time
            FROM food_delivery_orders
            GROUP BY Distance
            ORDER BY Distance;
        """,
        "title": "Distance vs delivery delay Analysis"
    },

    "9.Delivery rating vs delivery time Analysis": {
        "query": """
            select round(Delivery_Rating,1) AS Delivery_Rating, ROUND(AVG(Delivery_Time_Min),2) AS Avg_Delivery_Time
            from food_delivery_orders
            group by Delivery_Rating
            order by Delivery_Rating desc;
        """,
        "title": "Delivery rating vs delivery time Analysis"
    },

    "10.Highest Rated Restaurants Analysis": {
        "query": """
            select Restaurant_Name,ROUND(AVG(Delivery_Rating),2) AS Avg_Rating,COUNT(Order_ID) AS Total_Orders FROM food_delivery_orders
            GROUP BY Restaurant_Name
            ORDER BY Avg_Rating DESC
            LIMIT 10;
        """,
        "title": "Highest Rated Restaurants Analysis"
    },

    "11.Restaurants-wise Cancellation Analysis": {
        "query": """
            SELECT Restaurant_Name, COUNT(*) AS Total_Cancellations
            FROM food_delivery_orders           
            WHERE Cancellation_Reason != 'None'
            GROUP BY Restaurant_Name
        """,
        "title": "Restaurants-wise Cancellation Analysis"
    },

    "12.Cuisines-wise Performance Analysis": {
        "query": """
            SELECT Cuisine_Type,
            COUNT(Order_ID) AS Total_Orders,
            ROUND(SUM(Order_Value),2) AS Total_Revenue,
            ROUND(AVG(Delivery_Rating),2) AS Avg_Rating
            FROM food_delivery_orders
            GROUP BY Cuisine_Type
            ORDER BY Total_Revenue DESC;
        """,
        "title": "Cuisines-wise Performance Analysis"
    },

    "13.Peak Hour Demand Analysis": {
        "query": """
            SELECT Peak_Hour,
            COUNT(Order_ID) AS Total_Orders
            FROM food_delivery_orders
            GROUP BY Peak_Hour;
        """,
        "title": "Peak Hour Demand Analysis"
    },

    "14.Payment Mode Preferences Analysis": {
        "query": """
            SELECT Payment_Mode,
            COUNT(Order_ID) AS Total_Orders
            FROM food_delivery_orders
            GROUP BY Payment_Mode
            ORDER BY Total_Orders DESC;
        """,
        "title": "Payment Mode Preferences Analysis"
    },

    "15.Cancellation Reason Analysis": {
        "query": """
            SELECT Cancellation_Reason,
            COUNT(Order_ID) AS Total_Cancellations
            FROM food_delivery_orders
            WHERE Order_Status = 'Cancelled'
            GROUP BY Cancellation_Reason
            ORDER BY Total_Cancellations DESC;
        """,
        "title": "Cancellation Reason Analysis"
    },
}
# -------------------------------
# DROPDOWN
# -------------------------------
selected_task = st.selectbox(
    "📊 Select Analyst Task",
    list(TASKS.keys())
)

# -------------------------------
# RUN QUERY & DISPLAY
# -------------------------------
if st.button("Run"):
    try:
        query = TASKS[selected_task]["query"]
        title = TASKS[selected_task]["title"]

        df = pd.read_sql(query, engine)

        st.subheader(title)
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Database error: {e}")
        