import os

class LexicographicalIterator:
    def __init__(self, sentence_obj):
        self._sorted_words = sorted(sentence_obj.words)
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index < len(self._sorted_words):
            word = self._sorted_words[self._index]
            self._index += 1
            return word
        else:
            raise StopIteration
class Sentence:
    def __init__(self, content=""):
        if isinstance(content, str):
            self.words = content.split()
        elif isinstance(content, list):
            self.words = list(content)
        else:
            self.words = []
    def __len__(self):
        return len(self.words)
    def __getitem__(self, index):
        return self.words[index]
    def __setitem__(self, index, value):
        self.words[index] = value
    def __add__(self, other):
        if isinstance(other, Sentence):
            return Sentence(self.words + other.words)
        elif isinstance(other, str):
            return Sentence(self.words + [other])
        raise TypeError("Непідтримуваний тип операнда для +")
    def __sub__(self, other):
        if isinstance(other, Sentence):
            words_to_remove = set(other.words)
            return Sentence([w for w in self.words if w not in words_to_remove])
        elif isinstance(other, str):
            return Sentence([w for w in self.words if w != other])
        raise TypeError("Непідтримуваний тип операнда для -")
    def __contains__(self, item):
        return item in self.words
    def __str__(self):
        return " ".join(self.words)
    def __iter__(self):
        return LexicographicalIterator(self)
def process_text(filename, replacements, words_to_delete):
    if not os.path.exists(filename):
        print(f"Файл {filename} не знайдено.")
        return 0
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    sentence = Sentence(text)
    for i in range(len(sentence)):
        clean_word = sentence[i].strip(".,!?;:\"'()")
        if clean_word in replacements:
            sentence[i] = sentence[i].replace(clean_word, replacements[clean_word])
    for word in words_to_delete:
        sentence = sentence - word
    print(sentence)
    return len(sentence)
if __name__ == "__main__":
    test_filename = "test_text.txt"
    with open(test_filename, "w", encoding="utf-8") as f:
        f.write("Це дуже старий текст. Він містить погані слова та зайвий сміття.")
    replace_dict = {"старий": "новий", "погані": "гарні"}
    delete_list = ["зайвий", "сміття.", "дуже"]
    final_word_count = process_text(test_filename, replace_dict, delete_list)
    print(f"Загальна кількість слів після коригування: {final_word_count}\n")
    if os.path.exists(test_filename):
        os.remove(test_filename)
    print("--- Лексикографічний перебір слів (6.4.8) ---")
    text_for_iterator = "яблуко ананас банан груша"
    sentence_iter = Sentence(text_for_iterator)
    for word in sentence_iter:
        print(word)