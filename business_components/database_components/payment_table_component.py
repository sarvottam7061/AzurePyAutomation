import allure
from object_repository.tables.payment_table import *
from PyAuto.PyAutoDatabase import PySQLDatabase
from PyAuto.PyAutoLogger import get_logger

logger = get_logger()  # gets the logger and adds log to allure reports


@allure.step("validate sum of all the amounts paid")
def sum_of_all_payments(connection):
    # to access the results use .recordset and fetchall() or fetchone() functions
    # fetch one will return only one row
    total_amount_record = PySQLDatabase(connection).execute_query(query_total_amount).recordset.fetchone()
    assert float(
        total_amount_record[0]) == 67416.5099999208, f"The sum of all payment is not equal {total_amount_record[0]} to 67416.5099999208"


@allure.step("validate number of payments with ")
def num_of_payment_greater_8(connection):
    # fetchall() will return multiple rows
    count_amount = PySQLDatabase(connection).execute_query(query_amount_greater_8).recordset.fetchall()
    assert count_amount[0][
               0] == 857, f"The count of records greater than 8 is {count_amount[0][0]} and not equal to 857"


@allure.step("validate average amount of payments made")
def payment_average(connection):
    average = PySQLDatabase(connection).execute_query(query_amount_average).recordset.fetchone()
    assert average[0] > 4, f"Average value {average[0]} is not greater than expected value 4"


@allure.step("validate number of payments between 5 and 10 usd")
def validate_payment_between(connection):
    num_of_payments = PySQLDatabase(connection).get_row_count(query=query_amount_between)
    assert num_of_payments == 3843, f"The row count retrieved {num_of_payments} does not match 3843"
