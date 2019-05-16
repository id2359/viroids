import sys
#import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
import datetime

# needed for cloud integration
from sklearn.externals import joblib
from google.cloud import storage

MODELS_BUCKET = 'lrviroids-data/models'
TRAINING_BUCKET = 'lrviroids-data'
FEATURE_FILE = 'features.csv'

# ,ACCID,ARC1,ARC2,ARC3,ARC4,ARC5,ARC6,ARC7,ARC8,ARC9,ARC10,STRAIN,TYPE

TARGET_COLUMN = 'TYPE'
COLUMNS_TO_EXCLUDE = ['ACCID']


def to_float(df):
    return df.apply(pd.to_numeric, errors='coerce')


def fillna(df):
    return df.fillna(df.mean())


def download_data(training_data_bucket):
    bucket = storage.Client().bucket(training_data_bucket)
    # Path to the data inside the public bucket
    blob = bucket.blob(FEATURE_FILE)
    # Download the data
    blob.download_to_filename(FEATURE_FILE)
    # [END download-data]


def load_csv(filename):
    df = pd.read_csv(filename, header=0)
    df.drop(df.columns[[0]], axis=1, inplace=True)
    return df


def ttsplit(x, y):
    # split into a training and testing set
    x_train, x_test, y_train, y_test = train_test_split(x,
                                                        y,
                                                        test_size=0.50,
                                                        random_state=46)
    return x_train, x_test, y_train, y_test


def get_features(df):
    return df[df.columns.difference([TARGET_COLUMN]+COLUMNS_TO_EXCLUDE)].copy()


def get_target(df):
    return df[[TARGET_COLUMN]]


#TRAIN_CSV = sys.argv[1]

download_data(TRAINING_BUCKET)

train = load_csv(FEATURE_FILE)

x = get_features(train)
y = get_target(train)

x_train, x_test, y_train, y_test = ttsplit(x, y)

rfr = RandomForestClassifier(max_depth=5, random_state=0)

pipeline = make_pipeline(rfr)

# modify for cloud
model = 'model.joblib'  # this name must be used afaik
joblib.dump(pipeline, model)

# Upload the model to GCS
bucket = storage.Client().bucket(MODELS_BUCKET)
blob = bucket.blob('{}/{}'.format(
    datetime.datetime.now().strftime('viroids_model_%Y%m%d_%H%M%S'),
    model))
blob.upload_from_filename(model)
# [END export-to-gcs]

#model = pipeline.fit(x_train, y_train)
#predictions = model.predict(x_test)
#score = model.score(x_test, y_test)
#if float(score) > 0.90:
#    with open("model.pickle", "wb") as pickle_file:
#        pickle.dump(model, pickle_file)
