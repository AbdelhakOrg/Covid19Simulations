import pygame
import random
import math


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)

(width, height) = (400, 400)
box_size = 400

running = True

screen = pygame.display.set_mode((width, height))

N_INIT_COVID = 5
N_INIT_NON_COVID = 10
SPEED = 0000
threshold_distance = 20
threshold_contact = 9
step = 30

image_size = (20, 28)
black_image = pygame.image.load('black.png')
BLACK = pygame.transform.scale(black_image, image_size)
red_image = pygame.image.load('red.png')
RED = pygame.transform.scale(red_image, image_size)
green_image = pygame.image.load('green.png')
GREEN = pygame.transform.scale(green_image, image_size)
blue_image = pygame.image.load('blue.png')
BLUE = pygame.transform.scale(blue_image, image_size)

covid_list = []
ncovid_list = []


def main():
    global running

    pygame.init()

    pygame.display.set_caption("TRACING")
    screen.fill(WHITE)
    background_image = pygame.image.load("map.png").convert()
    screen.blit(background_image, [0, 0])
    pygame.display.update()

    # create our list of covid and non-covid users
    for id in range(0, N_INIT_NON_COVID + N_INIT_COVID):
        if id < N_INIT_NON_COVID:
            ncovid_list.append(User(id, [], False, GREEN, 0, [], True))
        else:
            covid_list.append(User(id, [], True, RED, 0, [], True))

    while running:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, [0, 0])

        # randomly stop moving or not

        for u in (covid_list + ncovid_list):
            # display
            u.draw()
            pygame.display.update()
            # move
            theta = 90 * random.choice([0, 1, 2, 3, 4])
            scale = random.choice([-step,  0, step])
            u.move_polar(theta, scale)

        pygame.time.delay(SPEED)

        print(covid_list[0].contacts_history)

        for i, c in enumerate(covid_list):
            for j, nc in enumerate(ncovid_list):
                # print(dist(y.pos(),x.pos()))
                if c.dist(nc) < threshold_distance:

                    # increment contacts when a covid encounter a noncovid
                    c.nb_contacts = c.nb_contacts + 1
                    nc.nb_contacts = nc.nb_contacts + 1

                    nc.contacts_history.append(c.user_id)
                    c.contacts_history.append(nc.user_id)

                    if nc.nb_contacts == (threshold_contact * 1/3):
                        nc.category = BLUE
                    if nc.nb_contacts == (threshold_contact * 2/3):
                        nc.category = BLACK
                    if nc.nb_contacts == threshold_contact:
                        nc.category = RED
                        nc.covid = True
                        # append in covid
                        covid_list.append(nc)
                        # remove from non covid
                        ncovid_list.remove(nc)
                        # del ncovid_list[j]


class User():

    def __init__(self, user_id, gps_positions, covid, category, nb_contacts, contacts_history, random_user):
        if random_user:
            pos = (random.randint(0, box_size), random.randint(0, box_size))
        else:
            pos = (0, 0)
        self.user_id = user_id
        self.gps_positions = [pos]
        self.contacts_history = []
        self.covid = covid
        self.category = category
        self.nb_contacts = nb_contacts

    def draw(self):
        size = min(5, self.nb_contacts + 1)
        pos = self.gps_positions[-1]
        # pygame.draw.circle(screen, self.category, pos, size)
        screen.blit(self.category,
                    (pos[0]-image_size[0]/2, pos[1]-image_size[1]/2))
        # print(self.covid, self.user_id)
        if self.covid == True:
            # print("test")
            pygame.draw.circle(screen, pygame.Color('#FF0000'),
                               pos, threshold_distance, 1)

    def move_polar(self, theta, scale):
        last_pos = self.gps_positions[-1]
        pos = (int(round(last_pos[0] + scale * math.cos(theta))),
               int(round(last_pos[1] + scale * math.sin(theta))))

        # return to center of the sceen if the user goes out
        if last_pos[0] > width or last_pos[0] < 0 or last_pos[1] > height or last_pos[1] < 0:
            pos = (int(width/2), int(height/2))

        self.gps_positions.append(pos)

    def move(self, x, y):
        last_pos = self.gps_positions[-1]
        pos = (last_pos[0] + x, last_pos[1] + y)

        # return to center of the sceen if the user go out
        if last_pos[0] > width or last_pos[0] < 0 or last_pos[1] > height or last_pos[1] < 0:
            pos = (int(width/2), int(height/2))

        self.gps_positions.append(pos)

    def dist(self, u):
        last_pos = self.gps_positions[-1]
        u_pos = u.gps_positions[-1]
        return math.sqrt((last_pos[0] - u_pos[0])**2 + (last_pos[1] - u_pos[1])**2)


if __name__ == '__main__':
    main()
