import pygame
import random
import math
import sys

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1480, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ornament Collector')
FPS = 60

main_menu = pygame.image.load("Assets/main_menu.png")

# player width/height
P_WIDTH = 120
P_HEIGHT = 72

# ornament width/height
O_WIDTH = 55
O_HEIGHT = 68

# enemy width/height
E_WIDTH = 58
E_HEIGHT = 55

# bottom panel width/height
BP_WIDTH = 1480
BP_HEIGHT = 143

# tree outline width/height
TO_WIDTH = 62
TO_HEIGHT = 113

# tree width (for all tree fills - so all trees besides the outline)
T_WIDTH = 55

# full tree height
FT_HEIGHT = 76

# 4/5 tree height
FOUR_T_HEIGHT = 62

# 3/5 tree height
THREE_T_HEIGHT = 49

# 2/5 tree height
TWO_T_HEIGHT = 35

# 1/5 tree height
ONE_T_HEIGHT = 21

# health bar outline width/height
HBO_WIDTH = 269
HBO_HEIGHT = 23

# health bar width/height
HB_WIDTH = 267
HB_HEIGHT = 21

# coin icon width/height
CI_WIDTH = 23
CI_HEIGHT = 18

# coin panel width/height
CP_WIDTH = 146
CP_HEIGHT = 59

# strokes panel width/height
SP_WIDTH = 230
SP_HEIGHT = 59

# score panel width/height
SCP_WIDTH = WIDTH - CP_WIDTH - SP_WIDTH
SCP_HEIGHT = 59

# upgrade button width/height
UB_WIDTH = 140
UB_HEIGHT = 62

# health font width
HF_WIDTH = 104

# retry button width/height
RB_WIDTH = 175
RB_HEIGHT = 35

max_health = 5000

# player x and y coordinates when first starting
P_X = 680
P_Y = 348

BALL_HEALTH_FONT = pygame.font.SysFont("centurygothic", 30)
COIN_FONT = pygame.font.SysFont("centurygothic", 15)
STROKES_FONT = pygame.font.SysFont("centurygothic", 20)
SCORE_FONT = pygame.font.SysFont("centurygothic", 40)
DIED_FONT = pygame.font.SysFont("centurygothic", 70)

retry_button = pygame.Rect(WIDTH//2 - RB_WIDTH//2, HEIGHT//2 - RB_HEIGHT//2 + 35, RB_WIDTH, RB_HEIGHT)
main_menu_button = pygame.Rect(WIDTH//2 - RB_WIDTH//2, retry_button.y + RB_HEIGHT + 25, RB_WIDTH, RB_HEIGHT)
dead_quit_button = pygame.Rect(WIDTH//2 - RB_WIDTH//2, retry_button.y + RB_HEIGHT*2 + 50, RB_WIDTH, RB_HEIGHT)

ornament_image = pygame.image.load("Assets/ornament.png")
character = pygame.image.load("Assets/character.png")
enemy_image = pygame.image.load("Assets/enemy.png")

bottom_panel = pygame.Rect(0, (HEIGHT - 126), BP_WIDTH, BP_HEIGHT)

tree_outline = pygame.image.load("Assets/tree_outline.png")

full_tree = pygame.image.load("Assets/tree_full.png")
four_tree = pygame.image.load("Assets/4part_tree.png")
three_tree = pygame.image.load("Assets/3part_tree.png")
two_tree = pygame.image.load("Assets/2part_tree.png")
one_tree = pygame.image.load("Assets/1part_tree.png")

healthbar_outline = pygame.image.load("Assets/healthbar_outline.png")
healthbar = pygame.Rect(TO_WIDTH + HF_WIDTH*2, HEIGHT - BP_HEIGHT + HB_HEIGHT//2 + BP_HEIGHT//2 - 9, HB_WIDTH, HB_HEIGHT)

coin_icon = pygame.image.load("Assets/coin_icon.png")
coin_panel = pygame.Rect(0, 0, CP_WIDTH, CP_HEIGHT)
coins = 0
coins_str = "0"

strokes_panel = pygame.Rect(WIDTH - SP_WIDTH, 0, SP_WIDTH, SP_HEIGHT)
score_panel = pygame.Rect(CP_WIDTH, 0, SCP_WIDTH, SCP_HEIGHT)

death_screen = pygame.Surface((WIDTH, HEIGHT))
death_screen.set_alpha(200)
death_screen.fill((0))

ENEMY_HIT_SOUND = pygame.mixer.Sound("Assets/enemy_hit_sound.wav")
ORNAMENT_COLLECT_SOUND = pygame.mixer.Sound("Assets/ornament_collect_sound.wav")
LEVEL_COMPLETE_SOUND = pygame.mixer.Sound("Assets/level_complete_sound.wav")

# upgrades
health_upgrade = pygame.Rect(healthbar.x + HB_WIDTH + 40, HEIGHT - BP_HEIGHT + BP_HEIGHT//2 - UB_HEIGHT//2 + 10, UB_WIDTH, UB_HEIGHT)
hu_image = pygame.image.load("Assets/health_upgrade.png")
health_upgrade_max = pygame.image.load("Assets/health_upgrade_max.png")

speed_upgrade = pygame.Rect(healthbar.x + HB_WIDTH + UB_WIDTH + 60, HEIGHT - BP_HEIGHT + BP_HEIGHT//2 - UB_HEIGHT//2 + 10, UB_WIDTH, UB_HEIGHT)
su_image = pygame.image.load("Assets/speed_upgrade.png")
speed_upgrade_max = pygame.image.load("Assets/speed_upgrade_max.png")


def draw(player, aim_line, tree_outline_r, full_tree_r, four, three, two, one, ornaments, enemies, tree_level, coins, max_strokes, level_strokes, score, hu_level, su_level, coins_for_hu, coins_for_su, hu_max, su_max, dead, reason_for_death):
    global death_screen
    
    screen.fill((255, 255, 255))
    
    for ornament in ornaments:
        screen.blit(ornament_image, (ornament.x, ornament.y))
    
    for enemy in enemies:
        screen.blit(enemy_image, (enemy.x, enemy.y))

    if aim_line: 
        pygame.draw.line(screen, "black", aim_line[0], aim_line[1], 2)
    
    pygame.draw.rect(screen, (231, 231, 231), bottom_panel)
    screen.blit(tree_outline, (tree_outline_r.x, tree_outline_r.y))
    screen.blit(character, (player.x, player.y))

    pygame.draw.rect(screen, (255, 248, 178), coin_panel)

    if tree_level == 1:
        screen.blit(one_tree, (one.x - 1, one.y + 11))
    elif tree_level == 2:
        screen.blit(two_tree, (two.x - 1, two.y + 5))
    elif tree_level == 3:
        screen.blit(three_tree, (three.x - 1, three.y - 3))
    elif tree_level == 4:
        screen.blit(four_tree, (four.x - 1, four.y - 9))
    elif tree_level == 5:
        screen.blit(full_tree, (full_tree_r.x - 1, full_tree_r.y - 11.5))
    elif tree_level == 0:
        screen.blit(tree_outline, (tree_outline_r.x, tree_outline_r.y))
    
    health_font = BALL_HEALTH_FONT.render("Health:", 1, "black")
    screen.blit(health_font, (TO_WIDTH + health_font.get_width() - 15, bottom_panel.centery - health_font.get_height()//2 - 8))

    coin_font = COIN_FONT.render(f"{coins}", 1, "black")
    screen.blit(coin_font, (30 + CI_WIDTH, CP_HEIGHT//2 - CI_HEIGHT//2))

    pygame.draw.rect(screen, (184, 185, 255), strokes_panel)
    strokes_font = STROKES_FONT.render(f"Remaining Strokes: {max_strokes - level_strokes}", 1, "black")
    screen.blit(strokes_font, (WIDTH - strokes_font.get_width() - 13, 13))
    
    pygame.draw.rect(screen, (234, 234, 234), score_panel)
    score_font = SCORE_FONT.render(f"{score}", 1, "black")
    screen.blit(score_font, (CP_WIDTH + SCP_WIDTH//2 - score_font.get_width()//2, SCP_HEIGHT//2 - score_font.get_height()//2))

    full_tree_r.centerx, full_tree_r.centery = tree_outline_r.centerx, tree_outline_r.centery
    four.centerx, four.centery = tree_outline_r.centerx, tree_outline_r.centery
    three.centerx, three.centery = tree_outline_r.centerx, tree_outline_r.centery
    two.centerx, two.centery = tree_outline_r.centerx, tree_outline_r.centery
    one.centerx, one.centery = tree_outline_r.centerx, tree_outline_r.centery

    pygame.draw.rect(screen, (255, 76, 76), healthbar)
    screen.blit(healthbar_outline, (TO_WIDTH + health_font.get_width()*2, bottom_panel.centery - HBO_HEIGHT//2 - 5)) #1042 (1176.5), 697 (708.8)

    screen.blit(coin_icon, (20, CP_HEIGHT//2 - CI_HEIGHT//2))

    screen.blit(hu_image, (health_upgrade.x, health_upgrade.y))
    screen.blit(su_image, (speed_upgrade.x, speed_upgrade.y))

    hu_level_font = COIN_FONT.render(f"CUR LVL: {hu_level}", 1, (110, 110, 110))
    su_level_font = COIN_FONT.render(f"CUR LVL: {su_level}", 1, (110, 110, 110))

    hu_coins = COIN_FONT.render(f"{coins_for_hu[hu_level]}", 1, "black")
    su_coins = COIN_FONT.render(f"{coins_for_su[su_level]}", 1, "black")

    screen.blit(hu_level_font, (health_upgrade.x + 50, health_upgrade.y + 15))
    screen.blit(hu_coins, (health_upgrade.x + 77, health_upgrade.y + 37))
    screen.blit(su_level_font, (speed_upgrade.x + 50, speed_upgrade.y + 13))
    screen.blit(su_coins, (speed_upgrade.x + 77, speed_upgrade.y + 35))

    if hu_max:
        screen.blit(health_upgrade_max, (health_upgrade.x, health_upgrade.y))
    if su_max:
        screen.blit(speed_upgrade_max, (speed_upgrade.x, speed_upgrade.y))
    
    if dead:
        screen.blit(death_screen, (0, 0))
        dead_font = DIED_FONT.render(f"You died! Your score was {score}!", 1, "white")
        screen.blit(dead_font, (WIDTH//2 - dead_font.get_width()//2, HEIGHT//2 - dead_font.get_height()//2 - 100))

        pygame.draw.rect(screen, "white", retry_button)
        pygame.draw.rect(screen, "white", main_menu_button)
        pygame.draw.rect(screen, "white", dead_quit_button)

        reason_font = STROKES_FONT.render(f"{reason_for_death}", 1, "white")
        screen.blit(reason_font, (WIDTH//2 - reason_font.get_width()//2, HEIGHT//2 - reason_font.get_height()//2 + dead_font.get_height() - 100))

        retry_font = COIN_FONT.render("Retry", 1, "black")
        main_menu_font = COIN_FONT.render("Main Menu", 1, "black")
        dead_quit_font = COIN_FONT.render("Quit", 1, "black")
        screen.blit(retry_font, ((retry_button.x + RB_WIDTH) - retry_font.get_width()//2 - RB_WIDTH//2, (retry_button.y + RB_HEIGHT) - retry_font.get_height()//2 - RB_HEIGHT//2 - 2))
        screen.blit(main_menu_font, ((main_menu_button.x + RB_WIDTH) - main_menu_font.get_width()//2 - RB_WIDTH//2, (main_menu_button.y + RB_HEIGHT) - main_menu_font.get_height()//2 - RB_HEIGHT//2 - 2))
        screen.blit(dead_quit_font, ((dead_quit_button.x + RB_WIDTH) - dead_quit_font.get_width()//2 - RB_WIDTH//2, (dead_quit_button.y + RB_HEIGHT) - dead_quit_font.get_height()//2 - RB_HEIGHT//2 - 2))

    pygame.display.update()


def generate_map(ornaments, enemies, player):
    # generate ornaments
    for _ in range(random.randint(3, 5)):
        ornament = pygame.Rect(random.randint(SCP_HEIGHT, WIDTH - O_WIDTH), random.randint(SCP_HEIGHT, HEIGHT - O_HEIGHT - BP_HEIGHT), O_WIDTH, O_HEIGHT)
        ornaments.append(ornament)

        for i in range(len(ornaments) - 1):
            if ornament.colliderect(ornaments[i]):
                ornament_collision = True
                while ornament_collision:
                    ornament.x, ornament.y = random.randint(SCP_HEIGHT, WIDTH - O_WIDTH), random.randint(SCP_HEIGHT, HEIGHT - O_HEIGHT - BP_HEIGHT)
                    if not ornament.colliderect(ornaments[i]):
                        ornament_collision = False
                        break
    
    # generate enemies
    for _ in range(random.randint(2, 4)):
        enemy = pygame.Rect(random.randint(SCP_HEIGHT, WIDTH - E_WIDTH), random.randint(SCP_HEIGHT, HEIGHT - E_HEIGHT - BP_HEIGHT), E_WIDTH, E_HEIGHT)
        enemies.append(enemy)

        for j in range(len(enemies) - 1):
            if enemy.colliderect(enemies[j]):
                enemy_collision = True
                while enemy_collision:
                    enemy.x, enemy.y = random.randint(SCP_HEIGHT, WIDTH - E_WIDTH), random.randint(SCP_HEIGHT, HEIGHT - E_HEIGHT - BP_HEIGHT)
                    if not enemy.colliderect(enemies[j]):
                        enemy_collision = False
                        break
    
    for k in range(len(ornaments)):
        for l in range(len(enemies)):
            c_ornament, c_enemy = ornaments[k], enemies[l]
            if c_ornament.colliderect(c_enemy):
                ornament_enemy_collision = True
                while ornament_enemy_collision:
                    c_ornament.x, c_ornament.y = random.randint(SCP_HEIGHT, WIDTH - P_WIDTH), random.randint(SCP_HEIGHT, HEIGHT - P_HEIGHT - BP_HEIGHT)
                    if not c_ornament.colliderect(c_enemy):
                        ornament_enemy_collision = False
                        break
    
    rplayercx, rplayercy = random.randint(SCP_HEIGHT, WIDTH - P_WIDTH), random.randint(SCP_HEIGHT, HEIGHT - P_HEIGHT - BP_HEIGHT)
    player.x, player.y = rplayercx, rplayercy
    for ornamentcp in ornaments:
        for enemycp in enemies:
            if player.colliderect(ornamentcp) or player.colliderect(enemycp):
                playercollision = True
                while playercollision:
                    rplayercx, rplayercy = random.randint(SCP_HEIGHT, WIDTH - P_WIDTH), random.randint(SCP_HEIGHT, HEIGHT - P_HEIGHT - BP_HEIGHT)
                    player.x, player.y = rplayercx, rplayercy

                    if not player.colliderect(ornamentcp) and not player.colliderect(enemycp):
                        playercollision = False
                        break

    return [max(3, len(ornaments) - 1), rplayercx, rplayercy, len(ornaments)]
    

def main():
    global coins, coins_str
    global max_health

    run = True
    clock = pygame.time.Clock()   
    velocity = [0, 0]
    dragging = False
    aim_line = []

    player = pygame.Rect(WIDTH//2 - P_WIDTH//2, HEIGHT//2 - P_HEIGHT//2 - BP_HEIGHT//2 + SCP_HEIGHT//2, P_WIDTH, P_HEIGHT)

    tree_outline_r = pygame.Rect(50, bottom_panel.centery - TO_HEIGHT//2 - 8, TO_WIDTH, TO_HEIGHT)
    full_tree_r = pygame.Rect(500, 300, T_WIDTH, FT_HEIGHT)
    four_tree_r = pygame.Rect(500, 300, T_WIDTH, FOUR_T_HEIGHT)
    three_tree_r = pygame.Rect(500, 300, T_WIDTH, THREE_T_HEIGHT)
    two_tree_r = pygame.Rect(500, 300, T_WIDTH, TWO_T_HEIGHT)
    one_tree_r = pygame.Rect(500, 300, T_WIDTH, ONE_T_HEIGHT)

    ornaments = []
    enemies = []

    tree_level = 0

    health = max_health

    level_strokes = 0
    max_strokes = 0
    speed_limiter = 11

    score = 0

    max_strokes, rplayercx, rplayercy, lvlornament_len = generate_map(ornaments, enemies, player)

    su_level = 0
    hu_level = 0
    coins_for_hu = [100, 150, 225, 338, 507]
    coins_for_su = [200, 300, 450, 675, 1013]
    su_max = False
    hu_max = False

    dead = False
    reason_for_death = ""

    with open("coins.txt", "r") as f_coins:
        coins = int(f_coins.read())
        f_coins.close()

    if coins < 1000000:
        coins_str = str(coins)
    elif 1000000 < coins < 1000000000:
        coins_str = f"{round(coins/1000000, 1)}M"
    elif 1000000000 <= coins < 1000000000000:
        coins_str = f"{round(coins/1000000000, 1)}B"
    elif 1000000000000 <= coins < 1000000000000000:
        coins_str = f"{round(coins/1000000000000, 1)}T"
    else:
        coins_str = str(coins)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if not dead:
                if event.type == pygame.QUIT:
                    run = False
                    break
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    de_x, de_y = event.pos # de = down event (mouse button down event)

                    if not dragging and int(velocity[0]) == 0 and int(velocity[1]) == 0:
                        if player.x + P_WIDTH >= de_x >= player.x and player.y + P_HEIGHT >= de_y >= player.y:
                            dragging = True
                            aim_line = [player.center, (de_x, de_y)]

                    if health_upgrade.x + UB_WIDTH >= de_x >= health_upgrade.x and health_upgrade.y + UB_HEIGHT >= de_y >= health_upgrade.y:
                        if coins_for_hu[hu_level] <= coins:
                            if not hu_max:
                                coins -= coins_for_hu[hu_level]
                                coins_str = str(coins)
                                if hu_level + 1 <= 4:
                                    max_health *= 1.1
                                    health *= 1.1
                                    hu_level += 1
                                else:
                                    hu_max = True
                    elif speed_upgrade.x + UB_WIDTH >= de_x >= speed_upgrade.x and speed_upgrade.y + UB_HEIGHT >= de_y >= speed_upgrade.y:
                        if coins_for_su[su_level] <= coins:
                            if not su_max:
                                coins -= coins_for_su[su_level]
                                coins_str = str(coins)
                                if su_level + 1 <= 4:
                                    speed_limiter *= 0.85
                                    su_level += 1
                                else:
                                    su_max = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging:
                        level_strokes += 1

                        ue_x, ue_y = event.pos # ue = up event (mouse button up event)

                        dx = ue_x - de_x # dx = distance of x points of up & down events
                        dy = ue_y - de_y # dy = distance of y points of up & down events
                        speed = math.sqrt(dx**2 + dy**2) / speed_limiter
                        angle = math.atan2(dy, dx)
                        velocity = [(speed * math.cos(angle)) * -1, (speed * math.sin(angle)) * -1]
                        aim_line = []
                        
                        dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        me_x, me_y = event.pos # me = move event (mouse move event)
                        dir_x = player.centerx - me_x
                        dir_y = player.centery - me_y
                        opposite_x = player.centerx + dir_x 
                        opposite_y = player.centery + dir_y
                        aim_line[1] = (opposite_x, opposite_y)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    d_de_x, d_de_y = event.pos

                    if retry_button.x + RB_WIDTH >= d_de_x >= retry_button.x and retry_button.y + RB_HEIGHT >= d_de_y >= retry_button.y:
                        health = max_health
                        healthbar.width = HB_WIDTH
                        main()
                    elif main_menu_button.x + RB_WIDTH >= d_de_x >= main_menu_button.x and main_menu_button.y + RB_HEIGHT >= d_de_y >= main_menu_button.y:
                        health = max_health
                        healthbar.width = HB_WIDTH
                        main_menu_screen()
                    elif dead_quit_button.x + RB_WIDTH >= d_de_x >= dead_quit_button.x and dead_quit_button.y + RB_HEIGHT >= d_de_y >= dead_quit_button.y:
                        pygame.quit()
                        sys.exit()
                        run = False
                        break
            if event.type == pygame.QUIT:
                run = False
                break
            
        if not dragging and velocity != [0, 0]:
            if player.x + int(velocity[0]) > 0 and player.x + P_WIDTH + int(velocity[0]) < WIDTH:
                player.x += int(velocity[0])
            else:
                velocity[0] *= -1

            if player.y + int(velocity[1]) > SCP_HEIGHT and player.y + P_HEIGHT + int(velocity[1]) < HEIGHT - BP_HEIGHT:
                player.y += int(velocity[1])
            else:
                velocity[1] *= -1
            
            velocity[0] *= 0.95
            velocity[1] *= 0.95

            for ornament in ornaments:
                if player.colliderect(ornament):
                    ornaments.remove(ornament)
                    tree_level += 1
                    if tree_level >= 5:
                        tree_level = 0
                        coins += 100
                        if coins < 1000000:
                            coins_str = str(coins)
                        elif 1000000 < coins < 1000000000:
                            coins_str = f"{round(coins/1000000, 1)}M"
                        elif 1000000000 <= coins < 1000000000000:
                            coins_str = f"{round(coins/1000000000, 1)}B"
                        elif 1000000000000 <= coins < 1000000000000000:
                            coins_str = f"{round(coins/1000000000000, 1)}T"
                        else:
                            coins_str = str(coins)
                    
                    if len(ornaments) <= 0:
                        LEVEL_COMPLETE_SOUND.play()
                        strokes_ratio = (max_strokes / level_strokes) * 100
                        score_added = strokes_ratio * lvlornament_len

                        enemies.clear()
                        ornaments.clear()
                        velocity = [0, 0]
                        level_strokes = 0
                        max_strokes, rplayercx, rplayercy, lvlornament_len = generate_map(ornaments, enemies, player)
                        player.x, player.y = rplayercx, rplayercy
                        score += int(round(score_added, 0))
                    else:
                        ORNAMENT_COLLECT_SOUND.play()
            
            for enemy in enemies:
                if player.colliderect(enemy):
                    ENEMY_HIT_SOUND.play()

                    health -= 500
                    decreasing_factor = health / max_health
                    new_hb_width = HB_WIDTH * decreasing_factor
                    healthbar.width = new_hb_width

                    velocity = [0, 0]
                    player.x, player.y = rplayercx, rplayercy
        
        if int(velocity[0]) == 0 and int(velocity[1]) == 0:
            if len(ornaments) > 0 and level_strokes >= max_strokes:
                reason_for_death = "You ran out of strokes!"
                dead = True
        if health <= 0:
            health = 0
            reason_for_death = "You ran out of health!"
            dead = True
        
        with open("coins.txt", "w") as f_coins:
            f_coins.write(str(coins))
            f_coins.close()
            
        draw(
            player, 
            aim_line, 
            tree_outline_r, 
            full_tree_r, 
            four_tree_r, 
            three_tree_r, 
            two_tree_r, 
            one_tree_r, 
            ornaments, 
            enemies, 
            tree_level, 
            coins_str,
            max_strokes,
            level_strokes,
            score,
            hu_level,
            su_level,
            coins_for_hu,
            coins_for_su,
            hu_max,
            su_max,
            dead,
            reason_for_death
        )
    
    pygame.quit()


def main_menu_screen():
    main_menu_on = True
    
    while main_menu_on:
        screen.fill((255, 255, 255))
        screen.blit(main_menu, (0, 0))

        pygame.draw.rect(screen, "lightgray", main_menu_button)
        play_text = COIN_FONT.render("Play", 1, "black")
        screen.blit(play_text, ((main_menu_button.x + RB_WIDTH) - play_text.get_width()//2 - RB_WIDTH//2, (main_menu_button.y + RB_HEIGHT) - play_text.get_height()//2 - RB_HEIGHT//2 - 2))

        pygame.draw.rect(screen, "lightgray", dead_quit_button)
        quit_text = COIN_FONT.render("Quit", 1, "black")
        screen.blit(quit_text, ((dead_quit_button.x + RB_WIDTH) - quit_text.get_width()//2 - RB_WIDTH//2, (dead_quit_button.y + RB_HEIGHT) - quit_text.get_height()//2 - RB_HEIGHT//2 - 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mm_de_x, mm_de_y = event.pos

                if main_menu_button.x + UB_WIDTH >= mm_de_x >= main_menu_button.x and main_menu_button.y + UB_HEIGHT >= mm_de_y >= main_menu_button.y:
                    main_menu_on = False
                    main()
                elif dead_quit_button.x + UB_WIDTH >= mm_de_x >= dead_quit_button.x and dead_quit_button.y + UB_HEIGHT >= mm_de_y >= dead_quit_button.y:
                    pygame.quit()
                    sys.exit()
                    main_menu_on = False
                    break
        
        pygame.display.update()


if __name__ == '__main__':
    main_menu_screen()