"""
This is desktop app for space_game script
Created by: Creator/Eversor
Date: 22 Feb
"""

import pygame
import random
import os

pygame.init()
pygame.mixer.init()
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

"""Function: load_image
    Brief: loads image from given path
    Params: image_path: the path to the image file
"""
def load_image(image_path):
    if isinstance(image_path, str) and os.path.exists(image_path):
        print(f"Загружаем изображение: {image_path}")
        return pygame.image.load(image_path)
    else:
        print(f"Ошибка: файл по пути {image_path} не найден.")
        return None

"""Function: play_background_music
    Brief: plays background music
    Params: None
"""
def play_background_music():
    music_file = "/home/usernamezero00/Desktop/5_Projects/Data_collection_auto/audio/Linkin Park - Session.mp3" 
    if os.path.exists(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1, 0.0)

class Raindrop:
    """Class: Raindrop
    Brief: represents a single raindrop object
    Params: speed_factor: speed factor for raindrop movement
    """
    def __init__(self, speed_factor=1):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-20, screen_height - 1)
        self.length = random.randint(2, 5)
        self.width = random.randint(1, 3)
        self.speed = random.randint(2, 5)
        self.speed_factor = speed_factor

    """Function: update
        Brief: updates the position of the raindrop
        Params: None
    """
    def update(self):
        self.y += self.speed * self.speed_factor
        if self.y > screen_height:
            self.y = random.randint(-20, -1)
            self.x = random.randint(0, screen_width)

    """Function: draw
        Brief: draws the raindrop on the screen
        Params: screen: the pygame screen object
    """
    def draw(self, screen):
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + self.length), self.width)

    """Function: update_speed
        Brief: adjusts the speed of the raindrop
        Params: factor: new speed factor
    """
    def update_speed(self, factor):
        self.speed_factor = factor

class GameObject:
    """Class: GameObject
    Brief: represents a general game object with position, size, and image
    Params: x, y, width, height, image: parameters for positioning and visual representation
    """
    def __init__(self, x, y, width, height, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        if isinstance(self.image, str):
            self.image = load_image(self.image)
            if self.image:
                self.image = pygame.transform.scale(self.image, (self.width, self.height))

    """Function: draw
        Brief: draws the game object on the screen
        Params: screen: the pygame screen object
    """
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    """Function: update
        Brief: updates the position of the game object
        Params: speed: speed for vertical movement
    """
    def update(self, speed):
        self.y += speed

class Player(GameObject):
    """Class: Player
    Brief: represents the player character in the game
    Params: x, y, width, height, speed, image: parameters for the player
    """
    def __init__(self, x, y, width, height, speed, image=None):
        super().__init__(x, y, width, height, image)
        self.speed = speed

    """Function: move
        Brief: moves the player based on keyboard input
        Params: None
    """
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width:
            self.x += self.speed

class Coin(GameObject):
    """Class: Coin
    Brief: represents a coin object in the game
    Params: x, y, width, height, image: parameters for the coin
    """
    def __init__(self, x, y, width, height, image=None):
        super().__init__(x, y, width, height, image)

class Bomb(GameObject):
    """Class: Bomb
    Brief: represents a bomb object in the game
    Params: x, y, width, height, image: parameters for the bomb
    """
    def __init__(self, x, y, width, height, image=None):
        super().__init__(x, y, width, height, image)

class Game:
    """Class: Game
    Brief: main game class to manage the game logic
    Params: None
    """
    def __init__(self):
        """Function: __init__
            Brief: Initialize game objects and settings
            Params: None
        """
        self.screen = pygame.display.set_mode((600, 400))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.score = 0
        self.health = 3
        self.player = Player(300, 350, 50, 50, 5, "/home/usernamezero00/Desktop/5_Projects/PNG/rocket.png")
        self.coins = []
        self.bombs = []
        self.health_cubes = []
        self.objects_speed = 5
        self.raindrops = [Raindrop() for _ in range(100)]
        self.background = load_image("/home/usernamezero00/Desktop/5_Projects/PNG/beautiful-shining-stars-night-sky.jpg")
        self.bomb_image = load_image("/home/usernamezero00/Desktop/5_Projects/PNG/meteor-shower.png")
        self.heart_image = load_image("/home/usernamezero00/Desktop/5_Projects/PNG/heartbeat.png")
        self.coin_image = load_image("/home/usernamezero00/Desktop/5_Projects/PNG/reward.png")
        
        if self.bomb_image:
            self.bomb_image = pygame.transform.scale(self.bomb_image, (40, 40))
        if self.heart_image:
            self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))
        if self.coin_image:
            self.coin_image = pygame.transform.scale(self.coin_image, (30, 30))
            
        play_background_music()

    """Function: add_objects
        Brief: adds coins and bombs to the game
        Params: None
    """
    def add_objects(self):
        if random.randint(1, 100) <= 2:
            self.coins.append(Coin(random.randint(0, screen_width - 30), -30, 30, 30, self.coin_image))
        if random.randint(1, 100) <= 1:
            self.bombs.append(Bomb(random.randint(0, screen_width - 40), -40, 40, 40, self.bomb_image))

    """Function: update_objects
        Brief: updates the position of coins, bombs, and health cubes
        Params: None
    """
    def update_objects(self):
        for coin in self.coins[:]:
            coin.update(self.objects_speed)
            if coin.y > screen_height:
                self.coins.remove(coin)
            if (self.player.x < coin.x + coin.width and
                self.player.x + self.player.width > coin.x and
                self.player.y < coin.y + coin.height and
                self.player.y + self.player.height > coin.y):
                self.score += 1
                self.coins.remove(coin)

        for bomb in self.bombs[:]:
            bomb.update(self.objects_speed)
            if bomb.y > screen_height:
                self.bombs.remove(bomb)
            if (self.player.x < bomb.x + bomb.width and
                self.player.x + self.player.width > bomb.x and
                self.player.y < bomb.y + bomb.height and
                self.player.y + self.player.height > bomb.y):
                self.health -= 1
                self.bombs.remove(bomb)

        for health_cube in self.health_cubes[:]:
            health_cube.update(self.objects_speed)
            if health_cube.y > screen_height:
                self.health_cubes.remove(health_cube)
            if (self.player.x < health_cube.x + health_cube.width and
                self.player.x + self.player.width > health_cube.x and
                self.player.y < health_cube.y + health_cube.height and
                self.player.y + self.player.height > health_cube.y):
                self.health += 1
                self.health_cubes.remove(health_cube)

    """Function: increase_speed
        Brief: increases the speed of objects based on score
        Params: None
    """
    def increase_speed(self):
        if self.score >= 20 and self.score % 20 == 0:
            self.objects_speed = 5 + self.score // 20
            rain_speed_factor = 1 + self.score // 20 * 0.1
            for raindrop in self.raindrops:
                raindrop.update_speed(rain_speed_factor)

    """Function: draw_text
        Brief: draws text on the screen
        Params: text: the text to be drawn, color: the text color, x, y: coordinates on the screen
    """
    def draw_text(self, text, color, x, y):
        label = self.font.render(text, True, color)
        self.screen.blit(label, (x, y))

    """Function: game_over
        Brief: displays the game over message
        Params: None
    """
    def game_over(self):
        self.draw_text("GAME OVER!", RED, screen_width // 2 - 100, screen_height // 2)
        pygame.display.update()
        pygame.time.delay(2000)

    """Function: run
        Brief: main game loop
        Params: None
    """
    def run(self):
        running = True
        move_count = 0
        health_cube_spawned = False
        while running:
            if self.background:
                background_scaled = pygame.transform.scale(self.background, (screen_width, screen_height))
                self.screen.blit(background_scaled, (0, 0))
            else:
                self.screen.fill(WHITE)
            for raindrop in self.raindrops:
                raindrop.update()
                raindrop.draw(self.screen)

            self.add_objects()
            self.update_objects()
            self.increase_speed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.move()

            if self.score > 0 and self.score % 20 == 0 and not health_cube_spawned:
                self.health_cubes.append(GameObject(random.randint(0, screen_width - 40), -40, 40, 40, self.heart_image))
                self.health_cubes.append(GameObject(random.randint(0, screen_width - 40), -40, 40, 40, self.heart_image))
                self.health_cubes.append(GameObject(random.randint(0, screen_width - 40), -40, 40, 40, self.heart_image))
                self.health_cubes.append(GameObject(random.randint(0, screen_width - 40), -40, 40, 40, self.heart_image))
                self.health_cubes.append(GameObject(random.randint(0, screen_width - 40), -40, 40, 40, self.heart_image))
                health_cube_spawned = True

            if self.score % 20 != 0:
                health_cube_spawned = False

            self.player.draw(self.screen)
            for coin in self.coins:
                coin.draw(self.screen)
            for bomb in self.bombs:
                bomb.draw(self.screen)
            for health_cube in self.health_cubes:
                health_cube.draw(self.screen)

            self.draw_text(f"Score: {self.score}", WHITE, 10, 10)
            self.draw_text(f"Health: {self.health}", WHITE, 10, 40)

            if self.health <= 0:
                self.game_over()
                running = False

            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()
pygame.quit()
