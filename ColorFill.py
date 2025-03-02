import pygame
import sys
import random


pygame.init()


WINDOW_SIZE = 800
GRID_SIZE = 5
CELL_SIZE = 100
MARGIN = (WINDOW_SIZE - (GRID_SIZE * CELL_SIZE)) // 2

# Бои
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, YELLOW]


screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Color Fill Puzzle")


class ColorFillPuzzle:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_color = RED
        self.moves = 0
        self.game_won = False

    def is_valid_move(self, row, col, color):

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                if self.grid[new_row][new_col] == color:
                    return False
        return True

    def make_move(self, row, col):
        if not self.game_won and self.is_valid_move(row, col, self.selected_color):
            self.grid[row][col] = self.selected_color
            self.moves += 1
            self.check_win()

    def check_win(self):

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] is None:
                    return
        self.game_won = True

    def draw(self, screen):

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE


                cell_color = self.grid[row][col] if self.grid[row][col] is not None else WHITE
                pygame.draw.rect(screen, cell_color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)


        for i, color in enumerate(COLORS):
            x = 20 + i * 50
            y = WINDOW_SIZE - 60
            pygame.draw.rect(screen, color, (x, y, 40, 40))
            if color == self.selected_color:
                pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 44, 44), 2)


        font = pygame.font.Font(None, 36)
        moves_text = font.render(f"Moves: {self.moves}", True, BLACK)
        screen.blit(moves_text, (WINDOW_SIZE - 150, WINDOW_SIZE - 50))


        if self.game_won:
            win_text = font.render("Puzzle Completed!", True, BLACK)
            screen.blit(win_text, (WINDOW_SIZE // 2 - 100, 20))


def main():
    game = ColorFillPuzzle()
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos


                if WINDOW_SIZE - 60 <= y <= WINDOW_SIZE - 20:
                    color_index = (x - 20) // 50
                    if 0 <= color_index < len(COLORS):
                        game.selected_color = COLORS[color_index]


                elif MARGIN <= x <= WINDOW_SIZE - MARGIN and MARGIN <= y <= WINDOW_SIZE - MARGIN:
                    grid_x = (x - MARGIN) // CELL_SIZE
                    grid_y = (y - MARGIN) // CELL_SIZE
                    game.make_move(grid_y, grid_x)

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()