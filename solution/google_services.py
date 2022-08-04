import time
from googlesearch import search
from googletrans import Translator

translator = Translator()


def google_request(titles):
    """Make a Google requst by list of queries."""

    fake_source = 'панорама '
    true_source = 'лента '
    google_pred = []

    for title in titles:

        fake_flag = False
        for site_link in search(true_source + title, lang='ru', stop=3):
            if 'lenta.ru' in site_link:
                google_pred.append(0)
                break
            elif fake_flag:
                break
            else:
                for site_link in search(fake_source + title, lang='ru', stop=3):
                    if 'ryb.ru' or 'panorama.pub' in site_link:
                        google_pred.append(1)
                        fake_flag = True
                        break
                    else:
                        google_pred.append(2)
        time.sleep(1)

    return google_pred


def google_translate(text):
    """Make a Google translate by text."""
    translator.raise_Exception = True
    translated = translator.translate(text, src='ru', dest='en').text
    time.sleep(1)
    return translated
