import sqlite3
from config import TestConfig as config
from PyAuto.PyAutoLogger import get_logger
from lxml import etree
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PyAuto.PyAutoException import PyAutoExceptions
import allure
import math

logger = get_logger()

js_style = """
var proto = Element.prototype;
var slice = Function.call.bind(Array.prototype.slice);
var matches = Function.call.bind(proto.matchesSelector || 
                proto.mozMatchesSelector || proto.webkitMatchesSelector ||
                proto.msMatchesSelector || proto.oMatchesSelector);

// Returns true if a DOM Element matches a cssRule
var elementMatchCSSRule = function(element, cssRule) {
  return matches(element, cssRule.selectorText);
};

// Returns true if a property is defined in a cssRule
var propertyInCSSRule = function(prop, cssRule) {
  return prop in cssRule.style && cssRule.style[prop] !== "";
};
const styleSheets = Array.from(document.styleSheets).filter(
      (styleSheet) => !styleSheet.href || styleSheet.href.startsWith(window.location.origin)
    );
// Here we get the cssRules across all the stylesheets in one array
var cssRules = slice(styleSheets).reduce(function(rules, styleSheet) {
  return rules.concat(slice(styleSheet.cssRules));
}, []);
var getAppliedCss = function(elm) {
// get only the css rules that matches that element
var elementRules = cssRules.filter(elementMatchCSSRule.bind(null, elm));
var rules =[];
if(elementRules.length) {
for(i = 0; i < elementRules.length; i++) {
var e = elementRules[i];
rules.push({
    order:i,
    text:e.cssText
})
}
}
if(elm.getAttribute('style')) {
rules.push({
    order:elementRules.length,
    text:elm.getAttribute('style')
})
}
return rules;
}

var rules = getAppliedCss(arguments[0]);

return rules

"""


def connect_db():
    """
            Connect to the object repository db

                Args:
                    None

                Returns: returns the connection object

            """
    # logger.warning(config.object_repo_path)
    conn = sqlite3.connect(config.object_repo_path)
    return conn


def close_db(conn):
    """
             Connect to the object repository db

                 Args:
                     conn: connection object for object repository db

                 Returns: None

             """
    conn.close()


def insert_elements(values_passed):
    """
             To insert elements into object repository db

                 Args:
                     values_passed:

                 Returns: returns the connection object

             """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO elements(page_name, element_name, locators)
                VALUES(?, ?, ?)""", values_passed)
    except:
        cur.execute("""UPDATE elements SET locators = ?
                        WHERE page_name = ? and element_name = ?""",
                    (values_passed[2], values_passed[0], values_passed[1]))
    conn.commit()
    close_db(conn)


def get_elements(values_passed):
    """
                 Get elements from the object repo db

                     Args:
                         values_passed: tuple of (page_name, element_name)

                     Returns: returns one row of details about the element

                 """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT html_element, co_ordinates, window_size, css_style FROM elements
        WHERE page_name= ? and element_name = ?
        """, values_passed)
        row = cur.fetchone()
        close_db(conn)
    except:
        close_db(conn)
        row = None
    return row


def update_elements(values_passed):
    """
                 To update element values in object repository db

                     Args:
                         values_passed: tuple of html_element, co_ordinates, window_size, css_style, page_name
                                        and element_name

                     Returns: True for successful completion, False for issues

                 """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""UPDATE elements SET html_element = ?, co_ordinates =?, window_size = ?, css_style = ?
                        WHERE page_name = ? and element_name = ?""", values_passed)
        conn.commit()
        close_db(conn)
    except InterfaceError:
        close_db(conn)
        logger.error("Unable to update page elements for " + str(values_passed))
        return False
    except:
        logger.error("Something went wrong while updating " + str(values_passed))
        return False
    return True


def update_elements_healed_xpath(values_passed):
    """
                 Updates healed xpath value in the elements table

                     Args:
                         values_passed: tuple of healed_xpath, page_name and element_name

                     Returns: returns True for successful completion and False for any failure

                 """

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""UPDATE elements SET healed_xpath = ?
                        WHERE page_name = ? and element_name = ?""", values_passed)
        conn.commit()
        close_db(conn)
    except InterfaceError:
        close_db(conn)
        logger.error("Unable to update page elements for " + str(values_passed))
        return False
    except:
        logger.error("Something went wrong while updating " + str(values_passed))
        return False
    return True


def class_attributes(obj):
    """
                 retrieves all the attributes to be saved in your db

                     Args:
                         obj: pass self from your class file you need to save it

                     Returns: None

                 """
    page_name = obj.__class__.__name__
    for attribute in obj.__class__.__dict__.keys():
        if attribute[:2] != '__':
            value = getattr(obj, attribute)
            if not callable(value):
                insert_elements((page_name, attribute, str(value)))


def heal_element(obj, locatorList, page_source):
    """
                 heal the element that is not found

                     Args:
                         values_passed: self object from your class, list of locators to be compared against, and page source

                     Returns: returns the healed xpath

                 """

    page_name = obj.__class__.__name__
    element_name = None
    for attribute in obj.__class__.__dict__.keys():
        if attribute[:2] != '__':
            value = getattr(obj, attribute)
            if not callable(value):
                if value == locatorList:
                    element_name = attribute
                    break
    html_element, co_ordinate, window_size, css_style = get_elements((page_name, element_name))
    if html_element:
        # logger.warning(html_element+co_ordinate)
        # soup = BeautifulSoup(page_source, "lxml")
        # total_element = [str(tag) for tag in soup.find_all()]
        dom = etree.HTML(page_source)
        tree = etree.ElementTree(dom)
        all_elements = [etree.tostring(dom_element, encoding="unicode") for dom_element in dom.iter()]
        elements = process.extract(html_element, all_elements, limit=3, scorer=fuzz.token_sort_ratio)
        if elements[0][1] == 0:
            raise PyAutoExceptions("Unable to identify the element during self healing. Check if you are trying to find the \
                                    element in right page")
        # match_ratio = []
        # for i in total_element:
        #     ratio = fuzz.token_sort_ratio(i, html_element)
        #     match_ratio.append(ratio)
        # max_value = max(match_ratio)
        # element_index_found = [i for i, j in enumerate(match_ratio) if j == max_value]
        # if len(element_index_found) == 1:
        #     healed_element = total_element[element_index_found[0]]
        # else:
        #     pass
        xpath_elements = []
        element_indexes = []
        if (elements[0][1] / 100) < config.healing_score:
            raise PyAutoExceptions(
                f"""The elements found has healing score:{(elements[0][1] / 100)} lesser than threshold provided in config file,
                    try reducing the healing score or validate if the element is present in the page""")
        for element in elements:
            element_index = all_elements.index(element[0])
            #     healed_xpath = tree.getpath(all_elements[element_index])
            element_indexes.append(element_index)
        dom_elements = [dom for dom in dom.iter()]
        for i in element_indexes:
            healed_xpath = tree.getpath(dom_elements[i])
            xpath_elements.append(healed_xpath)
        # for element in elements:
        #     if (element[1]/100)>config.healing_score:
        #         search_html = etree.HTML(element[0])
        #         dom = etree.HTML(page_source)
        #         tree = etree.ElementTree(dom)
        #         for dom_element in dom.iter():
        #             if dom_element.attrib == search_html[0][0].attrib:
        #                 if dom_element.tag == search_html[0][0].tag:
        #                     if dom_element.text.strip().lower() == search_html[0][0].text.strip().lower():
        #                         healed_xpath = tree.getpath(dom_element)
        #                         xpath_elements.append(healed_xpath)
        #     else:
        #         raise PyAutoExceptions(
        #             "The elements found has less healing score, try reducing the healing score or validate if the element is present in the page")
        # logger.warning(xpath_elements)
        # logger.warning(elements)
        # logger.warning(element_indexes)
        healed_xpath = None
        if len(xpath_elements) == 3:
            if elements[0][1] - elements[1][1] >= 3 and elements[0][1] - elements[2][1] >= 3:
                healed_xpath = xpath_elements[0]
                healed_web_element = obj.driver.find_element_by_xpath(healed_xpath)
                obj.driver.execute_script(
                    "arguments[0].setAttribute('style', 'background:  #ffcccb; border: 2px solid red;');",
                    healed_web_element)
                with allure.step(f"Healing the element selectors for {element_name} in {page_name}"):
                    with allure.step(f"healed element xpath {xpath_elements[0]}, healing score: {elements[0][1]}"):
                        pass
                    with allure.step("other xpath suggestions:"):
                        pass
                    with allure.step(f"Suggestion 1: {xpath_elements[1]}, healing score: {elements[1][1]}"):
                        pass
                    with allure.step(f"Suggestion 2: {xpath_elements[2]}, healing score: {elements[2][1]}"):
                        pass
                    allure.attach(obj.driver.get_screenshot_as_png(),
                                  name='healed_element',
                                  attachment_type=allure.attachment_type.PNG)
            elif elements[0][1] - elements[1][1] < 3:
                healed_web_element1 = obj.driver.find_element_by_xpath(xpath_elements[0])
                healed_web_element2 = obj.driver.find_element_by_xpath(xpath_elements[1])
                css_style1 = obj.driver.execute_script(js_style, healed_web_element1)
                css_style2 = obj.driver.execute_script(js_style, healed_web_element2)
                element1 = fuzz.token_sort_ratio(css_style, css_style1)
                element2 = fuzz.token_sort_ratio(css_style, css_style2)
                if element1 >= element2:
                    healed_xpath = xpath_elements[0]
                    healed_web_element = obj.driver.find_element_by_xpath(xpath_elements[0])
                    obj.driver.execute_script(
                        "arguments[0].setAttribute('style', 'background:  #ffcccb; border: 2px solid red;');",
                        healed_web_element)
                    with allure.step(f"Healing the element selectors for {element_name} in {page_name}"):
                        with allure.step(f"healed element xpath {xpath_elements[0]}, healing score: {elements[0][1]}"):
                            pass
                        with allure.step("other xpath suggestions:"):
                            pass
                        with allure.step(f"Suggestion 1: {xpath_elements[1]}, healing score: {elements[1][1]}"):
                            pass
                        with allure.step(f"Suggestion 2: {xpath_elements[2]}, healing score: {elements[2][1]}"):
                            pass
                        # logger.info(
                        #     f"healed element xpath {xpath_elements[0]}, healing score: {elements[0][1]}")
                        # logger.info("other xpath suggestions:")
                        # logger.info(f"Suggestion 1: {xpath_elements[1]}, healing score: {elements[1][1]}")
                        # logger.info(f"Suggestion 2: {xpath_elements[2]}, healing score: {elements[2][1]}")
                        allure.attach(obj.driver.get_screenshot_as_png(),
                                      name='healed_element',
                                      attachment_type=allure.attachment_type.PNG)
                else:
                    healed_xpath = xpath_elements[1]
                    healed_web_element = obj.driver.find_element_by_xpath(xpath_elements[1])
                    obj.driver.execute_script(
                        "arguments[0].setAttribute('style', 'background:  #ffcccb; border: 2px solid red;');",
                        healed_web_element)
                    with allure.step(f"Healing the element selectors for {element_name} in {page_name}"):
                        with allure.step(f"healed element xpath {xpath_elements[1]}, healing score: {elements[1][1]}"):
                            pass
                        with allure.step("other xpath suggestions:"):
                            pass
                        with allure.step(f"Suggestion 1: {xpath_elements[0]}, healing score: {elements[0][1]}"):
                            pass
                        with allure.step(f"Suggestion 2: {xpath_elements[2]}, healing score: {elements[2][1]}"):
                            pass
                        # logger.info(f"healed element xpath {xpath_elements[1]}, healing score: {elements[1][1]}")
                        # logger.info("other xpath suggestions:")
                        # logger.info(f"Suggestion 1: {xpath_elements[0]}, healing score: {elements[0][1]}")
                        # logger.info(f"Suggestion 2: {xpath_elements[2]}, healing score: {elements[2][1]}")
                        allure.attach(obj.driver.get_screenshot_as_png(),
                                      name='healed_element',
                                      attachment_type=allure.attachment_type.PNG)
            else:
                healed_web_element1 = obj.driver.find_element_by_xpath(xpath_elements[0])
                healed_web_element2 = obj.driver.find_element_by_xpath(xpath_elements[1])
                healed_web_element3 = obj.driver.find_element_by_xpath(xpath_elements[2])
                css_style1 = obj.driver.execute_script(js_style, healed_web_element1)
                css_style2 = obj.driver.execute_script(js_style, healed_web_element2)
                css_style3 = obj.driver.execute_script(js_style, healed_web_element3)
                element1 = fuzz.token_sort_ratio(css_style, css_style1)
                element2 = fuzz.token_sort_ratio(css_style, css_style2)
                element3 = fuzz.token_sort_ratio(css_style, css_style3)
                decision_factor = (element1 - element2 > 5 and element1 - element3 > 5) or \
                                  (element2 - element1 > 5 and element2 - element3 > 5) or \
                                  (element3 - element1 > 5 and element3 - element2 > 5)
                if decision_factor:
                    new_elements = [element1, element2, element3]
                    index = new_elements.index(max(new_elements))
                    healed_xpath = xpath_elements[index]
                    healed_web_element = obj.driver.find_element_by_xpath(xpath_elements[index])
                    obj.driver.execute_script(
                        "arguments[0].setAttribute('style', 'background:  #ffcccb; border: 2px solid red;');",
                        healed_web_element)
                    with allure.step(
                            f"healed element xpath {xpath_elements[index]}, healing score: {elements[index][1]}"):
                        with allure.step(f"healed element xpath {xpath_elements[0]}, healing score: {elements[0][1]}"):
                            pass
                        # logger.info(
                        #     f"healed element xpath {xpath_elements[index]}, healing score: {elements[index][1]}")
                        other_elements = xpath_elements.copy()
                        other_elements.remove(index)
                        other_elements_score = elements.copy()
                        other_elements_score.remove(index)
                        with allure.step("other xpath suggestions:"):
                            pass
                        with allure.step(
                                f"Suggestion 1: {other_elements[0]}, healing score: {other_elements_score[0][1]}"):
                            pass
                        with allure.step(
                                f"Suggestion 2: {other_elements[1]}, healing score: {other_elements_score[1][1]}"):
                            pass
                        # logger.info("other xpath suggestions:")
                        # logger.info(f"Suggestion 1: {other_elements[0]}, healing score: {other_elements_score[0][1]}")
                        # logger.info(f"Suggestion 2: {other_elements[1]}, healing score: {other_elements_score[1][1]}")
                        allure.attach(obj.driver.get_screenshot_as_png(),
                                      name='healed_element',
                                      attachment_type=allure.attachment_type.PNG)
                else:
                    current_window_size = obj.driver.get_window_size()
                    x_y_coord1 = int(healed_web_element1.rect['x']) * window_size['width'] // current_window_size[
                        'width'], \
                                 int(healed_web_element1.rect['y']) * window_size['height'] // current_window_size[
                                     'height']
                    x_y_coord2 = int(healed_web_element2.rect['x']) * window_size['width'] // current_window_size[
                        'width'], \
                                 int(healed_web_element2.rect['y']) * window_size['height'] // current_window_size[
                                     'height']
                    x_y_coord3 = int(healed_web_element3.rect['x']) * window_size['width'] // current_window_size[
                        'width'], \
                                 int(healed_web_element3.rect['y']) * window_size['height'] // current_window_size[
                                     'height']
                    distance1 = math.dist(x_y_coord1, [co_ordinate['x'], co_ordinate['y']])
                    distance2 = math.dist(x_y_coord2, [co_ordinate['x'], co_ordinate['y']])
                    distance3 = math.dist(x_y_coord3, [co_ordinate['x'], co_ordinate['y']])
                    new_elements_dist = [distance1, distance2, distance3]
                    index = new_elements_dist.index(min(new_elements_dist))
                    healed_xpath = xpath_elements[index]
                    healed_web_element = obj.driver.find_element_by_xpath(xpath_elements[index])
                    obj.driver.execute_script(
                        "arguments[0].setAttribute('style', 'background:  #ffcccb; border: 2px solid red;');",
                        healed_web_element)
                    with allure.step(f"Healing the element selectors for {element_name} in {page_name}"):
                        with allure.step(
                                f"healed element xpath {xpath_elements[index]}, healing score: {elements[index][1]}"):
                            pass
                        # logger.info(
                        #     f"healed element xpath {xpath_elements[index]}, healing score: {elements[index][1]}")
                        other_elements = xpath_elements.copy()
                        other_elements.remove(index)
                        other_elements_score = elements.copy()
                        other_elements_score.remove(index)
                        with allure.step("other xpath suggestions:"):
                            pass
                        with allure.step(
                                f"Suggestion 1: {other_elements[0]}, healing score: {other_elements_score[0][1]}"):
                            pass
                        with allure.step(
                                f"Suggestion 2: {other_elements[1]}, healing score: {other_elements_score[1][1]}"):
                            pass
                        # logger.info("other xpath suggestions:")
                        # logger.info(f"Suggestion 1: {other_elements[0]}, healing score: {other_elements_score[0][1]}")
                        # logger.info(f"Suggestion 2: {other_elements[1]}, healing score: {other_elements_score[1][1]}")
                        allure.attach(obj.driver.get_screenshot_as_png(),
                                      name='healed_element',
                                      attachment_type=allure.attachment_type.PNG)
        else:
            healed_xpath = xpath_elements[0]
            healed_web_element = obj.driver.find_element_by_xpath(xpath_elements[0])
            obj.driver.execute_script(
                "arguments[0].setAttribute('style', 'background:  #ffcccb; border: 2px solid red;');",
                healed_web_element)
            with allure.step(f"Healing the element selectors for {element_name} in {page_name}"):
                with allure.step(f"healed element xpath {xpath_elements[0]}, healing score: {elements[0][1]}"):
                    pass
                allure.attach(obj.driver.get_screenshot_as_png(),
                              name='healed_element',
                              attachment_type=allure.attachment_type.PNG)
                try:
                    with allure.step("other xpath suggestions:"):
                        pass
                    with allure.step(f"Suggestion 1: {xpath_elements[1]}, healing score: {elements[1][1]}"):
                        pass
                    with allure.step(f"Suggestion 2: {xpath_elements[2]}, healing score: {elements[2][1]}"):
                        pass
                    # logger.info("other xpath suggestions:")
                    # logger.info(f"Suggestion 1: {xpath_elements[1]}, healing score: {elements[1][1]}")
                    # logger.info(f"Suggestion 2: {xpath_elements[2]}, healing score: {elements[2][1]}")
                except:
                    logger.warning(f"No other elements found")
        update_elements_healed_xpath((healed_xpath, page_name, element_name))
        return healed_web_element
    else:
        raise PyAutoExceptions("To enable self healing, the locator should be valid the very first time it is being captured")


def update_page_element(obj, locatorList, html_element, co_ordinates, window_size, css_style):
    """
                     update the page elements with details passed from your test

                         Args:
                             values_passed: self object from your class, list of locators to be compared against, and page source

                         Returns: returns the healed xpath

                     """
    page_name = obj.__class__.__name__
    element_name = None
    for attribute in obj.__class__.__dict__.keys():
        if attribute[:2] != '__':
            value = getattr(obj, attribute)
            if not callable(value):
                if value == locatorList:
                    element_name = attribute
                    break
    update_elements((html_element, co_ordinates, window_size, css_style, page_name, element_name))


def get_last_healed_xpath(obj, locatorList):
    """
                         get the last healed xpath

                             Args:
                                 obj: self object from the class
                                 locatorList: list of locators for the element

                             Returns: return the healed element xpath from history

                         """
    page_name = obj.__class__.__name__
    element_name = None
    for attribute in obj.__class__.__dict__.keys():
        if attribute[:2] != '__':
            value = getattr(obj, attribute)
            if not callable(value):
                if value == locatorList:
                    element_name = attribute
                    break
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT healed_xpath FROM elements
            WHERE page_name= ? and element_name = ?
            """, (page_name, element_name))
        row = cur.fetchone()
        close_db(conn)
    except:
        close_db(conn)
        row = None
    return row