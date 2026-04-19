import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import json
class NLTKInvertedIndex:
    def __init__(self):
        self.index = {}  # This will hold your term frequencies
        self.ps = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def save_index(self):
        with open('index.json', 'w') as f:
            json.dump(self.index, f)

    def load_index(self):
        try:
            with open('index.json', 'r') as f:
                self.index = json.load(f)
        except FileNotFoundError:
            self.index = {}

    def add_document(self, link, text):
        sentences = sent_tokenize(text)
        for sentence in sentences:
            words = word_tokenize(sentence)
            for word in words:
                word = word.lower()
                word = self.ps.stem(word)
                if word not in self.stop_words:
                    if word not in self.index:
                        self.index[word] = {}
                    self.index[word][link] = self.index[word].get(link, 0) + 1

    def search(self, query):
        query_words = word_tokenize(query)
        found_links = set()
        for word in query_words:
            word = word.lower()
            word = self.ps.stem(word)
            if word not in self.stop_words:
                    if word in self.index:
                        doc_dict = self.index[word]
                        found_links.update(doc_dict.keys())
        return list(found_links)

if __name__ == "__main__":
    engine = NLTKInvertedIndex()
    engine.add_document("link1", "The quick brown fox jumps.")
    engine.add_document("link2", "The fox is smart.")
    engine.save_index()
    print(engine.search("fox"))


