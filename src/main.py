from src.data_retrieve import WaitTimeDataRetriever
from datetime import datetime

if __name__ == '__main__':
    data_retriever = WaitTimeDataRetriever()
    data_retriever.retrieve(begin_datetime=datetime(2022, 11, 8), verbose=True)
