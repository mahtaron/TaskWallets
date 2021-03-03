from datetime import date

time_file = "time"


def write_to_file():
    with open(time_file, "w") as file:
        file.write(day_today())

def read_from_file():
    with open(time_file, "r") as file:
        last_time = file.read()
    return last_time

def day_today():
    return str(date.today().strftime("%Y%m%d"))