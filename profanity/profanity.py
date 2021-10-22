import re
import json

from profanity import __path__

with open(f"{__path__[0]}/profanity.json", "r") as f:
    profanity = json.load(f)

with open(f"{__path__[0]}/english_words.txt", "r") as f:
    english_words = [x for x in f.read().split("\n") if len(x) > 0]

def get_profanity(strin : str, convert_lookalikes:bool=False) -> bool:
    """ returns a list of words where profanity was detected """
    # `strin` does not change, but `msg` does
    msg = strin.lower()
    profanity_detected = []

    # eliminate clean strings
    for cleanstring in profanity["cleanstrings"]:
        while cleanstring in msg:
            idx = msg.index(cleanstring)
            msg = msg[:idx] + msg[idx + len(cleanstring):]

    # print(f"{msg=}")

    # convert lookalikes to ascii letters (! -> i, 0 -> o, etc)
    if convert_lookalikes:
        for i in range(0, len(msg)):
            # check for lookalikes up to ten characters long
            for k in range(1,10):
                if msg[i:i+k] in profanity["lookalikes"]:
                    msg = msg.replace(msg[i:i+k], profanity["lookalikes"][msg[i:i+k]])

    # print(f"{msg=}")

    # check for priority profanity
    profanity_detected = [w for w in profanity["priority"] if w in msg]
    if len(profanity_detected) > 0:
        return (True, profanity_detected)

    # print(f"{msg=}")

    # if the string has been reduced to nothing its obviously not profane
    if msg == "":
        return (False, [])

    # parse words as continuous strings of letters and everything else separately
    message_words= []
    letters = "abcdefghijklmnopqrstuvwxyz"
    current_word = ""
    on_letter = msg[0] in letters
    for char in msg:
        if char not in letters and on_letter == True:
            on_letter = False
            if current_word != "":
                message_words.append(current_word)
            current_word = char
        elif char in letters and on_letter == False:
            on_letter = True
            if current_word != "":
                message_words.append(current_word)
            current_word = char
        else:
            current_word += char
    if current_word != "":
        message_words.append(current_word)

    # print(f"{message_words=}")

    # throw out known english words
    # beautiful list comprehension but doesnt do quite enough: msg = "".join([w for w in message_words if w not in english_words])
    nonenglish_sections = []
    current_section = ""
    for item in message_words:
        if item in english_words:
            if current_section != "":
                nonenglish_sections.append(current_section)
                current_section = ""
                continue
        else:
            current_section += item
    if current_section != "":
        nonenglish_sections.append(current_section)

    # print(f"{nonenglish_sections=}")

    # check for normal profanity using char patterns rather than exact strings
    for nes in nonenglish_sections:
        if nes == " ":
            continue
        for cuss in profanity["normal"]["en-us"]:
            cuss_idx = 0 # indicates the character in the cuss we're currently looking for
            for char in nes:
                # if we're looking for the last character and we've found it, break.
                if cuss_idx == len(cuss) - 1 and char == cuss[len(cuss) - 1]:
                    profanity_detected.append(cuss)
                    break
                # if we're looking for the first character and we've found it, start.
                if char == cuss[0] and cuss_idx == 0:
                    cuss_idx += 1
                    continue
                # if we haven't started (cuss_idx still 0), continue
                if not cuss_idx > 0:
                    continue
                # if we are looking for a character in the middle and we find it, increment cuss_idx
                if cuss_idx > 0 and char == cuss[cuss_idx]:
                    cuss_idx += 1
                # else if its not in letters or its a repeat of the current letter in the cuss, continue
                elif char not in letters or char == cuss[cuss_idx-1]:
                    continue
                # else if its a letter but not what we're on or looking for, reset.
                elif char in letters and cuss_idx > 0 and char != cuss[cuss_idx - 1]:
                    cuss_idx = 0

    # print(f"finally: {profanity_detected=}")

    # if we didnt convert lookalikes this time, then we should
    # union our current list with the list where we DO convert lookalikes
    if not convert_lookalikes:
        return list(set(profanity_detected).union(set(get_profanity(strin, convert_lookalikes=True))))
    else:
        return profanity_detected

def contains_profanity(msg : str) -> bool:
    return len(get_profanity(msg)) > 0

# taken from https://www.geeksforgeeks.org/python-check-url-string/
def get_links(arg):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    links = re.findall(regex,arg)
    return [x[0] for x in links]

def remove_links(arg):
    links = get_links(arg)
    while(len(links) > 0):
        while(links[0] in arg):
            arg = arg.replace(links[0], "")
        links.remove(links[0])

    return arg

