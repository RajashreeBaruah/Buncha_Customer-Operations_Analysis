import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("customers.csv")

# Select relevant features for clustering
features = df[['total_spend', 'num_orders']]

# Scale the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)


wcss = []  # Stores Within-Cluster Sum of Squares (WCSS)

# Try different values of K (1 to 10)
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=0)
    kmeans.fit(scaled_features)
    wcss.append(kmeans.inertia_)  # Inertia measures clustering compactness

# Plot Elbow Curve
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS values")
plt.title("Elbow Method for Optimal K")
plt.show()

# Apply K-Means with optimal K
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=0)
df['cluster'] = kmeans.fit_predict(scaled_features)

plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["total_spend"], y=df["num_orders"], hue=df["cluster"], palette="Set1")
plt.title("Customer Segments")
plt.xlabel("Total Spend")
plt.ylabel("Number of Orders")
plt.legend(title="Customer Type")
plt.show()

###################################################################################################################

# Load sales dataset
df2 = pd.read_csv("sales_data.csv")

# Convert order_date to datetime format
df2['order_date'] = pd.to_datetime(df2['order_date'])

# Extract month name for trend analysis
df2['month'] = df2['order_date'].dt.strftime('%B')

# Aggregate revenue per month
monthly_sales = df2.groupby('month')['revenue'].sum().reset_index()

# Sort months in calendar order
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=month_order, ordered=True)
monthly_sales = monthly_sales.sort_values('month')

# Plot sales trends
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales['month'], monthly_sales['revenue'], marker='o', linestyle='-', color='b')
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.title("Sales Trends - Peak Ordering Periods")
plt.grid()

# Add data labels
for i in range(len(monthly_sales)):
    plt.text(monthly_sales['month'][i], monthly_sales['revenue'][i], round(monthly_sales['revenue'][i], 2), fontsize=8, ha='right')

plt.show()

##################################################################################################################

# Load orders dataset
df3 = pd.read_csv("orders1.csv")

# Convert order_date to datetime format
df3['order_date'] = pd.to_datetime(df3['order_date'], format='%d-%m-%Y')

# Extract month name for trend analysis
df3['month'] = df3['order_date'].dt.strftime('%B')

# Aggregate total amount per customer
customer_spending = df3.groupby('customer_id')['total_amount'].sum().reset_index()

# Merge with customer segmentation data
customer_segmentation = df.merge(customer_spending, left_on='customer_id', right_on='customer_id', how='left')

# Visualize customer spending patterns
plt.figure(figsize=(8, 6))
sns.boxplot(x=customer_segmentation['cluster'], y=customer_segmentation['total_amount'], palette="Set2")
plt.title("Customer Spending Patterns by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Spend")
plt.xticks(rotation=45)
plt.show()

# Aggregate orders by city
city_orders = df3.groupby('city')['order_id'].count().reset_index().rename(columns={'order_id': 'num_orders'})

# Visualize orders by city
plt.figure(figsize=(10, 5))
ax = sns.barplot(x=city_orders['city'], y=city_orders['num_orders'], palette="coolwarm")
plt.title("Number of Orders by City")
plt.xlabel("City")
plt.ylabel("Total Orders")
plt.xticks(rotation=45)

# Add data labels
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=10, color='black')

plt.show()