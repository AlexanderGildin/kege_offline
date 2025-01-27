import pygame
from TimurTextInput import TextBox  

pygame.init()

class Table:
    def __init__(self, x, y, rows, cols, cell_width, cell_height, screen=None, max_len=5):
        self.x = x
        self.y = y
        self.rows = rows 
        self.cols = cols 
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.screen = screen
        self.max_len = max_len
        self.text_boxes = []
        self.font = pygame.font.SysFont(None, 36)
        self.create_text_boxes()

    def create_text_boxes(self):
        for i in range(self.cols):  
            row = []
            for j in range(self.rows):  
                row.append(TextBox(self.x + j * self.cell_width, self.y + i * self.cell_height, self.cell_width, self.cell_height, max_length=self.max_len, screen=self.screen))
            self.text_boxes.append(row)

    def draw(self):
        for row in self.text_boxes:
            for box in row:
                box.draw()
        for i in range(self.cols):  
            label_text = str(i + 1)
            label_surface = self.font.render(label_text, True, (255, 255, 255))
            self.screen.blit(label_surface, (self.x - 20, self.y + i * self.cell_height + self.cell_height // 2))

            pygame.draw.line(self.screen, (255, 255, 255), (self.x, self.y + (i + 1) * self.cell_height),
                            (self.x + self.rows * self.cell_width, self.y + (i + 1) * self.cell_height), 2)

        for i in range(self.rows): 
            label_text = str(i + 1)
            label_surface = self.font.render(label_text, True, (255, 255, 255))
            self.screen.blit(label_surface, (self.x + i * self.cell_width + self.cell_width // 2, self.y - 20))

            pygame.draw.line(self.screen, (255, 255, 255), (self.x + (i + 1) * self.cell_width, self.y),
                            (self.x + (i + 1) * self.cell_width, self.y + self.cols * self.cell_height), 2)

    def clear(self):
        for row in self.text_boxes:
            for col in row:
                col.clear_text()

    def save_answer(self, separator):
        res = []
        for row in self.text_boxes:
            for box in row:
                res.append(box.save_answer())
        return separator.join(res)

if __name__ == "__main__":
    screen = pygame.display.set_mode((1920, 1080))
    table = Table(1000, 130, 2, 4, 70, 50, screen=screen, max_len=3) 
    running = True

    while running:
        screen.fill((0, 0, 0)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for row in table.text_boxes:
                for box in row:
                    box.input(event) 

        table.draw()
        pygame.display.flip()
    print(table.save_answer(";"))

    pygame.quit()
