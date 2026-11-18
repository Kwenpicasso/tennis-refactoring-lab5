class TennisGame1:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1points = 0
        self.p2points = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.p1points += 1
        else:
            self.p2points += 1

    def score(self):
        if self.p1points == self.p2points:
            return self._equal_score()
        if self.p1points >= 4 or self.p2points >= 4:
            return self._endgame_score()
        return self._regular_score()

    def _equal_score(self):
        return {
            0: "Love-All",
            1: "Fifteen-All",
            2: "Thirty-All",
        }.get(self.p1points, "Deuce")

    def _endgame_score(self):
        minus_result = self.p1points - self.p2points
        if minus_result == 1:
            return "Advantage player1"
        if minus_result == -1:
            return "Advantage player2"
        if minus_result >= 2:
            return "Win for player1"
        return "Win for player2"

    def _regular_score(self):
        result = ""
        temp_score = 0
        for i in range(1, 3):
            if i == 1:
                temp_score = self.p1points
            else:
                result += "-"
                temp_score = self.p2points
            result += {
                0: "Love",
                1: "Fifteen",
                2: "Thirty",
                3: "Forty",
            }[temp_score]
        return result
