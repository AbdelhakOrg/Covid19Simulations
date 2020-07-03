import turtle
import random
import math 

import matplotlib.pyplot as plt

n_users=10
threshold_distance=20
threshold_contact=3
step_min = 10
step_max = 20

def dist(x,y):  
     d = math.sqrt((x[0] - x[1])**2 + (y[0] - y[1])**2)  
     return d

# change the color of the background
screen = turtle.Screen()
screen.bgcolor("white")
# size of our box
box_size = 500

# create a new user with a certain color
def create_user(color, nb_contacts):
     user_id = turtle.Turtle()
     user_id.penup()
     user_id.speed(0)
     user_id.width(1)
     user_id.shape("circle")
     user_id.color(color)
     user_id.shapesize(.3,.3)
     x, y = random.randint(-box_size/2, box_size/2), random.randint(-box_size/2, box_size/2)
     user_id.setpos(x,y)
     user = {"id": user_id, "category":color, "nb_contacts":nb_contacts}
     return user

# stamp and move the user
def move_user(user):
    #t.stamp()
    user_id = user["id"]
    user_id.penup()
    angle = random.randint(-90, 90)
    user_id.right(angle)
    step = random.randint(step_min, step_max)
    user_id.forward(step)
        
# is the user outside the box?
def is_outside_box(user, size):
     outside_box = False
     user_id = user["id"]
     x = user_id.xcor()
     y = user_id.ycor()
     if x < (size / -2)  or x > (size / 2):
          outside_box = True
     if y < (size / -2) or y > (size / 2):
          outside_box = True
     return outside_box

# create our list of users
users = []
for i in range (n_users):
     users.append(create_user("black", 0));
print(users)

# use the first user to draw our boundary box
user1 = users[0].get("id")
user1.penup()
user1.goto(box_size / 2, box_size / 2)
#user1.pendown()

for side in range(4):
     user1.pendown()
     user1.right(90)
     user1.forward(box_size)

user1.penup()
user1.goto(0, 0)
user1.pendown()
user1.pencolor("green")
user1.goto(0,box_size/2)
user1.goto(0,-box_size/2)
user1.goto(0, 0)
user1.goto(box_size/2, 0)
user1.goto(-box_size/2, 0)
user1.penup()
user1.goto(0, 0)

#==================
# Begin simulation
#==================

#count_contacts=[0]*n_users
covid=[users[0]]
covid[0]["id"].color("red")
covid[0]["category"] = "red"

ncovid = users[1:]

while len(ncovid) != 0:       
    #randomly stop moving or not
    for user in (covid + ncovid):
        if random.choice([0,1])==1:
            move_user(user)

    for i, c in enumerate(covid):
        for j, nc in enumerate(ncovid):
            #print(dist(y.pos(),x.pos()))
            if dist(c["id"].pos(),nc["id"].pos()) < threshold_distance:
                #increment contacts
                covid[i]["nb_contacts"] = covid[i].get("nb_contacts") + 1
                ncovid[j]["nb_contacts"] = ncovid[j].get("nb_contacts") + 1
                
                #increment size
                s = covid[i]["id"].shapesize()
                covid[i]["id"].shapesize(s[0]+.1, s[1]+.1)

                if ncovid[j]["nb_contacts"] == (threshold_contact-2):
                    ncovid[j]["category"] = "cyan"
                    ncovid[j]["id"].color("cyan")
                if ncovid[j]["nb_contacts"] == (threshold_contact-1):
                    ncovid[j]["category"] = "green"
                    ncovid[j]["id"].color("green")
                if ncovid[j]["nb_contacts"] == threshold_contact:
                    ncovid[j]["category"] = "red"
                    ncovid[j]["id"].color("red")

                    #append in covid
                    covid.append(nc)
                    #remove from non covid
                    ncovid.remove(nc)

    for u in users:
        if is_outside_box(u, box_size) == True:
            # turn the user around and move it back
            u["id"].goto(0,0)

for c in covid:
    print (c["nb_contacts"])
