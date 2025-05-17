import random
import pygame
import pgzrun

WIDTH = 800
HEIGHT = 800

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
game_state = MENU

player_img = "ship"
enemy_img = "enemy"
bullet_img = "bullet"
background_img = "bck2"

shoot_sound = "shoot"
score_sound = "score"
dead_sound = "dead"

score = 0
enemy_speed = 2
max_enemy_speed = 5
max_enemies = 5
health = 2

def scale_actor(actor, factor):
    surf = actor._surf
    size = (int(surf.get_width() * factor), int(surf.get_height() * factor))
    actor._surf = pygame.transform.scale(surf, size)
    actor._update_pos()

class Player:
    def __init__(self):
        self.actor = Actor(player_img)
        scale_actor(self.actor, 0.5)
        self.actor.pos = (WIDTH // 2, HEIGHT - 70)
        self.speed = 5

    def move(self):
        if keyboard.left and self.actor.left > 0:
            self.actor.x -= self.speed
        if keyboard.right and self.actor.right < WIDTH:
            self.actor.x += self.speed
        if keyboard.up and self.actor.top > 0:
            self.actor.y -= self.speed
        if keyboard.down and self.actor.bottom < HEIGHT:
            self.actor.y += self.speed

    def draw(self):
        self.actor.draw()

    def get_bullet_position(self):
        return (self.actor.x + self.actor.width // 2, self.actor.top)

    def shoot(self):
        x, y = self.get_bullet_position()
        bullet = Bullet(x, y)
        bullets.append(bullet)
        sounds.shoot.play()

class Bullet:
    def __init__(self, x, y):
        self.actor = Actor(bullet_img)
        scale_actor(self.actor, 0.4) 
        self.actor.pos = (x-90, y)
        self.speed = 7

    def update(self):
        self.actor.y -= self.speed

    def draw(self):
        self.actor.draw()

    def off_screen(self):
        return self.actor.y < 0

class Enemy:
    def __init__(self, speed):
        self.actor = Actor(enemy_img)
        scale_actor(self.actor, 0.3)
        self.actor.pos = (random.randint(40, WIDTH - 40), -40)
        self.speed = speed

    def update(self):
        self.actor.y += self.speed

    def draw(self):
        self.actor.draw()

    def off_screen(self):
        return self.actor.y > HEIGHT

player = Player()
bullets = []
enemies = []
game_timer = 0

def draw():
    screen.clear()
    screen.blit(background_img, (0, 0))

    if game_state == MENU:
        screen.draw.text("SPACE SHOOTER", center=(WIDTH//2, HEIGHT//3), fontsize=60, color="white")
        screen.draw.text("Press Q to Start", center=(WIDTH//2, HEIGHT//2), fontsize=40, color="yellow")
        screen.draw.text("ESC to Quit", center=(WIDTH//2, HEIGHT//1.5), fontsize=30, color="orange")

    elif game_state == PLAYING:
        player.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=30, color="white")
        screen.draw.text(f"Health: {health}", topleft=(10, 50), fontsize=30, color="red")

    elif game_state == GAME_OVER:
        screen.draw.text("YOU LOSE!", center=(WIDTH//2, HEIGHT//3), fontsize=80, color="red")
        screen.draw.text(f"Final Score: {score}", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="white")
        if pygame.time.get_ticks() - game_timer > 3000:
            screen.draw.text("Press Q to Return to Menu", center=(WIDTH//2, HEIGHT//1.5), fontsize=30, color="yellow")

def update():
    global game_state, score, enemy_speed, health, game_timer

    if keyboard.escape:
        quit()

    if game_state == MENU:
        if keyboard.q:
            start_game()

    elif game_state == PLAYING:
        player.move()

        for bullet in bullets[:]:
            bullet.update()
            if bullet.off_screen():
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.update()
            if enemy.off_screen():
                enemies.remove(enemy)
                health -= 1
                if health <= 0:
                    game_state = GAME_OVER
                    game_timer = pygame.time.get_ticks()
                    sounds.dead.play()

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if enemy.actor.colliderect(bullet.actor):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    score += 1
                    enemy_speed = min(enemy_speed + 0.1, max_enemy_speed)
                    sounds.score.play()
                    break

        for enemy in enemies[:]:
            if enemy.actor.colliderect(player.actor):
                enemies.remove(enemy)
                health -= 1
                sounds.dead.play()
                if health <= 0:
                    game_state = GAME_OVER
                    game_timer = pygame.time.get_ticks()
                break

    elif game_state == GAME_OVER:
        if keyboard.q and pygame.time.get_ticks() - game_timer > 3000:
            game_state = MENU

def start_game():
    global score, bullets, enemies, player, enemy_speed, health, game_state
    score = 0
    bullets = []
    enemies = []
    player = Player()
    enemy_speed = 2
    health = 2
    game_state = PLAYING

def on_key_down(key):
    if game_state == PLAYING and key == keys.T:
        player.shoot()

def spawn_enemy():
    if game_state == PLAYING and len(enemies) < max_enemies:
        enemies.append(Enemy(enemy_speed))

clock.schedule_interval(spawn_enemy, 1.0)


pgzrun.go()

