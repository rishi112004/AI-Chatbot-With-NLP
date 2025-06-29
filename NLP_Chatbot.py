
import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required resources
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

# Sample corpus (you can expand this or load from a file)
corpus = """
Hello, how can I help you?
I can assist you with your questions.
What is your name?
I am a chatbot created using NLTK.
How are you?
I'm just a program, but I'm functioning as expected!
What can you do?
I can answer your basic questions using NLP.
Goodbye!
See you later!
"""

# Preprocessing
lemmatizer = WordNetLemmatizer()
sent_tokens = nltk.sent_tokenize(corpus.lower())

def LemTokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting inputs and responses
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["Hi", "Hey there!", "Hello!", "I'm glad you are talking to me!"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo_response += "I’m sorry, I don’t understand you."
    else:
        robo_response += sent_tokens[idx]
    sent_tokens.pop()
    return robo_response

# Chat loop
print("Chatbot: My name is NLPBot. Type 'bye' to exit.")

while True:
    user_response = input("You: ").lower()
    if user_response == 'bye':
        print("Chatbot: Bye! Take care.")
        break
    elif greeting(user_response) is not None:
        print("Chatbot:", greeting(user_response))
    else:
        print("Chatbot:", response(user_response))
