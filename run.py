#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from math import trunc
from time import sleep, time

try:
    import requests
    import json
except ImportError or NameError:
    os.system("python -m pip install --upgrade pip")
    os.system("pip install requests json")
    print("retry!")

#########################################
# ==========  CONFIGURATION  ========== #
DIR = ".server"
MEMORY = 4
PORT = 25565
JAVA_PATH = "java"  # java bin path
DEBUG_PORT = 5005  # ref: https://www.spigotmc.org/wiki/intellij-debug-your-plugin/
DEFAULT_PLUGINS = [
    ""
]
JVM_ARGS = [
    # ref: https://www.spigotmc.org/wiki/intellij-debug-your-plugin/
    "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005",
]
JAR_ARGS = [
    "--nogui"
]
AUTO_START = True
# ==========   STATIC INFO   ========== #
SERVER_JAR_NAME = "paper-server.jar"
SERVER_PATH = os.path.join(f"./{DIR}")
PROPERTIES_AUTO_DOWNLOAD = False
SERVER_JAR_PATH = os.path.abspath(os.path.join(f"./{DIR}", SERVER_JAR_NAME))
SERVER_EULA_PATH = os.path.abspath(os.path.join(f"./{DIR}", "eula.txt"))
SERVER_PROPERTIES_PATH = os.path.abspath(
    os.path.join(f"./{DIR}", "server.properties"))
SERVER_PLUGIN_PATH = os.path.abspath(
    os.path.join(f"./{DIR}/plugins", SERVER_JAR_NAME))
ALLOW_OVER_RESTART = False
# DEFAULT_PLUGINS = True
# ==========   TO DO LI ST   ========== #
# JVM auto install and using as JAVA_PATH
# Default Plugins
# VERY CUTTY KAWAII CAT
# ==========  KNOWN  ISSUES  ========== #
# WE DON'T HAVE CAT
#########################################


files_for_location_check = ["build.gradle", "build.gradle.kts"]
check_count = 0
found = False

for f in files_for_location_check:
    if found:
        break
    # file found
    if f in os.listdir("./"):
        found = True
    # file not found
    else:
        check_count = check_count + 1
        if check_count == len(files_for_location_check):
            exit(
                f"!! The script should be run from the same location as {files_for_location_check}")
        pass

print("^----------[ READY SERVER ]----------^")
# check server dir
if not os.path.exists(DIR):
    os.mkdir(f"./{DIR}")
    print(f"Server directory ({DIR}) not found - generate")
else:
    print(f"Server directory ({DIR}) found - pass")

# check jar
if SERVER_JAR_NAME not in os.listdir(f"./{DIR}"):
    paper_version_res = requests.get(
        "https://api.papermc.io/v2/projects/paper/versions/1.20.1/")

    # paper sad
    if paper_version_res.status_code != 200:
        exit("Can't fetch paper build, Please install manually")

    # paper happy
    else:
        paper_build = json.loads(paper_version_res.content)['builds'][-1]
        print(f"Paper Version: {paper_build}")

        print("Downloading...")

        with open(SERVER_JAR_PATH, "wb") as file:
            res = requests.get(
                f"https://api.papermc.io/v2/projects/paper/versions/1.20.1/builds/{paper_build}/downloads/paper-1.20.1-{paper_build}.jar")
            file.write(res.content)

        print("Complete!")

# server jar check again
if SERVER_JAR_NAME in os.listdir(f"./{DIR}"):
    print("Paper found")

# eula check
if "eula.txt" not in os.listdir(f"./{DIR}"):
    try:
        with open(SERVER_EULA_PATH, "r") as file:
            file.readlines()
    except FileNotFoundError:
        with open(SERVER_EULA_PATH, "w"):
            pass

if "eula.txt" in os.listdir(f"./{DIR}"):
    with open(SERVER_EULA_PATH, "r") as file:
        eula_txt = "".join(file.readlines()).split("\n")

        if "eula=true" in eula_txt:
            print("eula=true - pass")
        else:
            yes_words = ["yes", "y", "yeah", "agree", "ye", "ok", "sure", "si", "sp", "네", "넹", "I agree", "true", "okay"]

            print("^----------[ EULA SECTION ]----------^")

            if not input("Do you agree with Mojang's Eula? : ") in yes_words:
                exit("If you do not agree to Mojang's Eula, can't start the server. :)")
            else:
                with open(SERVER_EULA_PATH, "w") as eula:
                    eula.write("eula=true")
                print("Eula Agreed. Starting Server...")

# properties
if "server.properties" not in os.listdir(f"./{DIR}"):
    if not PROPERTIES_AUTO_DOWNLOAD:
        pass
    with open(SERVER_PROPERTIES_PATH, "w") as file:
        properties = requests.get("https://server.properties/")
        if properties.status_code != 200:
            print(
                "Couldn't find server.properties, tried to download it but failed. Run by default.")
            pass
        file.write(properties.content.decode('utf-8'))

        print("server.properties not found. - generated")


# start fun
def start():
    return os.system(
        f"cd {SERVER_PATH} && "
        + f"\"{JAVA_PATH}\" -Xms{MEMORY}G -Xmx{MEMORY}G "
        + " ".join(JVM_ARGS)
        + f" -jar {SERVER_JAR_PATH} "
        + " ".join(JAR_ARGS)
    )


# ^----------[ START ]----------^ #
if not AUTO_START:
    exit(f"Server Stopped. ({start()})")
else:
    stack = 0
    while AUTO_START:
        sleep(2)
        stack = stack + 1
        last_time = trunc(time())
        print(f"PMC :: Starting Server.. - [Stack: {stack}]")
        code = start()
        print(f"PMC :: Server Stopped. [Code: {code}]")
        if code != 0:
            exit("Exit code is not \'0\'. - exit")
        elif (last_time + 5) > trunc(time()):
            if ALLOW_OVER_RESTART:
                pass
            else:
                exit("The server restarts too quickly. - exit")