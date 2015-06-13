import re
import unitydoc

#rename_command = re.compile("^!rename +(.+)$")
#valid_name = re.compile("^[A-Za-z_]+$")

def response(self, prefix, command, params, trailing):
    if command == 'PRIVMSG' and params == self.channel and trailing.startswith('!define'):
        self.send("PRIVMSG {} :{}".format(self.channel,
            "Okay, let me google that for you.. NOT!"))
    elif command == 'PRIVMSG' and params == self.channel and trailing.startswith('!save'):
        self.send("PRIVMSG {} :{}".format(self.channel,
            "Why not write it down yourself?"))
    elif command == 'PRIVMSG' and params == self.channel and trailing.startswith('!help'):
        self.send("PRIVMSG {} :{}".format(self.channel,
            "Did you really think I would help you? Bwahahahaahaaaa!"))
    elif command == 'PRIVMSG' and trailing.startswith('!unity'):
        if params == self.channel:
            recipient = self.channel
        else:
            recipient = prefix.split('!', 1)[0]
        if trailing.strip() == '!unity':
            self.send("PRIVMSG {} :{}".format(recipient,
                "http://docs.unity3d.com/ScriptReference/"))
        else:
            query = re.sub(r"^.unity ?", "", trailing)
            for score, title, page, summary in unitydoc.PerformSearch(query)[0:3]:
                self.send("PRIVMSG {} :{}".format(recipient,
                    "<http://docs.unity3d.com/ScriptReference/{}.html> {}".format(page, summary)))

#    elif command == 'PRIVMSG' and params == self.channel and trailing.startswith('!rename'):
#        match = rename_command.match(trailing)
#        if match and valid_name.match(trailing):
#            self.send("NICK {}".format(match.groups()[0]))
#        else:
#            self.send("PRIVMSG {} :{}".format(self.channel, "Not going to name myself like that!"))
    elif command == 'PRIVMSG' and params == self.channel and trailing.startswith('!'):
        self.send("PRIVMSG {} :{}".format(self.channel,
            "Ask for !help"))

def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]
