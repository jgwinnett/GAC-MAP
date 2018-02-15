import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.cross_validation import StratifiedKFold, cross_val_score, train_test_split
import pandas as pd
from sklearn_pandas import DataFrameMapper
from bs4 import BeautifulSoup
import re
import nltk
import numpy as np
from nltk.corpus import stopwords



def importSource():
    # Build the initial DF and shape it appropriately
    df = pd.read_excel('training.xlsx', header=0, index_col ='Index')
    df = df[['Abstract','is5G']]
    df.reset_index(inplace=True, drop=True)
    return df

def importPickle(path):
    df = pd.read_pickle(path)
    return df

def onlyWords(x):
    noPunc = re.sub("[^a-zA-Z0-9]"," ",x)
    return noPunc

def removeStopWords(w, stops):

    words = w.split(' ')
    words = [y for y in words if not y in stops]
    words[:] = [x for x in words if " " not in x]
    words = " ".join(str(x) for x in words)
    return words

def dataClean(df):
    df['Abstract'] = df['Abstract'].apply(lambda x: BeautifulSoup(x,"lxml").get_text())
    df['Abstract'] = df['Abstract'].apply(lambda x: onlyWords(x))
    stops = set(stopwords.words("english"))
    df['Abstract'] = df['Abstract'].apply(lambda x: removeStopWords(x, stops))

    return(df)

def pickler(df):

    df.to_pickle('Cleaned.pickle')

def BagOfWordszer(train, test):

    vectorizer = CountVectorizer(analyzer = "word",
                                 tokenizer = None,
                                 preprocessor = None,
                                 stop_words= None,
                                 max_features = 10000)
    abstractList = []

    arr = train.values

    for n in arr:
        abstractList.append(n)

    train_data_features = vectorizer.fit_transform(abstractList)

    train_data_features = train_data_features.toarray()

    print(train_data_features.shape)

    #######

    abstractList = []

    arr = test.values

    for n in arr:
            abstractList.append(n)

    test_data_features = vectorizer.transform(abstractList)

    test_data_features = test_data_features.toarray()

    print(test_data_features)

    return(train_data_features, test_data_features)

def TFIDerizer(train_data, test_data):

    tfid = TfidfTransformer()

    tfid_train = tfid.fit_transform(train_data)
    tfid_test = tfid.transform(test_data)

    return (tfid_train, tfid_test)


def trainer(abs_train, abs_test, is5G_train, is5G_test):

    classifier = MultinomialNB().fit(abs_train, is5G_train)

    all_predictions = classifier.predict(abs_test)

    deeEff = pd.DataFrame(all_predictions, columns=['yes/no'])

    grouped = deeEff.groupby('yes/no')

    groupy = grouped.get_group('Yes')

    print(groupy)



    #print('accuracy', accuracy_score(is5G_test, all_predictions))



def trainTestSplit(df):

    abs_train, abs_test, is5G_train, is5G_test = \
        train_test_split(df['Abstract'], df['is5G'], test_size=0.2)

    return abs_train, abs_test, is5G_train, is5G_test

# df = importSource()
# dataClean(df)
# pickler(df)
# print(df.head)
#
df = importPickle('Cleaned.pickle')
abs_train, abs_test, is5G_train, is5G_test = trainTestSplit(df)
#train_data, test_data = BagOfWordszer(abs_train, abs_test)
# # train_data, test_data = TFIDerizer(train_data, test_data)
# trainer(train_data, test_data, is5G_train, is5G_test)

df2 = importPickle('CORDIS_DF.pickle')
df3 = pd.DataFrame(columns=["Abstract"])

df3['Abstract'] = df2['objective'].values
df3 = dataClean(df3)
seriez = df3.squeeze()
train_data, test_data = BagOfWordszer(abs_train, seriez)
trainer(train_data, test_data, is5G_train, is5G_test)
