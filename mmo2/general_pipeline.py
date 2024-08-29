from langchain_ollama import ChatOllama
from agents import*
import json


def split_items_list(items_list, max_size=2):
    # Split items_list into chunks of max_size
    return [items_list[i:i + max_size] for i in range(0, len(items_list), max_size)]


model = ChatOllama(
    model="llama3:70b-instruct-q6_K", temperature=0, json=True,
)

map_parsed = get_resource_map()
character_state = get_character_state()

history = ''

main_goal = 'kill yellow slime'

# General planner
for step in range(5):
  if step == 0:
    system_prompt = '''You are a main planning agent for a system that plays a video game named Artifactsmmo.  
    The map of the game contains locations with x and y coordinates.
    You have inventory and equipment 
    Do not come up with facts, items, locations and so on,  that is not mentioned directly to you.
    You have low level actions like move to location or fight and so on. 
    You can also give commands to other modules of the system to perform more complicated task like crafting some items that you need to achive your goal.
    Write your answer in the following json format:
    {
      "main_goal": "...",
      "plan_steps": [
        {
          "sub_goal_1": "...",
          "notes_for_sub_goal_1": "...",
        },
        {
          "sub_goal_2": "...",
          "notes_for_sub_goal_1": "...",
        },
        {
          "sub_goal_...": "...",
          "notes_for_sub_goal_1": "...",
        }
      ]
    }
    '''
    question = f"""
        Your main goal is to {main_goal}. Write a hight level plan on how to achive this goal.
        Do not write anything else exept plan in json.
    """
  else:
    system_prompt = '''You are a main planning agent for a system that plays a video game named Artifactsmmo.  
    The map of the game contains locations with x and y coordinates. 
    You have low level actions like move to location or fight or gather and so on. 
    You can also give commands to other modules of the system to perform more complicated task like crafting some items that you need to achive your goal.
    Write your answer in the following json format:
    {
      "main_goal": "...",
      "plan_steps": [
        {
          "sub_goal_1": "...",
          "notes_for_sub_goal_1": "...",
        },
        {
          "sub_goal_2": "...",
          "notes_for_sub_goal_1": "...",
        },
        {
          "sub_goal_...": "...",
          "notes_for_sub_goal_1": "...",
        }
      ]
    }
    '''
    question = f"""
          Character information: {character_state}
          Your main goal is to {main_goal}. Given the history of your interactions with the environment, construct a new high level plan on how to achive your goal. If you can not kill slime you can check avaliable upgrades. 
          History of interactions with environment:{history}
          Do not write anything else exept plan in json.
      """
     
  messages = [
      ("system", system_prompt),
      ("human", f"{question}"),
  ]

  response_message = model.invoke(messages)
  plan0 = response_message.content
  plan = json.loads(response_message.content)
  print(response_message.content)

  result = ''

  for step in plan['plan_steps']:
      for key, value in step.items():
          if key.startswith('sub_goal'):
            sub_goal = value  
          if key.startswith('note'):
            note = value  
          print(f"{key}: {value}")
      
      result = create_agent(sub_goal + result, note)