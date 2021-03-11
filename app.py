from utils import database, current_time
import os
from getpass import getpass

current_user_id = None
USER_CHOICE_ADMIN = """
Enter:
- 'a' to add a task
- 'l' to list all tasks
- 'r' to check out the task
- 'd' to delete a task
- 'u' to list all users
- 'n' to add a new user
- 'p' to update points
- 'rt' to refresh tasks
- 'li' to list shop items
- 'ai' to add item to shop
- 'di' to delete item from shop
- 'b' to buy shop item

- 'q' to quit

Your choice: """

USER_CHOICE_USER = """
Enter:
- 'l' to list all tasks
- 'r' to check out the task
- 'u' to list all users
- 'li' to list shop items
- 'b' to buy shop item
- 'q' to quit

Your choice: """


def menu():
    database.create_task_table()
    global current_user_id
    while current_user_id is None:
        if current_time.day_today() > current_time.read_from_file():
            database.refresh_check()
            current_time.write_to_file()
        else:
            while current_user_id is None:
                current_user = prompt_user_login()
                current_user_id = current_user[0][1]
            if current_user_id == 1:
                USER_CHOICE = USER_CHOICE_ADMIN
            else:
                USER_CHOICE = USER_CHOICE_USER
            user_input = input(USER_CHOICE)
            while user_input != 'q':
                if user_input == 'a':
                    prompt_add_task()
                elif user_input == 'l':
                    prompt_list_tasks()
                elif user_input == 'r':
                    prompt_check_task()
                elif user_input == 'd':
                    prompt_delete_task()
                elif user_input == 'u':
                    prompt_list_users()
                elif user_input == 'p':
                    prompt_user_amount()
                elif user_input == 'n':
                    prompt_add_user()
                elif user_input == 'rt':
                    prompt_refresh_check()
                elif user_input == 'ai':
                    prompt_add_shop()
                elif user_input == 'di':
                    prompt_delete_shop()
                elif user_input == 'li':
                    prompt_list_all_shop()
                elif user_input == 'b':
                    prompt_buy_item()
                elif user_input == 'terminate':
                    raise SystemExit(0)
                user_input = input(USER_CHOICE)
            current_user_id = None
            cls()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt_user_login():
    welcome = "Wrong Username Or Password!"
    while welcome == "Wrong Username Or Password!":
        username = input('Enter Your Username: ')

        password = getpass('Enter Your Password: ')
        welcome = f"Welcome, {username}" if database.user_login(username, password) else "Wrong Username Or Password!"
        print(welcome)
    return database.user_login(username, password)


def prompt_add_task():
    task = input("Enter Task Name: ")
    points = input("Enter Amount of Points: ")
    database.add_task(task, points)


def prompt_list_users():
    for user in database.list_users():
        print(user['id'], user['username'], user['amount'])


def prompt_add_user():
    username = input("Enter New Username: ")
    password = input("Enter New Password: ")
    database.add_account(username, password)


def prompt_user_amount():
    database.list_users()
    user_id = input("Enter User ID: ")
    points_amount = input("Enter Amount of Points: ")
    database.update_amount(user_id, points_amount)


def prompt_list_tasks():
    for task in database.get_all_tasks():
        check = database.get_user(task['checked']) if task['checked'] else "None"
        print(task['id'], task['task'], task['points'], check)


def prompt_refresh_check():
    database.refresh_check()


def prompt_check_task():
    id_t = input("Type in Task ID that you want to Check Out: ")
    points = database.get_task(id_t)  # need to check if task already checked out.
    if points[0][1]:
        print("Sorry, this task is already checked out.")
    else:
        database.check_task(id_t, current_user_id, points[0][0])


def prompt_delete_task():
    id_t = input("Type in Task ID that you want to delete: ")
    database.delete_task(id_t)


def prompt_add_shop():
    item = input("Type in Item Name: ")
    price = int(input("Type in Item price: "))
    database.add_shop(item, price)


def prompt_delete_shop():
    id_i = input("Enter Item ID to Delete it: ")
    database.delete_shop(id_i)


def prompt_list_all_shop():
    for shop in database.list_shop():
        print(shop['id'], shop['item'], shop['price'])


def prompt_buy_item():
    id_i = int(input("Type in Item ID to buy it: "))
    database.buy_item(id_i, current_user_id)


cls()
menu()
