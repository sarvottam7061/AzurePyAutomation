from selenium.webdriver.common.keys import Keys

from PyAuto.PyAutoDesktop import PyAutoWindows


class PosDemo(PyAutoWindows):
    locatorCheckout = {"title": "Checkout", "auto_id": "orderBtn"}
    locatorCoffee = {"title": "Coffee"}
    locatorIceCream = {"title": "Ice Cream Cone"}
    locatorCake = {"title": "Cheese Cake"}
    locatorCupCake = {"title": "Cupcake"}
    locatorCookies = {"title": "Cookies"}
    locatorEspresso = {"title": "Espresso"}
    locatorCappuccino = {"title": "Cappuccino"}
    locatorCardNum = {"auto_id": "CardDataBox"}
    locatorOk = {"title": "OK"}
    locatorCashOk = {"title": "Ok"}
    locatorCredit = {"title": "Credit", "auto_id": "CreditButton"}
    locatorCash = {"title": "Cash", "auto_id": "CashButton"}
    locatorPayment = {"title": "$20.00", "auto_id": "twentyButton"}
    locatorSearchBox = {"title": "Item # or Item Name", "auto_id": "TextBox"}

    def __init__(self, app):
        super().__init__(app)  # call super class constructor

    def checkout_order_credit(self, card_num):
        self.find_element_wait(self.locatorCheckout).click()
        self.find_element_wait(self.locatorCoffee).click()
        self.find_element_wait(self.locatorIceCream).click()
        self.find_element_wait(self.locatorCake).click()
        self.find_element_wait(self.locatorCappuccino).click()
        self.find_element_wait(self.locatorCookies).click()
        self.find_element_wait(self.locatorCupCake).click()
        self.find_element_wait(self.locatorCredit).click()
        self.wait_enter_text(self.locatorCardNum, card_num)
        self.find_element_wait(self.locatorOk).click()

    def checkout_order_cash(self):
        self.find_element_wait(self.locatorCheckout).click()
        self.find_element_wait(self.locatorSearchBox).send_keys("Cupcake", Keys.ENTER)#.send_keys(Keys.ENTER)
        self.find_element_wait(self.locatorSearchBox).send_keys("Cookies", Keys.ENTER)#.send_keys(Keys.ENTER)
        self.find_element_wait(self.locatorSearchBox).send_keys("Espresso", Keys.ENTER)#.send_keys(Keys.ENTER)
        self.find_element_wait(self.locatorCoffee).click()
        self.find_element_wait(self.locatorIceCream).click()
        self.find_element_wait(self.locatorCake).click()
        self.click_wait_locator(self.locatorCappuccino)
        self.click_wait_locator(self.locatorCash)
        self.click_wait_locator(self.locatorPayment)
        self.find_element_wait(self.locatorCashOk).click()
