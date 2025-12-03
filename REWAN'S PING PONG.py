import turtle
import tkinter as tk

# setup window =================
# Detect screen size and set responsive dimensions
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# Set window size to 85% of screen (responsive)
WINDOW_WIDTH = max(400, min(1400, int(screen_width * 0.85)))
WINDOW_HEIGHT = max(300, min(900, int(screen_height * 0.85)))

window = turtle.Screen()
window.title("REWAN`S PING PONG GAME")
window.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
window.tracer(0)  # set delay for update drawings
window.bgcolor(0, 0, 1)

# responsive dimensions (calculated from window size)
HALF_WIDTH = WINDOW_WIDTH // 2
HALF_HEIGHT = WINDOW_HEIGHT // 2
PLAYER_X_OFFSET = HALF_WIDTH - 50
BORDER_TOP = HALF_HEIGHT - 50
BORDER_BOTTOM = -(HALF_HEIGHT - 50)
PLAYER_COLLISION_X_LEFT = -HALF_WIDTH + 50
PLAYER_COLLISION_X_RIGHT = HALF_WIDTH - 50
SCORE_BOUNDARY = HALF_WIDTH + 50

# Responsive scaling factor (for text and object sizes)
SCALE_FACTOR = WINDOW_WIDTH / 800  # normalized to 800px base width

# setup game projects ===========
# ball
ball = turtle.Turtle()
ball.speed(0)  # drawing speed(fastest)
ball.shape("circle")
ball.color("orange")
# scale factor = default size (20px = 20px)
ball.shapesize(stretch_len=1, stretch_wid=1)
ball.goto(x=0, y=0)  # start position
ball.penup()  # stop drawing lines when moving
ball_speed_x = 0.5  # ball movement speed in x direction
ball_speed_y = 0.5  # ball movement speed in y direction

# ball shadow
ball_shadow = turtle.Turtle()
ball_shadow.speed(0)
ball_shadow.shape("circle")
ball_shadow.color("white")
ball_shadow.shapesize(stretch_len=1, stretch_wid=1)
ball_shadow.goto(x=0, y=0)
ball_shadow.penup()
ball_shadow.hideturtle()

# center line
center_line = turtle.Turtle()
center_line.speed(0)
center_line.shape("square")
center_line.color("pink")
# width => 500px = 25 * 20 px default
center_line.shapesize(stretch_len=0.1, stretch_wid=25)
center_line.penup()
center_line.goto(0, 0)

# player 1
player1 = turtle.Turtle()
player1.speed(0)
player1.shape("square")
player1.shapesize(stretch_len=0.1, stretch_wid=5)
player1.color("black")
player1.penup()
player1.goto(x=-PLAYER_X_OFFSET, y=0)

# player 2
player2 = turtle.Turtle()
player2.speed(0)
player2.shape("square")
player2.shapesize(stretch_len=0.1, stretch_wid=5)
player2.color("red")
player2.penup()
player2.goto(x=PLAYER_X_OFFSET, y=0)

# score text
score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.goto(x=0, y=int(HALF_HEIGHT - 40))
font_size_large = max(12, int(14 * SCALE_FACTOR))
score.write("player1 : 0 player 2 : 0", align="center",
            font=("courier", font_size_large, "normal"))

score.hideturtle()   # we hide the object because we only want to see the text
p1_score, p2_score = 0, 0     # variables

# result box (winner announcement)
result_box = turtle.Turtle()
result_box.speed(0)
result_box.color("white")
result_box.penup()
result_box.hideturtle()

# pause game state
is_paused = False
result_display_time = 0  # counter for how long to show result

# game timer
game_time = 43200  # 12 hours = 43200 seconds (at ~60 FPS)
time_text = turtle.Turtle()
time_text.speed(0)
time_text.color("yellow")
time_text.penup()
time_text.goto(x=0, y=-(HALF_HEIGHT - 40))
font_size_small = max(10, int(12 * SCALE_FACTOR))
time_text.write("Time: 720:00", align="center", font=("courier", font_size_small, "normal"))
time_text.hideturtle()

# game over state
game_over = False

def toggle_pause():
    global is_paused
    is_paused = not is_paused

def restart_game():
    global game_time, p1_score, p2_score, result_display_time, game_over
    game_time = 43200  # reset to 12 hours
    p1_score = 0
    p2_score = 0
    result_display_time = 0
    game_over = False
    ball.goto(0, 0)
    ball_speed_x = 0.5
    ball_speed_y = 0.5
    result_box.clear()
    score.clear()
    score.write(f"player1 : 0 player 2 : 0", align="center",
                font=("courier", font_size_large, "normal"))
    time_text.clear()
    time_text.write("Time: 720:00", align="center", font=("courier", font_size_small, "normal"))

# player movement ===========
def p1_move_up():
    if player1.ycor() < BORDER_TOP:
        player1.sety(player1.ycor() + 20)

def p1_move_down():
    if player1.ycor() > BORDER_BOTTOM:
        player1.sety(player1.ycor() - 20)

def p2_move_up():
    if player2.ycor() < BORDER_TOP:
        player2.sety(player2.ycor() + 20)

def p2_move_down():
    if player2.ycor() > BORDER_BOTTOM:
        player2.sety(player2.ycor() - 20)

# get users inputs (key bindings)
window.listen()   # tell the window to expect user inputs
window.onkeypress(p1_move_up, "w")  # ensure the keyboard in "en" and "small"
window.onkeypress(p1_move_down, "s")
window.onkeypress(p2_move_up, "Up")
window.onkeypress(p2_move_down, "Down")
window.onkeypress(toggle_pause, "space")  # pause/resume with space key during gameplay

# game loop ================
while True:
    window.update()

    # if game is over, allow restart with space key
    if game_over:
        window.onkeypress(restart_game, "space")
        continue
    
    # during gameplay, space pauses/resumes
    window.onkeypress(toggle_pause, "space")

    # skip game update if paused
    if is_paused:
        continue

    # handle result display: show popup but DO NOT pause the level timer
    if result_display_time > 0:
        result_display_time -= 1
        if result_display_time == 0:
            result_box.clear()

    # decrease game timer
    if game_time > 0:
        game_time -= 1
        minutes = game_time // 60
        seconds = game_time % 60
        time_text.clear()
        time_text.write(f"Time: {minutes}:{seconds:02d}", align="center", font=("courier", font_size_small, "normal"))
    else:
        # Game time ended - show game over message
        time_text.clear()
        result_box.clear()
        result_box.goto(0, 0)
        if p1_score > p2_score:
            result_box.write(f"GAME OVER!\nPlayer 1 Wins!\nFinal Score: {p1_score} - {p2_score}\nPress SPACE to Restart", 
                           align="center", font=("courier", max(14, int(16 * SCALE_FACTOR)), "bold"))
        elif p2_score > p1_score:
            result_box.write(f"GAME OVER!\nPlayer 2 Wins!\nFinal Score: {p1_score} - {p2_score}\nPress SPACE to Restart", 
                           align="center", font=("courier", max(14, int(16 * SCALE_FACTOR)), "bold"))
        else:
            result_box.write(f"GAME OVER!\nIt's a Tie!\nFinal Score: {p1_score} - {p2_score}\nPress SPACE to Restart", 
                           align="center", font=("courier", max(14, int(16 * SCALE_FACTOR)), "bold"))
        # Mark game as over and stop gameplay
        game_over = True
        window.update()
        continue

    # ball movement ========
    ball.setx(ball.xcor() + ball_speed_x)
    ball.sety(ball.ycor() + ball_speed_y)
    
    # shadow follows ball with offset
    ball_shadow.setx(ball.xcor() + 2)
    ball_shadow.sety(ball.ycor() - 2)

    # ball & borders collision
    if ball.ycor() > BORDER_TOP:    # top border
        ball.sety(BORDER_TOP)
        ball_speed_y *= -1  # invert y direction

    if ball.ycor() < BORDER_BOTTOM:    # bottom border
        ball.sety(BORDER_BOTTOM)
        ball_speed_y *= -1  # invert y direction

    # ball & players collision ==============

    # collision with player 1
    if (ball.xcor() < PLAYER_COLLISION_X_LEFT and ball.xcor() > PLAYER_COLLISION_X_LEFT - 40 and 
        ball.ycor() > (player1.ycor() - 50) and 
        ball.ycor() < (player1.ycor() + 50)):
        ball.setx(PLAYER_COLLISION_X_LEFT)
        ball_speed_x *= -1

    # collision with player 2
    if (ball.xcor() > PLAYER_COLLISION_X_RIGHT and ball.xcor() < PLAYER_COLLISION_X_RIGHT + 40 and 
        ball.ycor() > (player2.ycor() - 50) and 
        ball.ycor() < (player2.ycor() + 50)):
        ball.setx(PLAYER_COLLISION_X_RIGHT)
        ball_speed_x *= -1

    # score handling
    if ball.xcor() > SCORE_BOUNDARY:
        ball.goto(0, 0)
        ball_speed_x = -0.5
        ball_speed_y = 0.5
        score.clear()
        p1_score += 1
        score.write(f"player1 : {p1_score} player 2 : {p2_score}", align="center",
                    font=("courier", font_size_large, "normal"))

        # show result box
        result_box.clear()
        result_box.goto(0, 0)
        result_box.write(f"Player 1 Scored!\nScore: {p1_score} - {p2_score}", 
                        align="center", font=("courier", max(14, int(16 * SCALE_FACTOR)), "bold"))
        result_display_time = 180  # show result for ~3 seconds (180 frames)

    if ball.xcor() < -SCORE_BOUNDARY:
        ball.goto(0, 0)
        ball_speed_x = 0.5
        ball_speed_y = 0.5
        score.clear()
        p2_score += 1
        score.write(f"player1 : {p1_score} player 2 : {p2_score}", align="center",
                    font=("courier", font_size_large, "normal"))

        # show result box
        result_box.clear()
        result_box.goto(0, 0)
        result_box.write(f"Player 2 Scored!\nScore: {p1_score} - {p2_score}", 
                        align="center", font=("courier", max(14, int(16 * SCALE_FACTOR)), "bold"))
        result_display_time = 180  # show result for ~3 seconds (180 frames)
