import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import json
import unicodedata

class NLTKInvertedIndex:
    def __init__(self):
        self.index = {}  # This will hold your term frequencies
        self.ps = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.metadata = {}

    def normalize_text(self, text):
        # This converts characters like 'ā' to 'a'
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

    def save_index(self):
        with open('index.json', 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=4)

        with open('metadata.json', 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=4)

    def load_index(self):
        try:
            with open('index.json', 'r') as f:
                self.index = json.load(f)
        except FileNotFoundError:
            self.index = {}
        try:
            with open('metadata.json', 'r') as f:
                self.metadata = json.load(f)
        except FileNotFoundError:
            self.metadata = {}

    def add_metadata(self, link, title, snippet):
        self.metadata[link] = {
            'title': title,
            'snippet': snippet
        }

    def add_document(self, link, text):
        sentences = sent_tokenize(text)
        for sentence in sentences:
            words = word_tokenize(sentence)
            for word in words:
                word = self.normalize_text(word.lower())
                word = self.ps.stem(word)
                if word not in self.stop_words:
                    if word not in self.index:
                        self.index[word] = {}
                    self.index[word][link] = self.index[word].get(link, 0) + 1

    def search(self, query):
        query_words = word_tokenize(query)
        scores = {}
        for word in query_words:
            word = self.normalize_text(word.lower())
            word = self.ps.stem(word)
            if word not in self.stop_words:
                    if word in self.index:
                        doc_dict = self.index[word]
                        for url, frequency in doc_dict.items():
                            scores[url] = scores.get(url, 0) + frequency
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results




