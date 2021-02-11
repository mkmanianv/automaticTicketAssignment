import string

from bs4 import BeautifulSoup
from nltk import WordNetLemmatizer, LancasterStemmer, RegexpTokenizer, re, WordPunctTokenizer
from nltk.corpus import stopwords
import pandas as pd


class PreProcessing:
    lemmatizer = ""
    stemmer = ""
    tokenizer = ""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = LancasterStemmer()
        self.tokenizer = RegexpTokenizer(r'\w+')

    def data_clean(self, sentence):
        if pd.isnull(sentence):
            return sentence
        sentence = sentence.lower()
        # Remove email
        sentence = re.sub(r'\S*@\S*\s?', '', sentence)
        sentence = ' '.join([w for w in sentence.split() if not self.is_valid_date(w)])
        sentence = re.sub(r"received from:", ' ', sentence)
        sentence = re.sub(r"select the following link to view the disclaimer in an alternate language.", ' ', sentence)
        sentence = re.sub(r"from:", ' ', sentence)
        sentence = re.sub(r"to:", ' ', sentence)
        sentence = re.sub(r"subject:", ' ', sentence)
        sentence = re.sub(r"re:", ' ', sentence)
        sentence = re.sub(r"fw:", ' ', sentence)
        sentence = re.sub(r"sent:", ' ', sentence)
        sentence = re.sub(r"ic:", ' ', sentence)
        sentence = re.sub(r"cc:", ' ', sentence)
        sentence = re.sub(r"bcc:", ' ', sentence)
        tok = WordPunctTokenizer()
        pat1 = r'@[A-Za-z0-9]+'
        pat2 = r'https?://[A-Za-z0-9./]+'
        combined_pat = r'|'.join((pat1, pat2))

        soup = BeautifulSoup(sentence, 'lxml')
        souped = soup.get_text()
        stripped = re.sub(combined_pat, '', souped)
        try:
            clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
        except:
            clean = stripped
        letters_only = re.sub("[^a-zA-Z]", " ", clean)
        words = tok.tokenize(letters_only)
        sentence = (" ".join(words)).strip()
        # Remove underscores
        sentence = re.sub(r'\_', ' ', sentence)

        # Remove new line characters
        sentence = re.sub(r'\n', ' ', sentence)
        # Remove hashtag while keeping hashtag sentence
        sentence = re.sub(r'#', '', sentence)
        # &
        sentence = re.sub(r'&;?', 'and', sentence)
        # Remove HTML special entities (e.g. &amp;)
        sentence = re.sub(r'\&\w*;', '', sentence)
        # Remove hyperlinks
        sentence = re.sub(r'https?:\/\/.*\/\w*', '', sentence)
        # Remove characters beyond Readable formart by Unicode:
        sentence = ''.join(c for c in sentence if c <= '\uFFFF')
        sentence = sentence.strip()
        # Remove unreadable characters  (also extra spaces)
        sentence = ' '.join(re.sub("[^\u0030-\u0039\u0041-\u005a\u0061-\u007a]", " ", sentence).split())

        # Single character
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
        sentence = sentence.strip()
        sentence = self.remove_punctuation(sentence)
        tokens = self.make_tokens(sentence)
        stopwords = self.remove_stopwords(tokens)
        lem_words=self.word_lemmatize(stopwords)
        return ' '.join(map(str, lem_words))

    def is_valid_date(self, date_str):
        try:
            parser.parse(date_str)
            return True
        except:
            return False

    def remove_punctuation(self, sentence):
        try:
            no_punct = "".join([c for c in sentence if c not in string.punctuation])
            return no_punct
        except:
            print("remove_punctuation: sentence,", sentence)
            return sentence

    def make_tokens(self, sentence):
        return self.tokenizer.tokenize(sentence.lower())

    def remove_stopwords(self, words):
        return [w for w in words if w not in stopwords.words('english')]

    def word_lemmatize(self, words):
        return [self.lemmatizer.lemmatize(item) for item in words]