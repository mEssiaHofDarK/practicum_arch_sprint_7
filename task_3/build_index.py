from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader


def main():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", show_progress=True)
    vector_storage = Chroma(
        collection_name="my_d2_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_my_d2_collection_db",
    )
    loader = DirectoryLoader("../task_2/knowledge_base", glob="**/*.txt", show_progress=True)
    docs = loader.load()

    all_splits = text_splitter.split_documents(docs)

    vector_storage.add_documents(documents=all_splits)


if __name__ == "__main__":
    main()
