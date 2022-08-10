import pygame, random, sys, time
from pygame.locals import *

# SCREEN
pygame.init()

screen_width = 1170
screen_height = 658
forest_width = 1200
forest_height = 658
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('arte-definitiva/background.png')
forest = pygame.image.load('arte-definitiva/s-forest.png')

speed = 10
gravity = 3.5
game_speed = 20
pygame.display.set_caption('Shadow Runner v1.0')
font = pygame.font.SysFont(None, 50)
click = False

mainClock = pygame.time.Clock()


class Person(pygame.sprite.Sprite):

    def __init__(self, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('arte-definitiva/person1.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person2.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person3.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person4.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person5.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person6.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person7.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person8.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person9.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/person10.png').convert_alpha()]

        self.speed = speed
        self.isJumping = False
        self.isDead = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5
        self.counter = 0
        self.score = 0

        self.current_image = 0

        self.image = pygame.image.load('arte-definitiva/person1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.left = screen_width / 15
        self.rect.bottom = int(560)
        self.rect[0] = 50
        self.rect[1] = 550

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.rect == 550:
            self.rect[1] += 0
            self.speed += 0
        if self.rect[1] < 530:
            self.rect[1] += self.speed
            self.speed += gravity * 2

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.isJumping = True
        if self.rect[1] >= 500:
            self.isJumping = False

        if self.isJumping:
            self.current_image = (self.current_image + 0)
            self.image = self.images[self.current_image]
        else:
            self.current_image = (self.current_image + 1) % 10
            self.image = self.images[self.current_image]

    def bump(self):
        self.speed = -20
        self.rect[1] -= 50


class Forest(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('arte-definitiva/s-forest.png')

        self.image = pygame.transform.scale(self.image, (forest_width, forest_height))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = screen_height - forest_height

    def update(self):
        self.rect[0] -= game_speed


class Wolf(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('arte-definitiva/wolf1.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/wolf2.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/wolf3.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/wolf4.png').convert_alpha(),
                       pygame.image.load('arte-definitiva/wolf5.png').convert_alpha()]

        self.current_image = 0
        xpos = random.randint(600, 1200)
        self.image = pygame.image.load('arte-definitiva/wolf1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = 550

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_image = (self.current_image + 5) % 5
        self.image = self.images[self.current_image]

        self.rect[0] -= game_speed


def is_off_screen(sprite):
    return sprite.rect[0] <= -(sprite.rect[2])


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    global click
    while True:

        screen.blit(background, (0, 0))
        screen.blit(forest, (0, -302))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(25, 580, 200, 50)
        button_2 = pygame.Rect(275, 580, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                sair()
        pygame.draw.rect(screen, (0, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)

        draw_text('Jogar', font, (255, 255, 255), screen, 75, 585)
        draw_text('Sair do jogo', font, (255, 255, 255), screen, 275, 585)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def game():
    person_group = pygame.sprite.Group()
    person = Person()
    person_group.add(person)

    forest_group = pygame.sprite.Group()
    for i in range(2):
        forest = Forest(forest_width * i)
        forest_group.add(forest)

    wolf_group = pygame.sprite.Group()
    for i in range(2):
        wolf = Wolf(screen_width * i)
        wolf_group.add(wolf)

    clock = pygame.time.Clock()
    player_person = Person(44, 47)
    isDead = False
    running = True
    while True:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    person.bump()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    break

        screen.blit(background, (0, 0))

        if is_off_screen(forest_group.sprites()[0]):
            new_forest = Forest(forest_height - 20)
            forest_group.add(new_forest)

            forest_group.remove(forest_group.sprites()[0])

        if is_off_screen(wolf_group.sprites()[0]):
            wolf_group.remove(wolf_group.sprites()[0])

            wolf = Wolf(screen_width * 2)

            wolf_group.add(wolf)

        player_person.update()
        person_group.update()
        forest_group.update()
        wolf_group.update()
        forest_group.draw(screen)
        wolf_group.draw(screen)
        person_group.draw(screen)
        pygame.display.update()

        if pygame.sprite.groupcollide(person_group, wolf_group, False, False, pygame.sprite.collide_mask):
            print('colisão')
            isDead = True
            gameover()
            if isDead is True:
                print('yes')
                gameover()


def gameover():
    global click

    while True:

        screen.blit(background, (0, 0))
        screen.blit(forest, (0, -302))

        draw_text('GAME OVER', font, (0, 0, 0), screen, 480, 250)


        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(25, 580, 300, 50)
        button_2 = pygame.Rect(400, 580, 300, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                sair()
        pygame.draw.rect(screen, (0, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)

        draw_text('Jogar novamente', font, (255, 255, 255), screen, 25, 585)
        draw_text('Sair do jogo', font, (255, 255, 255), screen, 450, 585)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def sair():
    pygame.quit()


main_menu()



