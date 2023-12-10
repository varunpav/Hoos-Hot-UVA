[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/xHnRfY9D)
# CS3240 Project: Group B29

## Purpose

This project is a game of "hot cold" that may be accessed and played on a web browser.

## Tools Used

* Frameworks: Django
* Languages: JavaScript, Python
* Web Technologies: HTML, CSS
* Platforms: Heroku

## Functionality

* Google Login - Users sign in with Google and their data is synced to this account.
* Admin Users - Admin users have the ability to approve user submissions for games.
* Easy and Hard Modes - Users can choose between difficulty levels.
* Tutorial Level - Users can play a tutorial level to help them understand the gameplay.
* Game Continuation - Users can easily jump back in to a game they have yet to complete.
* Score Tracking - Users' total scores, games played, and the number of submissions they approve are stored in the database.
* Leaderboard - There is a leaderboard where users can view their rank based on multiple metrics.
* Game Submission - Users can submit custom games.
* Google Maps API - The site uses Google Maps to create and play games. 

## Gameplay Rules

* The player will start in a randomized start location. This location will be farther from campus if the difficulty is set to hard.
* Next, the player will drag the red pin to another location on the screen, and click the 'Get Hint' button.
* This button will display whether the user is:
    * Hot: The user's current distance from the goal location is less than half of their previous distance.
    * Cold: The user's current distance more than 1.5 times farther from the goal location than their previous distance.
    * Warm: The user's current distance is closer, but not less than half of their previous distance.
    * Cooler: The user's distance is farther, but not more than 1.5 times farther than their previous distance.
* Once the user is at the goal location, when they click 'Get Hint', they will be shown the win screen, displaying how many hints they used.
* The user's total score is updated by 100 - (5 * the number of hints used).
