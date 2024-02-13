class Dataanalyzer:
    def __init__(self, df):
        self.df = df
    def review_score(self):
        review_df = self.df["review_score"].value_counts().sort_values(ascending=False)
        return review_df
    
    def daily_orders(self):
        daily_orders_df = self.df.resample(rule='M', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        daily_orders_df = daily_orders_df.reset_index()
        daily_orders_df.rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        }, inplace=True)
        return daily_orders_df
    
    def customer_spent(self):
        customer_spent_df = self.df.resample(rule="D", on="order_approved_at").agg({
            "payment_value":"sum"}).reset_index()
        return customer_spent_df
    
    def order_products_sum(self):
        sum_products = self.df.groupby("product_category_name_english").agg({"product_id":"count"}).sort_values("product_id", ascending=False).reset_index()
        return sum_products
    
    def count_customer_state(self):
        customer_state_count = self.df.customer_state.value_counts().sort_values(ascending=False)
        return customer_state_count
    
