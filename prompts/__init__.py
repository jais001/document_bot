from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


## Prompt Template
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise. Donot use your own knowledge to provide answer."
    "\n\n"
    "{context}"
)

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


PROMPT_TEMPLATE_WITH_HISTORY = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. Answer
    like a human using the following pieces of retrieved context to answer the question. 
If you don't know the answer, say that you 
don't know. Use three sentences maximum and keep the
answer concise. Donot use your own knowledge to provide answer.

#Previous Chat History:
{chat_history}

#Question: 
{question} 

#Context: 
{context} 

#Answer:"""
)
