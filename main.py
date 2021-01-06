import time


def get_links_from_page(my_webpage):
    """
    get links for competitions from one page
    :param my_webpage: link to page for scrapping
    :return: links from one page
    """
    competition_links = []
    for i in range(1, 20):
        try:
            compet = my_webpage.find_element_by_xpath(
                '//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/a[' + str(i) + ']')
        except:
            # print('not now')
            continue
        competition_links.append(compet.get_attribute("href"))
    return competition_links


def connect():
    """
    create chrome driver
    :return: chrome driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    driver.get("https://www.kaggle.com/search?q=in%3Acompetitions")
    time.sleep(5)
    return driver


def get_links_from_site(driver, num_pages=450):
    """
    get competition links from kaggle site
    :param driver: chrome driver
    :param num_pages: number of pages to scrap
    :return: list of links
    """
    competition_links = []
    for i in range(num_pages):
        competition_links += get_links_from_page(driver)
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[3]/div/button[2]').click()
        time.sleep(5)
    return competition_links


def extract_links_to_file(file_name):
    """
    extract links to .txt file
    :param file_name: output filename
    :return: nothing
    """
    kaggle_driver = connect()
    competition_links = get_links_from_site(kaggle_driver)
    output_comp_links = open(file_name, 'w')
    for link in competition_links:
        output_comp_links.write(link + '\n')
    output_comp_links.close()


if __name__ == '__main__':

    links_file ='kaggle_links.txt'
    extract_links_to_file(links_file)

