class bcolors:
    GREEN = '\u001b[32m'
    RED = '\u001b[31m'
    CYAN = '\u001b[36m'
    BLACK = '\u001b[30;1m'
    WHITE = '\u001b[37;1m'
    BG_BLUE = '\u001b[44;1m'
    BG_WHITE = '\u001b[47;1m'
    BG_PINK = '\u001b[45m'
    END = '\033[0m'


def print_table(table, selected=None, valid_moves=None):
    for i in range(len(table)):
        if i == 0:
            print("    0    1    2    3    4    5    6    7")
            print("  __________________________________________")
        for j in range(len(table[i])):
            if j == 0:
                print(i, end=" |")
            if table[i][j] == "b" or table[i][j] == "B":
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(bcolors.BG_BLUE + bcolors.BLACK + " " +
                          str(table[i][j]) + " " + bcolors.END, end="  ")
                else:
                    print(bcolors.GREEN + " " +
                          str(table[i][j]) + " " + bcolors.END, end="  ")
            elif table[i][j] == "c" or table[i][j] == "C":
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(bcolors.BG_BLUE + bcolors.BLACK + " " +
                          str(table[i][j]) + " " + bcolors.END, end="  ")
                else:
                    print(bcolors.RED + " " +
                          str(table[i][j]) + " " + bcolors.END, end="  ")

            elif valid_moves and (i, j) in valid_moves:
                print(bcolors.BG_WHITE + bcolors.BLACK + str(i) +
                      " " + str(j) + bcolors.END, end="  ")
            else:
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(bcolors.BG_PINK + bcolors.BLACK + " " +
                          str(table[i][j]) + " " + bcolors.END, end="  ")
                else:
                    print(" " + str(table[i][j]) + " ", end="  ")
        print("| " + str(i))
    print("  ------------------------------------------")
    print("    0    1    2    3    4    5    6    7")
