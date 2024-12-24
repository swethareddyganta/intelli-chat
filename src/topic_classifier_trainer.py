from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import joblib
import json
from tqdm import tqdm


def tokenize_sentences(text):
    
    words = text.split()[:16]
    
    sentences = [' '.join(words[i:i+4]) for i in range(0, len(words), 4)]
    return sentences



def load_json(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def flatten_json(json_data):
    rows = []
    for topic, articles in json_data.items():
        for article in articles:
            summary_sentences = tokenize_sentences(article['summary'])  
            for sentence in summary_sentences:
                rows.append({'Text': sentence, 'Label': topic})
    return pd.DataFrame(rows)


def preprocess_data(json_file):
    
    json_data = load_json(json_file)
    json_df = flatten_json(json_data)

    
    tsv_files = ['/content/questions_caring.tsv', '/content/questions_enth.tsv', '/content/questions_frnd.tsv', '/content/questions_prof.tsv', '/content/questions_witty.tsv']
    tsv_dataframes = [pd.read_csv(file, sep='\t') for file in tsv_files]

    
    chitchat_df = pd.concat(tsv_dataframes)
    chitchat_df['Label'] = 'chitchat'
    chitchat_df['Text'] = chitchat_df['Question']

    
    combined_df = pd.concat([json_df, chitchat_df], ignore_index=True)

    return combined_df


def count_samples_per_class(df):
    class_counts = df['Label'].value_counts()
    print("Number of samples per class before balancing:")
    print(class_counts)
    return class_counts


def balance_classes(df):
    
    min_samples = df['Label'].value_counts().min()

    balanced_dfs = []
    for label in df['Label'].unique():
        class_df = df[df['Label'] == label]
        
        if len(class_df) > min_samples:
            class_df = class_df.sample(min_samples, random_state=42)
        elif len(class_df) < min_samples:
            class_df = class_df.sample(min_samples, replace=True, random_state=42)
        balanced_dfs.append(class_df)

    
    balanced_df = pd.concat(balanced_dfs, ignore_index=True)

    
    print("Number of samples per class after balancing:")
    print(balanced_df['Label'].value_counts())

    return balanced_df


def vectorize_data(df):
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['Text'])
    y = df['Label']
    return X, y, vectorizer


def train_svm_classifier(X, y):
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    svm_model = SVC(kernel='linear', random_state=42, verbose=True)

    
    print("Starting training...")
    svm_model.fit(X_train, y_train)
    print("Training complete!")

    
    y_pred = svm_model.predict(X_test)

    
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    return svm_model



def main():
    
    combined_df = preprocess_data('/content/final_wikipedia_data_Final.json')

    
    count_samples_per_class(combined_df)

    
    balanced_df = balance_classes(combined_df)

    
    X, y, vectorizer = vectorize_data(balanced_df)

    
    svm_model = train_svm_classifier(X, y)

    
    joblib.dump(svm_model, 'svm_model.pkl')
    joblib.dump(vectorizer, 'svm_vectorizer.pkl')


main()
