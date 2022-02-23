import sys
import requests
import time
import os
import ipaddress

APIkey = "5ad37f25a4d94b288df60921e1524f02" # Defines the API key to be used. Only change if the requests are no longer working.

try:
    datafile = sys.argv[1]

except IndexError:
    print(f"Usage: {sys.argv[0]} <iplist.txt>")
    sys.exit()

class colors:
    LIGHTPURPLE = '\033[1;35m'
    LIGHTGREEN = "\033[1;32m"
    LIGHTRED = "\033[1;31m"
    LIGHTCYAN = "\033[1;36m"
    LIGHTWHITE = "\033[1;37m"
    LIGHTYELLOW = "\x1b[93m"

with open(datafile ,"r") as data:
    database = data.read().splitlines()
    file = []
    sort = []
    count = 0
    database.reverse()

    for i in database:
        count = count + 1

    print("Searching [{}] IP's for torrent activity".format(count))

    for line in database:
        line = line.split()
        line.reverse()
        ip = line[0]
        del line[0]
        line.reverse()

        def string(line):
            convstring = " "
            return (convstring.join(line))

        name = string(line)

        test = "{} {}".format(ip, name)

        if test in file:
            pass
        else:
            toappend = "{} {}".format(ip, name)
            file.append(toappend)

    count = 0

    for counting in file:
        count = count + 1

    print("{}Checking for activity on {}{}{} IP's\n".format(colors.LIGHTPURPLE, colors.LIGHTYELLOW, count, colors.LIGHTWHITE))

    left = 0
    cnt = 1

    for IP in file:
        try:
            if left == 50:
                left = 0
                print(f"\n{colors.LIGHTYELLOW}{count} {colors.LIGHTWHITE}Left\n")

            IP = IP.split()
            ip = IP[0]
            del IP[0]

            def string(IP):
                convstring = " "
                return (convstring.join(IP))

            name = string(IP)

            r = requests.get("https://api.antitor.com/history/peer/?ip="+ ip +"&key={}".format(APIkey))
            res = r.json()

            try:
                country = res['geoData']['country']
            except KeyError:
                country = ""
            try:
                city = res['geoData']['city']
            except KeyError:
                city = ""
            try:
                isp = res['isp']
            except:
                isp = "Non Defined ISP"

            checkporn = res['hasPorno']
            checkbadporn = res['hasChildPorno']

            if len(res['contents']) > 0:
                lenght = len(res['contents'])

                if checkporn == True:
                    print("{}[ACTIVITY DETECTED] {}{} - [{}]{} has as a activity lenght of {}{}{} [Watches LEGAL PORN]{} | [{}({})] - {}[{}]{}".format(colors.LIGHTGREEN, colors.LIGHTWHITE, ip, name, colors.LIGHTCYAN, colors.LIGHTWHITE, len(res['contents']),colors.LIGHTRED, colors.LIGHTWHITE, country, city, colors.LIGHTPURPLE, isp, colors.LIGHTWHITE))
                    add = f"[{cnt}][{len(res['contents'])}][ACTIVITY SORTING({lenght})] [{ip}] - [{name}] [!LP] | [{country}({city})] - [{isp}]"
                    cnt = cnt + 1

                elif checkbadporn == True:
                    print("{}[ACTIVITY DETECTED] {}{} - [{}]{} has as a activity lenght of {}{}{} [Watches ILLEGAL PORN]{} | [{}({})] - {}[{}]{}".format(colors.LIGHTGREEN, colors.LIGHTWHITE, ip, name, colors.LIGHTCYAN, colors.LIGHTWHITE, len(res['contents']),colors.LIGHTRED, colors.LIGHTWHITE, country, city, colors.LIGHTPURPLE, isp, colors.LIGHTWHITE))
                    add = f"[{cnt}][{len(res['contents'])}][ACTIVITY SORTING({lenght})] [{ip}] - [{name}] [!IP] | [{country}({city})] - [{isp}]"
                    cnt = cnt + 1

                elif checkporn == True and checkbadporn == True:
                    print("{}[ACTIVITY DETECTED] {}{} - [{}]{} has as a activity lenght of {}{}{} [Watches PORN & ILLEGAL PORN]{} | [{}({})] - {}[{}]{}".format(colors.LIGHTGREEN, colors.LIGHTWHITE, ip, name, colors.LIGHTCYAN, colors.LIGHTWHITE, len(res['contents']),colors.LIGHTRED, colors.LIGHTWHITE, country, city, colors.LIGHTPURPLE, isp, colors.LIGHTWHITE))
                    add = f"[{cnt}][{len(res['contents'])}][ACTIVITY SORTING({lenght})] [{ip}] - [{name}] [!LP&!IP] | [{country}({city})] - [{isp}]"
                    cnt = cnt + 1

                else:
                    print("{}[ACTIVITY DETECTED] {}{} - [{}]{} has as a activity lenght of {}{}{} | [{}({})] - {}[{}]{}".format(colors.LIGHTGREEN, colors.LIGHTWHITE, ip, name, colors.LIGHTCYAN, colors.LIGHTWHITE, len(res['contents']), colors.LIGHTWHITE, country, city, colors.LIGHTPURPLE, isp, colors.LIGHTWHITE))
                    add = f"[{cnt}][{len(res['contents'])}][ACTIVITY SORTING({lenght})] [{ip}] - [{name}] | [{country}({city})] - [{isp}]"
                    cnt = cnt + 1

                sort.append(add)

            else:
                print(f"{colors.LIGHTRED}[NO ACTIVITY] {colors.LIGHTWHITE}{ip} - [{name}] | [{country}({city})] - {colors.LIGHTPURPLE}[{isp}]{colors.LIGHTWHITE}")

            count = count - 1
            left = left + 1

        except TypeError:
            pass

        except KeyError:
            pass

    print("\n\n")

    for results in sort:
        if "[!LP]" in results:
            color = colors.LIGHTYELLOW
        elif "[!IP]" in results:
            color = colors.LIGHTRED
        elif "[!LP&!IP]" in results:
            color = colors.LIGHTRED
        else:
            color = colors.LIGHTCYAN

        print("{}{}{}".format(color,results,colors.LIGHTWHITE))
