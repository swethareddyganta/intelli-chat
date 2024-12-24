import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""

        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        tokens = text.split()
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.ps.stem(word) for word in tokens]

        return tokens

if __name__ == '__main__':
    p = Preprocessor()
    # print(p.tokenizer('There are people'))
    given_input = str(input('Print the query to tokenize \n'))
    print(p.tokenizer(given_input))


