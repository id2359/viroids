import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
import datetime

# needed for cloud integration
from sklearn.externals import joblib
from google.cloud import storage

MODELS_BUCKET = 'lrviroids-data'  # subbucket didn't work..
TRAINING_BUCKET = 'lrviroids-data'
FEATURE_FILE = 'features.csv'
FEATURE_FILE = 'snps.features'
STANDARD_MODEL_NAME = 'model.joblib'  # don't know why

# ,ACCID,ARC1,ARC2,ARC3,ARC4,ARC5,ARC6,ARC7,ARC8,ARC9,ARC10,STRAIN,TYPE

TARGET_COLUMN = 'TYPE'
COLUMNS_TO_EXCLUDE = ['ACCID']


def to_float(df):
    return df.apply(pd.to_numeric, errors='coerce')


def fillna(df):
    return df.fillna(df.mean())


def download_data(training_data_bucket):
    bucket = storage.Client().bucket(training_data_bucket)
    print "got training bucket"
    blob = bucket.blob(FEATURE_FILE)
    print "got feature file %s" % FEATURE_FILE
    blob.download_to_filename(FEATURE_FILE)
    print "downloaded %s" % FEATURE_FILE


def load_csv(filename):
    df = pd.read_csv(filename, header=0)
    print "read %s into dataframe" % filename
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


download_data(TRAINING_BUCKET)

train = load_csv(FEATURE_FILE)
print "loaded %s ok" % FEATURE_FILE

x = get_features(train)
print "got features"
y = get_target(train)
print "got target column"

x_train, x_test, y_train, y_test = ttsplit(x, y)
print "split into train and test"

classifier = RandomForestClassifier(max_depth=5, random_state=0)
print "created classifier"

pipeline = make_pipeline(classifier)
print "made pipeline"

# modify for cloud
model_name = STANDARD_MODEL_NAME
joblib.dump(pipeline, model_name)
print "joblib dumped %s" % model_name

# Upload the model to GCS
bucket = storage.Client().bucket(MODELS_BUCKET)
print "got bucket %s" % MODELS_BUCKET
blob = bucket.blob('{}/{}'.format(
    datetime.datetime.now().strftime('viroids_model_%Y%m%d_%H%M%S'),
    model_name))
print "created model blob"
blob.upload_from_filename(model_name)
print "uploaded %s to %s" % (model_name, MODELS_BUCKET)

print "train.py finished"
