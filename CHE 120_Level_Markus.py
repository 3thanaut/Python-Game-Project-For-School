#Created by Ethan Nauta
#Level created by Markus Pollak

#--Resources Used--#:
#https://youtu.be/QFvqStqPCRU?si=gmiGOuEnrZTYafuq -- video watched until 26:02 for help setting up methods for the game.
#https://www.geeksforgeeks.org/allowing-resizing-window-in-pygame/ -- where I found the method that allows window resizing.
#https://www.geeksforgeeks.org/how-to-get-the-size-of-pygame-window/ -- where I found the method that returns window size.

#Bring in pygame module
import pygame, sys

pygame.init()

#define screen size and amount of tiles on screen.
screen_x = 800
screen_y = 400
screen_x2 = screen_x
screen_y2 = screen_y
screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
pygame.display.set_caption('Resizable')


#create a matrix to position the map tiles!
#MP: As the group member in charge of designing the more difficult of the two mazes, I investigated what size matrix would be needed
#MP: as the base of an appropriately sized level, capable of a suitably complex design without devolving into unnecessary convolusion.
#MP: I determined that a 25 by 25 grid was an appropriate scale to encompass the maze. In order to include an outer wall, this was expanded to 27 by 27.

#MP: In addition to designing the matrix, the matrix_columns and matrix_rows variables were adjusted to allow the game's code to function on a level of the chosen size.
matrix_columns = int(27)
matrix_rows = int(27)
matrix_column_count = 0
matrix_row_count = 0

#MP: The matrix which serves to define most of the maze's physical structure utilizes the following elements:
#MP: matrix[][] == 0 indicates a tile (square) of the maze which is permanently impassable, acting as the maze's walls. 
#MP: This is accomplished using the key specifications within the blockCollision() function, as defined below
#MP: matrix[][] == 1 indicates a tile which is permanently passable, acting as the maze's corridors
#MP: matrix[][] > 1  indicates a door, which is a tile which is conditionally passable, based on whether the player has last picked up the related key.
#MP: The door and key are defined by the makeDoor() and makeKey() functions respectively, each defined and implemented below 
#MP: matrix[][] == -1 indicates the goal of the maze. This tile is initially described in the blockCollision() functionas defined below. 
matrix = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,-1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
          [0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
          [0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
          [0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0],
          [0,1,1,1,1,0,1,0,0,1,0,1,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0],
          [0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,1,1,1,1,0],
          [0,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,0,1,0,0,1,0,0,0,0,0],
          [0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0],
          [0,0,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,1,1,0,1,1,1,1,1,0,1,0,0,1,0,0,1,1,1,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0],
          [0,0,1,1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0],
          [0,0,1,0,0,0,0,0,0,1,1,1,0,1,0,1,1,0,1,1,0,1,0,0,0,0,0],
          [0,0,2,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,1,1,1,1,0],
          [0,0,1,1,1,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0],
          [0,0,0,0,0,1,0,0,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,0,0,1,0],
          [0,1,1,0,0,1,1,1,1,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0],
          [0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1,1,1,1,0],
          [0,0,1,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,0],
          [0,0,1,1,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0],
          [0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0],
          [0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]


#initialize player object, the object should be divisible to an even number to allow the smooth collision. 
#(ie 50/2 = 25 which is not even so ideally don't use that)
plyr_size = 60
test_surface = pygame.Surface((plyr_size, plyr_size))
test_surface.fill(pygame.Color("gold"))

plyr_key = "gold"

#size of every tile in the game, their spacing and collision will scale with this. Change it to whatever!
#(just make sure the player doesn't spawn in a block)
tile_size = 100

#these are some methods I was told to use from a video which seem to work. They are elements of pygame.
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

#x and y position of the top left corner of the screen on the map.
x_pos = -350
y_pos = -150

#the actual x and y positions of the centre of the player character.
r_xpos = 50
r_ypos = 50

#state of players available keyboard inputs.
w_state = 0
a_state = 0
s_state = 0
d_state = 0

#players speed in the game. Each key corresponds to a direction!
w_speed = 10
a_speed = 10
s_speed = 10
d_speed = 10

#a dictionary that stores the numbers of a door to the color of the door
#used later for comparing the players color to the door color to check if they may pass!
door_dict = {}

#places the player in the give row column of the matrix!
def posPlayer(row, column):

    global x_pos
    global y_pos
    global r_xpos
    global r_ypos

    x_pos += tile_size*column
    y_pos += tile_size*row

    r_xpos += tile_size*column
    r_ypos += tile_size*row



#MP: Using the posPlayer() function, the starting position of the player was defined to fit the maze's layout, and vital variables tied to this value were created and globalized. 
posPlayer(3,9)


#make a door of whatever color the user chooses, then make a number for that doors associated key
#color must be a string defined in pygames base colors
#number must be an integer greater than 1
def makeDoor(color, number, current_columns, current_rows):

    #make sure to only draw door when needed
    if matrix[current_rows][current_columns] == number:

        door = pygame.Surface((tile_size,tile_size))
        door.fill(pygame.Color(color))

        screen.blit(door, (columns*tile_size - x_pos, rows*tile_size - y_pos))

        door_dict[number] = color

#create a key object that is associated with the door it opens by number and color
#position is two numbers, a row and a column for the key to be placed in the matrix
def makeKey(color, column, row, current_column, current_row):

    #just to make the game not draw the key every single time it draws any other object in the game
    if current_column == column and current_row == row:

        key = pygame.Surface((plyr_size/2, plyr_size/2))
        key.fill(pygame.Color(color))

        screen.blit(key, (column*tile_size - x_pos + 0.5*tile_size - 0.5*plyr_size/2, row*tile_size + 0.5*tile_size - 0.5*plyr_size/2 - y_pos))

        #also check if player is touching the key, players position is relative to their middle, dont forget
        #the reason why check y and checkx have new constraints is because the difference between the size of the key and the size
        #of the tile needs to be incorportated for proper collision
        check_y = (rows*tile_size - r_ypos <= 0.5*plyr_size - (0.5*tile_size - 0.25*plyr_size) + 1 and rows*tile_size - r_ypos >= -tile_size - 0.5*plyr_size + (0.5*tile_size - 0.25*plyr_size) - 1)
        check_x = (columns*tile_size - r_xpos <= 0.5*plyr_size - (0.5*tile_size - 0.25*plyr_size) + 1 and columns*tile_size - r_xpos >= -tile_size - 0.5*plyr_size + (0.5*tile_size - 0.25*plyr_size) - 1)

        if check_x and check_y:

            #need to globally edit the players color definition
            global plyr_key

            if plyr_key != color:

                test_surface.fill(color)
                plyr_key = color


def blockCollision():

    #if player is in y range of square, can trigger x collisions, and vice versa
    check_y = (rows*tile_size - r_ypos <= 0.5*plyr_size + 1 and rows*tile_size - r_ypos >= -tile_size - 0.5*plyr_size - 1)
    check_x = (columns*tile_size - r_xpos <= 0.5*plyr_size + 1 and columns*tile_size - r_xpos >= -tile_size - 0.5*plyr_size - 1)


    #if the player is inside of a square, push them out in the direction they are closest to
    if check_x and check_y:
        
        print (matrix[rows][columns]) #added this
        #checks if the player is in the win square
        if matrix[rows][columns] == -1:

            print('win')

        print('you are touching square ', rows, ' ', columns)

        #Using globals here to make sure the values are edited globally
        if rows*tile_size - r_ypos > 0.5*plyr_size - 1:

            if matrix[rows-1][columns] != 0:
                print('hitting top')
                global s_speed 
                s_speed = 0

        elif rows*tile_size - r_ypos < -tile_size - 0.5*plyr_size + 1:

            if matrix[rows+1][columns] != 0:
                print('hitting bottom')
                global w_speed
                w_speed = 0

        if columns*tile_size - r_xpos > 0.5*plyr_size - 1:

            if matrix[rows][columns-1] != 0:
                print('hitting left')
                global d_speed
                d_speed = 0

        elif columns*tile_size - r_xpos < -tile_size - 0.5*plyr_size + 1:

            if matrix[rows][columns+1] != 0:
                print('hitting right')
                global a_speed
                a_speed = 0

        return w_speed, a_speed, s_speed, d_speed


#core loop of the game, runs at 30FPS, and handles all collision
while True:

    screen_x1, screen_y1 = screen.get_size()


    if screen_x1 != screen_x2:

        x_pos -= 0.5*(screen_x1 - screen_x2)
        screen_x2 = screen_x1
        screen_x = screen_x2

    if screen_y1 != screen_y2:

        y_pos -= 0.5*(screen_y1 - screen_y2)
        screen_y2 = screen_y1
        screen_y = screen_y2

    #at the start of every step of the game, check for all input events.
    for event in pygame.event.get():

        #assures game will be completely closed. Also got this from the video linked at the top.
        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:

                w_state = -1
            if event.key == pygame.K_a:

                a_state = -1
            if event.key == pygame.K_s:

                s_state = 1
            if event.key == pygame.K_d:

                d_state = 1

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:

                w_state = 0
            if event.key == pygame.K_a:

                a_state = 0
            if event.key == pygame.K_s:

                s_state = 0
            if event.key == pygame.K_d:

                d_state = 0



    #either pass a pygame base color or a RGB tuple, 
    #there is a list of available base colors in the documentation!
    screen.fill(pygame.Color("blue"))


    #for each row, adjust the position of each tile in each column to the appropriate spacing.
    for rows in range(matrix_rows):

        for columns in range(matrix_columns):


            #in the map matrix, a zero is defined as a wall, or unwalkable surface!
            if matrix[rows][columns] == 0:

                blockCollision()

#----------------------------------------------------------------------------------------------------#
            #makeDoor(color, number_in_matrix, current_column, current_row)

            
            #MP: In the two function calls below, the two doors of the level are defined.  
            #MP: Each of these doors is, in addition to the columns and rows variables which contain the players current position,
            #MP: given two arguments. These are an integer which is used to represent it in the matrix, and a string containing one of pygame's basic colours.
            #MP: These parameters are used by the makeDoor() function to create and incorporate an appropriately coloured tile into the game's world.
            #MP: Respectively, they define the position and the colour of the tile.
            #MP: The color parameter is additionally put to use by assigning it to the door_dict[] dictionary with the key being the integer representing the door in the matrix.
            #MP: This dictionary will play a vital role in allowing the door's key to work, as later outline using a makeKey() function call. 
            makeDoor('orange', 2, columns, rows)
            makeDoor('purple', 3, columns, rows)


#----------------------------------------------------------------------------------------------------#


            #if a player is going to run into a door
            if matrix[rows][columns] > 1:

                if plyr_key != door_dict[matrix[rows][columns]]:

                    blockCollision()


            #-1 is the entry which the player has to get to to win.
            if matrix[rows][columns] == -1:

                blockCollision()

                win = pygame.Surface((tile_size,tile_size))
                win.fill(pygame.Color("black"))

                screen.blit(win, (columns*tile_size - x_pos, rows*tile_size - y_pos))


            #0 is defined as a wall, walls are drawn as white
            if matrix[rows][columns] == 0:

                water = pygame.Surface((tile_size,tile_size))
                water.fill(pygame.Color("white"))

                screen.blit(water, (columns*tile_size - x_pos, rows*tile_size - y_pos))

            #1 is defined as grass, or a walkable surface!
            if matrix[rows][columns] == 1:

                grass = pygame.Surface((tile_size,tile_size))
                grass.fill(pygame.Color("green"))

                screen.blit(grass, (columns*tile_size - x_pos, rows*tile_size - y_pos))

#----------------------------------------------------------------------------------------------------#
            #makeKey(color, column_key, row_key, current_column, current_row)
            
            #MP: The makeKey() function defines the keys which allow the player to pass through the doors without being stopped by the blockCollision() function.
            #MP: Unlike the Level's doors, the keys defined by the MakeKey() function do not have a value accociated with them 
            #MP: that can be placed in the matrix. Rather their function parameters include matrix coordinates which define where in the matrix the key should be superimposed.
            #MP: The columns and rows arguments once again serve to convey the players current position
            #MP: The colour parameter allows the key to be accociated to a door as defined by a makeDoor() function call.
            #MP: As outlined just below the makeDoor function calls, the player moving into a door (a matrix element with a value > 1) usually results in a blockCollision() function call setting the player's speed to 0 and thereby stopping them.
            #MP: However, should the player have most recently come into contact with the appropriate key, and thereby have the plyr_key variable set to the door's accociated color as stored in the door_dict dictionary,
            #MP: a conditional prevents the blockCollision() function call and thereby lets the player pass through.

            #MP: This function call creates and places an orange key for the door which was assigned the 'orange' color argument.
            makeKey("orange", 1, 2, columns, rows)

            #MP: This function call creates and places a purple key for the door which was assigned the 'purple' color argument.
            makeKey("purple", 12, 9, columns, rows)


#----------------------------------------------------------------------------------------------------#


            columns += 1

        rows += 1




    #if a and d active, dont move, else move
    x_pos += a_state*a_speed + d_state*d_speed
    y_pos += w_state*w_speed + s_state*s_speed

    r_xpos += a_state*a_speed + d_state*d_speed
    r_ypos += w_state*w_speed + s_state*s_speed

    w_speed = 5
    a_speed = 5
    s_speed = 5
    d_speed = 5


    #Positions the test surface on the screen relative to top left of object
    screen.blit(test_surface,(0.5*screen_x - 0.5*plyr_size, 0.5*screen_y - 0.5*plyr_size))

    #draw all elems each step
    pygame.display.update()

    #sets the fps of the game, game may still run too slow. This runs 30 fps.
    clock.tick(60)
