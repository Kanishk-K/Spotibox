# Spotibox
Spotibox is a project made by Kanishk Kacholia and Aanchal Singhal. The purpose of Spotibox is to provide users with a seamless way to interface with music through an aesthetically pleasing and intriguing IOT device. Users can create custom cards containing information about their favorite playlists and swipe them across Spotibox to begin playing their music.

<img src="images/20220801_153628.jpg" alt="Spotibox Image">

# Setup
## Software
1. Install and Setup Raspbian (Debian 11 "Bullseye" required) onto your Raspberry Device
2. pip install the requirements needed for the python files
> pip3 install -r requirements.txt
3. Setup [Spotifyd](https://spotifyd.github.io/spotifyd/installation/Raspberry-Pi.html)
4. Setup a [Spotify Web API Endpoint](https://developer.spotify.com/documentation/web-api/)
5. Clone this repository
6. Run the python program and copy the device ID into config.
```bash
cd spotibox
python3 main.py
```
7. Copy a playlist or album URI and write it into card
```bash
cd spotibox
python3 write.py
```
8. Setup SystemCTL files 
```
touch /etc/systemd/system/spotibox.service
```
9. Insert the following into that file (omit comments if needed)
```ini
[Unit]
Description=Spotibox Service # Service Name
Wants=network-online.target # Pre-req network access
After=network-online.target # Enforce network access

[Service]
Type=simple
User=YOUR USER PROFILE # To specifiy user this runs on
WorkingDirectory=/home/LOCALREPOSITORYNAME # Where Spotibox files are located 
ExecStart=/home/LOCALREPOSITORYNAME/spotibox.sh # Start our script
Restart=on-failure # In case of failure restart
RestartSec=5 # Wait 5 seconds on restarting

[Install]
WantedBy=multi-user.target # Run script on startup.
```

## Hardware
1. Connect the RFID in the following [configuration](https://cdn.pimylifeup.com/wp-content/uploads/2017/10/RFID-Fritz-v2.png)
2. Attach analog buttons to pins 18,23, and 24 to represent Skip, Previous, and Pause respectively.
3. Attach an optional LED to pin 17, this will tell you when the Raspberry pi is active and the script is running waiting for a RFID scan.

## External
1. Prior to running Spotibox, the program will require some information about your device and API. You can find API information on your Spotify Application dashboard, please fill them accordingly. Likewise you can find information about active devices through Spotify's online API [interface](https://developer.spotify.com/console/get-users-available-devices/)
2. Once you have all of this setup you should be able to run `python3 main.py` in Spotibox. This should begin playing your most recent track, OR ask you for a login prior to playing your most recent track.
3. After this is all done, just restart your Raspberry Pi and music should begin automatically playing after a couple of seconds!