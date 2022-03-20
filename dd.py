def readfile():
    str_maze = []
    file = open(f"C:\\input_hw1.txt", 'r', encoding='utf-8')
    with file as f:
        lines = f.readlines()
        txt = [[i.replace("\n", "")]for i in lines]
        for i in range(0, len(txt)):
            middle_list = txt[i][0].split(" ")
            if "" in middle_list:
                middle_list.remove("")
            str_maze.append(middle_list)
    return str_maze

def get_maze(num, maze_txt):
    maze = []
    count = 0
    column = 0
    row = 0
    if num != 0:
        for i in range(1, len(maze_txt)):
            if i == 1:
                column = int(maze_txt[1][0]) + 1
                row = i
                count += 1
                continue
            elif i > column:
                column += int(maze_txt[i][0]) + 1
                row = i
                count += 1
                continue
            if i <= column and num == count:
                rowlist = []
                for garo in range(0, int(maze_txt[row][1])):
                    rowlist.append(int(maze_txt[i][garo]))
                maze.append(rowlist)
    return maze

def solve_maze(count, trace, maze, column, row):
    if column + 1 == len(maze) and row + 1 == len(maze[-1]):
        return 1
    if column + 1 < len(maze) and maze[column + 1][row] == 1 and trace != "U":
        count += solve_maze(count, "D", maze, column + 1, row)
    if column - 1 >= 0 and maze[column - 1][row] == 1 and trace != "D":
        count += solve_maze(count, "U", maze, column - 1, row)
    if row + 1 < len(maze[column]) and maze[column][row + 1] == 1:
        count += solve_maze(count, "R", maze, column, row + 1)
    if row + 1 < len(maze[column]) and column + 1 < len(maze) and maze[column + 1][row + 1] == 1:
        count += solve_maze(count, "RD", maze, column + 1, row + 1)
    return count

# def solve_maze2(count, trace, maze, column, row):
#     trace_list = []
#     if column + 1 == len(maze) and row + 1 == len(maze[-1]):
#         trace.append(1)
#         return trace
#     if column + 1 < len(maze) and maze[column + 1][row] == 1 and trace[-1] != "U":
#         trace += ["D"]
#         trace_list.append(solve_maze2(count, trace, maze, column + 1, row))
#     if column - 1 >= 0 and maze[column - 1][row] == 1 and trace[-1] != "D":
#         trace += ["U"]
#         trace_list.append(solve_maze2(count, trace, maze, column - 1, row))
#     if row + 1 < len(maze[column]) and maze[column][row + 1] == 1:
#         trace += ["R"]
#         trace_list.append(solve_maze2(count, trace, maze, column, row + 1))
#     if row + 1 < len(maze[column]) and column + 1 < len(maze) and maze[column + 1][row + 1] == 1:
#         trace += ["RD"]
#         trace_list.append(solve_maze2(count, trace, maze, column + 1, row + 1))
#     return trace_list
def solve_maze3(count, trace, maze, column, row):
    if column + 1 == len(maze) and row + 1 == len(maze[-1]):
        global count2
        count2 += 1
        return True
    if column + 1 < len(maze) and maze[column + 1][row] == 1 and trace != "U":
        solve_maze3(count, "D", maze, column + 1, row)
    if column - 1 >= 0 and maze[column - 1][row] == 1 and trace != "D":
        solve_maze3(count, "U", maze, column - 1, row)
    if row + 1 < len(maze[column]) and maze[column][row + 1] == 1:
        solve_maze3(count, "R", maze, column, row + 1)
    if row + 1 < len(maze[column]) and column + 1 < len(maze) and maze[column + 1][row + 1] == 1:
        solve_maze3(count, "RD", maze, column + 1, row + 1)
    return True

str_maze = readfile()
for num in range(1,6):
    maze = get_maze(num, str_maze)
    count2 = 0
    route = solve_maze3(0,"",maze,0,0)
    print(count2)





















def solve_maze2(count, trace, maze, column, row):
    trace_list = []
    if column + 1 == len(maze) and row + 1 == len(maze[-1]):
        trace.append(1)
        return trace
    for nowcolumn in range(0, len(maze)):
        for nowrow in range(0, len(maze[column])):
            if nowcolumn + 1 < len(maze) and maze[nowcolumn + 1][nowrow] == 1 and trace[-1] != "U":
                trace += ["D"]
                trace_list.append(solve_maze2(count, trace, maze, nowcolumn + 1, nowrow))
            if nowcolumn - 1 >= 0 and maze[nowcolumn - 1][nowrow] == 1 and trace[-1] != "D":
                trace += ["U"]
                trace_list.append(solve_maze2(count, trace, maze, nowcolumn - 1, nowrow))
            if nowrow + 1 < len(maze[nowcolumn]) and maze[nowcolumn][nowrow + 1] == 1:
                trace += ["R"]
                trace_list.append(solve_maze2(count, trace, maze, nowcolumn, nowrow + 1))
            if nowrow + 1 < len(maze[nowcolumn]) and nowcolumn + 1 < len(maze) and maze[nowcolumn + 1][nowrow + 1] == 1:
                trace += ["RD"]
                trace_list.append(solve_maze2(count, trace, maze, nowcolumn + 1, nowrow + 1))
    return trace_list

def solve_maze(count, trace, maze, column, row):
    if column + 1 == len(maze) and row + 1 == len(maze[-1]):
        return 1
    for nowcolumn in range(0, len(maze)):
        for nowrow in range(0, len(maze[column])):
            if nowcolumn + 1 < len(maze) and maze[nowcolumn + 1][nowrow] == 1 and trace != "U":
                count += solve_maze(count, "D", maze, column + 1, nowrow)
            if nowcolumn - 1 >= 0 and maze[nowcolumn - 1][nowrow] == 1 and trace != "D":
                count += solve_maze(count, "U", maze, nowcolumn - 1, nowrow)
            if nowrow + 1 < len(maze[nowcolumn]) and maze[nowcolumn][nowrow + 1] == 1:
                count += solve_maze(count, "R", maze, nowcolumn, nowrow + 1)
            if nowrow + 1 < len(maze[nowcolumn]) and nowcolumn + 1 < len(maze) and maze[nowcolumn + 1][nowrow + 1] == 1:
                count += solve_maze(count, "RD", maze, nowcolumn + 1, nowrow + 1)
    return count