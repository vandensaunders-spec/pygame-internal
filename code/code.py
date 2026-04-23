import turtle
import time
import random

delay = 0.1

# Game state
game_over = False
frame_count = 0

# Score
score = 0
high_score = 0

# Load high score
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game by Van")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0) # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "right"
head.prev_x = 0
head.prev_y = 0

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

segments = []

# Segment creation frame tracking
segment_creation_frame = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def restart_game():
    global score, delay, game_over
    game_over = False
    score = 0
    delay = 0.1
    head.goto(0, 0)
    head.prev_x = 0
    head.prev_y = 0
    head.direction = "right"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    segment_creation_frame.clear()
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

def show_game_over():
    pen.color("white")
    pen.goto(0, 0)
    pen.write("GAME OVER", align="center", font=("Courier", 40, "bold"))
    pen.goto(0, -40)
    pen.write("Press SPACE to restart", align="center", font=("Courier", 16, "normal"))
    pen.goto(0, 260)

def move():
    head.prev_x = head.xcor()
    head.prev_y = head.ycor()
    
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(restart_game, "space")

# Main game loop
while True:
    wn.update()
    frame_count += 1

    if game_over:
        show_game_over()
        time.sleep(0.1)
        continue

    # Move the snake
    move()

    # Check for collision with food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        new_segment.goto(head.xcor(), head.ycor())
        segments.append(new_segment)
        segment_creation_frame.append(frame_count)

        # Increase the score
        score += 10

        # Increase speed
        delay -= 0.005
        delay = max(0.05, delay)

        if score > high_score:
            high_score = score
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head was
    if len(segments) > 0:
        segments[0].goto(head.prev_x, head.prev_y)

    # Check for head collision with the body segments
    for index, segment in enumerate(segments):
        if segment.distance(head) < 20:
            # Skip collision if segment was just created this frame
            if segment_creation_frame[index] != frame_count:
                game_over = True

    # Check for head collision with the boundaries
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        game_over = True

    time.sleep(delay)
