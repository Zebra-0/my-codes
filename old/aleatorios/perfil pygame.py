import pygame

WIDTH = 800
HEIGHT = 600
class Character:
    def __init__(self, name, max_health, strength):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.strength = strength

class Game:
    def __init__(self):
        self.screen = None
        self.character_image = None
        self.character = None

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.character_image = pygame.image.load("fotodoperfil.jpg")
        self.character_image = pygame.transform.scale(self.character_image, (100, 100))

    def run(self):
        self.init_pygame()

        self.character = Character("luiz", 100, 50)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.blit(self.character_image, (0, 0))
            self.draw_character_status(self.character)
            pygame.display.flip()

    def draw_character_status(self, character):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Nome:{character.name}", 1, (255, 255, 255))
        self.screen.blit(text, (100, 10))

        text = font.render("Vida: {}/{}".format(character.health, character.max_health), 1, (255, 255, 255))
        self.screen.blit(text, (100, 50))

        text = font.render("Força: {}".format(character.strength), 1, (255, 255, 255))
        self.screen.blit(text, (100, 90))


if __name__ == '__main__':
    game = Game()
    game.run()
