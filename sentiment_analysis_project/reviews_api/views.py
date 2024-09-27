import os
import time
import pandas as pd
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import FileUploadSerializer
from groq import Groq

# Directory to store uploaded files
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize the Groq client using an environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            file = request.FILES['file']
            file_path = os.path.join(UPLOAD_DIR, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Process the uploaded file
            reviews, error = self.process_file(file_path)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

            # Perform sentiment analysis using the Groq API
            sentiment_scores = self.analyze_sentiment(reviews)
            if 'error' in sentiment_scores:
                return Response({'error': sentiment_scores['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(sentiment_scores, status=status.HTTP_200_OK)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_file(self, file_path):
        """
        Extracts review text from the uploaded file. Supports both CSV and XLSX formats.
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return None, "Unsupported file format"

            if 'Review' in df.columns:
                reviews = df['Review'].dropna().tolist()
                return reviews, None
            else:
                return None, "Review column not found in the file"
        except Exception as e:
            return None, str(e)

    def analyze_sentiment(self, reviews):
        """
        Calls the Groq API to perform sentiment analysis on each review, handling rate limits.
        """
        try:
            positive_score, negative_score, neutral_score = 0.0, 0.0, 0.0

            for review in reviews:
                while True:
                    try:
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": f"Analyze the sentiment of this review: '{review}'",
                                }
                            ],
                            model="llama3-8b-8192",
                        )

                        # Process the response
                        result = chat_completion.choices[0].message.content.lower()
                        if 'positive' in result:
                            positive_score += 1
                        elif 'negative' in result:
                            negative_score += 1
                        else:
                            neutral_score += 1

                        # Break the loop if the request is successful
                        break

                    except Exception as e:
                        # Check for rate limit error (code 429)
                        if 'rate_limit_exceeded' in str(e):
                            # Extract the retry time from the error message (if available)
                            wait_time = 2  # Default wait time in seconds
                            if 'Please try again in' in str(e):
                                try:
                                    wait_time = float(str(e).split('Please try again in')[1].split('s')[0].strip())
                                except ValueError:
                                    pass

                            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                            time.sleep(wait_time)
                        else:
                            return {'error': str(e)}

            num_reviews = len(reviews)
            return {
                "positive": positive_score / num_reviews if num_reviews else 0,
                "negative": negative_score / num_reviews if num_reviews else 0,
                "neutral": neutral_score / num_reviews if num_reviews else 0
            }
        except Exception as e:
            return {'error': str(e)}

def index(request):
    return render(request, 'index.html')
