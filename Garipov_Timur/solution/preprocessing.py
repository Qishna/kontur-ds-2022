import re
import string
from pymystem3 import Mystem
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


nltk.download("stopwords")
mystem = Mystem()
stemmer = PorterStemmer()


def preprocess_text(text, lang):
    """Preprocess russian or english text."""

    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[0-9]', '', text)

    if lang == 'rus':
        ru_stopwords = stopwords.words("russian")
        text = text.lower()
        tokens = mystem.lemmatize(text)
        tokens = [token for token in tokens if token not in ru_stopwords
                  and token != " "
                  and token.strip() not in string.punctuation]
        text = " ".join(tokens)

    else:
        eng_stopwords = stopwords.words('english')
        text = text.lower()
        text = text.translate(str.maketrans(
            '', '', string.punctuation + string.digits))
        text = ' '.join(stemmer.stem(token)
                        for token in text.split() if token not in eng_stopwords)

    return text
