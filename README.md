# Time Without Numbers (TWN)

> A non-numeric desktop timer and passive activity tracker designed to support people with dyscalculia and time blindness.

![Screenshot](https://i0.wp.com/auliawiradarmo.blog/wp-content/uploads/2026/02/twn-_thumbnail.png?resize=1024%2C576&ssl=1)

## Video Demo
https://youtu.be/hD2uj2Fq5Po

## Background
Long before time was measured in numbers, humans oriented themselves through experience—sunrise and sunset, changing seasons, the waxing and waning of the moon—using these natural markers to guide everyday decisions. For many people with ADHD, time blindness reflects a reliance on similar experiential cues, in which the passage of time is difficult to sense, and the temporal continuum collapses into merely two markers: now and not now, resembling an object permanence challenge applied to time, where what or whom is no longer present here and now easily slips from mind. Furthermore, for someone with dyscalculia, the challenge is compounded by the very nature of numerical abstraction itself, in which clocks and dates expressed in numbers fail to convey meaning.

## Description
TWN is a Python-based Windows desktop widget that addresses time blindness as a representational mismatch by translating numeric time into experiential anchors—one song, one Pomodoro, one podcast episode—so that time is felt through accessible metaphor. It is a timer without digits, using shapes, colours, and movements to embody concepts that often elude the neurodiverse mind. It is also equipped with an activity tracker that quietly functions in the background, helping users make sense of where the time has gone.

## Features
### Timer
TWN consist of six time metaphors, ranging from five minutes to two hours. This reduces the steps for deciding the time length and typing numbers to a single click. Inspired by a digital music player, the alarm interface displays only a circular progress ring that fills over time, deliberately omitting the changing numbers typically used in a stopwatch.

The metaphors are as follows:

| Metaphor | Duration |
| --- | --- |
| One song | 5 minutes |
| One meditation | 10 minutes |
| One pomodoro | 25 minutes |
| One podcast | 45 minutes |
| One workout | 60 minutes |
| One movie | 120 minutes |

### Tracker
As an additional feature, TWN tracks various background applications (.exe) and groups them under several activity categories. Every ten minutes, a new block will appear beside the text. This also eliminates the need for numbers, as users can estimate time spent based on block length. No interaction is required; this feature will be activated automatically whenever the user starts the desktop.

The activities and the applications tracked are as follows:

| Activity | Application |
| --- | --- |
| Working | Ms Word, Ms Excel, Notepad, Obsidian, Notion |
| Creating | Ms PowerPoint, Canva, Figma |
| Coding | VS Code |
| Chatting | WhatsApp, Claude, ChatGPT |
| Meeting | Zoom, Ms Teams |
| Other | Google Chrome |

## How to Use
1. Launch TWN
2. Choose one of the six time metaphor buttons
3. Press the play button to start the timer
4. Press the pause or stop button if necessary
5. When the time is up, there will be an alarm
6. Press the logo to choose another time metaphor and return to the main interface

## Design Decisions
### Programming
The project was separated into three Python files:
1. `main.py` handles the Tkinter interface, screen layout, assets, user input, and update loops;
2. `timer.py` contains the timer logic, such as duration, play, pause, stop, remaining time, and progress calculation;
3. `tracker.py` contains the passive activity tracking logic, including detecting the active Windows application and categorising it.

Each file has one clear responsibility, so changes can be made without affecting unrelated parts of the program. This makes the program easier to understand, maintain, and debug. These files also illustrate a few key programming concepts: classes such as Timer and ActivityTracker encapsulate state and behaviour, while dictionaries are used to store timer configurations and map application process names to activity categories. The program is event-driven. Tkinter responds to button clicks and schedules repeated checks at set intervals, rather than executing from top to bottom like a simple script.

### Universal/Assistive
Because this project is based on personal needs and lived experience, some design decisions are necessarily subjective and reflect what is familiar to the maker, like a 10-minute daily meditation to improve focus. However, anchors such as a one-hour workout or a two-hour film were chosen because they are common references and are likely to be recognised by many users. TWN is therefore not intended to be a universal productivity tool, but rather an assistive design for people who find conventional numeric timers difficult, stressful, or cognitively unhelpful. By providing only six options, it also reduces the decision fatigue common among neurodiverse people.

For many people, removing numbers from a timer would make a simple task less efficient. However, for users with dyscalculia, the same omission can reduce cognitive load and make time easier to perceive. In that sense, TWN is closer to assistive technology than universal technology. It intentionally prioritises the needs of a specific group rather than trying to optimise for everyone. Like prescription glasses or crutches, some tools are valuable precisely because they are designed around particular bodies, minds, or access needs, not because they are equally useful to all users.

## Limitations & Future Improvement
A current limitation of TWN is that it has not yet been packaged as a Windows .exe file, so it must still be run directly from Python using python main.py. This makes it less convenient as an everyday desktop widget, although it is sufficient for testing and demonstrating the MVP. The activity tracker also does not store persistent history, as the data is reset when the application closes or Windows restarts. It also does not offer a turn-off option for users who do not want to use the tracker.

Future improvements could include packaging the project as an executable so it can be launched like a normal Windows application. The timer could also be expanded to support custom non-numeric durations while preserving the core design principle of avoiding countdown numbers. For the tracker, future versions could add browser tab detection so that the activities are not homogenised under “other”, daily or weekly statistics, and a local history system to help users review patterns over time. 

## Credits
*Course:*
CS50x Introduction to Programming
https://cs50.harvard.edu/x/

*Tools:*
VS Code, Python, Tkinter, Canva (interface guide)

*External Libraries:*
Pillow, pywin32, psutil

*Tech Support:*
ELM (The University of Edinburgh) in debugging, reviewing code, and assisting with the interface development using Tkinter.

*Logo:*
Hand-drawn by yours truly. Fun fact: The logo is inspired by the "Jeremy Bearimy" concept of time that appeared on one of my favourite TV series, "The Good Place".

*Painting:*
Pompeo Batoni (1740-1745) - Tempo di inaugurazione verità
https://commons.wikimedia.org/wiki/File:Pompeo_Batoni_-_Tempo_di_inaugurazione_verit%C3%A0_%28Art_Institute_of_Chicago%29.jpg

*Icons:*
Lucide
https://lucide.dev/icons/

*Sound:*
freesound_community from Pixabay
https://pixabay.com/sound-effects/city-church-clock-strikes-4-86907/

—

© Aulia Ardista Wiradarmo 2026