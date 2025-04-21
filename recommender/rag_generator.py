from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ProductRAGGenerator:
    def __init__(self, model_name="tiiuae/falcon-rw-1b", max_new_tokens=200):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
        self.model.eval()
        self.max_new_tokens = max_new_tokens

    def generate(self, query, documents):
        product_context = ""
        for doc in documents:
            product_context += f"- {doc.metadata['title']} by {doc.metadata['brand']} - {doc.metadata['url']}\n  {doc.page_content}\n"

        prompt = f"""
You are a helpful assistant for a fashion recommendation bot.

User Query: "{query}"

Here are some matching products:
{product_context}

Based on the user request, choose the 2-3 most relevant items. Explain why they match, and include the product name, brand, and a clickable link.
Answer:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
                outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=self.max_new_tokens,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)