from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

URL = f"https://www.simplyrecipes.com/latest/"
FILE_NAME = 'recipe_links_simplyrecipes.txt'
EMPTY_LINKS = 'recipe_empty.txt'
PATTERN = 'simplyrecipes.com/recipes/'


def connect(url=URL):
    """
    create chrome driver
    :return: chrome driver:obj
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    driver.get(url)
    time.sleep(5)
    return driver


def get_links_from_one_page(my_webpage):
    """
    To collect links for each recipe from one page
    :param my_webpage: link to page for scrapping: selenium obj
    :return: links from one page: list[str]
    """
    recipe_links = []
    # we know that on this website we have 26 links per page
    for i in range(1, 27):
        try:
            recipe = my_webpage.find_element_by_xpath(
                f'//*[@id="page"]/div[2]/div/div/div/div/div/ul/li[{i}]/div/div[2]/h2/a')
        except:
            continue
        recipe_links.append(recipe.get_attribute("href"))
    return recipe_links


def get_links_from_site(recipe_driver, num_pages=132):
    """
    To list pages on website and collect links into list
    :param recipe_driver: obj  chrome driver
    :param num_pages: int number of pages to scrap / default 132
    :return: list of links
    """
    all_pages_links = []
    for i in range(1, num_pages):

        # get links from one page
        page = get_links_from_one_page(recipe_driver)
        all_pages_links.append(page)

        try:
            # go to next page
            recipe_driver.find_element_by_class_name('rpg-next').click()
            time.sleep(5)
            print(f'page {i} is collected')
        except NoSuchElementException:
            print('I guess the page have no more recipes')
            continue
    return all_pages_links


def extract_links_to_file(file_name):
    """
    To write down links into .txt file
    :param file_name: output filename / FILE_NAME in the same dir
    :return: void
    """
    # create a driver
    recipe_driver = connect()

    # collect links
    recipe_links = get_links_from_site(recipe_driver)

    # write down links to the txt file
    output_recipe_links = open(file_name, 'w')
    empty_links = open(EMPTY_LINKS, 'w')
    for link_list in recipe_links:
        for url in link_list:
            if url.__contains__(PATTERN):
                output_recipe_links.write(url + '\n')
            else:
                empty_links.write(url + '\n')
    output_recipe_links.close()
    empty_links.close()

    print(f'links are in {file_name} file')


def get_recipe(link, counter_to_print=1):
    pass


if __name__ == '__main__':
    json_file = {}
    links_file = FILE_NAME
    extract_links_to_file(links_file)
    print('links are collected, the program is finished')
    recipe_links = open(links_file, "r").readlines()
    for counter_to_print, link in enumerate(recipe_links):
        one_recipe = get_recipe(link, counter_to_print)
        json_file.append(one_recipe)
