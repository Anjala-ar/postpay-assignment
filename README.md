# Customer Metrics - Table of Contents

** Important Note:** 

The latest order date in the given input is `2022-01-05`, and since the date difference is calculated based on current date(today), output columns like `orders_on_customer_id_7D` and `shop_id_count_paid_orders_90D` are going to be default I set

#Setup Instructions
run `python setup.py install`

# Operation Instructions
For this exercise, I decided to keep things simple and add the 3 columns  as requested. The input data seemed quite clean, and so I didn't add any data-cleaning functionalities.
I have also added a write_data function which will save the data to your local.

Note: Do not change the order of running statements in the main and the some outputs are dependant on the
output from the previous steps!

## Basic Usage

(a). Run Main file for adding the functionalities, successful run should have the data saved to your local path

## Running Tests

(a) Added basic unit tests for test the working of the main functions

## Project Structure

1. Data: executors >> data > >resources
2. Main file : executors >> src >> main
3. Main file : executors >> src >> test

## Expected Output

The output is a df with the 3 columns added along with the input - 
1. orders_on_customer_id_7D - The number of orders on customer  id in the last 7 days 
2. customer_id_has_paid - `True` - if the customer has paid prior to this order, `False` - Otherwise
3. shop_id_count_paid_orders_90D - The number of paid orders on shop id
