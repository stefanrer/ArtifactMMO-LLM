import os
import re
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from parsers import* 
from agent_actions_compact import*

map_parsed = get_resource_map_list()

model = ChatOllama(
    model="llama3.1:70b-instruct-q6_K", temperature=0,
)

local_embeddings = OllamaEmbeddings(model="bge-large:latest")


directory_path = 'vectorstore/map'

if not os.path.exists(directory_path):
    vectorstore_map = FAISS.from_texts(texts=map_parsed, embedding=local_embeddings)
    vectorstore_map.save_local(directory_path)
else:
    vectorstore_map = FAISS.load_local(directory_path, local_embeddings, allow_dangerous_deserialization=True)


#retrieved_docs = vectorstore_map.similarity_search("yellow slime", k=2)
#print(retrieved_docs)


character_name = "Zaur"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFub2tpbSIsInBhc3N3b3JkX2NoYW5nZWQiOiIifQ.OsCHHHu137HfnNhZS_51h-9lazB7zGb_mDeCi00pXqE"
agent_actions = agent_actions_compact(character_name, token)


def create_agent(goal, note):
    
    character_state = get_character_state()

    response = ''
    
    avaliable_actions = '[move(x_coordinare, y_coordinate), fight(), check_inventory(), check_equiped_items(), unequip_item(slot), equip_item(slot, item), check_craftable_items(), craft_item(item)]. Examples of slot: weapon, helmet, boots...'

    system_prompt = f"""You are a part of an agent system that plays video game. You need to achive the goal you are provided with.
        This is information about your character: {character_state}.
        You can request information on the location of objects on the map. To do it write: "Locate <object> on the map of the environment"
        Here is the list of avaliable actions: {avaliable_actions}
        To perform an action just respond with: "Perform action: action". Do not write anything else
        Focus only on the provided goal, do not do anything else.
        Persorm only one action or request at a time.
        If the task is finished write this in the end of your response: "Task done"
        """
    
    question = f"""
        Your goal is: {goal}
        {note}
    """
    
    messages = [
            ("system", system_prompt),
            ("human", f"{question}"),
        ]
    

    additional_data = ''
    while 'task done' not in response.lower():
        
        response_message = model.invoke(messages)
        response = response_message.content
        messages.append(("assistant", f"{response}"))
        print("Agent responce: ", response)

        if 'locate' and 'map' and 'environment' in response_message.content.lower():
            match = re.search(r"Locate (\w+(?: \w+)?) on the map of the environment", response, re.IGNORECASE)
            if match:
                object_name = match.group(1)
                print("Extracted object:", object_name)
                additional_data = vectorstore_map.similarity_search(object_name, k=2) 
                messages.append(("human", str(additional_data)))
            else:
                print("No object found")
            print('map provided') 

        if 'perform action' in response_message.content.lower():
            system_prompt = f"""Your task is to select a relevant action to the query from this list: {avaliable_actions}
            Answer exactly with one action from the list and do not write anything else.
        """
            messages1 = [
                    ("system", system_prompt),
                    ("human", f'query:{response}'),
                ]
            
            action = model.invoke(messages1).content
            print("Action performed: ", action)
            result = execute_action(action, agent_actions)
            messages.append(("human", str(result)))
            print("Action result: ", result)
            #match = re.search(r"perform action: (\w+\(.*?\))|(\w+)", response, re.IGNORECASE)
            #if match:
                # This will get the first matching group that is not None
            #    action = match.group(1) if match.group(1) else match.group(2)
            #    print("Extracted action:", action)
            #    result = execute_action(action, agent_actions)
            #    messages.append(("human", str(result)))
            #    print(result)
            #else:
            #    print("No action found")
            


    return response
#goal = 'Gather information about the map and locate a Yellow Slime'
#create_agent(goal)    