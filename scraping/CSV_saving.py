import csv
import os


def csv_transfer(dictionary_list, category_name):
    """transfert of book informations to a csv file"""

    first_dictionary = dictionary_list[0]
    columns_header = []
    for k in first_dictionary:
        columns_header.append(k)

    data_dict = []
    for d in dictionary_list:
        data_dict.append(d.values())

    if not os.path.exists("category files"):
        os.makedirs("category files")

    os.chdir("category files")

    if not os.path.exists(category_name):
        os.makedirs(category_name)

    os.chdir(category_name)

    with open(
        category_name + " category.csv", "w", encoding="utf-8-sig", newline=""
    ) as essai:
        writer = csv.writer(essai)
        dict_writer = csv.DictWriter(essai, fieldnames=columns_header)
        dict_writer.writeheader()

        for i in data_dict:
            writer.writerow(i)

    essai.close()