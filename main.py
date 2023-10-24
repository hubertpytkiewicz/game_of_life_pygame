import pygame
import numpy as np
import argparse

SQUARE_SIZE = 8
ALIVE = 1
DEAD = 0
STATES = [ALIVE, DEAD]
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

parser = argparse.ArgumentParser(description="Game of life in Pygame")

parser.add_argument('--height', type=int, default=100, help="Specifies height of the board.")
parser.add_argument('--width', type=int, default=100, help="Specifies width of the board.")
parser.add_argument('--board', type=str, help="Specify csv file of a starting board state.")

args = parser.parse_args()

if args.board is not None:
    board = np.loadtxt(args.board, delimiter=",", dtype=int)
    BOARD_HEIGHT, BOARD_WIDTH = board.shape
else:
    BOARD_WIDTH = args.width
    BOARD_HEIGHT = args.height
    board = np.random.choice(STATES, BOARD_HEIGHT*BOARD_WIDTH , p=[0.2, 0.8]).reshape(BOARD_HEIGHT, BOARD_WIDTH)

SCREEN_WIDTH = BOARD_WIDTH*SQUARE_SIZE
SCREEN_HEIGHT = BOARD_HEIGHT*SQUARE_SIZE

num_rows, num_columns = board.shape

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Simple Pygame App")

running = True
fps = 16

def count_neighbours(board: np.ndarray, row: int, column: int) -> int:
    return int(board[(row-1)%num_rows][(column-1)%num_columns] + board[(row-1)%num_rows][column] + board[(row-1)%num_rows][(column+1)%num_columns] + \
               board[row][(column-1)%num_columns] + board[row][(column+1)%num_columns] + \
               board[(row+1)%num_rows][(column-1)%num_columns] + board[(row+1)%num_rows][column] + board[(row+1)%num_rows][(column+1)%num_columns])

def game_loop(running: bool) -> None:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        screen.fill(BLACK)
        for row in range(num_rows):
            for column in range(num_columns):
                if board[row][column] == ALIVE:
                    pygame.draw.rect(screen, GREEN, (column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        compare_board = board.copy()
        for row in range(num_rows):
            for column in range(num_columns):
                alive_neighbours = count_neighbours(compare_board, row, column)
                if alive_neighbours < 2 or alive_neighbours > 3:
                    board[row][column] = 0
                elif alive_neighbours == 3:
                    board[row][column] = 1
        
        pygame.display.flip()
        
        pygame.time.wait(int(1000/fps))

game_loop(running)

pygame.quit()