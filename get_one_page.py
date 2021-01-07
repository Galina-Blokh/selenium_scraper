import numpy as np
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from main import FILE_NAME, connect


def get_recipe(link):
    json_file = {}  # not real json because of utf-8 encoding
    ingredients_list = []
    instructions_list = []

    # create a driver
    recipe_driver = connect(link)
    # get ingredients
    try:
        result_ingr = recipe_driver.find_element_by_xpath('//*[@id="sr-recipe-callout"]/div[4]')
    except:

        WebDriverWait(recipe_driver, 5).until(EC.alert_is_present(), 'Timed out waiting for alerts to appear')
        alert = recipe_driver.switch_to.alert
        alert.accept()
        print("alert accepted")
        result_ingr = recipe_driver.find_element_by_xpath('//*[@id="sr-recipe-callout"]/div[4]')
    options_ingr = result_ingr.find_elements_by_tag_name("ul")
    if not options_ingr:
        result_ingr = recipe_driver.find_element_by_xpath('// *[ @ id = "sr-recipe-callout"] / div[3]')
        options_ingr = result_ingr.find_elements_by_tag_name("ul")
    for paragr in options_ingr:
        ingredients_list.append(paragr.text)
    # get instructions
    result_instr = recipe_driver.find_element_by_xpath(
        '//*[@id="sr-recipe-method"]/div')
    options_instr = result_instr.find_elements_by_tag_name("p")
    for paragraph in options_instr:
        if paragraph.text != '':
            instructions_list.append(paragraph.text.strip())
        else:
            continue
    recipe_driver.close()
    json_file["Recipe"] = '\n\n'.join(ingredients_list)
    json_file['INSTRUCTIONS'] = '\n\n'.join(instructions_list)

    return json_file


def print_json(url_to_get_recipe, json_file, counter=1):
    """
    To print to the console json beautiful format
    :param url_to_get_recipe:str
    :param json_file:dict
    :return void
    """

    print(str(counter) + " Url: {} \n{{\n \t\t{} :\n\t\t\t\t[".format(url_to_get_recipe, list(json_file.keys())[0]))
    for i in json_file['Recipe'].split('\n'):
        print('\t\t\t\t\t\t {}'.format(i))
    print('\t\t\t\t]')
    print('\n\t\t' + str(list(json_file.keys())[1] + ':'))
    print('"' + json_file['INSTRUCTIONS'] + '"')
    print('}\n')


if __name__ == '__main__':
    links_file = FILE_NAME
    with open(links_file, 'r') as f:
        link = f.readlines()
        for i in np.arange(273, len(link)):
            list_json = []
            l = link[i]
            json_file = get_recipe(l.strip())
            print_json(l.strip(), json_file, i)
            list_json.append(json_file)
            csv_columns = [str(list(json_file.keys())[0]), str(list(json_file.keys())[1])]
            try:
                with open('recipe_additional.csv', 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    for data in list_json:
                        writer.writerow(data)
            except IOError:
                print("I/O error")
