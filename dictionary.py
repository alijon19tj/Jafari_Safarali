# dictionary.py
import os

class Dictionary:
    def __init__(self, filename="words.txt"):
        self.words = set()
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self.words.add(word)
            print(f"✅ Қомус бор шуд: {len(self.words)} калима")
        else:
            print(f"❌ Файли '{filename}' ёфт нашуд!")

    def is_valid(self, word, stem):
        word = word.lower().strip()
        if not word:
            return False
        if not word.startswith(stem.lower()):
            return False
        return word in self.words