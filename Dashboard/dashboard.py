import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from analyzer import Dataanalyzer
from datetime import datetime, timedelta
import locale

sns.set_style("whitegrid")
sns.set(rc={"axes.facecolor":"#FFF9ED","figure.facecolor":"#FFF9ED"})
palette = ["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60","#84596B","#917B99","#AE8CA3","#C4A7CB"]

st.title("Brazilian E-Commerce Public Dataset")
st.write("**Dashboard for analyzing Brazilian E-Commerce Public Dataset**")

all_df = pd.read_csv("all_data.csv")
all_df.drop("Unnamed: 0", axis=1, inplace=True)


datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col3:
        st.write(' ')

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    
all_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & (all_df["order_approved_at"] <= str(end_date))]

#get the data
func = Dataanalyzer(all_df)
orders_product_sum = func.order_products_sum()
review_score = func.review_score()
daily_orders = func.daily_orders()
customer_spent = func.customer_spent()
customer_state_count = func.count_customer_state()

#plot product category sells most
st.subheader("Order Product")

sum_product = orders_product_sum.product_id.sum()
st.markdown(f"Total Products Category: **{sum_product}**")

f,ax = plt.subplots(1,2, figsize=(50,25))
sns.barplot(data=orders_product_sum.head(5), y="product_category_name_english", x="product_id",ax=ax[0],palette=palette)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=80,y=1.05)
ax[0].set_title("Highest products sold", loc="center", fontsize=90,y=1.05)
ax[0].tick_params(axis='y', labelsize=55)
ax[0].tick_params(axis='x', labelsize=50)

sns.barplot(data=orders_product_sum.sort_values(by="product_id", ascending=True).head(5), y="product_category_name_english", x="product_id",ax=ax[1],palette=palette)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Fewest products sold", loc="center", fontsize=90, y=1.05)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)
plt.tight_layout()
st.pyplot(f)


# plot review score
st.subheader("Review Score")
st1, st2 = st.columns(2)

with st1:
    most_rating = review_score.idxmax()
    st.markdown(f"Most Common Rating by Customer: **{most_rating}**")
with st2:
    avg_review_score = review_score
    weighted_sum = (avg_review_score.index * avg_review_score).sum()
    total_count = avg_review_score.sum()
    average_rating = round(weighted_sum / total_count,2)
    st.markdown(f"Average Rating: **{average_rating}**")

f, ax = plt.subplots(figsize=(12, 6))
sns.barplot(review_score.index, review_score.values, order = review_score.index, palette=palette)
ax.set_title("Customer Review Score",loc="center", fontsize=25,y=1.05)
ax.set_xlabel("Rating")
ax.set_ylabel("Rating_Count")

for i, v in enumerate(review_score.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')
st.pyplot(f)

#plot daily orders
st.subheader("Monthly Orders Delivered")
st1, st2 = st.columns(2)

with st1:
    total_order = daily_orders["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

locale.setlocale(locale.LC_ALL, 'pt_BR')
total_revenue = daily_orders["revenue"].sum()
with st2:
    st.markdown(f"Total Revenue: **{locale.currency(total_revenue, grouping=True, symbol=None)}**R$")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders["order_approved_at"],
    y=daily_orders["order_count"],
    color="#682F2F",
    marker="o"
)
ax.tick_params(axis="x", rotation=45)
ax.set_title("Time Plot Monthly Orders",loc="center", fontsize=25,y=1.05)
ax.set_xlabel("Order_Approved_at")
ax.set_ylabel("Order_count")
#ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

#plot customer spent
st.subheader("Customer Spend Money")
col1, col2 = st.columns(2)

locale.setlocale(locale.LC_ALL, 'pt_BR')
total_spend = customer_spent["payment_value"].sum()
with col1:
    st.markdown(f"Total Spend: **{locale.currency(total_spend, grouping=True, symbol=None)}**R$")

with col2:
    avg_spend = customer_spent["payment_value"].mean()
    st.markdown(f"Average Spend: **{avg_spend}**")
    
f, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=customer_spent["order_approved_at"], y= customer_spent["payment_value"], color="#682F2F")
ax.set_title("Customer Spend",loc="center", fontsize=25,y=1.05)
ax.set_xlabel("Order_Approved_at")
ax.set_ylabel("Total_Spend")
ax.tick_params(axis="x", rotation=45)
st.pyplot(f)

#plot tabs
st.subheader("Customer Analysis")
tab1, tab2 = st.tabs(["State", "Ontime"])

with tab1:
    most_state = customer_state_count.idxmax()
    st.markdown(f"Most customer state com from: {most_state}")
    
    f,ax = plt.subplots(figsize=(12,8))
    sns.barplot(y=customer_state_count.index, x=customer_state_count.values, palette=palette)
    ax.set_title("Customer State Count",loc="center", fontsize=25,y=1.05)
    ax.set_xlabel("Count")
    ax.set_ylabel("Customer State")
    st.pyplot(f)

with tab2:
    total_orders = len(all_df)
    on_time_deliveries = all_df['is_ontime'].sum()
    avg_ontime = round((all_df.is_ontime.sum() / len(all_df)), 2)
    labels=['On Time', 'Delayed']
    f, ax = plt.subplots(figsize=(12,6))
    plt.pie([on_time_deliveries, total_orders - on_time_deliveries], colors=["#9E726F", "#D6B2B1"], autopct='%1.1f%%')
    plt.legend(labels, loc='upper right')
    ax.set_title("Average Ontime vs Delayed",loc="center", fontsize=15,y=1.05)
    st.pyplot(f)
