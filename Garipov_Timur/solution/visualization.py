from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def generate_fakenews_wordcloud(df, is_fake, title):
    """Generate a wordcloud of words from dataframe sentences."""

    fig = plt.figure(figsize=(12, 8), dpi=80)
    wc = WordCloud(max_words=100).generate(
        " ".join(df[df['is_fake'] == is_fake]['title']))
    plt.title(title)
    plt.axis("off")
    plt.imshow(wc)
