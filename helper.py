import random
class QuestionBank:
    
    def __init__(self):
        self.questions = [("17 * 2 - 29 = ?", 5), ("(45 + 54) / 11 = ?", 9), ("(35 + 27 - 18) / 11 = ?", 4), ("2 + 3 = ?", 5),
                          ("(40 + 40) / 10 = ?", 8), ("1 + 2 + 5 - 6 = ?", 2), ("3! = ?", 6), ("(34 - 12 + 17 - 9) * 0 = ?", 0),
                          ("(72 - 2 - 10 - 20) / 10 = ?", 4), ("42 / 7 = ?", 6), ("0.5 * 0.5 * 4 = ?", 1), ("1 + 1 + 1 + 1 + 1 + 1 * 0 + 1 + 1 = ?", 7),
                          ("e^0 = ?", 1), ("ln(1) = ?", 0), ("ln(e) = ?", 1), ("ln(1/e) + 1 = ?", 0), ("f(x)=x^2, f'(2) = ?", 4),
                          ("f'(x)=2x, f(3) = ?", 9), ("2x + 3 = 7, x = ?", 2), ("7x - 6 = 8, x = ?", 2), ("2 * 3", 6),("e - (e - 2)", 2),
                          ("25 / 5 = ?", 5), ("2 cats and 1 chickens have ? legs", 9), ("5 + 5 - 1 = ?", 9), ("if anny has 5 apples and danny 4, how much is 5 + 1?", 6),
                          ("how many pants is a pair of pants", 1), ("3 * 3 / 3 * 3 / 3 * 3 / 3", 3)
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
    playerScores = {}
    numberOcc = {"0" : 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0}
    colors = Colors()
    def addPlayerPoint(self, name):
        if name in playerScores:
            playerScores[name] += 1
        else:
            playerScores[name] = 1
    
    def addNumberOccurence(self, number):
        numberOcc[number] += 1
    
    def getMostCommonNumber():
        maxNumber, maxNumberVal = "0", numberOcc["0"]
        for i in numberOcc:
            if numberOcc[maxNumber] < numberOcc[i]:
                maxNumber = i
                maxNumberVal = numberOcc[i]
        return maxNumber
    
    def getThreeBestPlayers():
        players = ["Empty", "Empty", "Empty"]
        p1, p2, p3
        if len(playerScores) == 1:
            name = playerScores.keys()[0]
            players[0] = "First: " + name + ", with " + playerScores[name] + " points" 
        elif len(playerScores) == 2:
            name1, name2 = playerScores.keys()[0],playerScores.keys()[1]
            score1, score2 = playerScores[name1], playerScores[name2]
            if score1 > score2:
                players[0] = colors.YELLOW + "First: " + colors.RESET + name1 + ", with " + score1 + " points"
                players[1] = "Second: " + name2 + ", with " + score2 + " points"
            else:
                players[0] = colors.YELLOW + "First: " + colors.RESET + name2 + ", with " + score2 + " points"
                players[1] = "Second: " + name1 + ", with " + score1 + " points"
        elif len(playerScores) >= 3:
            name1, name2, name3 = "", "", ""
            score1, score2, score3 = -1, -1, -1 
            for name in playerScores:
                if playerScores[name] > score1:
                    name3 = name2
                    score3 = score2
                    name2 = name1
                    score2 = score1
                    name1 = name
                    score1 = playerScores[name]
                elif playerScores[name] > score2:
                    name3 = name2
                    score3 = score2
                    name2 = name
                    score2 = playerScores[name]
                elif playerScores[name] > score3:
                    name3 = name
                    score3 = playerScores[name]
            players[0] = colors.YELLOW + "First: " + colors.RESET + name1 + ", with " + score1 + " points"
            players[1] = "Second: " + name2 + ", with " + score2 + " points"
            players[2] = "Third: " + name3 + ", with " + score3 + " points"

        return players
    
    def stats():
        players = getThreeBestPlayers()
        number = getMostCommonNumber()

        msg = f"""Game Statistics:
                  ------------------------
                  LeaderBoard:
                  {players[0]}
                  {players[1]}
                  {players[2]}
                  
                  most common valid answer: {number}"""



