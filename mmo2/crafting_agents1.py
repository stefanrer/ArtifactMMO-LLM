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

vectorstore = Chroma.from_texts(texts=items_list, embedding=local_embeddings)
  
goal = "Craft copper dagger"


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

print(map_parsed)

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

Avaliable functions for separate actions:

def move(self,X,Y):
        NAME = self.character_name
        TOKEN = self.token
        url = f"https://api.artifactsmmo.com/my/{NAME}/action/move"
        payload = {
            'x':X,
            'y':Y
            }
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization":f"Bearer {TOKEN}"
                    }
        response = requests.post(url, json=payload, headers=headers)
        response_j = response.json()
        
        if 'data' in response_j:
            self.sleep(response_j)
            return 'Success'
        if 'error' in response_j:
            err_code = response_j['error']['code']
            err_code = int(err_code)
            
            if err_code == 404:
                return 'No tile with such coodrinates'
            if err_code == 490:
                return 'You already arrived at destination'
    
        return 'Unexpected error, try again'
        
    def gather(self):
        NAME = self.character_name
        TOKEN = self.token        
        url = f"https://api.artifactsmmo.com/my/{NAME}/action/gathering"
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
                }
        response = requests.post(url, headers=headers)
        response_j = response.json()
        
        if 'data' in response_j:
            self.sleep(response_j)
            return 'Resource gathered'
 
        if 'error' in response_j:
            err_code = response_j['error']['code']
            err_code = int(err_code)
            
            if err_code == 598:
                return 'No resource on this tile'
            if err_code == 493:
                return 'You cant mine this resource, skill level to low'
            if err_code == 497:
                return 'Your inventory is full'
            
        return 'Unexpected error, try again'
                
        
    def craft(self,recepie_name):
        NAME = self.character_name
        TOKEN = self.token   
        url = f"https://api.artifactsmmo.com/my/{NAME}/action/crafting"
        payload = {
            "code": f"{recepie_name}",
            "quantity": 1
                }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {TOKEN}"
                    }
        response = requests.post(url, json=payload, headers=headers)
        response_j = response.json()
        
        if 'data' in response_j:
            self.sleep(response_j)
            return 'Item crafted'
        
        if 'error' in response_j:
            err_code = response_j['error']['code']
            err_code = int(err_code)
            
            if err_code == 404:
                return 'No such craft recepie'
            if err_code == 478:
                return 'Missing item or insufficient quantity'
            if err_code == 493:
                return 'You cant craft this item, skill to low'
            if err_code == 497:
                return 'Your inventory is full'
            if err_code == 598:
                return 'No workshop on tile where you stand'
            
        return 'Unexpected error, try again'
"""
question = f"""
Plan: {response_message.content}"""

messages = [
    ("system", system_prompt),
    ("human", f"{question}"),
]

response_message = model.invoke(messages)

print(response_message.content)
