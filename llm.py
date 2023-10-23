import glob
import os
import re
import warnings
import numpy as np
import pandas as pd
import textract
from PyPDF2 import PdfReader
from tenacity import retry, stop_after_attempt, wait_random_exponential
from vertexai.language_models import TextEmbeddingModel, TextGenerationModel

warnings.filterwarnings("ignore")

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def text_generation_model_with_backoff(**kwargs):
    return generation_model.predict(**kwargs).text


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def embedding_model_with_backoff(text=[]):
    embeddings = embedding_model.get_embeddings(text)
    return [each.values for each in embeddings][0]

def create_data_packet(file_name, file_type, page_number, file_content):
    """Creating a simple dictionary to store all information (content and metadata)
    extracted from the document"""
    data_packet = {}
    data_packet["file_name"] = file_name
    data_packet["file_type"] = file_type
    data_packet["page_number"] = page_number
    data_packet["content"] = file_content
    return data_packet

def files(path):
    """
    Function that returns only filenames (and not folder names)
    """
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def get_file_data():
  final_data = []
 
  for file_name in files("documents/"):
      path = f"documents/{file_name}"
      _, file_type = os.path.splitext(path)
      if file_type == ".pdf":
          # loading pdf files, with page numbers as metadata.
          reader = PdfReader(path)
          for i, page in enumerate(reader.pages):
              text = page.extract_text()
              if text:
                  packet = create_data_packet(
                      file_name, file_type, page_number=int(i + 1), file_content=text)
                  final_data.append(packet)
      else:
          # loading other file types
          text = textract.process(path).decode("utf-8")
          packet = create_data_packet(
              file_name, file_type, page_number=None, file_content=text
          )
          final_data.append(packet)

  pdf_data = pd.DataFrame.from_dict(final_data)
  pdf_data = pdf_data.sort_values(
          by=["file_name", "page_number"]
  )  # sorting the datafram by filename and page_number
  pdf_data.reset_index(inplace=True, drop=True)
  return(pdf_data)

class Model():
    def __init__(self):
        #self.generation_model = TextGenerationModel.from_pretrained("text-bison@001")
        #self.embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        self.pdf_data = get_file_data()

    def query(self, question):
        return 'result from llm'

myllm = Model()
