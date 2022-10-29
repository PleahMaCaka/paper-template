#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import trunc
import os
from time import sleep, time

try:
    import requests
    import json
except ImportError:
    os.system("pip install requests json")
    print("retry!")

#####################################
##########  Configrations  ##########
DIR = ".server"
MEMORY = 4
PORT = 25565
JAVA_PATH = "java" # java bin path
DEBUG_PORT = 5005 # ref: https://www.spigotmc.org/wiki/intellij-debug-your-plugin/
# DEFAULT_PLUGINS=[
#     "",
#     TODO make this
# ]
JVM_ARGS = [
    # "add here"
]
JAR_ARGS = [
    # "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005", # ref: https://www.spigotmc.org/wiki/intellij-debug-your-plugin/
    "--nogui" # '--nogui' and 'nogui' both work
    # "add here"
]
AUTO_START = True
##########   STATIC INFO   ##########
SERVER_JAR_NAME="paper-server.jar"
SERVER_PATH = os.path.join(f"./{DIR}")
SERVER_JAR_PATH = os.path.abspath(os.path.join(f"./{DIR}", SERVER_JAR_NAME))
SERVER_EULA_PATH = os.path.abspath(os.path.join(f"./{DIR}", "eula.txt"))
SERVER_PLUGIN_PATH = os.path.abspath(os.path.join(f"./{DIR}/plugins", SERVER_JAR_NAME))
ALLOW_OVER_RESTART = False
##########    TODO LIST    ##########
# JVM AutoInstall and using as JAVA_PATH
# VERY CUTTY KAWAII CAT
#####################################


files_for_location_check = ["build.gradle", "build.gradle.kts"]
check_count = 0
found = False

for f in files_for_location_check:
    if found: break
    # file found
    if f in os.listdir("./"):
        found = True
    # file not found
    else:
        check_count = check_count + 1
        if check_count == len(files_for_location_check):
            exit(f"!! The script should be run from the same location as {files_for_location_check}")
        pass
        

print("^----------[ READY SERVER ]----------^")
# check server dir
if not os.path.exists(DIR):
    os.mkdir("./.server")
    print(f"Server DIR ({DIR}) not found - create")
else:
    print(f"Server DIR ({DIR}) found - pass")

# check jar
if not SERVER_JAR_NAME in os.listdir(f"./{DIR}"):
    # request paper version info
    paper_version_res = requests.get("https://api.papermc.io/v2/projects/paper/versions/1.19.2/")

    # paper sad
    if paper_version_res.status_code != 200:
        exit("Can't fetch paper build, Please install manually")

    # paper happy
    else:
        paper_build = json.loads(paper_version_res.content)['builds'][-1]
        print(f"Paper Version: {paper_build}")

        print("Donwloading...")

        with open(SERVER_JAR_PATH, "wb") as file:
            res = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/1.19.2/builds/{paper_build}/downloads/paper-1.19.2-{paper_build}.jar")
            file.write(res.content)
            file.close()

        print("Complete!")

# server jar check again
if SERVER_JAR_NAME in os.listdir(f"./{DIR}"):
    print("Paper found - pass")


# eula check
if "eula.txt" in os.listdir(f"./{DIR}"):
    with open(SERVER_EULA_PATH, "r") as file:
        eula_txt = "".join(file.readlines()).split("\n")
        if "eula=true" in eula_txt:
            print("eula=true - pass")
            pass
        else:
            yes_words = ["yes", "y", "yeah", "agree", "ye", "ok", "sure"]

            print("^==========[EULA SECTION]==========^")
            eula_agree = input("Do you agree with Mojang's Eula? : ")

            if not eula_agree in yes_words:
                exit("If you do not agree to Mojang's Eula, you cannot start the server. :)")
            
            with open(SERVER_EULA_PATH, "w") as eula:
                eula.write("eula=true")

            print("Eula Agreed. Starting Server...")

# flattening args
jvm_custom_args = ""
for s in JVM_ARGS:
    jvm_custom_args += s + ""
jvm_custom_args += " "

jar_custom_args = ""
for s in JAR_ARGS:
    jar_custom_args += s + ""
jar_custom_args += " "


def start():
    return os.system(
        f"cd {SERVER_PATH} && "
        + f"{JAVA_PATH} -Xms{MEMORY}G -Xmx{MEMORY}G "
        + jvm_custom_args
        + f"-jar {SERVER_JAR_PATH} "
        + jar_custom_args
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
            if ALLOW_OVER_RESTART: pass
            else: exit("The server restarts too quickly. - exit")
