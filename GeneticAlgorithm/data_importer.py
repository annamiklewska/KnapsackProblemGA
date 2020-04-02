import csv
import logging

from common import Task
from common import Item

logging.basicConfig(level=logging.INFO)


# source for the following function: https://realpython.com/python-csv/
def read_csv(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        weights = []
        sizes = []
        costs = []
        line_count = 0
        for row in reader:
            if line_count == 0:
                n_items = int(row[0])
                max_weight = int(row[1])
                max_size = int(row[2])
                logging.info("No of items " + str(n_items) + " max weight: " + str(max_weight) + " max size: " + str(max_size))
                line_count += 1
            else:
                weights.append(int(row[0]))
                sizes.append(int(row[1]))
                costs.append(int(row[2]))
        logging.info("Task imported from the csv file")
        return Task(n_items, max_weight, max_size, weights, sizes, costs)


if __name__ == "__main__":
    task = read_csv("items.csv")
