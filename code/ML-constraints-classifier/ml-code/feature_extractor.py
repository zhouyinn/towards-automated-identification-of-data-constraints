from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
import sys
import pandas as pd
from scipy.sparse import hstack
from MLExpr import MLExpr
import numpy as np


def getSubCorpus(df: pd.DataFrame):
    corpus = []
    for i in range(len(df)):
        sentenceList = []
        for j in range(len(df.columns)):
            for cell in df.iloc[i, j]:
                sentenceList.append(cell)
        corpus.append(sentenceList)
    return corpus


# This method will get a sparse matrix from a dictionary
def getSparseMatrix(dict):
    vec = DictVectorizer()
    sparseMatrix = vec.fit_transform(dict)
    features = vec.feature_names_
    return sparseMatrix, features


class Processor:
    def __init__(self, train_index, test_index, expr: MLExpr, df):
        self.train_index = train_index
        self.test_index = test_index
        self.expr = expr
        self.df = df

    def getVectorRepresentation(self, x_train_Tfidf, x_test_Tfidf):
        new_train_vectors, new_test_vectors = x_train_Tfidf, x_test_Tfidf
        dict_feature = []
        if self.expr.use_dispat: dict_feature.append('dispat')
        if self.expr.use_ct: dict_feature.append('constraint_type')
        
        for df in dict_feature:
            # getting a dictionary for pattern column from df
            featureDict = self.getPatternDictDromDF(df)
            # get sparse matrix from dictionary
            sparseMatrixDF, features = getSparseMatrix(featureDict)
            train_f = sparseMatrixDF[self.train_index, :]
            test_f = sparseMatrixDF[self.test_index, :]
            if new_train_vectors is not None and new_test_vectors is not None:
                new_train_vectors = hstack((new_train_vectors, train_f))
                new_test_vectors = hstack((new_test_vectors, test_f))
            else:
                new_train_vectors = train_f
                new_test_vectors = test_f
        assert new_train_vectors is not None and new_train_vectors is not None
        return [new_train_vectors, new_test_vectors]

    # create dictionary for pattern from df
    def getPatternDictDromDF(self, feature):
        patterndfvalue = [self.df[feature]]
        patterndfheaders = [feature]
        patterndf = pd.concat(patterndfvalue, axis=1, keys=patterndfheaders)
        patterndict = patterndf.to_dict('records')
        return patterndict

    def transform_data(self):
        train = self.df.iloc[self.train_index]
        test = self.df.iloc[self.test_index]
        x = []
        if self.expr.use_frag:
            x += ['f_npos', 'f_ngrams']
        if self.expr.use_sent:
            x += ['s_npos', 's_ngrams']
        if self.expr.use_op:
            x += ['o_npos', 'o_ngrams']
        y = 'label'
        y_train = train[y]
        y_test = test[y]

        # Encoder = LabelEncoder()
        # y_train = Encoder.fit_transform(y_train.values.ravel())
        # y_test = Encoder.fit_transform(y_test.values.ravel())

        y_train = np.array(y_train)
        y_test = np.array(y_test)

        if len(x) != 0:
            x_train = train[x]
            x_test = test[x]
            x_train_corpus = getSubCorpus(x_train)
            x_test_corpus = getSubCorpus(x_test)

            def my_tokenizer(doc):
                return doc

            Tfidf_vect = TfidfVectorizer(max_features=sys.maxsize, tokenizer=my_tokenizer, lowercase=False)

            Tfidf_vect.fit(x_train_corpus)
            x_train_Tfidf = Tfidf_vect.transform(x_train_corpus)
            x_test_Tfidf = Tfidf_vect.transform(x_test_corpus)
        else:
            x_train_Tfidf, x_test_Tfidf = None, None

        vectors = self.getVectorRepresentation(x_train_Tfidf, x_test_Tfidf)
        x_train_Tfidf = vectors[0]
        x_test_Tfidf = vectors[1]
        if self.expr.smote is None:
            return x_train_Tfidf, y_train, x_test_Tfidf, y_test
        x_train_smote, y_train_smote = self.expr.smote.fit_resample(x_train_Tfidf, y_train)
        return x_train_smote, y_train_smote, x_test_Tfidf, y_test
