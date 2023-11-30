import numpy

x = 5
result = numpy.zeros((x,x))
i = 0
j = 0
counter = 1
keep = x
while True:
    if i == j and j == int(x/2):
        result[i, j] = counter
        break

    if j+1 < x and result[i, j+1] == 0:
        for _ in range(x):
            if i == x and j == x:
                break

            if result[i, j] == 0:
                result[i, j] = counter
                counter = counter + 1
            else:
                break
            j = j + 1
        j = j - 1
        i = i + 1

    if i+1 < x and result[i+1, j] == 0:
        for _ in range(x):
            if i >= x:
                i = i - 1
                break
            elif j >= x:
                j = j - 1
                break

            if result[i, j] == 0:
                result[i, j] = counter
                counter = counter + 1
            else:
                i = i - 1
                break
            i = i + 1

    if j-1 >= 0 and result[i, j-1] == 0:
        j = j - 1
        while True or result[i, j] != 0:
            if j == -1:
                j = j + 1
                break
            if result[i, j] == 0:
                result[i, j] = counter
                counter = counter + 1
            else:
                j = j + 1
                break
            j = j - 1

    if i-1 >= 0 and result[i-1, j] == 0:
        i = i - 1
        while True:
            if i == -1 or result[i, j] != 0:
                i = i + 1
                break

            if result[i, j] == 0:
                result[i, j] = counter
                counter = counter + 1
            else:
                break
            i = i - 1
        j = j + 1

print(result)
# for i in range(x):
#     for j in range(x):
#         if i+j == int(x/2) or j-i == int(x/2):
#             print("*\t", end="")
#         elif i-j == int(x/2) or j+i == x+int(x/2)-1:
#             print("*\t", end="")
#         else:
#             print(" \t", end="")
#
#         # if j == int(x / 2):
#         # elif i == int(x / 2):
#         #     print("*\t", end="")
#         # elif j + i == x - 1:
#         #     print("*\t", end="")
#         # elif i == 0 or i == x - 1:
#         #     print("*\t", end="")
#         # elif j == 0 or j == x - 1:
#         #     print("*\t", end="")
#         # elif i == j:
#         #     print("*\t", end="")
#         # else:
#         #     print(" \t", end="")
#     print("")
