# SpotifyAPIs

## Introduction

This repo is really just a personal project that I have used as a starter for playing around with the Spotify API. I hope to be adding more API scripts or maybe even develop a backend server to have these scripts running constantly. However, currently, these only exist as scripts that work (I hope!).

## Purpose and Content

Okay so, this all came about because I wanted to automate a means of creating monthly playlists. The idea was to have a way to get all songs that I like in a given month to be saved in a secondary playlist that is titled "Month Year". That has spiralled into two additional scripts and a third script which isn't really that important but it's a fun test case. So this repository -- at the time of writing contains:

- "**getMonthly.py**" -- as the name suggests, this script gets the monthly playlist. To break it down, this script uses the client ID and client secret key (which will explained below) that has been set up with the Spotify API to get the list of playlists the user has, looks for the "Liked Songs" and compares when these songs were added to the time the script was last run. Depending on the added dates on the songs, it places them into newly created and appropriately named playlists. If these playlists already exist, in case you decide to run this script multiple times a month, it will place the new songs into the appropriate playlist -- and should not make a new playlist!

## Some caveats

To run these scripts, you need to do follow a few steps:
    - Log in to Spotify Developers and create an appropriate app
    - Download and install python and the libraries
    - Download this git repository
    - Run the script
Don't worry, this will take you through each one of these steps

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
    - Beneath the ClientID, click "View client secret", copy that and save in the same document as the client ID
    - We are done with this page now. 

### Making env files

    - On your laptop, open notepad (or text editor of your choice. NOT MICROSOFT WORD)
    - Copy this format:
    ```txt
    CLIENT_ID="your_client_ID"
    CLIENT_SECRET="your_client_secret"
    APPSECRET="random_set_of_characters_you_choose_eg_hghshsfhsiofh949tbdadsfih"
    SCOPE="user-library-read playlist-modify-public playlist-modify-private"
    REDIRECTURI="http://127.0.0.1:5000/redirect"
    ```
    - **It is important that these are set up like this.**
    - Depending on the script you wish to run, the filename to save this as will be different. 
        - If you wish to run the batch deletion script, save this file as "**.batch_del_env**" 
        - If you wish to run the save discover weekly script, save this file as "**.weekly_env**" 
        - If you wish to run the monthly playlist script, save this file as "**.monthly_env**" 

## Running the scripts

There are two options on how to get the scripts running. You can either set it up to run on your phone or your computer/PC. Currently, I have tested it to work on Android phones and on Windows OS. However, the principle should still work on Linux/MacOS system. If you come across any issues, please open an issue and let me know.

### Running Spotify APIs on Android

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

#### Installing Python and its libraries

    - To run the script, we need python so install python with: `pkg install python`
        - Note: This will use ~623MB of storage
        - Accept with "Y" and proceed with the installation
    - Next, we will install packages that are needed to first get the scripts and then run them. The packages that are too be installed are:
        - Git -- git
        - Spotipy -- spotipy
        - dotenv -- python-dotenv
        - Flask -- flask
    - To install these packages, enter: `pip install <package_name>`
        - `pip install git` or 
        - `pip install python-dotenv`
        - Do this for all four packages
    - Great! Once that is done, we now need to set up termux to access the files storage on your device
    - To do this enter: `termux-setup-storage`
        - This will prompt you to give it access to your storage, press "Allow" or "Yes", whichever is in the affirmative
        - And that's it, now you can navigate your phone like any other linux device
    - Next I would highly recommend that you make a folder in `~/storage/shared` to hold the SpotifyAPI scripts. 


    - Install Python
    - Install python libraries
        - pip
        - python-dotenv
        - spotipy
        - flask
