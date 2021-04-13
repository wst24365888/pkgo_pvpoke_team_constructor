import itertools
import json

if __name__ == "__main__":
    pokes = []

    n = int(input("Enter the number of Pokemon you have ready: "))

    for i in range(0, n):
        ele = (input()).split(',')[0]

        pokes.append(ele)

    permutations_list = list(itertools.combinations(pokes, 3))

    print(f"Total length: {len(permutations_list)}")

    json.dump(permutations_list, open('permutations_list.json', 'w'))