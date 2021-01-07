import pickle

from main import FILE_NAME, connect


def get_recipe(link, counter_to_print=1):
    json_file = {}  # not real json because of utf-8 encoding
    ingredients_list = []
    instructions_list = []

    # create a driver
    recipe_driver = connect(link)
    # get ingredients
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

    json_file["Recipe"] = ingredients_list
    json_file['INSTRUCTIONS'] = '\n'.join(instructions_list)
    return json_file


def print_json(url_to_get_recipe, json_file):
    """
    To print to the console json beautiful format
    :param url_to_get_recipe:str
    :param json_file:dict
    :return void
    """

    print(u"Url: {} \n{{\n \t\t{} :\n\t\t\t\t[".format(url_to_get_recipe, list(json_file.keys())[0]))
    for k in json_file['Recipe']:
        print(u'\t\t\t\t\t\t {}'.format(str(k).strip()))
    print(u'\t\t\t\t]')
    print('\n\t\t' + str(list(json_file.keys())[1] + ':'))
    print('"' + json_file['INSTRUCTIONS'] + '"')
    print('}\n')


if __name__ == '__main__':
    links_file = FILE_NAME
    list_json = []
    with open(links_file, 'r') as f:
        link = f.readlines()
        for i, l in enumerate(link):
            json_file = get_recipe(l.strip(), counter_to_print=i + 1)
            print_json(l.strip(), json_file)
            list_json.append(json_file)
        file = open('recipe_additional.pkl', 'wb+')
        pickle.dump(list_json, file)
        file.close()
