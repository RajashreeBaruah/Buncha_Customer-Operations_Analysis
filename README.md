# Buncha Technologies - Customer & Operations Analysis  

## Overview  
This project analyzes **customer behavior, sales trends, and operational efficiency** to provide actionable insights that enhance business performance. It focuses on **customer retention, inventory management, and delivery performance** using **SQL, Excel, and Python**.  

## Datasets Used  
- `orders1.csv`  
- `customers.csv`  
- `inventory.csv`  
- `delivery_performance.csv`  
- `discount_campaign.csv`  
- `sales_data.csv`  

## Tools & Technologies  
- **SQL** (MySQL Workbench)  
- **Python** (Pandas, Matplotlib, Scikit-learn)  
- **MS Excel** (Pivot Tables, Charts, Dashboarding)  
- **VS Code**  

---

## SQL Analysis – Customer Purchase & Delivery Trends  
Key objectives:  
✔ Identify **customer retention patterns** and repeat purchase behavior  
✔ Evaluate **delivery efficiency** across different regions  
✔ Analyze **top customers** based on spending  

### Key SQL Queries  
✅ **Customers who haven't ordered in 60+ days but had at least 2 past orders**  
```sql
SELECT DISTINCT customer_id FROM orders1
WHERE customer_id IN (
    SELECT customer_id FROM orders1
    GROUP BY customer_id 
    HAVING COUNT(order_date) >= 2
)
GROUP BY customer_id
HAVING MAX(order_date) < DATE_SUB(CURDATE(), INTERVAL 60 DAY);
```
✅ **Average time between consecutive orders for repeat customers**  
```sql
FOR EACH CUSTOMER
WITH GAP_BETWEEN_ORDERS AS (
	SELECT customer_id,
	DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS 	DAYS_BETWEEN_ORDERS
	FROM orders1
	WHERE customer_id IN (
		SELECT customer_id FROM orders1
		GROUP BY customer_id         
		HAVING COUNT(order_date) > 1 -- repeat customers        
	)
)
SELECT customer_id, AVG(DAYS_BETWEEN_ORDERS) AS avg_time_btwn_consecutive_orders_for_each_customer
FROM GAP_BETWEEN_ORDERS
WHERE DAYS_BETWEEN_ORDERS IS NOT NULL
GROUP BY customer_id;
```

✅ **Top 10% of customers by total spend & their average order value**  
```sql
WITH customer_spending AS (
	SELECT customer_id, SUM(total_amount) AS total_spend, 
	COUNT(ORDER_DATE) AS NO_OF_ORDERS
	FROM orders1
	GROUP BY customer_id),
ranked_customers AS (
	SELECT customer_id, total_spend, TOTAL_SPEND/NO_OF_ORDERS AS AOV,
	PERCENT_RANK() OVER (ORDER BY total_spend DESC) AS percentile_rank
	FROM customer_spending)
SELECT customer_id, total_spend, AOV
FROM ranked_customers
WHERE percentile_rank <= 0.1  -- only top 10%
ORDER BY total_spend DESC;
```
✅ **Delivery time efficiency per region**  
```sql
WITH delivery_times AS (
	SELECT city, COUNT(CASE WHEN delivery_status = 'On Time' THEN 1 END) AS on_time_deliveries, 
	COUNT(*) as total_deliveries
	FROM ORDERS1 ORD INNER JOIN DELIVERY_PERFORMANCE DP
	ON ORD.ORDER_ID = DP.ORDER_ID
	GROUP BY city)
SELECT city, on_time_deliveries*100/total_deliveries AS delivery_time_efficiency
FROM delivery_times
GROUP BY city
ORDER BY delivery_time_efficiency DESC;
```

### Key Insights  
- **67 days** is the average time between repeat orders.  
- **Top 10% of customers** contribute significantly to revenue.  
- **Houston** has the highest delivery efficiency (84.9% on-time).  

---

## Excel Analysis – Sales & Inventory Dashboard  
Key objectives:  
✔ Track **monthly revenue growth** and seasonal variations  
✔ Compute **Average Order Value (AOV)**  
✔ Identify **customer retention trends**  
✔ Analyze **stock-out patterns**  

### Key Insights  
- **Dashboard**
  ![image](https://github.com/user-attachments/assets/4cf9088f-94e4-4126-bc64-7c3dc1d42257)

- **Revenue peaks in February, July, September, and October**, while August & November show declines.
  ![image](https://github.com/user-attachments/assets/aa0f1c52-a9ac-440d-87d7-9d21a4e6ba8f)

- **AOV = $252.57**, indicating high-value transactions per order.  
- **Customer Retention Rate = 36.81%**, meaning over 60% of customers don’t return.  
- **Milk, Chicken, and Fruits** are the most frequently out-of-stock products.
  ![image](https://github.com/user-attachments/assets/f852438f-8f15-433e-b307-9e8d80bb015e)
---

## Python Analysis – Customer Segmentation & Demand Patterns  
Key objectives:  
✔ Apply **K-Means Clustering** to segment customers based on **spending & order frequency**  
✔ Analyze **monthly sales trends**  
✔ Identify **city-wise order distribution**  

### Key Insights  
- **Customer Segments**:  
  🔴 **High Spend, High Orders** (Valuable buyers)  
  🟢 **Low Spend, High Orders** (Frequent, low-value buyers)  
  🔵 **Low Spend, Low Orders** (Occasional buyers)  
  🟣 **High Spend, Low Orders** (Big spenders, low frequency)
  ![image](https://github.com/user-attachments/assets/e9710860-3c86-4300-bf97-fa251dcfceb9)

- **Sales Peak in July & October**, aligning with discount campaigns.
  ![image](https://github.com/user-attachments/assets/549789ae-dc52-451a-b051-f5d65f646839)

- **San Francisco & Los Angeles** have the highest order volume.
  ![image](https://github.com/user-attachments/assets/edc5905a-5158-4925-9164-67cfe695b987)
---

## Business Case Study – Discount Impact Analysis  
Key objectives:  
✔ Assess **impact of discounts on total revenue & customer retention**  
✔ Identify **customer responsiveness to discounts**  
✔ Propose **strategies to optimize profitability**  

### Key Findings  
- **Total spend before discounts**: $1.28M → **After discounts**: $2.57M (2X growth)  
- **Customers who applied discounts vs. those who didn't**: Both groups increased spending, meaning other factors like seasonality or promotions also played a role.  
- **130 customers reduced spending even after receiving discounts**, indicating price sensitivity.  

### Recommendations  
✔ Implement **tiered discounts** (e.g., 10% for moderate buyers, 15% for high-value buyers).  
✔ **Avoid discounts for unresponsive customers** and offer alternative incentives like cashback.  
✔ **Use seasonal or event-based discounts** instead of continuous offers.  

---
