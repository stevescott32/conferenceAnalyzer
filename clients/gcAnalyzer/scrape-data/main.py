import nltk
import scrape
import textblob

print('Starting main')
talks = scrape.scrape_gen_conf()

blob = textblob.TextBlob(talks[0]["content"])
# print("Noun Phrases: ")
# for np in blob.noun_phrases:
#    print(np)

print("Sentiment analysis")
for talk in talks:
    blob = textblob.TextBlob(talk["content"])
    for s in blob.sentences:
        print(s)
        sentence_blob = textblob.TextBlob(str(s))
        print(sentence_blob.sentiment)
