import math
import pygame
import tkinter
from matplotlib.colors import is_color_like

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("waves Simulation")

NUM_OF_DOTS = 60
DOT_RADIUS = 5


def show_instructions():
    root = tkinter.Tk()
    root.title("instructions")
    root.geometry('600x220')
    root['bg'] = 'white'
    help_lbl = tkinter.Label(root, text="press i for instructions.\n" +
                                        "press a to add a wave.\n" +
                                        "press r to remove all waves \n" +
                                        "press s to show or hide super position of all waves\n" +
                                        "press d to hide the non super position waves\n" +
                                        "press f to freeze the simulation\n" +
                                        "press l to show or hide vertical lines\n" +
                                        "press o to change global options - speed and scale",
                             font=('Narkisim', 20), bg='white')
    help_lbl.pack()
    root.mainloop()


def apply_simulation_options(root, scale, speed):
    global SCALE, SPEED
    try:
        SCALE = 100 / float(scale)
        SPEED = float(speed)
    except:
        SCALE = 100 / 0.5
        SPEED = 2
    root.destroy()


def set_simulation_options():
    root = tkinter.Tk()
    root.title("set global settings")
    root.geometry('400x300')
    root['bg'] = 'white'
    scale_frame = tkinter.Frame(root, bg='white')

    scale_lbl = tkinter.Label(scale_frame, text='100px are _ meters:', font=('Narkisim', 16), bg='white')
    scale_lbl.grid(column=0, row=0, padx=5)

    scale_entry = tkinter.Entry(scale_frame, bd=2, width=30)
    scale_entry.insert(tkinter.END, f"{100 / SCALE}")
    scale_entry.grid(column=1, row=0, padx=5)

    scale_frame.pack(pady=45)

    speed_frame = tkinter.Frame(root, bg='white')

    speed_lbl = tkinter.Label(speed_frame, text='enter the speed (m/s):', font=('Narkisim', 16), bg='white')
    speed_lbl.grid(column=0, row=0, padx=5)

    speed_entry = tkinter.Entry(speed_frame, bd=2, width=30)
    speed_entry.insert(tkinter.END, f"{SPEED}")
    speed_entry.grid(column=1, row=0, padx=5)

    speed_frame.pack(pady=45)

    start_btn = tkinter.Button(root, text='set options', bd=0, font=('Narkisim', 20, 'bold'),
                               command=lambda: apply_simulation_options(root, scale_entry.get(), speed_entry.get()))
    start_btn.pack()

    root.mainloop()


WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
SUPER_POS_COLOR = (244, 252, 3)

NUMBERS_FONT = pygame.font.SysFont("comicsans", 20)
AXIS_FONT = pygame.font.SysFont("comicsans", 30)

SCALE = 100 / 0.5
SPEED = 2


class Wave:
    def __init__(self, dots=None):
        if dots is None:
            self.update_wave_settings()
            self.dots = [[(WIDTH / SCALE / NUM_OF_DOTS) * i, 0] for i in range(NUM_OF_DOTS + 1)]
        else:
            self.dots = dots
            self.color = SUPER_POS_COLOR

    def update_pos(self, t):
        for i, (x, y) in enumerate(self.dots):
            # y(x,t) = A*sin(wt - kx)
            new_y = self.amplitude * math.sin(
                (2 * math.pi * self.frequency * (t / 1000)) - (x * 2 * math.pi / self.wave_lambda))
            self.dots[i][1] = new_y

    def draw_wave(self, window):
        for x, y in self.dots:
            draw_x = x * SCALE
            draw_y = y * SCALE + HEIGHT / 2

            pygame.draw.circle(window, self.color, (draw_x, draw_y), DOT_RADIUS)

    def update_wave_settings(self):
        root = tkinter.Tk()
        root.title("add wave")
        root.protocol("WM_DELETE_WINDOW", lambda: self.apply_settings_changes(root, "1", "1", "red"))
        root.geometry('400x400')
        root['bg'] = 'white'
        A_frame = tkinter.Frame(root, bg='white')

        A_lbl = tkinter.Label(A_frame, text='enter the A(m):', font=('Narkisim', 16), bg='white')
        A_lbl.grid(column=0, row=0, padx=5)

        A_entry = tkinter.Entry(A_frame, bd=2, width=30)
        A_entry.insert(tkinter.END, "1")
        A_entry.grid(column=1, row=0, padx=5)

        A_frame.pack(pady=45)

        f_frame = tkinter.Frame(root, bg='white')

        f_lbl = tkinter.Label(f_frame, text='enter the f(Hz):', font=('Narkisim', 16), bg='white')
        f_lbl.grid(column=0, row=0, padx=5)

        f_entry = tkinter.Entry(f_frame, bd=2, width=30)
        f_entry.insert(tkinter.END, "1")
        f_entry.grid(column=1, row=0, padx=5)

        f_frame.pack(pady=45)

        color_frame = tkinter.Frame(root, bg='white')

        color_lbl = tkinter.Label(color_frame, text='enter the color:', font=('Narkisim', 16), bg='white')
        color_lbl.grid(column=0, row=0, padx=5)

        color_entry = tkinter.Entry(color_frame, bd=2, width=30)
        color_entry.insert(tkinter.END, "white")
        color_entry.grid(column=1, row=0, padx=5)

        color_frame.pack(pady=45)

        start_btn = tkinter.Button(root, text='add wave', bd=0, font=('Narkisim', 20, 'bold'),
                                   command=lambda: self.apply_settings_changes(root, A_entry.get(), f_entry.get(),
                                                                               color_entry.get()))
        start_btn.pack()

        root.mainloop()

    def apply_settings_changes(self, root, amplitude, frequency, color):
        try:
            self.amplitude = float(amplitude)
            self.frequency = float(frequency)
            self.wave_lambda = SPEED / self.frequency
        except:
            self.amplitude = 1.0
            self.frequency = 1.0
            self.wave_lambda = SPEED / self.frequency
        if is_color_like(color):
            self.color = color
        else:
            self.color = "white"

        root.destroy()

    def __add__(self, other):
        return Wave([[this_dot[0], this_dot[1] + other_dot[1]] for this_dot, other_dot in zip(self.dots, other.dots)])


def draw_background(window, first=False, lines=False):
    window.fill((50, 50, 50))

    pygame.draw.line(window, CYAN, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 5)
    pygame.draw.line(window, CYAN, (0, 0), (0, HEIGHT), 5)
    axis_text_x = AXIS_FONT.render(f"X[m]", True, CYAN)
    axis_text_y = AXIS_FONT.render(f"Y[m]", True, CYAN)
    window.blit(axis_text_x, (WIDTH - axis_text_x.get_width() - 5, HEIGHT // 2 - axis_text_x.get_height() - 5))
    window.blit(axis_text_y, (10, 6))
    # axis numbers - x
    for i in range(100, WIDTH, 100):
        number_text = NUMBERS_FONT.render(f"{round(i / SCALE, 1)}", True, CYAN)
        window.blit(number_text, (i, HEIGHT // 2 + number_text.get_height()))
    # axis numbers - y
    for i in range(100, HEIGHT, 100):
        number_text = NUMBERS_FONT.render(f"{round((i - HEIGHT / 2) / SCALE, 1)}", True, CYAN)
        window.blit(number_text, (7, i))

    if lines:
        for i in range(NUM_OF_DOTS + 1):
            x = (WIDTH / NUM_OF_DOTS) * i
            pygame.draw.line(window, (0, 0, 0), (x, 0), (x, HEIGHT), 3)

    if first:
        pygame.display.update()


def main():
    draw_background(WIN, True)

    show_instructions()

    run = True
    clock = pygame.time.Clock()

    waves = []
    show_super_pos = False
    show_others = True
    freeze = False
    lines = False
    timer = 0

    while run:
        dt = clock.tick(60)
        if not freeze:
            timer += dt

        draw_background(WIN, lines=lines)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    waves.append(Wave())
                if event.key == pygame.K_r:
                    waves.clear()
                if event.key == pygame.K_s:
                    show_super_pos = not show_super_pos
                if event.key == pygame.K_d:
                    show_others = not show_others
                if event.key == pygame.K_f:
                    freeze = not freeze
                if event.key == pygame.K_l:
                    lines = not lines
                if event.key == pygame.K_i:
                    show_instructions()
                if event.key == pygame.K_o:
                    set_simulation_options()
                    for wave in waves:
                        wave.wave_lambda = SPEED / wave.frequency
                        for i, dot in enumerate(wave.dots):
                            wave.dots[i][0] = (WIDTH / SCALE / NUM_OF_DOTS) * i

        for wave in waves:
            if not freeze:
                wave.update_pos(timer)
            if show_others:
                wave.draw_wave(WIN)

        super_pos_wave = None
        if len(waves) > 0:
            super_pos_wave = Wave(waves[0].dots.copy())
            for wave in waves[1:]:
                super_pos_wave += wave

        if show_super_pos and super_pos_wave:
            super_pos_wave.draw_wave(WIN)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
