from datetime import datetime, date
from os import makedirs
from os.path import exists
from sqlalchemy import create_engine, desc, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists
from sys import argv, exit
from textwrap import wrap


MEALS = ["breakfast", "lunch", "snack", "dinner"]

Base = declarative_base()


class Food(Base):
    __tablename__ = "foods"

    food_id = Column("food_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    meal = Column("meal", String)
    date = Column("date", Integer)

    def __init__(self, name, meal, date):
        self.name = name
        self.meal = meal
        self.date = date

    def __repr__(self):
        return f"{self.date} {self.meal}: {self.name}"


engine = create_engine("sqlite:///food.db", echo=True)

if not database_exists("sqlite:///food.db"):
    Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def main():

    # Adding foods to journal as a command line command, usage: python3 main.py [meal] [list of foods]

    if len(argv) >= 3:

        if argv[1].lower() in MEALS:
            meal = argv[1]
            today = date.today()

            insert_food(today, meal, argv[2:])
            exit()

    # Print main menu

    clear_console()
    print("****************")
    print("* MEAL JOURNAL *")
    print("****************")

    print("\nCS50P Final project, Veera Hiltunen (Helsinki, Finland)\n")

    while True:
        print("SELECT:")
        selection = input(
            "\n(1) Add foods\n(2) Print diary to file\n(3) Quit program\n\nSelection: ")
        if selection == "1":
            add_food()
        elif selection == "2":
            print_db()
        elif selection == "3":
            break

    print("\nThank you and good bye!\n")


# Defining functions for adding meal data to journal

def add_food():
    while (True):
        clear_console()
        print("** ADD FOODS TO JOURNAL **")
        day = get_day()
        if day == None:
            clear_console()
            break

        while (True):
            print(f"\n{day_string(day)}\n")
            meal = get_meal()
            if meal == None:
                break

            clear_console()

            while (True):
                print(f"\n{day_string(day)}: {meal.upper()}\n")
                food_list = get_food()
                if food_list == None:
                    break
                else:
                    insert_food(day, meal, food_list)
                    break


def get_day():

    while (True):
        user_input = input(
            "\nGive day in format DDMMYY (0: today, Enter: return): ")
        if user_input == "0":
            return date.today()
        if user_input.lower() == "":
            return None
        else:
            try:
                return (datetime.strptime(user_input, "%d%m%y"))
            except ValueError:
                continue


def get_meal():

    while (True):

        for i in range(len(MEALS)):
            print(f"({i+1}) {MEALS[i].capitalize()}")

        selection = input("\nSelect meal (Enter: return): ")
        if selection.lower() == "":
            return None
        else:
            try:
                return MEALS[int(selection)-1]
            except ValueError:
                print("\nInvalid selection!\n")
                continue


def get_food():

    food_list = []

    while (True):

        food = input("Add food (Enter: finish): ")
        if food.lower() == "":
            break
        elif food != "":
            food_list.append(food)

    if len(food_list) == 0:
        return None
    else:
        return food_list


def insert_food(day, meal, food_list):
    for food in food_list:
        session.add(Food(food, meal, datetime.strftime(day, "%y%m%d")))
    session.commit()
    clear_console()
    print("Meal and foods successfully added to your food diary! :) ")


def day_string(datetime_object):
    return datetime.strftime(datetime_object, "%A %-d %B %Y")


def printable_string(date_string):
    datetime_object = datetime.strptime(date_string, "%y%m%d")
    return day_string(datetime_object).upper()


# Defining functions for printing the meal journal

def print_db():

    if not exists("print"):
        makedirs("print")

    clear_console()
    print("** PRINT JOURNAL TO FILE **\n")

    filename = get_filename()
    if filename == None:
        clear_console()
        return

    print("")

    while (True):
        order = input(
            "Select order:\n\n(1) Newest to oldest\n(2) Oldest to newest\n\nSelection (Enter: return): ")
        if order == "1":
            query = session.query(Food.date).distinct().order_by(
                desc(Food.date)).all()
            break
        elif order == "2":
            query = session.query(
                Food.date).distinct().order_by(Food.date).all()
            break
        elif order == "":
            clear_console()
            return

    with open(f"{filename}", "w") as file:

        file.write("****   M E A L   J O U R N A L   ****\n")

        date_list = [row.date for row in query]

        print(date_list)

        for date in date_list:
            try:
                file.write(f"\n\n{printable_string(str(date))}\n\n")
            except ValueError:
                file.write(f"\n\n{date}\n\n")

            for meal in MEALS:
                meal_query = session.query(Food.meal).filter(
                    Food.date == date).filter(Food.meal == meal).distinct().all()
                meal_list = [row.meal for row in meal_query]

                for meal_result in meal_list:
                    file.write(f"{meal_result.capitalize()}:")

                    food_query = session.query(Food.name).filter(Food.date == date).filter(
                        Food.meal == meal_result).order_by(Food.name).all()

                    food_list = [row.name for row in food_query]

                    food_str = ''
                    for food in food_list:
                        food_str = f"{food_str} {food},"

                    wrapped = wrap(food_str.strip(','), width=70)

                    file.writelines('\n\t\t'.join(wrapped))
                    file.write("\n")

    clear_console()
    print(f"Food journal printed to file {filename}.\n")


def get_filename():

    new = ""

    while (True):
        filename = input(f"Give {new}filename (Enter: return): ")

        if filename == "":
            return None
        elif len(filename.split(".")) > 2:
            continue
        elif (len(filename.split(".")) == 2) and (filename.split(".")[1] == "txt"):
            filename = filename
        else:
            filename = f"{filename.lower()}.txt"

        if exists(f"print/{filename}"):
            while (True):
                selection = input(
                    f"\nFile {filename} exists. Do you want to replace the existing file? (Y/N): ").lower()
                if selection == "y":
                    return f"print/{filename}"
                elif selection == "n":
                    print("")
                    new = "new "
                    break
                else:
                    continue

        else:
            break

    return f"print/{filename}"


def clear_console(): return (print('\033c', end=''))


if __name__ == "__main__":
    main()
