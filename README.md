# SpotifyAPIs

## Introduction

This repo is really just a personal project that I have used as a starter for playing around with the Spotify API. I hope to be adding more API scripts or maybe even develop a backend server to have these scripts running constantly. However, currently, these only exist as scripts that work (I hope!). I understand the set-up seems lengthy but it is a single one-time set up and it takes ~30mins or so. Please do read the steps in full before starting to ensure efficient usage.

## Purpose and Content

Okay so, this all came about because I wanted to automate a means of creating monthly playlists. The idea was to have a way to get all songs that I like in a given month to be saved in a secondary playlist that is titled "Month Year". That has spiralled into two additional scripts and a third script which isn't really that important but it's a fun test case. So this repository -- at the time of writing contains:

- "**getMonthly.py**" -- as the name suggests, this script gets the monthly playlist. To break it down, this script uses the client ID and client secret key (which will explained below) that has been set up with the Spotify API to get the list of playlists the user has, looks for the "Liked Songs" and compares when these songs were added to the time the script was last run. Depending on the added dates on the songs, it places them into newly created and appropriately named playlists. If these playlists already exist, in case you decide to run this script multiple times a month, it will place the new songs into the appropriate playlist -- and should not make a new playlist!
- "**saveWeeklyDiscovery.py**" -- this script acts to save your Discover Weekly songs to an archive. Currently, that archive playlist will be called "Discover Weekly Archive"
- "**batchDelete.py**" -- this came about due to wanting to delete all the test playlists I made during the development of the "getMonthly" script. So this will delete any playlist that fits the pattern "Month Year" e.g. If I have two playlists named "March 2024" and "Mar 24", the script will only delete "March 2024"
- "**GetArtistTopTracks.py"** -- this is a starter/tester script that's more of a proof of concept. It will output the top 5 songs of any given artist. It is currently hardcoded for ACDC but this can be manually changed by you. I'm working on a way to ask you (the user) to enter your preferred artist. Watch this space.

## Some caveats

### General need-to-knows

To run these scripts, you need to do follow a few steps:
- Log in to Spotify Developers and create an appropriate app
- Download and install python and the libraries
- Download this git repository
- Run the script
Don't worry, this will take you through each one of these steps

### Currently known hiccups
After you have set up everything and run the script, there may be an error where the Discover Weekly playlist cannot be found, this is likely going to be because the Discover Weekly is not viewable on your profile. To fix this:

- On your Spotify app, go to your Discover Weekly playlist, click on the three vertical dots and select "Add to profile"
- Next on your chosen platform, either on Windows or Android, you want to delete the ".cache" that will have generated from running the script
- You can do this easily via Termux using "rm .cache" and you can simply navigate to the location on Windows and delete it
- Get in contact if this does not work.

## Set-Up

### Spotify Developers and Spotify App Creation

The purpose of this step is to essentially create a way to allow the script to talk to Spotify directly. Spotify calls this an "app" which can only be done through the Spotify Developer.

- So firstly, go to: "https://developer.spotify.com/" and log into your spotify account
- At the top right of the page, click your username and then click "Dashboard"
- On the dashboard page, click "Create app". 
- Fill in the page to be similar to this screenshot. However:
    - Change the name of the app to fit the script you wish to attach to this app. 
    - **Note: One script interacts with one app e.g. the batch deletion script can only interact with an app you make for batch deletion. The batch deletion app cannot interact with the batch deletion script AND the monthly playlist script**
    - The image: ![[Pasted image 20240324210214.png]]
    - It is important that you get the Redirect URI correct. It is "http://127.0.0.1:5000/redirect"
    - Also make sure to tick "Web API"
    - Once you have filled it in, click "Save"
    - This brings you to your App Home

## Getting the client ID and secret key

To be able to interact with this app you have created, you will need what is essentially the username and password for this app. To get this information:

- Click the "Settings" button in the App Home page
- On the settings page copy the "ClientID" and save it in a word/text document. **We will need this later**
  - If doing this on mobile, copy it to a safe location that you can retrieve it. Maybe your Notes app.
- Beneath the ClientID, click "View client secret", copy that and save in the same document as the client ID
- We are done with this page now.

## Running the scripts

There are two options on how to get the scripts running. You can either set it up to run on your phone or your computer/PC. Currently, I have tested it to work on Android phones and on Windows OS. However, the principle should still work on Linux/MacOS system. If you come across any issues, please open an issue and let me know.

### Running Spotify APIs on Android

#### Downloading the scripts

First thing is to download this package to your phone. On this github page, go to the green button that says "Code" (**Note this should be done on the device you want to run the script on!**). Select "Download ZIP". This should download a zip file to your Download/Downloads folder. Leave it there, we will come back to it.

#### Installing Termux

To run these scripts on Android, you need an app called "Termux". **Do not get termux from the Play store. That version is outdated. Use F-Droid or get the v8.apk from github. this link:** https://github.com/termux/termux-app/releases. I am using v0.118.0 ![[Pasted image 20240324214322.png]]
- On your mobile phone, go to the link: https://github.com/termux/termux-app/releases
- Download the v8a.apk -- in the image above, I got the *termux-app_v0.118.0+github-debug_arm64-v8a.apk* and installed it on my Android phone
    - Note: Your phone will likely ask you if you want to install/download, go ahead and Download anyway
    - Then to install you will need to grant access to installing apps from third-parties
    - Each mobile phone manufacturer handles this slightly differently
- Once the app is installed, open it  and do the following:
    - Type: `pkg update && pkg upgrade` and press enter
        - This updates and upgrade the Linux packages that come with Termux. Its important to do this so that steps after this don't fail
    - This will inform you that the update will take up a certain amount of space.
    - Enter "Y" for yes and press "Enter"
    - Next, during the update process, you will be prompted multiple times about files that are already on your device which clash with files that the package maintainer wants to install with a package. The default action is always to keep the version on your device. 
    - So with each prompt asking you something like "Configuration file '/data/data/com.termix/files/usr/etc/tls/openssl.cnf" or something similar, enter "N" to keep default

The next series of steps will take place in Termux.

#### Installing Python and its libraries

- To run the script, we need python so install python with: `pkg install python`
    - Note: This will use ~623MB of storage
    - Accept with "Y" and proceed with the installation
- Next we install git using `pkg install git`
- Then, we will install packages that are needed to first get the scripts and then run them. The packages that are too be installed are:
    - Spotipy -- spotipy
    - dotenv -- python-dotenv
    - Flask -- flask
- To install these packages, enter: `pip install <package_name>` 
    - `pip install python-dotenv`
    - `pip install spotipy`
    - `pip install flask`
- Great! Once that is done, we now need to set up Termux to access the files storage on your device
- To do this enter: `termux-setup-storage`
    - This will prompt you to give it access to your storage, press "Allow" or "Yes", whichever is in the affirmative
    - And that's it, now you can navigate your phone like any other linux device

#### Making the script folder

- Next (still on Termux) I would highly recommend that you make a folder in `~/storage/shared` to hold the SpotifyAPI scripts.
  - This is to make sure that all that you do stay in the right folder
  - To do this on Termux, type in the following commands:
    - `cd ~/storage/shared` = this will now change your location to the "shared" folder
    - Now we go back to the downloaded SpotifyAPI package we got earlier. In my case, it was downloaded to the "Download" folder
    - Still in the "shared" folder, type in `mv ./Download/SpotifyAPIS-main.zip ./` and enter
    - Next type `unzip ./SpotifyAPIs-main.zip` and enter
    - Next type `rm unzip ./SpotifyAPIs-main.zip` and enter
    - Finally type: `mv ./SpotifyAPIs-main ./SpotifyAPIs` and enter
  - Those set of commands have now made a folder of the scripts in the "shared" folder

#### Making env files

- Still on Termux, enter `cd SpotifyAPIs` to change location into the folder containing the scripts
- Next we want to use the clientID and cient secret you copied earlier
- Using the example that the monthly script is the desired script I want to run:
  - I will have copied and saved the clientID and client secret from Spotify Developers
  - Enter `nano .monthly_env_example`: This opens the file to be edited
  - Copy and paste your client 


- **It is important that these are set up like this.**
- Depending on the script you wish to run, the filename to save this as will be different.
    - If you wish to run the batch deletion script, save this file as "**.batch_del_env**"
    - If you wish to run the save discover weekly script, save this file as "**.weekly_env**"
    - If you wish to run the monthly playlist script, save this file as "**.monthly_env**"


