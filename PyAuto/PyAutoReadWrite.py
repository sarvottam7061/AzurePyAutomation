import pandas as pd
import json
from PyAuto.PyAutoSmartData import SmartData

try:
    from config import TestConfig as config
    test_data_path = config.testDataPath
except:
    test_data_path = None


class ReadWrite:

    def __init__(self, filePath, fileName):
        # Create a readwriter
        self.filePath = filePath
        self.fileName = fileName

    def load_excel(self, sheetName="General"):
        """
        Load an excel sheet into pandas data frame to access it in future

            Args:
                sheetName: defaults to General(from test data sheet), can be overridden to value passed

            Returns: returns the data frame as excel sheet

        """
        if sheetName == "General":
            td = pd.read_excel(self.filePath + self.fileName, sheet_name="General",
                               index_col="Test Case ID", dtype=str)
            return td
        else:
            td = pd.read_excel(self.filePath + self.fileName, sheet_name=sheetName, dtype=str)
            return td

    @staticmethod
    def get_parametrized_values_excel(td):
        """
        Returns data to pytest.mark.parametrize from excel sheet dataframe.

            Args:
                td: pandas dataframe, returned after loading an excel sheet.

            Returns: returns parametrized data required for data driven execution , list of list.

        """
        td_run = td[(td['Run'] == "yes") | (td['Run'] == "Yes") | (td['Run'] == "YES")]
        td_drop_run = td_run.drop(['Run'], axis=1)
        # data_from_excel = SmartData.generate_from_excel(td_drop_run.to_records(index=False))
        return td_drop_run.to_records(index=False) #[(Test, Tester, ..),()]
        # return data_from_excel

    @staticmethod
    def read_excel_cell_General(td, tc_id, column_name):
        """
        To read an excel cell from TestData.xlsx general sheet

            Args:
                td: data frame loaded from TestData.xlsx -> general sheet
                tc_id: Case id from TestData.xlsx -> general sheet
                column_name: Column name of TestData.xlsx -> general sheet

            Returns: String value from the cells

        """
        return td[column_name][tc_id]

    @staticmethod
    def read_excel_cell_row_column(td, row_index, column_name):
        """
        Read excel cell by passing the row index and column name

            Args:
                td: pandas dataframe loaded from excel sheet
                row_index: index number of the rows
                column_name: name of the column

            Returns: The cell value based on the row index and column name passed

        """
        return td[column_name][row_index]

    @staticmethod
    def set_value_excel_cell(td, row_num, column_name, value):
        """
        Set the value of a dataframe returned from excel load

            Args:
                td: pass data frame returned from excel
                row_num: pass the row number in which value has to be set
                column_name: pass the column name in which value has to be set
                value: pass the value to be set

            Returns: return the Data frame after setting the value passed

        """
        td[column_name][row_num] = value
        return td

    @classmethod
    def write_excel(cls, td, write_file_name, write_sheet_name, filePath=test_data_path, include_index=False):
        """
        Write the data frame to excel sheet

            Args:
                td: data frame returned after loading an excel sheet
                write_file_name: file name of the excel work book
                write_sheet_name: sheet name of the excel sheet
                filePath: path to save excel file in, defaults to test data path in pyautomation framework, if using
                          pyauto package, the default value is None and should be overridden if not the excel file
                          to be saved in same folder
                include_index: defaults to false, is the index to be included in excel sheet

            Returns: returns nothing

        """
        if filePath is None:
            writer = pd.ExcelWriter(write_file_name, engine='xlsxwriter')
        else:
            writer = pd.ExcelWriter(filePath + write_file_name, engine='xlsxwriter')
        td.to_excel(writer, sheet_name=write_sheet_name, index=include_index)
        writer.save()

    def load_json(self):
        """
        Loads the json file based on the filepath and name assigned using ReadWrite object

            Returns: returns the json data read from file

        """
        with open(self.filePath + self.fileName) as json_file:
            data = json.load(json_file)
        return data

    @classmethod
    def load_json_file(cls, path_to_file):
        """
        Class method to load json file and return json data

            Args:
                path_to_file: complete path to the file

            Returns: returns json data from file

        """
        with open(path_to_file) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def get_parametrized_values_json(data, TC_ID):
        """
        Returns data to pytest.mark.parametrize from json data

            Args:
                data: Test Data loaded from TestData.json
                TC_ID: Test case id for Data driven execution

            Returns: returns list of rows from the test data json file suitable for data driven execution

        """
        list_of_values = []
        for i in data[TC_ID]:
            if i['run'].lower() == "yes":
                i.pop('run')
                list_of_values.append(tuple(i.values()))
        return list_of_values

    @staticmethod
    def read_json_value(data, TC_ID, index_num, keyValue):
        """
        Read json value from the TC_ID and index num and key value

            Args:
                data: json data read from a file
                TC_ID: TC_ID of execution
                index_num: from different records of the data from the same test
                keyValue: key value to be parsed

            Returns:

        """
        return data[TC_ID][index_num], [keyValue]

    @staticmethod
    def set_value_json(data, key, value):
        """
        Alter the value of json data based on the key and value passed

            Args:
                data: json to be altered
                key: position of json to alter
                value: value to be assigned for the key

            Returns: returns altered data

        """
        data[key] = value
        return data


    def write_json(self, json_data, fileName, filePath=test_data_path):
        """
        write json_data in given file.

            Args:
                json_data:data to write in the file
                fileName:jason file name, should be end with.json
                filePath: set to `config.testDataPath, file path to json file

            Returns: None, does not return anything

        """
        if filePath:
            with open(filePath + fileName, 'w') as f:
                json.dump(json_data, f)
        else:
            with open(fileName, 'w') as f:
                json.dump(json_data, f)
        return self

