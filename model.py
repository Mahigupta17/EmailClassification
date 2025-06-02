import pandas as pd
import re
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense, Dropout
from tensorflow.keras.utils import to_categorical

df = pd.read_csv('email_data.csv')

def extract_subject(text):
    match = re.search(r'Subject:\s*(.+)', text, re.IGNORECASE)
    if match:
        return re.split(r'[\r\n]', match.group(1))[0].strip()
    return text.strip().split('.')[0][:100]

df['Subject'] = df['email'].apply(extract_subject)

le = LabelEncoder()
df['label_encoded'] = le.fit_transform(df['type'])

tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(df['Subject'])
seqs = tokenizer.texts_to_sequences(df['Subject'])
max_len = max(len(s) for s in seqs)
X = pad_sequences(seqs, maxlen=max_len, padding='post')
y = to_categorical(df['label_encoded'])

model = Sequential([
    Embedding(input_dim=5000, output_dim=64, input_length=max_len),
    GlobalAveragePooling1D(),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(y.shape[1], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=15, batch_size=8, validation_split=0.2)

model.save('model.h5')
with open('tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

def classify_email_subject(subject):
    seq = tokenizer.texts_to_sequences([subject])
    padded = pad_sequences(seq, maxlen=max_len, padding='post')
    pred = model.predict(padded)
    label = le.inverse_transform([np.argmax(pred)])
    return label[0]
