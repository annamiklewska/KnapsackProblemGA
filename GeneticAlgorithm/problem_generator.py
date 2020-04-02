import csv
import logging
import random as r

from structs import Item

logging.basicConfig(level=logging.INFO)


def _generate_items(n, w, s):
    """
    :param n: number of objects to choose
    :param w: maximum carrying capacity of the backpack
    :param s: maximum backpack size
    :return: list of items; Item(w_i, s_i, c_i)
    """
    # 1 < w_i < 10*w/n
    # 1 < s_i <10*s/n
    # 1 < c_i < n
    items = [Item(r.randint(2, 10*w/n - 1), r.randint(2, 10*s/n - 1), r.randint(2, n - 1)) for _ in range(n)]
    # 1 < 2_i < 10*w/n & 1 < s_i <10*s/n
    while not _check_criteria(items, w, s):
        items = [(r.randint(2, 10*w/n - 1), r.randint(2, 10*s/n - 1), r.randint(2, n - 1)) for _ in range(n)]
        logging.info('Criteria not met, new items generated')
    logging.info('Items generated')
    return items


def _check_criteria(items, w, s):
    """
    :param items: list of items; Item(w_i, s_i, c_i)
    :param w: maximum carrying capacity of the backpack
    :param s: maximum backpack size
    :return: evaluation whether items meet the criteria
    """
    if sum([item.weight for item in items]) <= 2*w:
        return False
    if sum([item.size for item in items]) <= 2*s:
        return False
    return True


def _save_file(n, w, s, output_file_name, items):
    """
    :param n: number of objects to choose
    :param w: maximum carrying capacity of the backpack
    :param s: maximum backpack size
    :param output_file_name: name of the generated file
    :param items: list of items; Item(w_i, s_i, c_i)
    """
    with open(output_file_name, 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([n, w, s])
        for item in items:
            writer.writerow([item.weight, item.size, item.cost])
    logging.info('CSV file saved')


def generate(n, w, s, output_file_name):
    """
    :param n: number of objects to choose
    :param w: maximum carrying capacity of the backpack
    :param s: maximum backpack size
    :param output_file_name: name of the file into which the task is to be saved
    file format:
        first row: n, w, s
        following rows: weight, size, cost (of individuals)
    """
    _save_file(n, w, s, output_file_name, _generate_items(n, w, s))


if __name__ == "__main__":
    generate(n=5, w=50, s=50, output_file_name="items_tiniest.csv")
