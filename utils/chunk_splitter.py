
def chunks_split(text,chunk_size= 400 , chunk_overlap = 100):

    words = text.split()
    chunks = []

    for i in range(0, len(words) , chunk_size - chunk_overlap):

        chunk = words[i:i + chunk_size]
        chunk_str = " ".join(chunk)
        chunks.append(chunk_str)
        

    return chunks
