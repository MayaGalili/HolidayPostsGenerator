from dotenv import load_dotenv
from openai import OpenAI
import json
import gradio as gr

load_dotenv(override=True)

import chromadb
from chromadb.utils import embedding_functions
import os


class MarketingDb:
    with open("resources/HolidaysDB.json", "r", encoding="utf-8") as f:
        holidays_data = json.load(f)




get_holidays_for_date_json = {
    "name": "find_my_holiday",
    "description": "Get the list of holidays for a given date or for an entire month.",
    "parameters": {
        "type": "object",
        "properties": {
            "month": {
                "type": "string",
                "description": "The full month name in English with Capital first letter(e.g. 'June', 'January')."
            },
                "day": {
                "type": "string",
                "description": "The day of the month as a string number (e.g. '10', '2'). If the user asks for the whole month, use 'Full Month'."
            }
        },
        "required": ["month", "day"],
        "additionalProperties": False
    }
}

search_knowledge_base_json = {
    "name": "search_company_knowledge_base",
    "description": "Search the Ag-Tech company's internal articles, products, and case studies for relevant context.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Topic or keyword to search in the knowledge base (e.g. 'soil sensors', 'bees')"
            }
        },
        "required": ["query"],
        "additionalProperties": False
    }
}


tools = [{"type": "function", "function": get_holidays_for_date_json}, 
         {"type": "function", "function": search_knowledge_base_json}]


class KnowledgeBase:

    def __init__(self):
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key_env_var="OPENAI_API_KEY",
            model_name="text-embedding-3-small",
        )
        self.client = chromadb.PersistentClient(path="./chroma_db_data")
        self.collection = self.client.get_or_create_collection(
            name="company_knowledge_base", embedding_function=openai_ef
        )

    def search(self, query: str, top_k: int = 2):
        results = self.collection.query(query_texts=[query], n_results=top_k)
        return results
    
class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "LinkedIn Post Generator"
        self.kb = KnowledgeBase()

    def find_my_holiday(self, month: str, day: str) -> dict:
        print("month:", month, "day:", day)
        print("month:", type(month), "day:", type(day))

        month_formatted = month.capitalize()
        print("found date in db:", MarketingDb.holidays_data[month][day])
        month_data = MarketingDb.holidays_data.get(month_formatted, {})
        results = {}
        if day in month_data:
            results[day] = month_data[day]
            
        if "Full Month" in month_data:
            results["Full Month"] = month_data["Full Month"]

        return results

    def search_company_knowledge_base(self, query: str):
        results =self.kb.search(query)
        return {"context": results['documents'][0]}

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}" + f" {arguments}", flush=True)

            if hasattr(self, tool_name):
                func = getattr(self, tool_name)
                result = func(**arguments)
            else:
                print(f"⚠️ Error: Tool '{tool_name}' not found!")
                result = {"error": f"Tool '{tool_name}' not found."}

            results.append({"role": "tool",
                            "content": json.dumps(result),
                            "tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        return f"""
            You are {self.name}, an AI Marketing Assistant for AgroScout.
            Your task is to generate 3 engaging LinkedIn post ideas connecting awareness days/holidays with AgroScout's technology and solutions.

            STRICT WORKFLOW - YOU MUST FOLLOW THESE STEPS IN ORDER:
            1. When the user gives you a date/month, call `find_my_holiday` to get the list of holidays.
            2. CRITICAL STEP: Once you receive the holiday results, YOU MUST IMMEDIATELY call `search_company_knowledge_base` using keywords from the relevant holidays/topics found (e.g., if you found 'National Potato Day', search for 'potato crop diseases analytics').
            3. DO NOT write the posts until you have received the context from `search_company_knowledge_base`.
            4. Once you have BOTH the holiday data AND the company knowledge base results, write 3 creative LinkedIn post ideas linking the holiday to AgroScout's technology.

            NEVER make up facts about AgroScout without searching the knowledge base first.
        """
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            print("im here...")
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

# Create the Gradio interface for Hugging Face Spaces
me = Me()
demo = gr.ChatInterface(me.chat, type="messages")

if __name__ == "__main__":
    demo.launch()
    