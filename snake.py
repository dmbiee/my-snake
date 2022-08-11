import pygame as pg
import sys 
import random
import time


RES = [800,600]

# ------- COLORS
RED = (198,17,51)
SILIVER = (198, 198, 198)
GOLD = (237, 192, 87)
SNAKE_COLOR = (104,157,87)

BG_MENU = (59,66,73)
FONT_COLOR_MENU = (200,200,200)

GAME_BG_COLOR = (36,39,45)
SETTING_BG_COLOR = (56,59,65)

EMPTY_PROGRESS_BAR = (76, 88, 101)
# ------- COLORS

# ------- CONTAINERS
menu_height = 100

pixel_param = 20

score = 0

bits_progress_bar = 0 # частичка которая заполняет прогрес бар при сьедении обычного фрукта

fruit_pos = None
golden_fruit_pos = None
timer_for_golden_fruit = 0 # переменная служащая подсчету сколько сьедено обычных фруктов, когда будет 10, то обнулится и создаст золотой фрукт

temp_var_for_golden_fruit = True # Переменная чтобы единоразово за появления фрукта засечь время для его удаления
temp_var_for_golden_progressbar = True
movement_position = 'Right' # Переменная для передвижения имеющая изначально стандартное направление
setting = False
start = True
# ------- CONTAINERS

pg.init()
pg.mixer.init()
pg.display.set_caption("snake 54")

screen = pg.display.set_mode(RES)

clock = pg.time.Clock()

def background(pg) :
    bg = pg.Surface(screen.get_size())
    bg.fill(GAME_BG_COLOR)
    return bg

def setting_background(pg):
    st_bg = pg.Surface(screen.get_size())
    st_bg.fill(SETTING_BG_COLOR)
    return st_bg

# -------------FRUCT
def draw_fruit(pg):
    # Фунция создает рандомную позицию для фрукта через random.randrange, с шагом в pixel_param
    fruit_pos = (random.randrange(0, screen.get_size()[0], pixel_param), random.randrange(menu_height, screen.get_size()[1], pixel_param))
    
    for snake_pixel in arr_snake:
    # Циклом проверяется находится ли позиция для нового фрукта в самом теле змейки, если да - то функция вызывается ещё раз
        if snake_pixel['x'] == fruit_pos[0] and snake_pixel['y'] == fruit_pos[1]:
            return draw_fruit(pg)
        
    # Рисуем фрукт по найденым координатам
    pg.draw.rect(screen, RED, (fruit_pos[0], fruit_pos[1], pixel_param, pixel_param))
    
    # Возращаем позицию чтобы закрепить фрукт
    return fruit_pos

def eat_fruit() :
    global timer_for_golden_fruit, fruit_pos, score, bits_progress_bar
    
    if fruit_pos == None: # Если фрукта на поле нету, то выходим из функции
        return
    
    if arr_snake[-1]['x'] == fruit_pos[0] and arr_snake[-1]['y'] == fruit_pos[1]: # Проверяет одинаковы ли координаты головы и фрукта
        fruit_pos = None # Сделано это чтобы в дальнейшем нарисовать новый фрукт

        # В данном случае хвост дублируется
        arr_snake.insert(0, { 
            'x': arr_snake[0]['x'],
            'y': arr_snake[0]['y'],
            'color': SNAKE_COLOR
        })

        score += 10

        if golden_fruit_pos == None:
            timer_for_golden_fruit += 1
            bits_progress_bar += (0.4*screen.get_size()[0]) / 10

def draw_golden_fruit(pg):
    # Фунция создает рандомную позицию для  золотого фрукта через random.randrange, с шагом в pixel_param
    global bits_progress_bar, timer_for_golden_fruit
    if timer_for_golden_fruit < 10: # Счетчик для появления золотого фрукта, добавляется при сьедении обычного 
        return
    
    golden_fruit_pos = (random.randrange(0, screen.get_size()[0], pixel_param), random.randrange(menu_height, screen.get_size()[1], pixel_param))

    for snake_pixel in arr_snake:
    # Циклом проверяется находится ли позиция для нового золотого фрукта в самом теле змейки, если да - то функция вызывается ещё раз
        if snake_pixel['x'] == golden_fruit_pos[0] and snake_pixel['y'] == golden_fruit_pos[1]:
            return draw_golden_fruit(pg)
        
    # Рисуем золотой фрукт по найденым координатам
    pg.draw.rect(screen, GOLD, (golden_fruit_pos[0], golden_fruit_pos[1], pixel_param, pixel_param))
    timer_for_golden_fruit = 0
    bits_progress_bar = 0
    # Возращаем позицию чтобы закрепить золотой фрукт
    return golden_fruit_pos

def eat_golden_fruit():
    global timer_for_golden_fruit, golden_fruit_pos, score,temp_var_for_golden_progressbar,temp_var_for_golden_fruit, bits_progress_bar
    
    if golden_fruit_pos == None:
        return
    
    if arr_snake[-1]['x'] == golden_fruit_pos[0] and arr_snake[-1]['y'] == golden_fruit_pos[1]: # Проверяет одинаковы ли координаты головы и золотого фрукта
        golden_fruit_pos = None # Сделано это чтобы в дальнейшем нарисовать новый золотой фрукт
        
        for _ in range(3):
            arr_snake.insert(0, { 
            'x': arr_snake[0]['x'],
            'y': arr_snake[0]['y'],
            'color': SNAKE_COLOR
        })
            
        score += 50
        temp_var_for_golden_progressbar = True
        temp_var_for_golden_fruit = True
        bits_progress_bar = 0

        

def move_golden_fruit(screen, random):
    global golden_fruit_pos, temp_var_for_golden_fruit, delete_time, timer_for_golden_fruit, bits_progress_bar, temp_var_for_golden_progressbar, temp_time

    vectors = ('Up', 'Down', 'Left', 'Right')

    if golden_fruit_pos == None:
        return
    
    temp_time = float('%0.5f' % time.time()) # Время в которое создался золотой фрукт, нужно чтобы вычесть когда его нужно убрать.
    
    if temp_var_for_golden_fruit: # if нужен чтобы единоразово записать данные в delete_time
        delete_time = (temp_time + 10)
        temp_var_for_golden_fruit = False
    
    
    if float('%0.1f' % temp_time) == float('%0.1f' % delete_time): # Когда temp_time == delete_time тогда очищаются использованые переменные для золотого фрукта
        golden_fruit_pos = None
        temp_var_for_golden_fruit = True
        temp_var_for_golden_progressbar = True
        bits_progress_bar = 0
        return
    
    temp_random = random.randrange(1,11)        #
    if temp_random == 5:                        # три строки которые определяют рандомность хождения золотого фрукта  
        move_vector = random.choice(vectors)    #
        
        if move_vector == 'Up':
            golden_fruit_pos = golden_fruit_pos[0], golden_fruit_pos[1] - pixel_param
            if golden_fruit_pos[1] < menu_height:
                golden_fruit_pos = golden_fruit_pos[0], screen.get_size()[1] - pixel_param
                
        if move_vector == 'Down':
            golden_fruit_pos = golden_fruit_pos[0], golden_fruit_pos[1] + pixel_param
            if golden_fruit_pos[1] + pixel_param > screen.get_size()[1]:
                golden_fruit_pos = golden_fruit_pos[0], menu_height
                
        if move_vector == 'Left':
            golden_fruit_pos = golden_fruit_pos[0] - pixel_param, golden_fruit_pos[1]
            if golden_fruit_pos[0] < 0:
                golden_fruit_pos = screen.get_size()[0] - pixel_param, golden_fruit_pos[1]
                
        if move_vector == 'Right':
            golden_fruit_pos = golden_fruit_pos[0] + pixel_param, golden_fruit_pos[1]
            if golden_fruit_pos[0] + pixel_param > screen.get_size()[0]:
                golden_fruit_pos = 0, golden_fruit_pos[1]
        
        return golden_fruit_pos
    
# -------------FRUCT

# -------------SNAKE

def new_snake() :
    snake = [] # Список сегментов змейки
    for i in range(0, 3):
        snake.append({
            'x':100,
            'y':menu_height + pixel_param,
            'color': SNAKE_COLOR
        })
    return snake

# Функция new_snake() вызывается 1 раз пока код проходит до бесконечного цикла и в arr_snake записывается
# список трёх сегментов змейки в который будет записыватся дальнейшие сегменты 
arr_snake = new_snake() 

def draw_snake(pg):
# Функция посегментно рисует квадратики змейки из переменной arr_snake, которая содержит список сегментов
    for pixel_snake in arr_snake:
        pg.draw.rect(screen, pixel_snake["color"], (pixel_snake["x"], pixel_snake["y"], pixel_param, pixel_param))

def move_snake(pg, screen):
    # Функция двигает змейку путем переставления "хвоста" змейки в нужную
    
    temp_pixel_snake = arr_snake.pop(0) # В временную переменную записываем сегмент хвоста

    if movement_position == 'Right' :                                               # Когда movment_position == Right, то 
        temp_pixel_snake['x'] = arr_snake[-1]['x'] + pixel_param                    # то хвост змейки во временной переменной присваевается 'x' координаты головы + pixel_param
        temp_pixel_snake['y'] = arr_snake[-1]['y']                                  # координаты хвоста "У" меняются на координаты головы
        if screen.get_size()[0]- pixel_param < arr_snake[-1]['x'] + pixel_param:    # В данном блаке реализован телепорт от обного края экрана в другой 
            temp_pixel_snake['x'] = 0                                               # Реализовано путём получения ширины экрана и если координаты головы больше чем ширина экрана 
                                                                                    # то временной переменной присваивается 0
    if movement_position == 'Left' :
        temp_pixel_snake['x'] = arr_snake[-1]['x'] - pixel_param
        temp_pixel_snake['y'] = arr_snake[-1]['y']
        if  0 > arr_snake[-1]['x'] - pixel_param:
            temp_pixel_snake['x'] = screen.get_size()[0] - pixel_param
  
    if movement_position == 'Up' :
        temp_pixel_snake['y'] = arr_snake[-1]['y'] - pixel_param
        temp_pixel_snake['x'] = arr_snake[-1]['x']
        if menu_height > arr_snake[-1]['y'] - pixel_param: 
            temp_pixel_snake['y'] = screen.get_size()[1] - pixel_param
  
    if movement_position == 'Down' :
        temp_pixel_snake['y'] = arr_snake[-1]['y'] + pixel_param
        temp_pixel_snake['x'] = arr_snake[-1]['x']
        if screen.get_size()[1] - pixel_param < arr_snake[-1]['y'] + pixel_param:
            temp_pixel_snake['y'] = menu_height
            
    # В переменную которая хранит список змейки, в конец присваевается временная переменная, якобы в голову
    arr_snake.append(temp_pixel_snake)
# -------------SNAKE

def new_game() :
    # Функция которая вызывается вызовом функции game_over() и приводит все переменные к изначальному виду.
    global arr_snake, movement_position, fruit_pos, score, timer_for_golden_fruit, golden_fruit_pos, bits_progress_bar,temp_var_for_golden_fruit,temp_var_for_golden_progressbar
    arr_snake = new_snake()
    movement_position = 'Right'
    golden_fruit_pos = None
    fruit_pos = None
    score = 0
    timer_for_golden_fruit = 0
    bits_progress_bar = 0
    temp_var_for_golden_progressbar = True
    temp_var_for_golden_fruit = True
   
 
def game_over():
    for pixel_snake in arr_snake : # Цикл проверяет каждый пиксель змейки 
        # print(len(arr_snake)-1 == arr_snake.index(pixel_snake))
        if len(arr_snake)-1 == arr_snake.index(pixel_snake): # Если количество сегментов змейки без головы равна  Я ХУЙ ЗНАЕТ ЧТО ЭТО И КАК РАБОТАЕТ 
            return 
        if arr_snake[-1]['x'] == pixel_snake['x'] and arr_snake[-1]['y'] == pixel_snake['y']: # Если координаты головы "Х" и "У" == одному из пикселей змейки, то вызывается new_game()
            new_game()
            return

def draw_menu(pg, screen): 
    global score
    pg.draw.rect(screen, BG_MENU, [0, 0 ,screen.get_size()[0], menu_height])
 
    # -------- score
    score_font_size = 30
    font_score = pg.font.Font(None, score_font_size)
    text_score = font_score.render( 'Score: ' + str(score), True, FONT_COLOR_MENU )
    text_setting = font_score.render( 'Setting (y)', True, FONT_COLOR_MENU )
    screen.blit( text_setting, ( screen.get_size()[0] - 150, ( menu_height -score_font_size ) / 2 ) )
    screen.blit( text_score, ( 50, ( menu_height -score_font_size ) / 2 ) )


def golden_fruit_progress_bar(screen):
    global bits_progress_bar, golden_fruit_pos, temp_var_for_golden_progressbar, delete_pr_bar_time
    menu_width = screen.get_size()[0] # Ширина интерфейса меню
    menu_height = 100                 # Высота интерфейса меню
    width_center = menu_width / 2
    height_center = menu_height / 2 
    pg.draw.rect(screen, EMPTY_PROGRESS_BAR, [width_center - 0.2*screen.get_size()[0], height_center - 0.25*pixel_param, 0.4*screen.get_size()[0], 0.5*pixel_param] )
    if golden_fruit_pos == None:
        pg.draw.rect(screen, SILIVER, [width_center - 0.2*screen.get_size()[0], height_center - 0.25*pixel_param, bits_progress_bar, 0.5*pixel_param] )
    if golden_fruit_pos != None:
        temp_pr_bar_time = time.time()
    
        if temp_var_for_golden_progressbar: # if нужен чтобы единоразово записать данные в delete_time
            delete_pr_bar_time = (temp_pr_bar_time + 10)
            temp_var_for_golden_progressbar = False
        bits_progress_bar = (0.4*screen.get_size()[0]) * ((delete_pr_bar_time - temp_pr_bar_time)* 0.1)
        pg.draw.rect(screen, GOLD, [width_center - 0.2*screen.get_size()[0], height_center - 0.25*pixel_param, bits_progress_bar, 0.5*pixel_param] )
    return

while start:
    
    window_width = screen.get_size()[0] # штрина окна
    window_height = screen.get_size()[1] # высота окна
    window_center = window_width / 2
    
    for event in pg.event.get():
        if event.type == pg.QUIT : 
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            sys.exit()
        if event.type == pg.KEYDOWN:
            start = False
    text = ("Controller W A S D or arrows")
    text2 =('For shutdown the game press ESC')
    text3 =('For open setting`s menu press Y')
    text4 = ('Press any button for Start')
    
    start_font_size = 30
    font_start = pg.font.Font(None, start_font_size)
    
    font_start.size(text)[0]
    
    text_start = font_start.render( text, True, FONT_COLOR_MENU )
    text_start2 = font_start.render( text2, True, FONT_COLOR_MENU )
    text_start3 = font_start.render( text3, True, FONT_COLOR_MENU )
    text_start4 = font_start.render( text4, True, FONT_COLOR_MENU) 
    screen.blit(background(pg),(0, 0))
    screen.blit( text_start, ( int(window_center) - (font_start.size(text)[0] / 2), 150 ) )
    screen.blit( text_start2, ( int(window_center) - (font_start.size(text2)[0] / 2), 200 ))
    screen.blit( text_start3, ( int(window_center) - (font_start.size(text3)[0] / 2), 250 ))
    screen.blit( text_start4, ( int(window_center) - (font_start.size(text4)[0] / 2), 400 ))
        
    pg.display.flip()
    
while 1:
    
    clock.tick(10)
    screen.blit(background(pg),(0, 0))
    
    draw_menu(pg, screen)
    golden_fruit_progress_bar(screen)
    
    for event in pg.event.get():
        
        if event.type == pg.QUIT : 
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_y:
            setting = True
        if event.type == pg.KEYDOWN : 
            if movement_position != 'Left' :
                if event.key == pg.K_RIGHT:
                    movement_position = 'Right'
                    clock.tick(30)

            if movement_position != 'Up' :
                if event.key == pg.K_DOWN :
                    movement_position = 'Down'
                    clock.tick(30)

            if movement_position != 'Right' :
                if event.key == pg.K_LEFT:
                    movement_position = 'Left'
                    clock.tick(30)

            if movement_position != 'Down' :
                if event.key == pg.K_UP:
                    movement_position = 'Up'
                    clock.tick(30)

        if event.type == pg.TEXTINPUT :
            if movement_position != 'Left' :
                if event.text == 'd':
                    movement_position = 'Right'
                    clock.tick(30)

            if movement_position != 'Up' :
                if event.text == 's' :
                    movement_position = 'Down'
                    clock.tick(30)

            if movement_position != 'Right' :
                if event.text == 'a':
                    movement_position = 'Left'
                    clock.tick(30)

            if movement_position != 'Down' :
                if event.text == 'w':
                    movement_position = 'Up'
                    clock.tick(30)
    
    # -------------FRUCT
    eat_fruit()
    
    if fruit_pos == None :
        fruit_pos = draw_fruit(pg)
    else: 
        pg.draw.rect(screen, RED, (fruit_pos[0], fruit_pos[1], pixel_param, pixel_param))
    
    eat_golden_fruit()
    # if timer_for_golden_fruit == 10:
    if golden_fruit_pos == None:
        golden_fruit_pos = draw_golden_fruit(pg)
    else:
        
        pg.draw.rect(screen, GOLD, (golden_fruit_pos[0], golden_fruit_pos[1], pixel_param, pixel_param))
    move_golden_fruit(screen, random)
    
    # -------------FRUCT
    
    # -------------SETTING_MENU
    while setting:
        
        fullscreen = False
        
        window_width = screen.get_size()[0] # штрина окна
        window_height = screen.get_size()[1] # высота окна
        window_center = window_width / 2
        
        window = 800/600
        
        text = ('Window size :')
        window_RES1 = ('(800, 600)')
        window_RES2 = ('(1280, 800 )')
        window_RES3 = ('(Toggle Fullscreen)')# 1600/900
        setting_font_size = 30
        font_setting = pg.font.Font(None, setting_font_size)
        
        
        mouse_pos = pg.mouse.get_pos()
        hitbox_mouse = pg.draw.circle(screen, (255,255,255), mouse_pos, 5)
        hitbox_window_RES1 = pg.draw.rect(screen, (255,255,255), [int(window_center), int(window_height)*0.2 ,font_setting.size(window_RES1)[0], font_setting.size(window_RES1)[1]])
        hitbox_window_RES2 = pg.draw.rect(screen, (255,255,255), [int(window_center), int(window_height)*0.3 ,font_setting.size(window_RES2)[0], font_setting.size(window_RES2)[1]])
        hitbox_window_RES3 = pg.draw.rect(screen, (255,255,255), [int(window_center), int(window_height)*0.6 ,font_setting.size(window_RES3)[0], font_setting.size(window_RES3)[1]])
        
        screen.blit(setting_background(pg),(0, 0))
        
        text_setting = font_setting.render(text, True, FONT_COLOR_MENU)
        text_window_RES1 = font_setting.render(window_RES1, True, FONT_COLOR_MENU)
        text_window_RES2 = font_setting.render(window_RES2, True, FONT_COLOR_MENU)
        text_window_RES3 = font_setting.render(window_RES3, True, FONT_COLOR_MENU)
        
        screen.blit(text_setting,(int(window_center) - font_setting.size(text)[0] - 10, int(window_height)*0.2))
        screen.blit(text_window_RES1,(int(window_center), int(window_height)*0.2)) 
        screen.blit(text_window_RES2,(int(window_center), int(window_height)*0.3))
        screen.blit(text_window_RES3,(int(window_center), int(window_height)*0.6))
        
        for event in pg.event.get():
    
            if event.type == pg.QUIT : 
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_y:
                setting = False
            
            
            if hitbox_window_RES1.colliderect(hitbox_mouse) and pg.mouse.get_pressed()[0] == True:
                pg.display.set_mode((800,600))
                window = 800/600
                if fullscreen == True:
                    pg.display.toggle_fullscreen()
                    fullscreen = False

            if hitbox_window_RES2.colliderect(hitbox_mouse) and pg.mouse.get_pressed()[0] == True:
                pg.display.set_mode((1280,800))
                window = 1280/800
                if fullscreen == True:
                    pg.display.toggle_fullscreen()
                    fullscreen = False
                    
            if hitbox_window_RES3.colliderect(hitbox_mouse) and pg.mouse.get_pressed()[0] == True:
                pg.display.set_mode((1600,900))
                window = "Fullscreen"
                if fullscreen == False:
                    pg.display.toggle_fullscreen()
                    fullscreen = True

        pg.display.flip()
        
    # -------------SETTING_MENU

    # -------------SNAKE
    move_snake(pg, screen)
    
    draw_snake(pg)

    # -------------SNAKE
    
    game_over()

    pg.display.flip()
