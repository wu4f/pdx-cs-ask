from flask import redirect, request, url_for, render_template, session
from flask.views import MethodView
from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import re

def format_docs(docs):
    output = "\n\n".join(doc.page_content for doc in docs)
    sources = {doc.metadata['source'] for doc in docs}
    source_list = "\nSource: ".join(source for source in sources)
    return output+source_list

class Query(MethodView):
    def get(self):
        return render_template('query.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        vectorstore = Chroma(
                embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
                persist_directory="./.chromadb"
        )
        llm = GoogleGenerativeAI(model="gemini-1.5-flash")
        retriever = vectorstore.as_retriever()

        prompt_template = """You are an assistant for question-answering tasks. Use the following context to answer the question.  Provide the source URLs of the context you used to perform the task and instruct the user to visit them for more information.  If you don't know the answer, just say that you don't know.

Question: {question}

Context: {context}

Answer: """

        # create a prompt example from above template
        prompt = PromptTemplate(
            input_variables=["question"],
            template=prompt_template
        )
 
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        answer = rag_chain.invoke(request.form['message'])
        return render_template('query.html',question=request.form['message'],answer=answer)
