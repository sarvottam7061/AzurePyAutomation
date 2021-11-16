import pandas as pd
import allure
import sqlalchemy

try:
    from config import TestConfig as config
    test_data_path = config.testDataPath
except:
    test_data_path = None


class PySQLDatabase:

    def __init__(self, connection):
        """
        Reusable functions for testing database

            Args:
                connection: database engine connection
        """
        self.con = connection
        self.recordset = None
        self.recordset_df = None

    def execute_query(self, query):
        """
        Execute a query and save the result in self.recordset

            Args:
                query: any valid sql query

            Returns: returns the PySQLDatabase object to facilitate method chaining.


        """
        self.recordset = self.con.execute(query)
        return self

    def query_save_data_frame(self, query):
        """
        Function to save the query result as a pandas dataframe in self.recodset_df

            Args:
                query: any valid sql query

            Returns: returns the PySQLDatabase object to facilitate method chaining.

        """
        self.recordset_df = pd.read_sql_query(query, self.con)
        return self

    def table_save_data_frame(self, table_name):
        """
        Function to save the complete table as a dataframe in self.recordset_df

            Args:
                table_name: valid table name from the database

            Returns: returns the PySQLDatabase object to facilitate method chaining.

        """
        self.recordset_df = pd.read_sql_table(table_name, self.con)
        return self

    def check_if_exists(self, query=None):
        """
        Check if any row exists after executing the query passed or already existing query.

            Args:
                query: defaults to None, when None the result from previously executed query is taken

            Returns: returns the PySQLDatabase to facilitate method chaining.

        """
        if query is not None:
            self.execute_query(query)
        if len(self.recordset.fetchall()):
            with allure.step("The record exists after executing the query"):
                assert True
        else:
            with allure.step("The records does not exist after executing the query"):
                assert False

        return self

    def execute_queries_from_file(self, file_name, file_path=test_data_path):
        """
        Execute list of queries from a sql file, to create the test environment before execution.

            Args:
                file_name: name to the .sql file.
                file_path: path to the sql file folder, defaults to test data path in pyautomation
                           framework, if using pyauto package, the default value is None and should be
                           overridden if not the query file is present in same folder as execution.

            Returns: returns the PySQLDatabase object to facilitate
                         method chaining.

        """
        if file_path:
            with open(file_path + file_name, 'rb') as file:
                query = sqlalchemy.sql.text(file)
        else:
            with open(file_name, 'rb') as file:
                query = sqlalchemy.sql.text(file)
        self.execute_query(query)
        return self

    def get_row_count(self, query=None):
        """
        Get the row count for the query passed or already executed query

            Args:
                query: valid query to be executed, defaults to None. When None, previously executed query will be taken.

            Returns: returns the total number of row count.

        """
        if query is not None:
            self.execute_query(query)
        return len(self.recordset.fetchall())

    def row_count_is_zero(self, query=None):
        """
        Validate the row count for the query passed or already executed query is zero or no results from query.

            Args:
                query: valid query to be executed, defaults to None. When None, previously executed query will be taken

            Returns: returns the PySQLDatabase object to facilitate method chaining.

        """
        if query is not None:
            self.execute_query(query)
        row_num = len(self.recordset.fetchall())
        assert row_num == 0, f'There are records retrieved from the query and is number is {row_num}'
        return self

    def row_count_equal_to(self, expected_row_num, query=None):
        """
        Validate the row count for the query passed or already executed query is equal to expected_row_num.

            Args:
                expected_row_num: The expected count of rows after executing query.
                query: valid query to be executed, defaults to None. When None,
                       previously executed query will be taken

            Returns: returns the PySQLDatabase object to facilitate method chaining

        """
        if query is not None:
            self.execute_query(query)
        row_num = len(self.recordset.fetchall())
        assert row_num == expected_row_num, f'The number of records {row_num} is not same as expected row num {expected_row_num}'
        return self
