from computator import computate

GRAPH = {
    "n": lambda xs: len(xs),
    "m": lambda xs, n: sum(xs) / n,
    "m2": lambda xs, n: sum([x * x for x in xs]),
    "v": lambda m, m2: m2 - (m * m)
}

def main():
    print computate(GRAPH, xs=[1, 2, 3, 6])

if __name__ == "__main__":
    main()
