import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
class ProductRAGGenerator:
    def __init__(self, temperature=0.3):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature)

        self.prompt_template = PromptTemplate.from_template("""
You are a helpful assistant for a fashion recommendation chatbot.

User Query: "{query}"

Here are some matching products:
{product_context}

Based on the user's request, choose the 5 most relevant items. Explain why they match, and include the product name, brand, and a clickable link.

Answer in a clear and friendly tone, if the link does not contain the name of the product in the query apologize and state that there is no match.
""")

    def generate(self, query, documents):
        product_context = ""
        for doc in documents:
            product_context += f"- {doc.metadata['title']} by {doc.metadata['brand']} - {doc.metadata['url']}\n  {doc.page_content}\n"

        prompt = self.prompt_template.format(query=query, product_context=product_context)
        return self.llm.invoke(prompt)