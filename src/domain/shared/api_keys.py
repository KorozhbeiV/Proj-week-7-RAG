"""
Use this file to reach necessary secrets from your .env file
"""

import dotenv
import os

dotenv.load_dotenv()

# Uses 'environ' instead of 'getenv' to raise a KeyError if there's no declared API key
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
QDRANT_API_KEY = os.environ['QDRANT_API_KEY']
QDRANT_CLASTER_ENDPOINT = os.environ['QDRANT_CLASTER_ENDPOINT']