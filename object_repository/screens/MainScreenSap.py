from PyAuto.PyAutoDesktop import PyAutoWindows


class MainScreen(PyAutoWindows):
    locatorNewItem = {"title": "New Item", "auto_id": "1070",
                      "class_name": "Button"}  # "xpath": "//*[@Name='New Item']"
    locatorNext = {"auto_id": "1535"}
    locatorDescription = {"auto_id": "8047", "title": "Description:",
                          "control_type": "Edit"}  # "title": "Description:",
    locatorApplicationServer = {"auto_id": "8072", "title": "Application Server:",
                                "control_type": "Edit"}  # "title": "Application Server:",
    locatorInstNum = {"auto_id": "8043", "title": "Instance Number:",
                      "control_type": "Edit"}  # "title": "Instance Number:",
    locatorSysId = {"auto_id": "8034", "title": "System ID:", "control_type": "Edit"}  # "title": "System ID:",
    locatorFinish = {"title": "Finish"}
    locatorConnectionType = {"title": "Connection Type:", "control_type": "ComboBox"}
    locatorCheckBox = {"auto_id": "8070", "control_type": "CheckBox"}
    locatorListView = {"auto_id": "1109"}
    locatorList = {"auto_id": "1008"}
    locatorList1 = {"title": "SAP 2AUTO"}
    locatorGetText = {"auto_id": "8026", "control_type": "Group"}
    locatorDropDown = {"auto_id": "1109"}
    locatorConnect = {"title": "SAP FICO", "control_type": "ListItem"}
    locatorSap7 = {"title": "SAP 7AUTO", "control_type": "ListItem"}
    # locatorDelete = {"title": "Delete ", "auto_id": "32782"}
    locatorTitle = {"control_type": "TitleBar"}  # , "auto_id": "TitleBar", "control_type": "TitleBar"
    locatorComboBox = {"auto_id": "1109", "control_type": "ComboBox"}
    locatorOpenButton = {"title": "Open", "control_type": "Button"}
    locatorCancel = {"title": "Cancel", "auto_id": "1007"}
    locatorMore = {"title": "More", "auto_id": "32798"}
    locatorDel = {"title": "Delete Item", "auto_id": "1023"}

    def __init__(self, app):
        super().__init__(app)  # call super class constructor

    def screen_shot_sap(self):
        self.take_screenshot("screenshot1")
        return self

    def check_child_of(self):
        res = self.is_child_of(self.locatorOpenButton, self.locatorComboBox)
        print(res)
        return self

    def right_click_element(self):
        self.right_click_at_element(self.locatorConnect)
        self.sleep(3)
        return self

    def right_click_at_given_coordinate(self):
        self.right_click_at_coordinate(300, 300)
        self.sleep(2)
        return self

    def drag_and_drop_window(self):
        self.mouse_drag_and_drop_by_offset(self.locatorTitle, 200, 100)
        self.sleep(2)
        return self

    def double_click_to_connect(self):
        self.double_click_element(self.locatorConnect)
        return self

    def get_the_list_items(self):
        count = self.get_list_item_count(self.locatorList)
        items = self.get_list_items(self.locatorList)
        print(count)
        print(items)
        return self

    def clear_description(self):
        self.wait_enter_text(self.locatorDescription, "SAP 8AUTO")
        self.clear_all_text(self.locatorDescription)
        return self

    def get_auto_id_finish(self):
        res = self.get_automation_id(self.locatorFinish)
        print(res)
        return self

    def check_text_should_be(self, text):
        ele = self.get_element_text(self.locatorGetText)
        print(ele)
        result = self.element_text_should_be(self.locatorGetText, text)
        self.find_element_wait(self.locatorCancel).click()
        print(result)
        return self

    def wait_till_application_server_visible(self):
        # manually move to new entry form
        self.navigate()
        self.wait_element_visibility(self.locatorApplicationServer).type_keys("204.87.89.45")
        self.sleep(3)
        self.find_element_wait(self.locatorCancel).click()
        return self

    def wait_enter_text_new_entry(self, description, app_server, inst_num, sys_id):
        self.wait_enter_text(self.locatorDescription, description)
        self.wait_enter_text(self.locatorApplicationServer, app_server)
        self.wait_enter_text(self.locatorInstNum, inst_num)
        self.wait_enter_text(self.locatorSysId, sys_id)
        self.wait_element_enabled(self.locatorNext).click()
        self.find_element_wait(self.locatorNext).click()
        self.find_element_wait(self.locatorFinish).click()

        return self

    def wait_next_enable(self):
        self.wait_enter_text(self.locatorDescription, "SAP 5AUTO")
        self.wait_enter_text(self.locatorApplicationServer, "183.87.89.45")
        self.wait_enter_text(self.locatorInstNum, "78")
        self.wait_enter_text(self.locatorSysId, "455") #enter by typing
        self.button_should_be_enabled(self.locatorNext)
        self.wait_element_enabled(self.locatorNext).click()
        self.find_element_wait(self.locatorNext).click()
        self.find_element_wait(self.locatorFinish).click()

        return self

    def wait_next_click(self):
        self.wait_enter_text(self.locatorDescription, "SAP 6AUTO")
        self.wait_enter_text(self.locatorApplicationServer, "183.87.89.45")
        self.wait_enter_text(self.locatorInstNum, "88")
        self.wait_enter_text(self.locatorSysId, "425")  # enter by typing
        self.click_wait_locator(self.locatorNext)
        self.find_element_wait(self.locatorNext).click()
        self.find_element_wait(self.locatorFinish).click()
        return self

    def navigate(self):
        print(self.get_parent_of_element(self.locatorNewItem))
        self.find_element_wait(self.locatorNewItem).click()
        self.find_element_wait(self.locatorNext).click()
        return self

    def navigate_to_list_view_dropdown(self):
        self.select_dropdown_value(self.locatorDropDown, "List View")
        return self

    def checkbox_element(self):
        self.checkbox_should_be_unchecked(self.locatorCheckBox)
        return self
