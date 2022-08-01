#!user/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from time import sleep

def wait_data():
        reader = SimpleMFRC522()
        idx,output =  reader.read()
        return output


if __name__ == "__main__":
        #############
        # PIN SETUP #
        #############
        """
        Using GPIO 18,18,23, and 24 is preferred however you may change this to any other valid GPIO pin if needed.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.OUT) # LED
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Next Button
        GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Prev Button
        GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Pause Button
        #############
        # API SETUP #
        #############
        """
        This will load all the data from config and log you into spotify. Make sure you're using graphical mode (GUI) to set this up.
        If you haven't logged into the application yet then you may have a slight pause as the chromium browser opens.
        """
        with open("config.json") as f:
                data = json.load(f)
        sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                        client_id = data["client_id"],
                        client_secret=data["client_secret"],
                        redirect_uri=data["redirect"],
                        scope="user-library-read user-read-currently-playing user-read-playback-state app-remote-control streaming")
                )
        print([i["id"] for i in sp.devices()["devices"]]) 
        # This prints all active spotify devices, copy the device_id of this device into config. If you don't see your device
        # there may be an issue with your setup with spotifyd.
        while(data["device_id"] not in [i["id"] for i in sp.devices()["devices"]]):
                sleep(2) # Wait until device is connected
        sp.transfer_playback(data["device_id"],force_play=True)
        playlist = sp.current_user_playing_track()["context"]
        playlist = None
        if playlist is not None:
                playlist = playlist["uri"]
        print(playlist)
        ##################
        # CALLBACK SETUP #
        ##################
        playing = True
        def pause(channel):
                global playing
                if playing:
                        sp.pause_playback()
                        print("Pausing")
                else:
                        sp.start_playback()
                        print("Playing")
                playing = not playing
                sleep(0.5)
        def next(channel):
                sp.next_track()
                print("Skipping")
                sleep(0.5)
        def prev(channel):
                sp.previous_track()
                print("Previous")
                sleep(0.5)


        GPIO.output(17,GPIO.HIGH)
        GPIO.add_event_detect(18,GPIO.RISING,callback=next,bouncetime=200)
        GPIO.add_event_detect(23,GPIO.RISING,callback=prev,bouncetime=200)
        GPIO.add_event_detect(24,GPIO.RISING,callback=pause,bouncetime=200)
        #########################
        # LOOP FOR RFID CHANGES #
        #########################
        try:
                while True:
                        rfid_data = wait_data().strip()
                        print(f"Chainging to {rfid_data} ")
                        print(len(rfid_data))
                        if len(rfid_data) >= 36 and rfid_data != playlist: # Check for proper RFID read and an actual change.
                                playlist = rfid_data
                                sp.start_playback(context_uri=playlist)
                                sp.shuffle(True)
                                sp.next_track()
                                sleep(2)

        finally:
                GPIO.output(17,GPIO.LOW)
                GPIO.cleanup()