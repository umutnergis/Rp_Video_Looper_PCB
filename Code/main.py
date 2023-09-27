import vlc
import subprocess
import os
import time
from datetime import datetime
from threading import Thread
import RPi.GPIO as GPIO



def get_video_duration(video_path):
    instance = vlc.Instance('--no-xlib')  
    media = instance.media_new(video_path)
    media.parse()
    duration = media.get_duration() / 1000 
    return duration

def button_state() -> int:
     if GPIO.input(ready_pin) == GPIO.HIGH:
       return 1
        

def relay_on(delay_time: int):
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(delay_time)
    
def relay_off():    
    GPIO.output(relay_pin, GPIO.LOW)

firstPlaying = True

def listenButton():
    count = 0
    money = get_money()
    money = int(money)
    global firstPlaying
    while True:
        if button_state() == 1:
            count = count +1
            print(count)
            time.sleep(0.5)
            if count == money:
                firstPlaying = False
                player.stop()
                player2.set_media(media2)
                player2.set_fullscreen(True)
                player2.play()
                relay_on(get_video_duration(film2))
                player2.stop()
                relay_off()
                time.sleep(0.2)
                count = 0
                firstPlaying = True


def playFirst():
    global firstPlaying
    while True:
        if firstPlaying:
            player.set_media(media)
            player.set_fullscreen(True)
            player.play()
            time.sleep(get_video_duration(film1))
            #player.stop()
            time.sleep(0.2)

def usb_path():
    usb_path = '/media/umut'
    for i in os.listdir(usb_path):
        print(i)
    usb_path += f'{os.listdir(usb_path)[0]}'
    print(usb_path)
    return usb_path

def video_path():
    #usb_path = usb_path()
    video_path1 = f'{usb_path()}/first.mp4'
    video_path2 = f'{usb_path}/second.mp4'
    return video_path1, video_path2

def get_money():
    money_path = "/media/umut/42F4-3D07/money.txt"
    with open(money_path, 'r') as f:
        money = f.read()
    return money

ready_pin = 17
relay_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(ready_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.LOW)

film1 = "/media/umut/42F4-3D07/first.mp4"
film2 = "/media/umut/42F4-3D07/second.mp4"



instance = vlc.Instance()
player = instance.media_player_new()
player2 = instance.media_player_new()
media = instance.media_new(film1)
media2 = instance.media_new(film2)

relay_off()
Thread(target=listenButton).start()
playFirst()