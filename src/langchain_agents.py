# 5_langchain_agents.py
# Define LangChain agents: extractor and compliance checker

import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent, AgentType

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model_name="gpt-4o",  # Or "gpt-3.5-turbo" if you want cheaper
    temperature=0
)

# Load Local Vector Database (for compliance policy RAG)
persist_directory = 'data/compliance_rag_db/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# 1. Extractor Agent - Summarize basic client information
extractor_template = PromptTemplate(
    input_variables=["document_text"],
    template="""
You are an information extractor for a bank's compliance department.

Given the following client document text:
{document_text}

Extract and summarize:
- Client Name
- Date of Birth
- Address
- Income
- Employment Status
- ID Number

Return in a clean JSON format.
"""
)
extractor_chain = LLMChain(llm=llm, prompt=extractor_template)

# 2. Compliance Checker Agent - Verify extracted data against compliance rules
def compliance_check(query):
    docs = vectordb.similarity_search(query, k=3)
    combined_text = " ".join([doc.page_content for doc in docs])

    prompt = f"""
You are a compliance officer assistant.

Given the following extracted client information:
{query}

And the following relevant compliance policies:
{combined_text}

Check and answer:
- Does the client's information comply with the policies?
- List any non-compliance areas.
- Provide a compliance score out of 10.

Return in a detailed but concise format.
"""

    response = llm.predict(prompt)
    return response

# Define LangChain Tools for Agents
tools = [
    Tool(
        name="Extract Client Information",
        func=lambda doc_text: extractor_chain.run(document_text=doc_text),
        description="Extracts structured client information from raw document text."
    ),
    Tool(
        name="Check Compliance",
        func=compliance_check,
        description="Checks extracted client information against compliance policies using local knowledge base."
    )
]

# Initialize Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=ConversationBufferMemory(memory_key="chat_history")
)

print("✅ LangChain multi-agent system initialized successfully.")

# Test Run (optional)
if __name__ == "__main__":
    print("\nQuick Agent Test:")
    sample_text = """
    Client Name: John Doe
    Date of Birth: 1985-04-23
    Address: 123 King Street, Sydney NSW
    Income: $55000
    Employment Status: Self-employed
    ID Number: 123-45-6789
    """
    output = agent.run(
        "Extract client information from this document and check compliance:\n" + sample_text
    )
    print("\nFinal Agent Output:\n", output)
