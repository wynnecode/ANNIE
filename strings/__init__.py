#
# Copyright (C) 2024 by Moonshining6@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/Moonshining6/ANNIE-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/Moonshining6/ANNIE-MUSIC/blob/master/LICENSE >
#
# All rights reserved

import os
import sys
from typing import List

import yaml

languages = {}
commands = {}

languages_present = {}


def get_command(value: str) -> List:
    return commands["command"].get(value, [])


def get_string(lang: str):
    return languages.get(lang, languages.get("en", {}))


# Load command files
for filename in os.listdir(r"./strings"):
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        try:
            with open(r"./strings/" + filename, encoding="utf8") as file:
                commands[language_name] = yaml.safe_load(file) or {}
        except Exception as e:
            print(f"Error loading command file '{filename}': {e}")
            sys.exit()

# Load language files
for filename in os.listdir(r"./strings/langs/"):
    if "en" not in languages:
        try:
            with open(r"./strings/langs/en.yml", encoding="utf8") as file:
                languages["en"] = yaml.safe_load(file) or {}
                languages_present["en"] = languages["en"].get("name", "English")
        except Exception as e:
            print(f"Error loading default language file 'en.yml': {e}")
            sys.exit()

    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        try:
            with open(r"./strings/langs/" + filename, encoding="utf8") as file:
                languages[language_name] = yaml.safe_load(file) or {}

            # Fill missing keys from "en"
            for item in languages["en"]:
                if item not in languages[language_name]:
                    languages[language_name][item] = languages["en"][item]

            languages_present[language_name] = languages[language_name].get(
                "name", f"Unknown ({language_name})"
            )
        except Exception as e:
            print(f"Error loading language file '{filename}': {e}")
            sys.exit()

# Final validation
if "en" not in languages:
    print("Error: Default 'en' language file is missing or invalid.")
    sys.exit()
