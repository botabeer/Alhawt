import random
from datetime import datetime
from linebot.models import TextSendMessage

# ===== نقاط الألعاب =====
POINTS_CORRECT = 2
POINTS_HINT = -1
POINTS_ANSWER = 0
POINTS_SKIP = 0

# ===== لعبة الأغنية =====
class SongGame:
    def __init__(self, db):
        self.db = db
        self.current_song = None
        self.answered = set()

    def start_game(self):
        songs = ["أغنية 1", "أغنية 2", "أغنية 3"]
        self.current_song = random.choice(songs)
        self.answered.clear()
        return f"🎵 ابدأ الأغنية: {self.current_song}"

    def check_answer(self, user_id, answer):
        if answer.lower() == self.current_song.lower() and user_id not in self.answered:
            self.answered.add(user_id)
            self.db['users'][user_id]['points'] += POINTS_CORRECT
            return True
        return False

# ===== لعبة الإنسان-حيوان-نبات =====
class HumanAnimalPlantGame:
    def __init__(self, db):
        self.db = db
        self.current_letter = None
        self.answers = {}
        self.scores = {}

    def start_game(self):
        letters = list("أبتثجحخدذرزسشصضطظعغفقكلمنهوي")
        self.current_letter = random.choice(letters)
        self.answers.clear()
        self.scores.clear()
        return f"✏️ ابدأ لعبة الإنسان-حيوان-نبات بحرف: {self.current_letter}"

    def check_answer(self, user_id, answer):
        answer = answer.lower()
        if answer.startswith(self.current_letter) and answer not in self.answers.get(user_id, []):
            self.scores[user_id] = self.scores.get(user_id, 0) + POINTS_CORRECT
            self.answers.setdefault(user_id, []).append(answer)
            self.db['users'][user_id]['points'] += POINTS_CORRECT
            return True
        return False

# ===== لعبة سلسلة الكلمات =====
class ChainWordsGame:
    def __init__(self, db):
        self.db = db
        self.start_words = ["قلم", "كتاب", "مدرسة", "باب"]
        self.current_word = None
        self.used_words = set()

    def start_game(self):
        self.current_word = random.choice(self.start_words)
        self.used_words.clear()
        return f"🔗 ابدأ السلسلة بكلمة: {self.current_word}"

    def check_answer(self, user_id, answer):
        if answer not in self.used_words and answer[-1] == self.current_word[-1]:
            self.used_words.add(answer)
            self.current_word = answer
            self.db['users'][user_id]['points'] += POINTS_CORRECT
            return True
        return False

# ===== لعبة الإجابة السريعة =====
class FastAnswerGame:
    def __init__(self, db):
        self.db = db
        self.question = None
        self.answered = False

    def start_game(self, questions):
        self.question = random.choice(questions)
        self.answered = False
        return f"⚡ أسرع إجابة: {self.question}"

    def check_answer(self, user_id, answer):
        if not self.answered:
            self.answered = True
            self.db['users'][user_id]['points'] += POINTS_CORRECT
            return True
        return False

# ===== لعبة ضد =====
class OppositeGame:
    def __init__(self, db):
        self.db = db
        self.word = None

    def start_game(self, words_pairs):
        self.word, self.correct = random.choice(words_pairs)
        return f"🔄 ما عكس الكلمة: {self.word}؟"

    def check_answer(self, user_id, answer):
        if answer == self.correct:
            self.db['users'][user_id]['points'] += POINTS_CORRECT
            return True
        return False

# ===== لعبة تكوين كلمات =====
class WordComposerGame:
    def __init__(self, db):
        self.db = db
        self.letters = []
        self.used_words = set()

    def start_game(self, letters):
        self.letters = letters
        self.used_words.clear()
        return f"🔡 كوّن كلمات باستخدام الحروف: {' '.join(self.letters)}"

    def check_answer(self, user_id, word):
        if all(c in self.letters for c in word) and word not in self.used_words:
            self.used_words.add(word)
            self.db['users'][user_id]['points'] += POINTS_CORRECT
            return True
        return False

# ===== لعبة الاختلاف =====
class DifferenceGame:
    def __init__(self, db):
        self.db = db
        self.images = []
        self.current_index = 0

    def start_game(self, images_list):
        self.images = images_list
        self.current_index = 0
        return f"🔎 اكتشف الاختلاف في الصورة: {self.images[self.current_index]}"

    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.images):
            return f"🔎 اكتشف الاختلاف في الصورة: {self.images[self.current_index]}"
        return "✅ انتهت اللعبة"

# ===== لعبة التوافق =====
class CompatibilityGame:
    def __init__(self, db):
        self.db = db

    def calculate_compatibility(self, name1, name2):
        if name1 > name2:
            name1, name2 = name2, name1
        combined = name1 + name2
        score = sum(ord(c) for c in combined) % 100
        return score
