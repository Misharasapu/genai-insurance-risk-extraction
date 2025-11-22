from typing import List


def chunk_text(
    text: str,
    max_words: int = 250,
    overlap: int = 50,
) -> List[str]:
    """
    Split a long text into overlapping chunks based on word count.

    Parameters
    ----------
    text : str
        The full document text as a single string.
    max_words : int, optional
        Maximum number of words in each chunk. Default is 250.
    overlap : int, optional
        Number of words that overlap between consecutive chunks.
        Default is 50.

    Returns
    -------
    List[str]
        A list of text chunks. Each chunk is a string containing
        up to max_words words, with overlap between neighbours.

    Raises
    ------
    ValueError
        If overlap is greater than or equal to max_words.
    """
    # Split the text into a list of words using whitespace
    words = text.split()

    # If the document is empty, return an empty list of chunks
    if not words:
        return []

    # Overlap must be smaller than the chunk size to make progress
    if overlap >= max_words:
        raise ValueError("overlap must be smaller than max_words")

    chunks: List[str] = []
    start = 0

    # Slide a window over the list of words
    while start < len(words):
        end = start + max_words

        # Select the slice of words for this chunk
        chunk_words = words[start:end]

        # Join the words back into a string
        chunk_text_str = " ".join(chunk_words).strip()

        # Only append non empty chunks
        if chunk_text_str:
            chunks.append(chunk_text_str)

        # Move the start index forward, keeping the desired overlap
        start = start + max_words - overlap

    return chunks
