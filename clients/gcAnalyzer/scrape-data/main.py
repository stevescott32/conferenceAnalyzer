import nltk
import scrape
import textblob

print('Starting main')
conf_talks = scrape.scrape_gen_conf(30)


def run_sentiment_analysis(talks):
    print("Sentiment analysis")
    for talk in talks:
        blob = textblob.TextBlob(talk["content"])
        for s in blob.sentences:
            print(s)
            sentence_blob = textblob.TextBlob(str(s))
            print(sentence_blob.sentiment)


def run_neg_noun_analysis(talks):
    for talk in talks:
        print("\n*******************************")
        print("Analyzing talk " + talk["title"])
        print("*******************************\n")
        blob = textblob.TextBlob(talk["content"])
        for s in blob.sentences:
            sentence_blob = textblob.TextBlob(str(s))
            polarity = sentence_blob.sentiment.polarity
            if polarity < 0:
                print("Sentence found with negative polarity: " + str(polarity))
                print(s)
                print("--- Nouns: --- ")
                for noun in sentence_blob.noun_phrases:
                    print(noun)

def word_freq_per_talk(word, talks):
    for talk in talks:
        blob = textblob.TextBlob(talk["content"])
        count = blob.words.count(word)
        print("The talk '" + talk["title"] + "' has the word " + word + " " + str(count) + " times")


# run_neg_noun_analysis(conf_talks)
word_freq_per_talk("hope", conf_talks)
