import pygame
from pygame.locals import *

pygame.init()

window_screen_width = 864
window_screen_height = 936

clock = pygame.time.Clock()
frames_per_second = 60
scroll_ground = 0
scroll_speed = 4
flying_movement = False
game_ends = False

window_screen = pygame.display.set_mode((window_screen_width, window_screen_height))
pygame.display.set_caption('Flappy Bird')

background_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/background_img.png')
ground_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/ground_img.png')

class bird(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        
        for num in range(1, 4):
            
            flappy_bird_image = pygame.image.load(f'flappy_bird_asset_pack/flappy_bird_img_assets/bird_anim{num}_img.png')
            self.images.append(flappy_bird_image)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
        self.velocity = 0
        self.clicked = False
    
    def update(self):
        
        if flying_movement == True:
            
            self.velocity += 0.5
            
            if self.velocity > 8:
                
                self.velocity = 8
            
            if self.rect.bottom < 768:
                
                self.rect.y += int(self.velocity)
        
        if game_ends == False:
            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                
                self.clicked = True
                self.velocity = -10
            
            if pygame.mouse.get_pressed()[0] == 0:
                
                self.clicked = False
            
            self.counter += 1
            flap_cooldown = 5
            
            if self.counter > flap_cooldown:
                
                self.counter = 0
                self.index += 1
                
                if self.index >= len(self.images):
                    
                    self.index = 0
                
            self.image = self.images[self.index]
            
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)

        else:
            
            self.image = pygame.transform.rotate(self.images[self.index], -90)

bird_group = pygame.sprite.Group()

flappy_bird = bird(100, int(window_screen_height / 2))

bird_group.add(flappy_bird)

run_window = True

while run_window:
    
    clock.tick(frames_per_second)
    
    window_screen.blit(background_image, (0, 0))
    window_screen.blit(ground_image, (scroll_ground, 768))
    
    bird_group.draw(window_screen)
    bird_group.update()
    
    if flappy_bird.rect.bottom > 768:
        
        game_ends = True
        flying_movement = False
    
    if game_ends == False:
        
        scroll_ground -= scroll_speed
        
        if abs(scroll_ground) > 35:
            
            scroll_ground = 0
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            run_window = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and flying_movement == False and game_ends == False:
            
            flying_movement = True
    
    pygame.display.update()

pygame.quit()