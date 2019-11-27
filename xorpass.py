#!/usr/bin/python3

try:
    import argparse
    import string
    import random
    import re
    from colorama import Fore
    from builtins import ImportError

except ImportError:
    print ("\
    Error: Install required libraries\n\
           pip3 install argparse string random re colorama builtins")
    exit()


def banner():
    print ("\n" +
           Fore.WHITE + "            |-------____                                                                       \n" +
           Fore.WHITE + "        |   |           \___           __  _____  ____                                         \n" +
           Fore.WHITE + "   ---------|               \          \ \/ / _ \|  _ \ "  + Fore.RED + "_ __   __ _ ___ ___   \n" +
           Fore.WHITE + "        |   |                \_______   \  / | | | |_) "   + Fore.RED + "| '_ \ / _` / __/ __| \n" +
           Fore.WHITE + "        |   |                /          /  \ |_| |  _ <"   + Fore.RED + "| |_) | (_| \__ \__ \ \n" +
           Fore.WHITE + "   ---------|            ___/          /_/\_\___/|_| \_\ " + Fore.RED + ".__/ \__,_|___/___/   \n" +
           Fore.WHITE + "        |   |       ____/                              "   + Fore.RED + "|_|                   \n" +
           Fore.WHITE + "            |-------                                          @devploit                        \n" )


class XORpass():
    DEFAULT_CHARSET = string.ascii_letters + string.digits
    SEPARATORS = '()[]{}:;+-/ "'  # type: Any

    def _calc_xor_char(self, payload_char, charset=DEFAULT_CHARSET, randomize=True):
        for first_char in (charset if not randomize else "".join(random.sample(charset, len(charset)))):
            for second_char in (charset if not randomize else "".join(random.sample(charset, len(charset)))):
                third_char = chr(ord(first_char) ^ ord(second_char) ^ ord(payload_char))
                if third_char != payload_char and third_char in charset:
                    return [first_char, second_char, third_char]
        raise Exception("Charset not valid for this payload. char=%c charset=%s" % (payload_char, charset))

    def _calc_xor_string(self, payload, charset=DEFAULT_CHARSET, randomize=True):
        if payload[0] == '"':
            payload = payload[1:-1]
        result = ["", "", ""]
        for c in payload:
            xored_chars = self._calc_xor_char(c, charset=charset, randomize=randomize)
            for i in range(3):
                result[i] += xored_chars[i]

        return result

    def encode(self, payload, charset=DEFAULT_CHARSET, randomize=True, badchars=""):
        charset = "".join([x if x not in badchars else "" for x in charset])

        payload_array = re.split(r'(\"[\w\- ]+\")|([\w\.]+)', payload)
        result = ""
        for word in payload_array:
            if word == None: continue
            if word == "" or word in self.SEPARATORS:
                result += word
                continue

            xored_words = self._calc_xor_string(word, charset=charset, randomize=randomize)
            xored_words = ['"' + x + '"' for x in xored_words]

            result += "(" + "^".join(xored_words) + ")"

        while True:
            match = re.search(r'(\(\([\^\w\"]+)\)\)', result)
            if not match: break
            result = result.replace(match.group(0), match.group(0)[1:-1])
        return result

    def _decode_string(self, payload_string):
        parts = payload_string.split("^")
        parts = [p.strip('"') for p in parts]

        result = ""
        for a, b, c in zip(*parts):
            result += chr(ord(a) ^ ord(b) ^ ord(c))

        if 1 in [c in self.SEPARATORS for c in result]:
            result = '"' + result + '"'
        return result

    def decode(self, payload):
        parts = re.split(r'([\^\w\"]+)', payload)
        result = ""
        for p in parts:
            if "^" in p:
                result += self._decode_string(p)
            else:
                result += p
        return result


def main():
    banner()
    parser = argparse.ArgumentParser(description="Encoder to bypass WAF filters using XOR operations.")
    grouped = parser.add_mutually_exclusive_group(required=True)
    grouped.add_argument("--encode", "-e", help="Encode the payload")
    grouped.add_argument("--decode", "-d", help="Decode the payload")
    parser.add_argument("--number", "-n", default=1, type=int, help="Number of encoded results")
    groupcb = parser.add_mutually_exclusive_group()
    groupcb.add_argument("--charset", "-c", default=string.ascii_letters + string.digits,
                         help="Select specific charset for encoding")
    groupcb.add_argument("--badchars", "-b", default="", help="Select specific badchars for encoding")

    args = parser.parse_args()

    if args.encode is not None:
        print(Fore.CYAN + "[" + Fore.WHITE + "+" + Fore.CYAN + "] Charset: " + Fore.WHITE + str(args.charset))
        print(Fore.YELLOW + "[" + Fore.WHITE + "-" + Fore.YELLOW + "] Badchars: " + Fore.WHITE + str(args.badchars))
        print(Fore.BLUE + "[" + Fore.WHITE + "*" + Fore.BLUE + "] Payload: " + Fore.WHITE + str(args.encode))
        try:
            for _ in range(args.number):
                result = XORpass().encode(args.encode, charset=args.charset, badchars=args.badchars)
                print(Fore.GREEN + "[" + Fore.WHITE + "#" + Fore.GREEN + "] Encoded Payload: " + Fore.WHITE + result)
        except Exception as ex:
            print("Error encoding the payload: ", ex)

    if args.decode is not None:
        print(Fore.BLUE + "[" + Fore.WHITE + "*" + Fore.BLUE + "] Encoded Payload: " + Fore.WHITE + str(args.decode))
        result = XORpass().decode(args.decode)
        print(Fore.GREEN + "[" + Fore.WHITE + "#" + Fore.GREEN + "] Decoded Payload: " + Fore.WHITE + result)


if __name__ == "__main__":
    main()
