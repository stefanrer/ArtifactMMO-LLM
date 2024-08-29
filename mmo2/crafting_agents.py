import faiss
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from data import*
from parsers import* 

def split_items_list(items_list, max_size=2):
    # Split items_list into chunks of max_size
    return [items_list[i:i + max_size] for i in range(0, len(items_list), max_size)]

model = ChatOllama(
    model="llama3.1:70b-instruct-q6_K", temperature=0,
)

local_embeddings = OllamaEmbeddings(model="bge-large:latest")

items_dict, items_list = get_crafting_tree_dict()

#items_split = split_items_list(items_list)
#create embeddings
vectorstore = Chroma.from_texts(texts=items_list, embedding=local_embeddings)
#for i, items_list1 in enumerate(items_split):
#    if i == 0:
#        vectorstore = FAISS.from_texts(items_list1, embedding=local_embeddings)
#    else:
#        print(items_list1)
#        vectorstore.add_texts(items_list1, embedding=local_embeddings)  

goal = "Craft copper dagger"
#goal = "Craft copper boots"

#retrieve from vectorstore
retrieved_docs = vectorstore.similarity_search(goal, k=1)
retrieved_item = retrieved_docs[0].page_content
print(retrieved_item)
retrieved_instruction = items_dict[retrieved_item]
print(retrieved_instruction)

#Create a plan

system_prompt = """Based on provided information create a specific plan on how to achive a goal. 
Count all items that you need to get to reach your goal, this includes all intermediate. For example, if you need 4 planks to craft a  1boat and 3 wood to craft 1 plank, you need 3 * 4 = 12 wood in total to craft 1 boat. Count all base resources you need to get to craft intended item, pay attention to the "[]" symbols in the information since they hold crafting information for each item

"""
question = f"""
Goal: {goal}
Information: {retrieved_instruction}
"""

messages = [
    ("system", system_prompt),
    ("human", f"{question}"),
]

response_message = model.invoke(messages)

print(response_message.content)

#Find a location

map_parsed = get_resource_map()

#system_prompt = """I will pay you 1000$ if you update the provided resource list with the locations (X and Y). You can incorporate information from the map of the environment on where to find necessary items (from gathering or as a monster drop) and what facilities to use to craft, it is necessary to point just one pair of coordinates. For example, if you're looking for a blue slimeball it is logically can be gathered from blue slimes (they will be mentioned as a blue_slime object).
#"""

system_prompt = """You will be provided with the plan on how to craft item and a map of the environment. Incorporate information to the plan from the map of the environment, on where to find needed items and what facilities to use to craft. Provide all necessary locations in x,y coordinates"""

question = f"""
Plan:  {response_message}
Map of the environment: {map_parsed}"""

messages = [
    ("system", system_prompt),
    ("human", f"{question}"),
]

response_message = model.invoke(messages)

print(response_message.content)

#Create a function
system_prompt = """You are a player that plays a game using api requests. You will be provided with code for actions, that you can perform and a plan, of what you need to do.
Your task is to write the function that will acomplish the goal of the plan.

"""
question = f"""
All actions code starts with:
headers = {{
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer 123"
}}

Code for action move: 
url = "https://api.artifactsmmo.com/my/name/action/move"
payload = {{
    "x": 0,
    "y": 0
}}
response = requests.post(url, json=payload, headers=headers)

Code for action gathering: 
url = "https://api.artifactsmmo.com/my/name/action/gathering"
response = requests.post(url, headers=headers)

Code for action crafting:
url = "https://api.artifactsmmo.com/my/name/action/crafting"
payload = {{
    "code": "string",
    "quantity": 1
}}
response = requests.post(url, json=payload, headers=headers)

Plan: {response_message.content}"""

messages = [
    ("system", system_prompt),
    ("human", f"{question}"),
]

response_message = model.invoke(messages)

print(response_message.content)
