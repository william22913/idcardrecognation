x = 5
for i in range(x):
    for j in range(x):
        if j == int(x / 2):
            print("*\t", end="")
        elif i == int(x / 2):
            print("*\t", end="")
        elif j + i == x - 1:
            print("*\t", end="")
        elif i == 0 or i == x - 1:
            print("*\t", end="")
        elif j == 0 or j == x - 1:
            print("*\t", end="")
        elif i == j:
            print("*\t", end="")
        else:
            print(" \t", end="")
    print("")
