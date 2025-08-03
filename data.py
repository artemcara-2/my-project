# Define a dummy calculate_score function
def calculate_score(lines, combo):
    # Example scoring logic
    return lines * 100 + combo * 50

# Define a dummy LevelManager class
class LevelManager:
    def __init__(self):
        self.level = 1
        self.difficulty = "Easy"
    def update(self, lines, score_gained):
        # Example logic for level up
        if score_gained > 200:
            self.level += 1
            self.difficulty = "Medium"
            return True
        return False
    def get_level(self):
        return self.level
    def get_difficulty(self):
        return self.difficulty

level_manager = LevelManager()

lines = 2
combo = 3
score_gained = calculate_score(lines, combo)
level_up = level_manager.update(lines, score_gained)

if level_up:
    print(f"🎉 Уровень повышен! Теперь ты на {level_manager.get_level()} ({level_manager.get_difficulty()})")
