import os
from groq import Groq

class LLMClient:
    def __init__(self):
        # Try to get API key from environment variables (set by Docker)
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"
    
    def generate_answer(self, question: str, context: list) -> str:
        """Generate answer using LLM with context"""
        # Prepare context text
        context_text = "\n\n".join([doc['text'] for doc in context])
        
        # Create prompt
        prompt = f"""
        You are an HR assistant. Answer the question based only on the provided context.
        If you don't know the answer, say "I don't have information about that in the HR policy."
        
        Context:
        {context_text}
        
        Question: {question}
        
        Answer:
        """
        
        try:
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful HR assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1024
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating answer: {str(e)}"