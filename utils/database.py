from .database_connection import DatabaseConnection

"""

Note: Comments

"""

tasks_file = 'tasks.db'


def create_task_table():
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS tasks(id integer primary key autoincrement, task text, points integer, checked integer)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS users(id integer primary key autoincrement, username text, password text, amount integer)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS shops(id integer primary key autoincrement, item text, price integer)')


def add_task(task, points):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()

        cursor.execute('INSERT INTO tasks (task, points, checked) VALUES (?, ?, 0)', (task, points))


def delete_task(id_t):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()

        cursor.execute('DELETE FROM tasks WHERE id = ?', (id_t,))


def check_task(id_t, id_u, points):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE tasks SET checked = ?  WHERE id = ?', (id_u, id_t))
        cursor.execute('UPDATE users SET amount = amount + ? WHERE id = ?', (points, id_u))


def get_user(id_u):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT username FROM users WHERE id = ?', (id_u,))
        username = cursor.fetchall()
        return username[0][0]


def get_task(id_t):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT points, checked FROM tasks WHERE id = ?', (id_t,))
        points = cursor.fetchall()
        return points


def refresh_check():
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE tasks SET checked = NULL')


def user_login(username, password):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT username, id FROM users WHERE username = ? and password = ?', (username, password))
        username = cursor.fetchall()
        return username


def add_account(username, password):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, password, amount) values (?, ?, 0)', (username, password))


def update_amount(id_u, amount):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET amount = ? WHERE id = ?', (amount, id_u))


def list_users():
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT id,username,amount FROM users')
        users = [{'id': row[0], 'username': row[1], 'amount': row[2]} for row in cursor.fetchall()]
        return users


def admin_account():
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()

        cursor.execute('INSERT INTO users (username, password, amount) values ("admin", "admin", 99)')


def get_all_tasks():
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM tasks')
        tasks = [{'id': row[0], 'task': row[1], 'points': row[2], 'checked': row[3]} for row in cursor.fetchall()]
        cursor.execute('DELETE FROM tasks')
        cursor.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "tasks"')
        for task in tasks:
            cursor.execute('INSERT INTO tasks (task, points, checked) VALUES (?, ?, ?)',
                           (task['task'], task['points'], task['checked']))
    return tasks


def list_shop():
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM shops')
        shops = [{'id': row[0], 'item': row[1], 'price': row[2]} for row in cursor.fetchall()]
        cursor.execute('DELETE FROM shops')
        cursor.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "shops"')
        for shop in shops:
            cursor.execute('INSERT INTO shops (item, price) VALUES (?, ?)', (shop['item'], shop['price']))
    return shops


def add_shop(item, price):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO shops (item, price) VALUES (?, ?)', (item, price))


def delete_shop(id_i):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM shops WHERE id = ?', (id_i,))

def get_shop(id_i):
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT item, price FROM shops WHERE id = ?', (id_i,))
        shop = cursor.fetchall()
        return shop


def buy_item(id_i, id_u):
    price = get_shop(id_i)[0][1]
    with DatabaseConnection(tasks_file) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET amount = amount - ? WHERE id = ?', (price, id_u))