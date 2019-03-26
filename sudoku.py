import pygame, random
pygame.init()


class Cell:
    def __init__(self, value, x, y, length):
        self.x = x
        self.y = y
        self.value = value
        self.isAppear = True
        self.isPress = False
        self.length = length

    def draw(self):
        if self.isPress:
            color = grey
        else:
            color = white
        pygame.draw.rect(screen, color, [self.x, self.y, self.length, self.length])
        pygame.draw.rect(screen, black, [self.x, self.y, self.length,self.length], 1)
        if self.isAppear:
            font = pygame.font.Font(None, self.length + 15)
            self.text = font.render(str(self.value), True, black)
            screen.blit(self.text, [self.x + (self.length - self.text.get_width()) / 2, self.y + (self.length - self.text.get_height()) / 2 + 3])


class Matrix:
    def __init__(self, n):
        self.n = n
        self.countAppear = n ** 4
        self.matrix = [[Cell(int((i * n + i / n + j) % (n*n) + 1),j * (size[0] // n ** 2), i * (size[0] // n ** 2), size[0] // n ** 2) for j in range(n*n)] for i in range(n*n)]

    def draw(self):
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                self.matrix[i][j].draw()

        for i in range(self.n ** 2):
            pygame.draw.rect(screen, black, [(i % self.n) * (size[0] // self.n ** 2) * self.n, (i // self.n) * (size[0] // self.n ** 2) * self.n, size[0] // self.n ** 2 * self.n, size[0] // self.n ** 2 * self.n],4)

    def mix(self):
        mixAmount = random.randrange(20, 30)
        for k in range(mixAmount):
            num1, num2 = random.sample(range(1, self.n ** 2 + 1), 2)
            for i in range(self.n ** 2):
                for j in range(self.n ** 2):
                    if self.matrix[i][j].value == num1:
                        self.matrix[i][j].value = num2
                    elif self.matrix[i][j].value == num2:
                        self.matrix[i][j].value = num1


    def hiding(self):
        for j in range(self.n ** 2):
            for i in range(self.n ** 2):
                num = random.randrange(1000)
                if num % 5 % 2 == 0:
                    self.matrix[i][j].isAppear = False
                    self.countAppear -= 1

    def isMousePress(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN

    def inWhichCell(self, xy):
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                if 0 <= xy[0] - self.matrix[i][j].x <= self.matrix[i][j].length and \
                        0 <= xy[1] - self.matrix[i][j].y <= self.matrix[i][j].length:
                    return self.matrix[i][j]

    def unPress(self):
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                self.matrix[i][j].isPress = False

def newNum(event):
    num = 0
    if event.type == pygame.KEYDOWN:
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




black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)

size = [540, 540]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Судоку')

clock = pygame.time.Clock()

matrix = Matrix(3)
matrix.mix()
matrix.hiding()
cell = matrix.matrix[0][0]

isNewNum = False

done = True

while matrix.countAppear != matrix.n ** 4 and done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if matrix.isMousePress(event):
            pos = pygame.mouse.get_pos()
            cell = matrix.inWhichCell(pos)
            matrix.unPress()
            if cell.isAppear == False:
                cell.isPress = True
                isNewNum = True
            else:
                isNewNum = False
        if isNewNum:
            num = newNum(event)
            if num != 0:
                if cell.value == num:
                    cell.isAppear = True
                    cell.isPress = False
                    matrix.countAppear += 1
                else:
                    cell.isPress = False
                isNewNum = False



    screen.fill(white)

    matrix.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()