# ingestion/chunking.py
#input data is broken down to chunks
#there is an overlap mechanism implemented to maintain context between chunks, but overlapping is not applicable
   #here since each record is handled in seperate
#there is one chunking strategy that can be implemented here. Each chunk can be summerized and shortened, thus cutting cost used in tokenization
from typing import List, Dict

#transforms json record into a singular text
def json_to_text(record: Dict) -> str:
    """
    Converts a structured JSON record into readable text.
    """
    sections = []

    for key, value in record.items():
        if value is None:
            continue

        section = f"{key.replace('_', ' ').title()}: {value}"
        sections.append(section)

    return "\n".join(sections)

#function for chunking the text
def chunk_text(
    text: str,
    chunk_size: int = 80, #defins chunk size, which is approximatley 80 words
    chunk_overlap: int = 10 #overlapping not neccessary since each record is a singular chunk, but it is still kept here for for good measure incase a record exceeds chunk size
) -> List[str]:
    """
    Splits text into overlapping word-based chunks.
    """
    words = text.split()

    #checks for overlap. used for evaluation
    if len(words) <= chunk_size:
        print("Overlap ignored")
        return [text]  # no overlap needed
    else:
        print("overlapped!")

    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start = end - chunk_overlap

    return chunks

#transforms json records into chunks
def chunk_json_record(record: Dict) -> List[str]:
    """
    End-to-end: JSON record → text → chunks
    """
    text = json_to_text(record)
    return chunk_text(text)
