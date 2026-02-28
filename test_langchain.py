try:
    from langchain_core.embeddings import Embeddings
    print("langchain_core is present")
except Exception as e:
    print(f"Error: {e}")
