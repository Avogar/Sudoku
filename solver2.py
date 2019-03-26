import pygame
from copy import deepcopy
from functools import reduce
pygame.init()

class Cell:
    def __init__(self, value, x, y, length):
        self.x = x
        self.y = y
        self.value = value
        self.isAppear = False
        self.isPress = False
        self.length = length
        self.color = black

    def draw(self):
        if self.isPress:
            color = grey
        else:
            color = white
        pygame.draw.rect(screen, color, [self.x, self.y, self.length, self.length])
        pygame.draw.rect(screen, black, [self.x, self.y, self.length,self.length], 1)
        if self.isAppear:
            font = pygame.font.Font(None, self.length + 15)
            self.text = font.render(str(self.value), True, self.color)
            screen.blit(self.text, [self.x + (self.length - self.text.get_width()) / 2, self.y + (self.length - self.text.get_height()) / 2 + 3])

class Matrix:
    def __init__(self, n):
        self.n = n
        self.matrix = [[Cell(0, j * (size[0] // n ** 2), i * (size[0] // n ** 2), size[0] // n ** 2) for j in range(n ** 2)] for i in range(n ** 2)]

    def draw(self):
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                self.matrix[i][j].draw()

        for i in range(self.n ** 2):
            pygame.draw.rect(screen, black, [(i % self.n) * (size[0] // self.n ** 2) * self.n, (i // self.n) * (size[0] // self.n ** 2) * self.n, size[0] // self.n ** 2 * self.n, size[0] // self.n ** 2 * self.n],4)

def solve(matrix, n):
    hidden = 0
    for i in range(n ** 2):
        for j in range(n ** 2):
            if matrix[i][j] == 0:
                matrix[i][j] = set(range(1,n ** 2 + 1))
                hidden += 1
            elif isinstance(matrix[i][j], set):
                hidden += 1
    isChange = True
    while hidden != 0 and isChange:
        isChange = False
        for i in range(n ** 2):
            for j in range(n ** 2):
                if isinstance(matrix[i][j], set):
                    newSet = matrix[i][j].copy()
                    rowNums = set()
                    rowSet = set()
                    columnNums = set()
                    columnSet = set()
                    squareNums = set()
                    squareSet = set()
                    for k in range(n ** 2):
                        if isinstance(matrix[i][k], int):
                            rowNums |= {matrix[i][k]}
                        elif k != j:
                            rowSet |= matrix[i][k]

                        if isinstance(matrix[k][j], int):
                            columnNums |= {matrix[k][j]}
                        elif k != i:
                            columnSet |= matrix[k][j]

                        if isinstance(matrix[i // n * n + k // n][j // n * n + k % n], int):
                            squareNums |= {matrix[i // n * n + k // n][j // n * n + k % n]}
                        elif i // n * n + k // n != i or j // n * n + k % n != j:
                            squareSet |= matrix[i // n * n + k // n][j // n * n + k % n]

                    newSet -= rowNums | columnNums | squareNums

                    if len(newSet - rowSet) == 1:
                        newSet -= rowSet
                    elif len(newSet - columnSet) == 1:
                        newSet -= columnSet
                    elif len(newSet - squareSet) == 1:
                        newSet -= squareSet

                    if newSet != matrix[i][j]:
                        if newSet == set():
                            return 'Empty'
                        isChange = True
                        matrix[i][j] = newSet
                        if len(newSet) == 1:
                            matrix[i][j] = list(newSet)[0]
                            hidden -= 1
    if hidden != 0:
        nowSet = 0
        i = -1
        while nowSet == 0:
            i += 1
            nowSet = next(filter(lambda x: isinstance(x, set), matrix[i]), 0)
        j = matrix[i].index(nowSet)
        for elem in nowSet:
            matrix[i][j] = elem
            newMatrix = deepcopy(matrix)
            attempt = solve(newMatrix, n)
            if not(isinstance(attempt, str)):
                return attempt
        return 'Empty'
    return matrix

def newNum(event):
    num = 0
    if event.key == pygame.K_1:
        num = 1
    elif event.key == pygame.K_2:
        num = 2
    elif event.key == pygame.K_3:
        num = 3
    elif event.key == pygame.K_4:
        num = 4
    elif event.key == pygame.K_5:
        num = 5
    elif event.key == pygame.K_6:
        num = 6
    elif event.key == pygame.K_7:
        num = 7
    elif event.key == pygame.K_8:
        num = 8
    elif event.key == pygame.K_9:
        num = 9
    return num

def inputNums(table):
    i = j = 0
    num = 0
    isNumInput = False
    currentCell = table.matrix[i][j]
    currentCell.isPress = True
    done = True
    isEnter = False
    newCell = False
    while done and not(isEnter):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    isEnter = True
                if event.key == pygame.K_DOWN and i != table.n ** 2 - 1:
                    i += 1
                    newCell = True
                elif event.key == pygame.K_UP and i != 0:
                    i -= 1
                    newCell = True
                elif event.key == pygame.K_LEFT and j != 0:
                    j -= 1
                    newCell = True
                elif event.key == pygame.K_RIGHT and j != table.n ** 2 - 1:
                    j += 1
                    newCell = True
                if event.key == pygame.K_BACKSPACE:
                    currentCell.value = 0
                    currentCell.isAppear = False
                num = newNum(event)
                if num != 0:
                    isNumInput = True

        if newCell:
            currentCell.isPress = False
            currentCell = table.matrix[i][j]
            currentCell.isPress = True
            newCell = False

        if isNumInput:
            currentCell.value = num
            currentCell.isAppear = True
            isNumInput = False

        screen.fill(white)

        table.draw()

        pygame.display.flip()

        clock.tick(100)
    currentCell.isPress = False
    return done, table

def check(matrix, n):
    for i in range(n ** 2):
        for j in range(n ** 2):
            if matrix[i][j].value != 0:
                for k in range(n ** 2):
                    if matrix[i][k].value == matrix[i][j].value and k != j:
                        return False
                    if matrix[k][j].value == matrix[i][j].value and k != i:
                        return False
                    if matrix[i][j].value == matrix[i // n * n + k // n][j // n * n + k % n].value and \
                            (i // n * n + k // n != i or j // n * n + k % n != j):
                        return False
    return True

def getMatrix(matrix):
    newMatrix = []
    for i in range(len(matrix)):
        newMatrix.append(list(map(lambda x: x.value, matrix[i])))
    return newMatrix

def fillTable(table, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if table.matrix[i][j].isAppear == True:
                table.matrix[i][j].color = blue
            table.matrix[i][j].value = matrix[i][j]
            table.matrix[i][j].isAppear = True





black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
blue = (0, 0, 140)

size = [540, 540]

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

table = Matrix(3)
done, table = inputNums(table)

if not(check(table.matrix, table.n)):
    done = False
    print('Error')
else:
    solution = solve(getMatrix(table.matrix), table.n)
    if solution == 'Empty':
        print('Empty')
        done = False
    else:
        fillTable(table, solution)


while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

    screen.fill(white)
    table.draw()
    pygame.display.flip()

    clock.tick(100)
pygame.quit()