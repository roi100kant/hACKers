import random
class QuestionBank:
    
    def __init__(self):
        self.questions = [("17 * 2 - 29 = ?", 5), ("(45 + 54) / 11 = ?", 9), ("(35 + 27 - 18) / 11 = ?", 4), ("2 + 3 = ?", 5),
                          ("(40 + 40) / 10 = ?", 8), ("1 + 2 + 5 - 6 = ?", 2), ("3! = ?", 6), ("(345 - 127 + 171 - 98) * 0 = ?", 0),
                          ("(72 - 2 - 10 - 20) / 10 = ?", 4), ("42 / 7 = ?", 6), ("0.5 * 0.5 * 4 = ?", 1), ("1 + 1 + 1 + 1 + 1 * 0 + 1 + 1 = ?", 6),
                          ("e^0 = ?", 1), ("ln(1) = ?", 0), ("ln(e) = ?", 1), ("ln(1/e) + 1 = ?", 0), ("f(x)=x^2, f'(2) = ?", 4),
                          ("f'(x)=2x, f(3) = ?", 9), ("2x + 3 = 7, x = ?", 2), ("7x - 6 = 8, x = ?", 2), ("2 * 3", 6),("e - (e - 2)", 2),
                          ("25 / 5 = ?", 5), ("how many legs 1 cats and 2 chickens have?", 8), ("5 + 5 - 1 = ?", 9), ("if Anny has 5 apples and John has only 3, how much is 1 + 1?", 2),
                          ("how many pants is a pair of pants", 1), ("3 * 3 / 3 * 3 / 3 * 3 / 3", 3), ("what chapter is the transport layer?", 3), 
                          ("what chapter is the network layer?", 4), ("what chapter is the link layer?", 5), ("what was the numebr of qyestions in the quiz?", 7),
                          ("9! / 8! = ?", 9), ("what number day is friday?", 6)
                         ]
    def getQ(self):
        return self.questions[random.randint(0, len(self.questions)-1)]

class Colors:
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    PURPLE = "\033[95m"
    YELLOW = "\033[93m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"


class GameStats:

    def __init__(self):
        self.playerScores = {}
        self.numberOcc = {"0" : 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0}

    def addPlayerPoint(self, name):
        name = name[:len(name)-1]
        if name in self.playerScores:
            self.playerScores[name] += 1
        else:
            self.playerScores[name] = 1
    
    def addNumberOccurence(self, number):
        self.numberOcc[number] += 1
    
    def getMostCommonNumber(self):
        maxNumber = "0"
        for i in self.numberOcc:
            if self.numberOcc[maxNumber] < self.numberOcc[i]:
                maxNumber = i
        return maxNumber
    
    def getThreeBestPlayers(self):
        players = ["Empty", "Empty", "Empty"]
        
        if len(self.playerScores) == 1:
            name = list(self.playerScores.keys())[0]
            players[0] = f"{Colors.YELLOW}First:{Colors.RESET} {name}, with {self.playerScores[name]} points" 
        
        elif len(self.playerScores) == 2:
            name1, name2 = list(self.playerScores.keys())[0],list(self.playerScores.keys())[1]
            score1, score2 = self.playerScores[name1], self.playerScores[name2]

            if score1 > score2:
                players[0] = f"{Colors.YELLOW}First:{Colors.RESET} {name1}, with {score1} points"
                players[1] = f"Second: {name2}, with {score2} points"
            else:
                players[0] = Colors.YELLOW + "First: " + Colors.RESET + f"{name2}, with {score2} points"
                players[1] =  f"Second: {name1}, with {score1} points"
        
        elif len(self.playerScores) >= 3:
            name1, name2, name3 = "", "", ""
            score1, score2, score3 = -1, -1, -1 

            for name in self.playerScores:
                if self.playerScores[name] > score1:
                    name3, score3 = name2, score2
                    name2, score2 = name1, score1
                    name1, score1 = name, self.playerScores[name]
                elif self.playerScores[name] > score2:
                    name3, score3 = name2, score2
                    name2, score2 = name, self.playerScores[name]
                elif self.playerScores[name] > score3:
                    name3, score3 = name, self.playerScores[name]

            players[0] = f"{Colors.YELLOW}First:{Colors.RESET} {name1}, with {score1} points"
            players[1] = f"{Colors.PURPLE}Second:{Colors.RESET}{name2}, with {score2} points"
            players[2] = f"Third:  {name3}, with {score3} points"

        return players
    
    def stats(self):
        players = self.getThreeBestPlayers()
        number = self.getMostCommonNumber()

        msg = f"""
{Colors.RED}------------------------------------{Colors.RESET}
{Colors.BOLD}Fun game Statistics:{Colors.RESET}

LeaderBoard:

{players[0]}
{players[1]}
{players[2]}
                  
most common valid answer: {number}
{Colors.RED}------------------------------------{Colors.RESET}\n\n"""
        return msg



