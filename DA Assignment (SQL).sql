/* QUESTION 1
Identify customers who haven't placed an order in the last 60 days but had at least 2 orders before.
*/
SELECT customer_id FROM orders1
WHERE customer_id IN (
	SELECT customer_id FROM orders1 
    GROUP BY customer_id HAVING COUNT(order_date) >= 2
    )
GROUP BY customer_id
HAVING MAX(order_date) < DATE_SUB(CURDATE(), INTERVAL 60 DAY);



/* QUESTION 2
Calculate the average time between consecutive orders for repeat customers
*/

-- FOR EACH CUSTOMER
WITH GAP_BETWEEN_ORDERS AS (
	SELECT customer_id,
		DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS DAYS_BETWEEN_ORDERS
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
 
 
-- FOR ALL REPEAT CUSTOMERS AS A WHOLE
WITH avg_gap_each_customer AS (
	WITH GAP_BETWEEN_ORDERS AS (
	SELECT customer_id,
		DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS DAYS_BETWEEN_ORDERS
	FROM orders1
	WHERE customer_id IN (
		SELECT customer_id FROM orders1 GROUP BY customer_id HAVING COUNT(order_date) > 1
        )
	)
	SELECT customer_id, AVG(DAYS_BETWEEN_ORDERS) AS avg_time_btwn_consecutive_orders_for_each_customer
	FROM GAP_BETWEEN_ORDERS
	WHERE DAYS_BETWEEN_ORDERS IS NOT NULL
	GROUP BY customer_id
)
SELECT AVG(avg_time_btwn_consecutive_orders_for_each_customer) AS OVERALL_AVG_TIME_BETWEEN_CONSECUTIVE_ORDERS
from avg_gap_each_customer;


/* QUESTION 3
Determine the top 10% of customers by total spend and their average order value
*/
WITH customer_spending AS (
    SELECT customer_id, SUM(total_amount) AS total_spend, COUNT(ORDER_DATE) AS NO_OF_ORDERS
    FROM orders1
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT customer_id, total_spend, TOTAL_SPEND/NO_OF_ORDERS AS AOV,
           PERCENT_RANK() OVER (ORDER BY total_spend DESC) AS percentile_rank
    FROM customer_spending
)
SELECT customer_id, total_spend, AOV
FROM ranked_customers
WHERE percentile_rank <= 0.1  -- only top 10%
ORDER BY total_spend DESC;



/* QUESTION 4
Analyze delivery time efficiency by calculating the percentage of on-time deliveries per region
*/
WITH delivery_times AS (
	SELECT city, COUNT(CASE WHEN delivery_status = 'On Time' THEN 1 END) AS on_time_deliveries, COUNT(*) as total_deliveries
    FROM ORDERS1 ORD INNER JOIN DELIVERY_PERFORMANCE DP
	ON ORD.ORDER_ID = DP.ORDER_ID
	GROUP BY city
)
SELECT city, on_time_deliveries*100/total_deliveries AS delivery_time_efficiency
FROM delivery_times
GROUP BY city
ORDER BY delivery_time_efficiency DESC;