# src/extraction.py
import os
import json
from typing import Optional, Dict

from dotenv import load_dotenv
from groq import Groq

from .validation import validate_extracted_json
from .prompt_template import build_prompt


# Load environment variables (API key)
load_dotenv()

# Create Groq client once (efficient)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_llm_on_chunk(chunk_text: str, max_retries: int = 1) -> Optional[Dict]:
    """
    Send a chunk of text to Groq (LLaMA 3) for structured JSON extraction.

    Parameters
    ----------
    chunk_text : str
        A single text chunk from the document.
    max_retries : int, optional
        How many times to retry if JSON parsing fails.

    Returns
    -------
    dict or None
        A validated dictionary matching the JSON schema,
        or None if extraction fails.
    """

    # Build the final prompt with the chunk text inserted
    prompt = build_prompt(chunk_text)

    # Try extraction up to max_retries times
    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are a JSON extraction assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0
            )

            # Extract content string from LLM
            content = response.choices[0].message["content"]

            # Attempt to parse JSON
            data = json.loads(content)

            # Validate JSON structure and controlled vocabularies
            validated = validate_extracted_json(data)
            return validated

        except Exception as e:
            print(f"Attempt {attempt + 1}: Error during extraction or parsing: {e}")

    # If we reach this point, all retries failed
    return None
