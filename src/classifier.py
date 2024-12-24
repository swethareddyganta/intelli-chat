
import joblib
import os
def test_model(texts, svm_model, vectorizer):
    # Vectorize the new text using the same vectorizer
    X_new = vectorizer.transform(texts)

    # Make predictions
    predictions = svm_model.predict(X_new)

    return predictions

def topic(text, model_path = 'svm_model.pkl', vect_path = 'svm_vectorizer.pkl'):
    new_data = [text]
    svm_model = joblib.load(model_path)
    vectorizer = joblib.load(vect_path)
    predictions = test_model(new_data, svm_model, vectorizer)
    final_ans = {
    'chitchat':'General Conversation',
    'health':'Health',
    'Environment':'Environment',
    'education':'Education',
    'sports':'Sports',
    'politics':'Politics',
    ' Travel':'Travel',
    'food':'Food',
    'Entertainment':'Entertainment',
    'Technology':'Technology',
    'Economy':'Economy'
}
    return final_ans[predictions[0]]

if __name__== '__main__':
    print(topic('how are you'))
