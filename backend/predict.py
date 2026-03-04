import os
import pickle
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# determine the directory containing this script so that models can be
# loaded regardless of the current working directory when the module is
# executed. Using a hard-coded relative path (e.g. "emotion_model.pkl")
# will fail when the script is started from a different folder, which is
# what caused the "No such file or directory" error.
base_dir = os.path.dirname(__file__)

model_path = os.path.join(base_dir, "emotion_model.pkl")
vectorizer_path = os.path.join(base_dir, "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

stop_words = set(stopwords.words('english'))

# label encoder mapping from training data
# obtained by fitting sklearn.preprocessing.LabelEncoder on the
# 'train.txt' labels.  Keeping it here lets us convert the numeric
# prediction back into a human-readable emotion.
label_map = {
    0: "anger",
    1: "fear",
    2: "joy",
    3: "love",
    4: "sadness",
    5: "surprise",
}

def clean_text(txt):
    txt = txt.lower()
    txt = txt.translate(str.maketrans('', '', string.punctuation))
    words = txt.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

def predict_emotion(text):
    text = clean_text(text)
    vec = vectorizer.transform([text])
    raw = model.predict(vec)[0]
    try:
        raw = raw.item()
    except AttributeError:
        pass
    # map numeric label to emotion name; if unknown just stringify
    return label_map.get(raw, str(raw))