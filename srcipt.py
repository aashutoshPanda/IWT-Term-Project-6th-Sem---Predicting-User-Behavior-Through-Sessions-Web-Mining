import sqlite3
from collections import OrderedDict

import os

# System call
os.system("")

# Class of different styles


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


log_file = open('ecommerce.log', 'r')
log_file_lines = log_file.readlines()

count = 0
# Strips the newline character


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def sort(dictionary):
    return OrderedDict(
        sorted(dictionary.items(), key=lambda item: -item[1]))


def should_ignore(method, path, status_code):
    if(method != 'GET'):
        return True
    if(status_code != "200"):
        return True

    ignore_paths = ['media', 'admin', 'static']
    for ignore_path in ignore_paths:
        if(path.startswith(ignore_path)):
            return True
        if(path == ''):
            return True
    return False


filtered_log_lines = []
for line in log_file_lines:
    # print(line.split())
    method, path, _, status_code, _ = line.split()
    method = method.lstrip('"')
    path = path.strip('/')
    if(not should_ignore(method, path, status_code)):
        filtered_log_lines.append([method, path, status_code])

# print(filtered_log_lines)
category_dictionary = OrderedDict()
product_dictionary = OrderedDict()
for _, path, _ in filtered_log_lines:
    if(path.startswith('categories/')):
        category = remove_prefix(path, 'categories/')
        # print(category)
        if(category in category_dictionary):
            category_dictionary[category] += 1
        else:
            category_dictionary[category] = 1
    else:
        product = path
        if(product in product_dictionary):
            product_dictionary[product] += 1
        else:
            product_dictionary[product] = 1

category_dictionary = sort(category_dictionary)
most_visited_category = list(category_dictionary)[0]

print(style.YELLOW, f"Most visited category by the user is :",
      style.WHITE, most_visited_category)

product_dictionary = sort(product_dictionary)
most_visited_product = list(product_dictionary)[0]

print(style.YELLOW, f"Most visited product by the user is :",
      style.WHITE, most_visited_product)

query_items_from_most_visited_category = f"SELECT * from shop_product where category_id is (SELECT id from shop_category where name='{most_visited_category}' COLLATE NOCASE)"
query_items_from_most_visited_product = f"SELECT * from shop_product where category_id is (SELECT category_id from shop_product where slug = '{most_visited_product}' COLLATE NOCASE)"

con = sqlite3.connect('db.sqlite3')


def sql_fetch(con, command, message):
    cursorObj = con.cursor()
    cursorObj.execute(command)
    rows = cursorObj.fetchall()
    print(style.YELLOW, message)
    for index, row in enumerate(rows):
        print(style.WHITE, f"{index+1}) ", row[1])


sql_fetch(con, query_items_from_most_visited_category,
          "Suggested Products from most visited category :")
sql_fetch(con, query_items_from_most_visited_product,
          "Suggested products similar to the from most visited product :")
