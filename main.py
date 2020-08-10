import pygame
import random

pygame.init()
screen = pygame.display.set_mode((850, 550))
pygame.display.set_caption("Gato")
x = pygame.image.load("x.png")
o = pygame.image.load("o.png")
SQUARE_LENGTH = 150
SQUARE_SEPARATION = 25
SQUARE_COLOR = (255, 255, 255)
grid = board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
font = pygame.font.Font("freesansbold.ttf", 32)
win_score = 0
tie_score = 0
lose_score = 0


def show_score():
    wins = font.render("Wins: " + str(win_score), True, (255, 0, 0))
    ties = font.render("Ties: " + str(tie_score), True, (255, 255, 255))
    loses = font.render("Loses: " + str(lose_score), True, (0, 0, 255))
    screen.blit(wins, (550, 25))
    screen.blit(ties, (550, 75))
    screen.blit(loses, (550, 125))


def draw_grid():
    global board
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    global turno_x
    turno_x = True
    global won
    won = False
    for i in range(3):
        for j in range(3):
            grid[i][j] = ((pygame.draw.rect(screen, SQUARE_COLOR, (
                (SQUARE_SEPARATION + SQUARE_LENGTH) * j + 25, (SQUARE_SEPARATION + SQUARE_LENGTH) * i + 25,
                SQUARE_LENGTH,
                SQUARE_LENGTH))))


def random_move():
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    while board[x][y] != 0:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
    return x, y


def check_winner():
    tie = True
    for i in range(3):
        if board[i][0] != 0:
            if board[i][0] == board[i][1] and board[i][0] == board[i][2]:
                return board[i][0]
    for i in range(3):
        if board[0][i] != 0:
            if board[0][i] == board[1][i] and board[0][i] == board[2][i]:
                return board[0][i]
    if board[0][0] != 0:
        if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
            return board[0][0]
    if board[2][0] != 0:
        if board[2][0] == board[1][1] and board[2][0] == board[0][2]:
            return board[2][0]
    for row in board:
        for tile in row:
            if tile == 0:
                tie = False
    if tie:
        return 0


scores = {
    1: -10,
    0: 0,
    2: 10,
}


def best_move():
    best_score = -10
    move = 0, 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minimax(board, 0, False)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    move = i, j
    return move


def minimax(board, depth, is_maximizing):
    result = check_winner()
    if result is not None:
        score = scores[result]
        return score
    if is_maximizing:
        max_evaluation = -10
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = minimax(board, depth + 1, False)
                    board[i][j] = 0
                    max_evaluation = max(score, max_evaluation)
        return max_evaluation
    else:
        min_evaluation = 10
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minimax(board, depth + 1, True)
                    board[i][j] = 0
                    min_evaluation = min(score, min_evaluation)
        return min_evaluation


draw_grid()
running = True
won = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if won:
                draw_grid()
            else:
                pos = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if grid[i][j].collidepoint(pos) and board[i][j] == 0:
                            screen.blit(x, grid[i][j])
                            board[i][j] = 1
                            if check_winner() == 1:
                                win_score += 1
                                won = True
                            elif check_winner() == 0:
                                tie_score += 1
                                won = True
                            if not won:
                                move = best_move()
                                screen.blit(o, grid[move[0]][move[1]])
                                board[move[0]][move[1]] = 2
                                if check_winner() == 2:
                                    lose_score += 1
                                    won = True
                                elif check_winner() == 0:
                                    tie_score += 1
                                    won = True
    pygame.draw.rect(screen, (0, 0, 0), (550, 0, 300, 550))
    show_score()
    pygame.display.update()
pygame.quit()
