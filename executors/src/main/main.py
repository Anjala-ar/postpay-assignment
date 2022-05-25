from pathlib import Path

import pandas as pd
import numpy as np
from datetime import date
import warnings

warnings.filterwarnings("ignore")

'''
Static : A class that holds all static values used by the functions, also reads the customer data
GetColumns : A class that holds all column values for the input data, and also all the expected columns in the output
'''


class Static:
    here = Path(__file__).parent.parent.parent
    table_name = "interview_df.csv"
    input_path = str(here) + "/data/input_data"

    date_interval_num_orders = "7D"  # Tunable parameter, if we want to get the order details for any other time period
    date_interval_paid_orders = "90D"  # Tunable parameter, if we want to get the paid orders for any other time period
    today = pd.to_datetime(date.today())  # Holds today's date
    out_table_name = f"customer_metrics_{today}.csv"
    output_path = str(here) + "/data/output_data"

    @property
    def get_table_name(self):
        return self.table_name

    @property
    def location(self):
        return self.input_path

    @property
    def get_path(self):
        return self.location + "/" + self.get_table_name

    def get_order_details(self):
        return pd.read_csv(self.get_path, parse_dates=[GetColumns.created_date])


class GetColumns:
    order_id = "order_id"
    customer_id = "customer_id"
    created_date = "created_date"
    order_amount = "order_amount"
    shop_id = "shop_id"
    order_status = "order_status"
    order_for_7_days = "order_for_7_days"
    customer_id_has_paid = "customer_id_has_paid"
    shop_id_count_paid_orders_90D = "shop_id_count_paid_orders_90D"


# helper function which helps filters data given a date interval
def date_delta(order_details, interval):
    order_details["date_interval"] = [(Static.today - dt).days for dt in order_details[GetColumns.created_date]]
    return np.where(order_details["date_interval"] <= interval, True, False)


# Returns a dataframe with the column <order_for_7_days>,
# that represents the number of orders on customer id in the last 7 days
# In case the customer has not placed any orders given the interval, the column value defaults to
# `No orders placed in the last 7 days`
def get_orders_for_time_delta(order_details):
    order_details[GetColumns.order_for_7_days] = \
        order_details.set_index(GetColumns.created_date).groupby(GetColumns.customer_id).rolling(
            Static.date_interval_num_orders, closed="left").count().reset_index()[GetColumns.order_status]
    order_details[GetColumns.order_for_7_days] = \
        order_details[GetColumns.order_for_7_days].fillna(
            f"No orders placed in the last {Static.date_interval_num_orders} days")
    return order_details


# Returns a dataframe with the column <customer_id_has_paid>,
# a boolean value that represents if the customer has paid prior to this order
def get_payment_status(order_details):
    exempt_current_orders = order_details.groupby(GetColumns.customer_id).first()[GetColumns.order_id]
    prior_orders_paid = \
        order_details[~order_details[GetColumns.order_id].isin(exempt_current_orders)].groupby(GetColumns.order_status)[
            GetColumns.customer_id].agg(set).drop('paid')
    try:
        all_unpaid_customers = prior_orders_paid[0].union(prior_orders_paid[1])
    except:
        all_unpaid_customers = prior_orders_paid[0]
    order_details[GetColumns.customer_id_has_paid] = [customer_id not in all_unpaid_customers for customer_id in
                                                      order_details[GetColumns.customer_id]]
    return order_details


# Returns a dataframe with the column <shop_id_count_paid_orders_90D>,
# that represents the number of paid orders on shop id in the last 90 days
# In case the shop_id doesnt any paid paid order in the given the interval, the column value defaults to
# `No Paid Orders in the last 90 days`
def get_shop_id_count_paid_orders_90d(order_details):
    order_details["if_paid"] = np.where(order_details["order_status"] == 'paid', 1, 0)

    shop_id_count_paid_orders_90D = \
        order_details.set_index("created_date").groupby(["shop_id"]).rolling("90D", closed="left") \
            .sum().reset_index() \
            .fillna(0)
    order_details[GetColumns.shop_id_count_paid_orders_90D] = \
        shop_id_count_paid_orders_90D.groupby(["shop_id", "created_date"])["if_paid"].transform('sum')
    order_details[GetColumns.shop_id_count_paid_orders_90D] = \
        order_details[GetColumns.shop_id_count_paid_orders_90D].fillna(
            f"No Paid Orders in the last {Static.date_interval_paid_orders} days")
    order_details.drop(["if_paid"], axis=1, inplace=True)

    return order_details


# writes output data to path
def write_data(out_data, path):
    out_data.to_csv(path)


if __name__ == '__main__':
    static = Static()
    data = static.get_order_details()
    data = get_payment_status(data)
    data = get_orders_for_time_delta(data)
    data = get_shop_id_count_paid_orders_90d(data)

    write_data(data, static.output_path + '/' + static.out_table_name)
