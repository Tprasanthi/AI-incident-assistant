from typing import Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(
    text: str,
    metadata: dict[str, Any],
    chunk_size: int = 1200,
    chunk_overlap: int = 150,
) -> list[dict[str, Any]]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_text(text)

    return [
        {
            "text": chunk,
            "metadata": {
                **metadata,
                "chunk_index": index,
            },
        }
        for index, chunk in enumerate(chunks)
    ]
