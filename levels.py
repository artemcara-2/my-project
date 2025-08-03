class LevelManager:
    def __init__(self):
        self.levels = {
            i: {
                "speed": max(120, 500 - i * 20),  # чем выше уровень, тем быстрее
                "lines": i * 10,                  # сколько линий нужно очистить
                "score": i * 1000,                # сколько очков нужно набрать
                "difficulty": [
                    "Easy", "Normal", "Hard", "Very Hard",
                    "Insane", "Extreme", "Impossible"
                ][min(i // 3, 6)]                 # текстовая сложность
            } for i in range(1, 21)
        }
        self.current_level = 1
        self.total_lines = 0
        self.total_score = 0

    def update(self, lines_cleared, score_gained):
        prev_level = self.current_level
        self.total_lines += lines_cleared
        self.total_score += score_gained
        for level in range(1, 21):
            if (self.total_lines >= self.levels[level]["lines"] and
                self.total_score >= self.levels[level]["score"]):
                self.current_level = level
        return self.current_level > prev_level

    def get_speed(self):
        return self.levels[self.current_level]["speed"]

    def get_level(self):
        return self.current_level

    def get_difficulty(self):
        return self.levels[self.current_level]["difficulty"]
