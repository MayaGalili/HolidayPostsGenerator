from dotenv import load_dotenv
from openai import OpenAI
import json
from pypdf import PdfReader
import gradio as gr
import pandas as pd


load_dotenv(override=True)


def find_my_holiday(date: str):
    df = MarketingDb.holiday_df
    result =df[df['Date'] == date].T.dropna()
    if not result.empty:
        return result.to_dict()
    else:
        return {}


get_holidays_for_date_json = {
    "name": "find_my_holiday",
    "description": "Get the list of holidays for a given date.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The date to look up, in the same format as the table (e.g. 'June 10')"
            }
        },
        "required": ["date"],
        "additionalProperties": False
    }
}


tools = [{"type": "function", "function": get_holidays_for_date_json}]


class MarketingDb:
    holiday_df = pd.read_csv("resources/HolidaysDB.tsv", sep='\t')

class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "LinkedIn Post Generator"

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}" + f" {arguments}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"""
        Your goal is to generate good and interesting LinkedIn posts for an Ag-Tech company via its Marketing help site. 
        The post will be a 'did you know?' or 'fun fact' style post, that will increase the company's engagement.
        Your responsibility is to represent {self.name} for interactions with the marketing team on the website as faithfully as possible.
        Be professional and engaging, as if talking to a co-worker or manager that is using the website.
        If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to post generation.
        If the user is engaging in discussion, try to steer them towards giving you a date that they are interested in; ask for the date they want and, when provided, use your find_my_holiday_json tool to get the holidays for that date.
        If holidays are found, generate 3 LinkedIn post ideas and ask the user to pick their favorite. If no holidays are found, inform the user.
        With this context, please chat with the user, always staying in character as {self.name}.
        """
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
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
    