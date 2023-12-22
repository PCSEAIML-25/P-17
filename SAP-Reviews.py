import pandas as pd
from textblob import TextBlob
from zipfile import ZipFile
import plotly.express as px

# Read data from CSV file
def read_csv(file_path):
    with ZipFile(file_path, 'r') as zip_ref:
        # Assuming the CSV file is the only file in the ZIP archive
        csv_file = zip_ref.namelist()[0]
        with zip_ref.open(csv_file) as file:
            return pd.read_csv(file)

# Perform sentiment analysis using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    # Classify the polarity of the review (-1 to 1: negative to positive)
    return analysis.sentiment.polarity

# Get overall sentiment summary
def get_sentiment_summary(sentiment_scores):
    average_score = sentiment_scores.mean()
    if average_score > 0:
        return "Positive"
    elif average_score < 0:
        return "Negative"
    else:
        return "Neutral"

# Get the file path from the user
zip_file_path = input("Enter the path to the ZIP file: ")

# Read data from CSV within the ZIP file
try:
    data = read_csv(zip_file_path)
except (FileNotFoundError, pd.errors.EmptyDataError):
    print(f"Error: Unable to read CSV file from {zip_file_path}")

# Check the column names in the CSV file
print("Column names in the CSV file:", data.columns.tolist())

# Perform sentiment analysis on each review and add the result to a new column
if 'review' in data.columns:
    data['Sentiment'] = data['review'].apply(analyze_sentiment)

    # Display the results
    print(data[['review', 'Sentiment']])

    # Scatter plot for sentiment analysis
    scatter_plot = px.scatter(data, x='review', y='Sentiment', title='Sentiment Analysis')

    # Bar chart for overall sentiment
    overall_sentiment = get_sentiment_summary(data['Sentiment'])
    overall_bar_chart = px.bar(x=['Overall Sentiment'], y=[overall_sentiment], title='Overall Sentiment')

    # Histogram for sentiment distribution
    sentiment_histogram = px.histogram(data, x='Sentiment', nbins=50, title='Sentiment Distribution')

    # Display the plots
    scatter_plot.show()
    overall_bar_chart.show()
    sentiment_histogram.show()

    # Overall sentiment analysis
    print(f"\nThe Overall Sentiment Analysis: {overall_sentiment}")

    # Thank you message
    print("\nThank you for using this sentiment analysis tool!")

else:
    print("Error: 'review' column not found in the CSV file.")
