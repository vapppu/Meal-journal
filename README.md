# MEAL JOURNAL

## [Video Demo](https://www.youtube.com/watch?v=KUKaFWudExE>)

## Overview

Meal journal is a command-line tool for tracking dailymeals. It has two functionalities: adding information about meals and printing out a text file including the entire meal journal.

Meal Journal is Veera Hiltunen's final project for [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/2022/) course.

## Inserting meals

Meal Journal provides two ways of inserting meal information:

### 1. Command-line arguments:

It is possible to add meal information for the current date in the command line by running the following in the root of the project directory:

```
python3 project.py [meal] [food1 food2 food3...]
```

For example:

```
python3 project.py lunch potatoes salmon broccoli
```

This would add potatoes, salmon and broccoli for your meal journal for the ongoing day.

### 2. Terminal user interface:

By running the program without additional command line arguments, you access the command-line user interface of the program. This allows you to insert data of several meals of one day. You can also insert foods retrospectively for past days as well.

## Printing journal data

The printing journal feature prints your journal to the /prints directory in the program root. You get to name your journal file, and specify whether you want the journal to be printed from newest to oldest or the other way around.

## Files

- project.py: Contains all the functionalities of the program (due to the final project specifications)
- food.db is the sqlite database. If it doesn't exist then the program is started, it will be created.
- tests.py contains some tests for certain functions. In the future, I wish to refractor the program so that it could be tested more thoroughly. Since the program relies so much on user input, it is difficult to create tests in its current form and with my skills.
- requirements.txt contains the required packages for running the program.
- print directory will be created when the journal is printed to file for the first time. The outputted .txt files will appear in this folder.

## Future development

In the future, the program could be improved by adding the following features, among others:

- printing the journal entries inside a specified time frame
- editing and deleting journal entries
- letting the user modify the appearance of the printed journal
