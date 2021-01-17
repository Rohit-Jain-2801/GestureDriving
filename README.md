# GestureDriving
Playing Racing Games using Gestures!

<br/>

## Description
Do you want to play racing game without touching your keyboard keys 🙄? Then you are at the right place 😇. This project is an application of `Hand Detection`, that helps demonstrate and simulate Gesture-based Driving 😎.

<br/>

## Getting Started
1. Clone [this](https://github.com/Rohit-Jain-2801/GestureDriving.git) repo.
2. Make sure all necessary [dependencies](https://github.com/Rohit-Jain-2801/GestureDriving/blob/master/requirements.txt) are installed.
3. Dive into the project folder & run `python run.py` in your terminal.
4. Wait for the program to load-up & voila 🥳 then you can play game using gestures!

<br/>

## Video Demonstration
[![GestureDriving Gameplay](https://img.youtube.com/vi/JV34EVwH1cs/maxresdefault.jpg)](https://youtu.be/JV34EVwH1cs)
* YouTube Video - GestureDriving Gameplay of DiRT 3 game

<br/>

## Walkthrough
* Taking arguments from terminal
    + Used [argparse](https://docs.python.org/3/library/argparse.html) library to handle command-line arguments.
    + Tried to make sure, the whole program is manually configurable.
    + Optional Arguments:
        | Arg | Argument | Description |
        | :----: | :----: | :---- |
        | -h | --help | Show Help Messages |
        | -dr | --displayRunning | Display the Running Processes Paths |
        | -de | --displayEnlisted | Display the Enlisted Processes Paths |
        | -a val | --add val | Number of Process Paths to be added to Collection |
        | -rm | --remove | Remove Process Path(s) from Collection |
        | -e | --edit | Edit Process Path(s) in Collection |
        | -dc | --default_configuration | Display Default Configuration |
        | -c | --configure | Run with Manual Configuration. Place "-1" to skip |
    + **Note:** `-c` optional argument takes a number of arguments/values-
        - `frame_width`: width of the input camera video
        - `frame_height`: height of the input camera video
        - `fps_div`: frames to be considered apart from each other
        - `min_detection_conf`: minimum detection confidence
        - `min_tracking_conf`: minimum tracking confidence
        - `measure`: `0` for distance measure or `1` for comparison measure
        - `nitrous`: `0` for no-nitrous or `1` for nitrous support
        - `dir_thr_sm`: direction threshold small
        - `dir_thr_bg`: direction threshold big
        - `app_flag`: apply keyboard mapping to all applications
* Displaying Running processes paths
    + Used [psutil](https://psutil.readthedocs.io/en/latest/) library to get list of running processes paths.
* Add, remove, edit, display Collection/Enlisted processes paths
    + Used basic file operations on `txt` file.
    + The program will only run if process's path enlisted is found to be running.
    + If `No` process is enlisted, the program will run in `Demo` mode.
* Display default configuration
    + Used `inspect` module to get default configuraton arguments.
* Detecting hands in the realtime video feed
    + Used [OpenCV](https://docs.opencv.org/4.5.1/) to access VideoCamera and to display landmarks & other stuffs on it.
    + Used [MediaPipe](https://mediapipe.dev/) for Hands Detection & Tracking.
* Implementing driving actions
    + Without Nitrous support
        - `Right Thumb Down`: Acceleration (`Up Arrow`)
        - `Left Thumb Down`: Reverse (`Down Arrow`)
        - `Both Thumbs Up`: No Action
    + With Nitrous support
        - `Right Thumb Down`: Nitrous & Acceleration (`Ctrl + Up Arrow`)
        - `Left Thumb Down`: Reverse (`Down Arrow`)
        - `Both Thumbs Up`: Acceleration (`Up Arrow`)
    + **Note:** If both the thumbs are down, preference will be given to `left thumb`.
* Implementing turning actions
    + Considered angle of rotation to make a turn.
        - While angle below `dir_thr_sm`: no action.
        - While angle between `dir_thr_sm` & `dir_thr_bg`: button is pressed & released.
        - While angle above `dir_thr_bg`: button is pressed until angle is no longer above.
* Support for One-Hand Driving
    + Driving actions will be dependent upon the hand used (left/right).
    + Turning actions will take center of video frame as reference.
* Configuring Driving & Turning actions
    + Can be easily re-configured with little knowledge of python 🤗.
* Determining if thumb is down enough
    + Considered `constant*handSize` to get a threshold for determining if thumb is down on index-finger.
* Implementing key-mappings of keyboard
    + Used [keyboard](https://github.com/boppreh/keyboard) library for key-mappings.
* Determining if enlisted process is focused
    + Used [win32gui](http://timgolden.me.uk/pywin32-docs/win32gui.html) library to get `hwnd`, passing it to [win32process](http://timgolden.me.uk/pywin32-docs/win32process.html) library to get it's corresponding `pid`.
    + This is followed by matching it to enlisted process `pid` got from psutil.
    + If both the pids' matches, then key-mapping are performed else not.
    + This ensures key-mappings are restricted to enlisted process only.

<br/>

## Future Scope
* Provide options for changing key-mappings.
* Provide GUI Interface for manual configuration.
* Improve Hand detection & tracking specially in case of high contrast.
* Improve thumb-based & turn action while playing.
* Support for multiple applications at a time.
* Support for OS other than Windows.
* Automatic start-up support when OS loads.
