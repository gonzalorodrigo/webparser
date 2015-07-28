#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import smtplib
import datetime


# This a simple program to test my Python learning
# the idea is to check a certain blocket site and detect new flats
# To make this work: modify the email server info down.


def getRelevantArea(url, startingString, endString):
    intoIt = 0
    outCad = ""

    for line in getUrlContent(url):
        line = line.strip()
        if not intoIt and startingString in line:
            intoIt = 1
            pos = line.find(startingString)

            line = line[pos:]
            # print line

        if intoIt and endString in line:
            if outCad == "":
                outCad = line
            intoIt = 0
            return outCad.strip()
        if intoIt:
            outCad = outCad + line


def getUrlContent(url):
    return urllib2.urlopen(url)


def getText(old):
    theText = ""
    try:
        f = open(old, "r")
        theText = f.read()
        f.close()
    except:
        print "Old File doesn't exist"
    return theText


def dumpFile(file, text):
    try:
        f = open(file, "w")
        #   print "va a escribir"
        f.write(text)
        f.close()
    except:
        print "Can't create file"


def compareTexts(old, new):
    return old == new


def sendEmail(toAdd, fromAdd, text):
    server = smtplib.SMTP()
    server.connect("smtp.server.somewhere")
    server.starttls()
    server.login("mail@server.somewhere", "password")
    server.sendmail(fromAdd, toAdd, text)
    server.quit()


def notify(toAdd, fromAdd, theUrl, specific):
    subj = "New Stuff at site: " + specific
    text = ("New Stuff at site\nGo to " + theUrl + "\n\nAutomatic generated! \n"
            "Mailer")
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    text = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (fromAdd, toAdd,
                                                              subj, date, text)
    sendEmail(toAdd, fromAdd, text)


def multiNotify(emailToBeNotified, emailFrom, url, specificString):
    for email in emailToBeNotified:
        notify(email, emailFrom, url, specificString)


def checkSite(url, startHtml, stopHtml, lastReadFile, emailToBeNotified,
              emailFrom, specificString):
    print "Checking: " + specificString
    newHtml = getRelevantArea(url, startHtml, stopHtml)
    # print newHtml
    oldHtml = getText(lastReadFile)

    if compareTexts(oldHtml, newHtml):
        print specificString + ": No changes in HTML"
    else:
        print specificString + ": Changes on HTML, Sending Email"
        multiNotify(emailToBeNotified, emailFrom, url, specificString)

    dumpFile(lastReadFile, newHtml)


emailToBeNotified = ["someone@somwwhere"]
emailToBeNotifiedV2 = ["someone@somwwhere"]
emailToBeNotifiedV3 = ["someone@somwwhere"]

emailFrom = "info@onworld.es"


# Blocket site for pianos
# checkSite("http://www.blocket.se/vasterbotten?q=piano&cg=6160&w=1&st=s&c=0&ca=2&is=1&l=0&md=th",
#          "item_list",
#          "<div class",
#          "/tmp/Blocket-Piano.xml",
#          emailToBeNotifiedV2,
#          emailFrom,
#          "Piano-Search")

# blocket Site for Sofas
# checkSite("http://www.blocket.se/vasterbotten?q=b%E4ddsoffa&cg=0&w=1&st=s&ca=2&is=1&l=0&md=th",
#          "item_list",
#          "<div class",
#          "/tmp/Blocket-Sofa.xml",
#          emailToBeNotifiedV3,
#          emailFrom,
#          "BedSofa-Search")

# checkSite("http://www.blocket.se/vasterbotten?q=l%F6pband&cg=0&w=1&st=s&ca=2&is=1&l=0&md=th",
#          "item_list",
#          "<div class",
#          "/tmp/Blocket-Lopband.xml",
#          emailToBeNotifiedV2,
#          emailFrom,
#          "Lopband-Search")

# checkSite("http://www.blocket.se/vasterbotten?q=Honda+sn%F6slunga&cg=0&w=3&st=s&ca=2&is=1&l=0&md=th",
#          "item_list",
#          "<div class",
#          "/tmp/Blocket-Honda.xml",
#          emailToBeNotifiedV2,
#          emailFrom,
#          "Honda Snoslunga-Search")

# checkSite("http://www.blocket.se/hela_sverige?q=Honda+sn%F6slungor&cg=0&w=3&st=s&ca=2&is=1&l=0&md=th",
#          "item_list",
#          "<div class",
#          "/tmp/Blocket-Honda2.xml",
#          emailToBeNotifiedV2,
#          emailFrom,
#          "Honda Snoslungor-Search")
# BLocket Site

# for Flats
checkSite("http://www.blocket.se/vasterbotten/lagenheter?ca=2&w=1&cg=3020&st=u&m=25&f=a&l=0&md=th",
          "<div itemscope",
          "<div class=",
          "/tmp/BlocketLast.xml",
          emailToBeNotified, emailFrom,
          "Flats on Blocket")


# Lerstenen Site
# checkSite("http://www.lerstenen.se/index.asp?page=61",
#          "<BODY",
#          "</body>",
#          "/tmp/LerstenenLast.xml",
#          emailToBeNotified,emailFrom,
#          "Lerstenen")


# kvalstar Site
# checkSite("http://kvalster.se/Umea",
#          "Init",
#          "</script>",
#          "/tmp/KvalsterLast.xml",
#          emailToBeNotified,emailFrom,
#          "Kvalster")
