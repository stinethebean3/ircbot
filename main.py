from socket import socket, AF_INET, SOCK_STREAM
import requests

server = "irc.freenode.net"
channel = "#testbot"
nick = "weather6"
name = "Weather Bot"
port = 6667

irc = socket(AF_INET, SOCK_STREAM)
print("connecting to: %s" % server)

irc.connect((server, port))
print("connected")

message="USER %s %s %s %s \n\r" % (nick, "0", "*", name)
irc.send(message.encode('utf-8'))
print("sent user")

message="NICK %s \n\r" % nick
irc.send(message.encode('utf-8'))
print("sent nick") 

message="JOIN %s \n\r" % channel
irc.send(message.encode('utf-8'))
print("joined channel") 

while 1:
    text = irc.recv(2040).decode('utf-8')
    print(text)

    if text.find("PING") != -1:
        message="PONG %s \n\r" % text.split()[1] 
        irc.send(message.encode('utf-8')) 

    if text.find("PRIVMSG #testbot :!weather") != -1:
        location=text.split()[4]
        query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='%s') and u='f'" % location
        print(query)
        response=requests.get("http://query.yahooapis.com/v1/public/yql?q=%s&format=json" % query)
        data = response.json()["query"]["results"]["channel"]["item"]
        intro = data["title"]
        temp_f = data["condition"]["temp"]
        temp_c = round((int(temp_f) - 32) * 5.0/9.0)
        condition = data["condition"]["text"]
        message="PRIVMSG #testbot :%s: %sF/%sC %s \n\r" % (intro, temp_f, temp_c, condition)
        irc.send(message.encode('utf-8'))

