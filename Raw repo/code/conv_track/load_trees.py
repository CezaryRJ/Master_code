from frame import *
from tqdm import tqdm

def print_tree(index):
    print("Index = " + str(index))
    for x in trees[index]:
        print(x)
        for y in trees[index][x]:
            print(y)

slash = get_slash()

reader = open( "t" + slash + "trees.txt","r",encoding="utf-8")

lines = reader.readlines()

trees = dict()

i = 0
trees_read = 0

pbar = tqdm(total=len(lines))

while i < len(lines) and lines[i][:3] == "---": #tree

    tree_index = int(lines[i][3:])

    #print("Tree index = " + str(tree_index))

    trees[tree_index] = dict()

    i = i + 2
    pbar.update(2)

    while lines[i] != "§\n":

        while lines[i][:-1].isnumeric():
            level = lines[i][:-1]
            i = i + 1
            pbar.update(1)
            trees[tree_index][level] = list()

            #print(level)
            while lines[i] != "Δ\n":

                while lines[i] == "α\n":
                    i = i + 1
                    pbar.update(1)
                    tmp = ""
                    while lines[i] != "Ω\n":
                        tmp = tmp + lines[i]
                        i = i + 1
                        pbar.update(1)

                    trees[tree_index][level].append(tmp)
                    i = i + 1
                    pbar.update(1)
                    #print(lines[i])

            i = i + 2
            pbar.update(2)

    i = i + 5
    pbar.update(5)

    trees_read = trees_read + 1
    #print_tree(tree_index)


print("Trees read from file = " + str(len(trees)))
