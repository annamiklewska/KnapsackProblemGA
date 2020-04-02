from data_importer import read_csv

# Solution based on the following source:
# https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/


def run(file_name):
    task = read_csv(file_name)
    n_items = task.n_items  # n
    max_weight = task.max_weight  # W
    max_size = task.max_size
    weights = task.weights  # wt
    sizes = task.sizes
    costs = task.costs  # val

    k = [[0 for _ in range(max_weight + 1)] for _ in range(n_items + 1)]

    for i in range(n_items + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                k[i][w] = 0
            elif weights[i - 1] <= max_weight and sizes[i - 1] <= max_size:
                k[i][w] = max(costs[i - 1] + k[i - 1][w - weights[i - 1]], k[i - 1][w])
            else:
                k[i][w] = k[i - 1][w]
    return k[n_items][max_weight]


if __name__ == "__main__":
    print(run("items.csv"))
