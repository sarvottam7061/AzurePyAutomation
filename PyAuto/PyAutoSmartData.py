import json

import pandas as pd
import rstr
from faker import Faker

import re

try:
    from config import TestConfig as config
    test_data_path = config.testDataPath
    resources_path = config.resourcesFolderPath
except:
    test_data_path = None


smart_data_pattern = r"\$\{([A-Za-z0-9|_]+)\}\$"
smart_search_pattern = r'\$[r]\{([\Wa-zA-Z0-9_]+)\}[r]\$'

language_dict = {'ar': 'ar_AA', 'es': 'es_ES', 'fr': 'fr_FR', 'it': 'it_IT', 'ja': 'ja_JP', 'ko': 'ko_KR',
                 'ta': 'ta_IN', 'zh': 'zh_CN', 'fa': 'fa_IR', 'hi': 'hi_IN'}


class SmartData:

    def write_smart_data_to_excel(self):
        df = pd.read_excel(config.testDataPath + config.testDataFileName, sheet_name=None)
        broken_name = config.testDataFileName.split(".")
        test_data_name = broken_name[0] + "_generated." + broken_name[1]
        excel_writer = pd.ExcelWriter(config.testDataPath + test_data_name)
        for sheet in df.keys():
            smart_df = df[sheet]
            if len(df[sheet]) > 0:
                smart_df = SmartData.generate_from_excel(df[sheet])
            smart_df.to_excel(excel_writer, sheet_name=sheet, index=False)

        excel_writer.save()
        return self

    def write_smart_data_to_json(self):
        f = open(config.testDataPath + config.testDataFileName, )
        json_data = json.load(f)
        for tc in json_data:
            if type(json_data[tc]) == str:
                json_data[tc] = SmartData.generate_from_json(json_data[tc])
            else:
                SmartData.break_till_element(json_data[tc])

        broken_name = config.testDataFileName.split(".")
        test_data_name = broken_name[0] + "_generated." + broken_name[1]
        # json_data_str = str(json_data).replace("'", "\"")
        json_data_str = json.dumps(json_data)
        # print(json_data_str)
        with open(config.testDataPath + test_data_name, "w") as outfile:
            outfile.write(str(json_data_str))
        return self

    @staticmethod
    def json_data_sequential(json_data):
        for tc in json_data:
            if type(json_data[tc]) == str:
                json_data[tc] = SmartData.generate_from_json(json_data[tc])
            else:
                SmartData.break_till_element(json_data[tc])
        return json_data


    @staticmethod
    def break_till_element(json_row):
        if type(json_row) == list:
            for element in json_row:
                for i in element:
                    if type(element[i]) == dict:
                        SmartData.break_till_element(element[i])
                    else:
                        element[i] = SmartData.generate_from_json(element[i])
                        # print(element[i])
        if type(json_row) == dict:
            for single_value in json_row:
                if type(json_row[single_value]) == dict:
                    SmartData.break_till_element(json_row[single_value])
                else:
                    json_row[single_value] = SmartData.generate_from_json(json_row[single_value])
                    # print(json_row[single_value])


    @staticmethod
    def get_custom_patterns_from_json():
        '''
        This function will get the json data from CustomPatters.json which contains regex patters to generate custom data

        Returns: content of CustomPatterns.json in dictionary format

        '''
        with open(resources_path+"CustomPatterns.json") as patterns_file:
            custom_patterns_dict = json.load(patterns_file)
        return custom_patterns_dict

    @staticmethod
    def generate_smart_data(func_name, locale='en_US'):
        '''
        Generates Smart Data from Faker class according to the function name provided.

        Args:
            func_name: Name of the faker function required to generate the data
            locale: Language/Region specific data can be generated (By default locale is English_US)

        Returns: generated smart-data in string

        '''
        fake = Faker(locale)
        try:
            class_method = getattr(fake, func_name)()
            return class_method
        except:
            print(f"\nRequesting Smart-Data for \"{func_name}\" is not valid.")
            return func_name

    @staticmethod
    def generate_from_excel(data_from_excel):
        '''
        Will get the data from excel file and parse the smart data.

        Args:
            data_from_excel: test data from excel suitable for data driven execution

        Returns: Modified excel data containing Smartly generated Data

        '''

        custom_patterns_data = SmartData.get_custom_patterns_from_json()

        # print(data_from_excel)
        for row in range(len(data_from_excel)):
            for col_name in list(data_from_excel):
                if data_from_excel["Run"][row] == "Yes" or data_from_excel["Run"][row] == "yes" or data_from_excel["Run"][row] == "YES":
                    cell = re.search(smart_data_pattern, str(data_from_excel[col_name][row]))
                    if cell is None:
                        try:
                            search_for_regex = re.search(smart_search_pattern, str(data_from_excel[col_name][row]))
                            if search_for_regex.group(1) in custom_patterns_data:
                                generated_result = rstr.xeger(custom_patterns_data.get(search_for_regex.group(1)))
                            else:
                                generated_result = rstr.xeger(search_for_regex.group(1))
                            data_from_excel.loc[row, col_name] = re.sub(smart_search_pattern, generated_result, str(data_from_excel[col_name][row]))
                        except:
                            continue
                    if cell is not None:
                        try:
                            if cell.group(1).lower().split("|")[1] in language_dict.keys():
                                data_from_excel.loc[row, col_name] = SmartData.generate_smart_data(cell.group(1).lower().split("|")[0], locale=cell.group(1).lower().split("|")[1])

                            elif cell.group(1).lower().split("|")[1] not in language_dict.keys():
                                # print(cell.group(1).lower().split("|")[1], "is not a valid language, making it as English.")
                                data_from_excel.loc[row, col_name] = SmartData.generate_smart_data(cell.group(1).lower().split("|")[0])
                        except:
                            data_from_excel.loc[row, col_name] = SmartData.generate_smart_data(cell.group(1).lower())
        return data_from_excel



    @staticmethod
    def generate_from_json(data_from_json):
        '''
        Will get the data from json file and parse the smart data.

        Args:
            data_from_json: test data from json suitable for data driven execution

        Returns: Modified json data containing Smartly generated Data


        '''

        custom_patterns_data = SmartData.get_custom_patterns_from_json()

        cell = re.search(smart_data_pattern, data_from_json)
        if cell is None:
            try:
                search_for_regex = re.search(smart_search_pattern, data_from_json)
                if search_for_regex.group(1) in custom_patterns_data:
                    generated_result = rstr.xeger(custom_patterns_data.get(search_for_regex.group(1)))
                else:
                    generated_result = rstr.xeger(search_for_regex.group(1))
                data_from_json = re.sub(smart_search_pattern, generated_result, data_from_json)
                return data_from_json
            except:
                return data_from_json

        if cell is not None:
            try:
                if cell.group(1).lower().split("|")[1] in language_dict.keys():
                    data_from_json = SmartData.generate_smart_data(cell.group(1).lower().split("|")[0], locale=cell.group(1).lower().split("|")[1])
                elif cell.group(1).lower().split("|")[1] not in language_dict.keys():
                    data_from_json = SmartData.generate_smart_data(cell.group(1).lower().split("|")[0])
            except:
                data_from_json = SmartData.generate_smart_data(cell.group(1).lower())
            return data_from_json

        # print(data_from_json)
        # for i in range(0, len(data_from_json)):
        #     for j in range(0, len(data_from_json[i])):
        #         data_from_json[i] = list(data_from_json[i])
        #         cell = re.search(smart_data_pattern, str(data_from_json[i][j]))
        #         if cell is None:
        #             try:
        #                 search_for_regex = re.search(smart_search_pattern, str(data_from_json[i][j]))
        #                 if search_for_regex.group(1) in custom_patterns_data:
        #                     generated_result = rstr.xeger(custom_patterns_data.get(search_for_regex.group(1)))
        #                 else:
        #                     generated_result = rstr.xeger(search_for_regex.group(1))
        #                 data_from_json[i][j] = re.sub(smart_search_pattern, generated_result, data_from_json[i][j])
        #             except:
        #                 continue
        #         if cell is not None:
        #             try:
        #                 if cell.group(1).lower().split("|")[1] in language_dict.keys():
        #                     data_from_json[i][j] = SmartData.generate_smart_data(cell.group(1).lower().split("|")[0], locale=cell.group(1).lower().split("|")[1])
        #
        #                 elif cell.group(1).lower().split("|")[1] not in language_dict.keys():
        #                     print(cell.group(1).lower().split("|")[1], "is not a valid language, making it as English.")
        #                     data_from_json[i][j] = SmartData.generate_smart_data(cell.group(1).lower().split("|")[0])
        #             except:
        #                 data_from_json[i][j] = SmartData.generate_smart_data(cell.group(1).lower())
        #     data_from_json[i] = tuple(data_from_json[i])


