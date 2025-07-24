# Developing an AI-Driven Chatbot - Application for Mental Well-being Support

# Importing Required Libraries
from transformers import pipeline
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load a sentiment-analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Function to analyze mood
def analyze_mood(user_input):
    analysis = sentiment_analyzer(user_input)
    mood_score = analysis[0]['score']
    sentiment = analysis[0]['label']

    # Map sentiment and score to mood levels
    if sentiment == "POSITIVE" and mood_score > 0.9:
        mood = "Very Happy"
    elif sentiment == "POSITIVE":
        mood = "Happy"
    elif sentiment == "NEGATIVE" and mood_score > 0.9:
        mood = "Very Sad"
    elif sentiment == "NEGATIVE":
        mood = "Sad"
    else:
        mood = "Neutral"

    return mood, mood_score

# Define chatbot responses based on mood levels
def chatbot_response(user_input):
    mood, score = analyze_mood(user_input)
    response = ""

    if mood == "Very Happy":
        response = "You seem to be in great spirits! Keep shining and spread the positivity."
    elif mood == "Happy":
        response = "I'm glad to hear you're feeling good. What made your day brighter?"
    elif mood == "Neutral":
        response = "It seems like you're feeling okay. Let me know if there's something specific you'd like to talk about."
    elif mood == "Sad":
        response = "I'm here to listen. It's okay to feel down sometimes. What's been on your mind?"
    elif mood == "Very Sad":
        response = "I'm sorry to hear that you're feeling this way. Please know you're not alone. How can I support you?"

    return f"{response}\n\nMood: {mood}, Confidence: {score:.2f}"

# Function to save mood data
def save_mood_data(user_input):
    mood, score = analyze_mood(user_input)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {'Timestamp': [timestamp], 'Input': [user_input], 'Mood': [mood], 'Confidence': [score]}
    df = pd.DataFrame(data)
    df.to_csv('mood_tracking_data.csv', mode='a', header=not pd.io.common.file_exists('mood_tracking_data.csv'), index=False)
    return mood

# Function to visualize mood trends
def plot_mood_trends():
    df = pd.read_csv('mood_tracking_data.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    mood_counts = df.groupby('Date')['Mood'].value_counts().unstack().fillna(0)
    mood_counts.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Mood Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Mood Count')
    plt.legend(title="Moods")
    plt.show()

# Define Gradio interface
def chatbot_interface(user_input):
    save_mood_data(user_input)  # Save mood data
    return chatbot_response(user_input)

interface = gr.Interface(
    fn=chatbot_interface,
    inputs="text",
    outputs="text",
    title="AI-Driven Mental Well-being Chatbot",
    description="Chatbot providing mood-specific responses and tracking trends over time."
)

# Launch interface
if __name__ == "__main__":
    interface.launch()
