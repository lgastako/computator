from computator import computate

GRAPH = {
    "n": lambda xs: len(xs),
    "m": lambda xs, n: sum(xs) / n,
    "m2": lambda xs, n: sum([x * x for x in xs]) / float(n),
    "v": lambda m, m2: m2 - (m * m)
}

def main():
    print computate(GRAPH, xs=[1, 2, 3, 6])

    # output:
    #
    # {'xs': [1, 2, 3, 6], 'm2': 12.5, 'm': 3, 'n': 4}

if __name__ == "__main__":
    main()
