import pygame
import numpy as np
import time
import threading
import colorsys

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

chakra_frequencies = {
    'Root Chakra - 198 Hz': 198.0,
    'Sacral Chakra - 208 Hz': 208.0, 
    'Solar Plexus Chakra - 264 Hz': 264.0,
    'Heart Chakra - 319 Hz': 319.0,
    'Throat Chakra - 370 Hz': 370.0,
    'Third Eye Chakra - 426 Hz': 426.0,
    'Crown Chakra - 481 Hz': 481.0
}

brainwave_frequencies = {
    'Delta': 2,
    'Theta': 6,
    'Alpha': 10,
    'Beta': 16
}

def generate_tone(frequency, duration=1, volume=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    tone *= volume
    return tone

def generate_binaural_beat(base_freq, beat_freq, duration=1, sample_rate=44100):
    left_channel = generate_tone(base_freq - beat_freq / 2, duration, 0.5, sample_rate)
    right_channel = generate_tone(base_freq + beat_freq / 2, duration, 0.5, sample_rate)
    binaural_beat = np.array([left_channel, right_channel]).T
    return np.ascontiguousarray(binaural_beat)

import tkinter as tk
from tkinter import ttk

class BinauralBeatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binaural Beats Generator")
        self.is_playing = False
        self.current_chakra = 'Root Chakra - 198 Hz'
        self.current_wave = 'Delta'
        self.volume = 0.25

        self.setup_ui()

        self.fade_and_update_audio()

        self.running = True
        self.animation_thread = threading.Thread(target=self.run_animation)
        self.animation_thread.start()

    def setup_ui(self):
        self.chakra_frame = tk.Frame(self.root)
        self.chakra_frame.pack(side=tk.LEFT, padx=10)

        self.brainwave_frame = tk.Frame(self.root)
        self.brainwave_frame.pack(side=tk.LEFT, padx=10)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, pady=10)

        self.volume_slider = ttk.Scale(self.control_frame, from_=1.0, to=0.0, orient=tk.VERTICAL, command=self.change_volume)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(side=tk.LEFT)

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.chakra_buttons = {}
        for chakra in chakra_frequencies.keys():
            btn = tk.Button(self.chakra_frame, text=chakra, command=lambda c=chakra: self.change_chakra(c))
            btn.pack(fill=tk.X, pady=2)
            self.chakra_buttons[chakra] = btn

        self.wave_buttons = {}
        for wave in brainwave_frequencies.keys():
            btn = tk.Button(self.brainwave_frame, text=wave, command=lambda w=wave: self.change_wave(w))
            btn.pack(fill=tk.X, pady=2)
            self.wave_buttons[wave] = btn

        self.info_label = tk.Label(self.root, text=f"Frequency: {chakra_frequencies[self.current_chakra]} Hz | Binaural Beat: {brainwave_frequencies[self.current_wave]} Hz")
        self.info_label.pack(side=tk.BOTTOM, pady=10)

    def change_volume(self, val):
        self.volume = float(val)
        if self.is_playing:
            self.current_sound.set_volume(self.volume)

    def toggle_play(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_button.config(text="Pause")
            self.play_audio()
        else:
            self.toggle_pause()

    def toggle_pause(self):
        self.is_playing = False
        self.play_button.config(text="Play")
        self.current_sound.fadeout(1000)

    def change_chakra(self, chakra):
        self.current_chakra = chakra
        self.fade_and_update_audio()

    def change_wave(self, wave):
        self.current_wave = wave
        self.fade_and_update_audio()

    def fade_and_update_audio(self):
        if self.is_playing:
            self.current_sound.fadeout(1000)
            time.sleep(1)
            self.play_audio()

        self.info_label.config(text=f"Frequency: {chakra_frequencies[self.current_chakra]} Hz | Binaural Beat: {brainwave_frequencies[self.current_wave]} Hz")

    def play_audio(self):
        freq = chakra_frequencies[self.current_chakra]
        beat = brainwave_frequencies[self.current_wave]

        binaural_beat = generate_binaural_beat(freq, beat, duration=1)
        sound_array = (binaural_beat * (2**15 - 1)).astype(np.int16)
        self.current_sound = pygame.sndarray.make_sound(sound_array)
        self.current_sound.set_volume(self.volume)
        self.current_sound.play(loops=-1, fade_ms=1000)
    
    def run_animation(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Binaural Beat Animation")
        clock = pygame.time.Clock()
        screen.fill((203,50,52))
        umbral = 0
        angle = 0  # Ángulo de rotación en grados

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            freq = chakra_frequencies[self.current_chakra]
            beat = brainwave_frequencies[self.current_wave]
            t = pygame.time.get_ticks() / 1000.0

            if freq == 198:
                color = (203,50,52)
            elif freq == 208:
                color = (255,128,0)
            elif freq == 264:
                color = (250,250,55)
            elif freq == 319:
                color = (65,169,76)
            elif freq == 370:
                color = (135,206,250)
            elif freq == 426:
                color = (50,82,123)
            elif freq == 481:
                color = (106,13,173)
            else:
                color = (0,0,0)

            if umbral >= 1:
                rect_surface = pygame.Surface((800,600),pygame.SRCALPHA)
                rect_color = (color[0],color[1],color[2], 60)
                rect_surface.fill(rect_color)
                screen.blit(rect_surface, (0, 0))
                angle += (1/(freq))  # Ángulo de rotación en grados
                rotated_screen = pygame.transform.rotate(screen, angle)
                # Ajustar la posición para centrar la pantalla rotada
                rotated_rect = rotated_screen.get_rect(center=screen.get_rect().center)
                # Dibujar la pantalla rotada
                screen.blit(rotated_screen, rotated_rect.topleft)
                if angle >= 360:
                    angle = 0
                umbral = 0
                
            
        
            color1 = (255-color[0]), (255-color[1]) ,(255-color[2])
            color2 = ((255+color[0])//2), ((255+color[1])//2) ,((255+color[2])//2)
            color3 = (255-color[0]), (255-color[1]) ,(255-color[2])
            color4 = ((255+color[0])//2), ((255+color[1])//2) ,((255+color[2])//2)

            for i in range(800):
                x = i
                y = int(300 + 100 * np.sin(2 * np.pi * (freq/4) * t + (i / 800.0) * 2 * np.pi))
                pygame.draw.circle(screen, (color1), (x, y), int(self.volume * 10) +1)

            for i in range(800):
                x = i
                y = int(300 + 100 * np.sin(2 * np.pi * ((beat+freq)/4) * t + (i / 800.0) * 2 * np.pi))
                pygame.draw.circle(screen, (color2), (x, y), int(self.volume * 10) +1)
            for i in range(800):
                y = i
                x = int(300 + 100 * np.sin(2 * np.pi * (freq/4) * t + (i / 800.0) * 2 * np.pi))
                pygame.draw.circle(screen, (color3), (x, y), int(self.volume * 10) +1)

            for i in range(800):
                y = i
                x = int(300 + 100 * np.sin(2 * np.pi * ((beat+freq)/4) * t + (i / 800.0) * 2 * np.pi))
                pygame.draw.circle(screen, (color4), (x, y), int(self.volume * 10) +1)

            umbral += 1

            pygame.display.flip()
            #clock.tick(beat)
            clock.tick(6+(beat/2)+(freq/100))
            #clock.tick(beat*(freq//100))
        
        pygame.quit()

root = tk.Tk()
app = BinauralBeatsApp(root)
root.mainloop()
app.running = False
app.animation_thread.join()
