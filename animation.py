import colorsys
import turtle

# Setup Screen
screen = turtle.Screen()
screen.bgcolor("black")

t = turtle.Turtle()
t.speed(0)
turtle.tracer(2)  # Drawing fast karne ke liye

h = 0  # Color (Hue) starting point

for i in range(180):
    # HSV color ko RGB (Red, Green, Blue) me convert karna
    c = colorsys.hsv_to_rgb(h, 0.60, 0.90)
    t.pencolor(c)  # Pen ka color set karo
    h += 0.02  # Har step me color thoda badlao

    # Math-based pattern drawing
    t.circle(i, 90)  # Circle arc draw karna
    t.left(90)
    t.circle(i, 90)
    t.left(70)

turtle.done()

