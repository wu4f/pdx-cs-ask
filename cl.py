import chainlit as cl
from query import rag_chain

@cl.on_chat_start
async def on_chat_start():
    logo = cl.Image(name="logo", display="inline", url="https://codelabs.cs.pdx.edu/images/pdx-cs-logo.png")
    await cl.Message(content="", elements=[logo]).send()

    welcome_text = (
        "👋 **Welcome to the Portland State CS Chatbot!**\n\n"
        "Ask me anything about the CS program, courses, or resources at PSU.\n\n"
        "**Here are some things you can try asking:**\n"
        "- How many credits are required for the MS in Computer Science?\n"
        "- Who do I contact for academic advising?\n"
        "- What's the deadline to apply for Fall term?\n"
        "- Tell me about the graduate cybersecurity certificate.\n"
        "- Which faculty work in AI?\n"
    )
    await cl.Message(content=welcome_text).send()

@cl.on_message
async def on_message(message: cl.Message):
    user_query = message.content
    answer = rag_chain.invoke(user_query)
    await cl.Message(content=answer).send()

if __name__ == "__main__":
    cl.run()

