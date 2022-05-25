import unittest

import pandas as pd

from executors.src.main.main import get_payment_status, get_orders_for_time_delta, get_shop_id_count_paid_orders_90d


class MyTestCase(unittest.TestCase):
    data = {'order_id': ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            'customer_id': ["a", "b", "c", "a", "d", "f", "c", "b", "d"],
            'created_date': [pd.to_datetime('2022-05-15'), pd.to_datetime('2022-05-13'),
                             pd.to_datetime('2022-05-14'), pd.to_datetime('2022-05-11'),
                             pd.to_datetime('2022-05-07'), pd.to_datetime('2022-05-05'),
                             pd.to_datetime('2022-05-10'), pd.to_datetime('2022-05-09'),
                             pd.to_datetime('2022-05-05')],
            'order_amount': [1000, 200, 200, 4000, 1650, 600, 700, 450, 350],
            'shop_id': ["1000", "1001", "1000", "1003", "1002", "1001", "1002", "1003", "1001"],
            'order_status': ["paid", "due", "unpaid", "paid", "paid", "due", "unpaid", "unpaid", "unpaid"]

            }
    test_df = pd.DataFrame(data)

    def test_get_payment_status(self):
        customer_data = get_payment_status(self.test_df)
        self.assertEqual(set(customer_data[customer_data.customer_id_has_paid == True]["customer_id"]), {"a","f"})

    def test_get_orders_for_time_delta(self):
        customer_data = get_orders_for_time_delta(self.test_df)
        self.assertEqual(set(customer_data[customer_data.customer_id == "a"]["order_for_7_days"]),
                         {1.0, 'No orders placed in the last 7D days'})

    def test_get_shop_id_count_paid_orders_90d(self):
        customer_data = get_shop_id_count_paid_orders_90d(self.test_df)
        self.assertEqual(set(customer_data[customer_data.shop_id == "1002"]["shop_id_count_paid_orders_90D"]),
                         {0, 1})


if __name__ == '__main__':
    unittest.main()
