"""
Yelp reviews data-set layout
data fields: type, review_id, date, business_id, stars, text, votes, user_id
data needed: stars, text
time:        380 sec
"""
import time
import csv
import json
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import words

stopword = stopwords.words("english")                  # get stopwords [127]
english_vocab = set(w.lower() for w in words.words())  # get frequent used words [234,377]


def get_review():
    dword = {}
    with open("cache/yelp_academic_dataset_review_small.json") as infile:
        review = json.load(infile)                                # list of dicts
        review = [(rev["stars"], rev["text"]) for rev in review]  # extract only (star, text)

    # create a dict of words with value: (rating, count)
    for rev in review:
        word = tokenize(rev[1])
        for w in word:
            if w in dword.keys():
                dword[w][0] += int(rev[0])  # star rating
                dword[w][1] += 1            # word count
            else:
                dword[w] = [rev[0], 1]      # default

    # compute average star rating of each words (total, count) ==> (w, total/count)
    # sort by rating ascending order
    return sorted([(w, dword[w][0]/dword[w][1]) for w in dword.keys() if int(dword[w][1]) >= 10],
                  key=lambda x: x[1])


def tofile(word):
    # write to file
    with open("results/words-sentlvl.csv", "w") as outfile:
        outfile.write("Word,Sentiment Level\n")
        writer = csv.writer(outfile, delimiter=",")
        writer.writerows(word[:500])   # most negative
        writer.writerows(word[-500:])  # most positive


def tokenize(text):
    word = set(w.lower() for w in word_tokenize(text))
    word = [w for w in word if w not in stopword and w in english_vocab]  # filter stopwords and check dict
    word = [WordNetLemmatizer().lemmatize(w) for w in word]               # lemmatization of words
    return word


def main():
    t = time.time()
    print("begin", int(t))
    print("Extracting and analyzing reviews from json file...")
    word = get_review()
    print("Writing to csv file...")
    tofile(word)
    print("end: ", int(time.time() - t))


if __name__ == '__main__':
    main()
