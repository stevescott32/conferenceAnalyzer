import nltk
import scrape
import textblob

print('Starting main')
talks = scrape.scrape_gen_conf()

print(talks[0]["content"])
blob = textblob.TextBlob(talks[0]["content"])
print("Nouns phrases:")
for np in blob.noun_phrases:
    print(np)
