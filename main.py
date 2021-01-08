import csv
import numpy as np
from get_recipes import print_json, FILE_NAME, extract_links_to_file, get_recipe


def main():
    """
    The main crawling data function:
    1. To extract links from website into txt file
    2. To read from txt file line by line and collect recipe ingredients
    and recipe instructions into variable.
    3. To write dow line by line each page data into csv file
    By the function run will print into console what is collected
    :return: void
    """
    # get all links from site
    links_file = FILE_NAME
    extract_links_to_file(links_file)
    print('Links are collected, the program is finished')

    # get data from each page
    with open(links_file, 'r') as f:
        link = f.readlines()
        for i in np.arange(0, len(link)):
            list_json = []
            l = link[i]
            json_file = get_recipe(l.strip())
            print_json(l.strip(), json_file, i + 1)
            list_json.append(json_file)

            # write down a line into csv file with collected data
            csv_columns = [str(list(json_file.keys())[0]), str(list(json_file.keys())[1])]
            try:
                with open('recipe_additional.csv', 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    for data in list_json:
                        writer.writerow(data)
            except IOError:
                print("I/O error")


if __name__ == '__main__':
    main()
