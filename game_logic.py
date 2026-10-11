# game_logic.py
import random

class GameLogic:
    STEMS_EASY = ["fl", "pen", "str", "pre", "com", "con", "dis", "pro", "mis", "re"]
    STEMS_HARD = ["intro", "inter", "trans", "under", "over", "multi", "super", "semi"]
    ROUND_DURATIONS = [60, 70, 95]

    def __init__(self, dictionary):
        self.dict = dictionary
        self.reset_game()

    def reset_game(self):
        self.current_round = 0
        self.current_stem = ""
        self.score = 0
        self.words_entered = set()
        self.time_left = 0
        self.is_running = False
        self.bubble_levels = {i: 0 for i in range(4, 14)}
        self.stars = 0
        self.word_length_counts = {}

    def start_round(self):
        self.is_running = True
        duration = self.ROUND_DURATIONS[self.current_round]
        self.time_left = duration

        if self.current_round == 0:
            self.current_stem = random.choice(self.STEMS_EASY)
        else:
            all_stems = self.STEMS_EASY + self.STEMS_HARD
            self.current_stem = random.choice(all_stems)

        self.words_entered.clear()
        self.word_length_counts.clear()
        self.bubble_levels = {i: 0 for i in range(4, 14)}

        return self.current_stem, duration

    def tick(self, dt=1):
        if not self.is_running:
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.is_running = False

    def submit_word(self, word):
        word = word.lower().strip()

        if not self.dict.is_valid(word, self.current_stem):
            return False, "❌ Калима дуруст нест!", 0, []

        if word in self.words_entered:
            return False, "⚠️ Ин калимаро аллакай навиштӣ!", 0, []

        self.words_entered.add(word)
        length = len(word)

        if length < 4:
            return True, "Калима хеле кӯтоҳ аст", 0, []

        points = length * 10 * (self.current_round + 1)

        if length not in self.word_length_counts:
            self.word_length_counts[length] = 0
        self.word_length_counts[length] += 1

        bonus = 0
        bubble_updates = []

        if length in self.bubble_levels:
            if self.bubble_levels[length] < 3:
                self.bubble_levels[length] += 1
                bubble_updates.append(length)

                if self.bubble_levels[length] == 3:
                    self.stars += 1
                    bonus = points * 3
                    points += bonus

        self.score += points

        msg = f"✅ +{points} хол"
        if bonus > 0:
            msg += f" (🎁 БОНУС +{bonus}!)"

        return True, msg, points, bubble_updates

    def next_round(self):
        self.current_round += 1
        if self.current_round >= len(self.ROUND_DURATIONS):
            return False
        return True