import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error 
from sklearn.ensemble import RandomForestClassifier

#,ACCID,ARC1,ARC2,ARC3,ARC4,ARC5,ARC6,ARC7,ARC8,ARC9,ARC10,STRAIN,TYPE

TARGET_COLUMN = 'TYPE'
COLUMNS_TO_EXCLUDE = ['ACCID']

def to_float(df):
    return df.apply(pd.to_numeric, errors='coerce')

def fillna(df):
    return df.fillna(df.mean())

def load_csv(filename):
    df = pd.read_csv(filename, header=0)
    df.drop(df.columns[[0]],axis=1,inplace=True)
    del df['STRAIN']  
    return df

def ttsplit(x,y):
    # split into a training and testing set
    x_train, x_test, y_train, y_test = train_test_split(x,
                                                        y,
                                                        test_size=0.50,
                                                        random_state=42)
    return x_train, x_test, y_train, y_test


def get_features(df):
    return df[df.columns.difference([TARGET_COLUMN]+COLUMNS_TO_EXCLUDE)].copy()

def get_target(df):
    return df[[TARGET_COLUMN]]


TRAIN_CSV = sys.argv[1]

train = load_csv(TRAIN_CSV)

x = get_features(train)
y = get_target(train)


# In[10]:

x_train, x_test, y_train, y_test = ttsplit(x,y)


rfr = RandomForestClassifier(max_depth=2, random_state=0)

pipeline = make_pipeline(rfr)

model = pipeline.fit(x_train, y_train)

predictions = model.predict(x_test)

print "y_test = %s" % y_test
print "predictions = %s" % predictions
print model.score(x_test, y_test)
