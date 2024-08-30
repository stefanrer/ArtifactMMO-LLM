import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import ChatOllama


local_embeddings = OllamaEmbeddings(model="bge-large:latest")
model = ChatOllama(
    model="llama3.1:70b-instruct-q6_K", temperature=0
)
monster_stats = {}
monster_names = []
with open("game_data/monsters.json") as j_file:
    monsters = json.load(j_file)
    for monster in monsters['data']:
        monster_names.append(monster['name'])
        monster_type = monster['code']
        monster_level = monster['level']
        monster_hp = monster['hp']
        monster_attack = [monster['attack_fire'], monster['attack_earth'], monster['attack_water'],
                          monster['attack_air']]
        monster_res = [monster['res_fire'], monster['res_earth'], monster['res_water'], monster['res_air']]
        monster_stats[monster['name']] = (f"level {monster_level} monster of type {monster_type}, \n\t"
                                          f"stats: hp: {monster_hp}\n\t"
                                          f"attack_fire: {monster['attack_fire']}, attack_earth: {monster['attack_earth']}, attack_water: {monster['attack_water']}, attack_air: {monster['attack_air']}\n\t"
                                          f"res_fire: {monster['res_fire']}, res_earth: {monster['res_earth']}, res_water: {monster['res_water']}, res_air: {monster['res_air']}")

with open('game_data/char_stats.json', 'r') as f:
    char_data = json.load(f)
    char_hp = char_data['data'][0]['hp']
    char_attack_fire = char_data['data'][0]['attack_fire']
    char_attack_earth = char_data['data'][0]['attack_earth']
    char_attack_water = char_data['data'][0]['attack_water']
    char_attack_air = char_data['data'][0]['attack_air']
    char_dmg_fire = char_data['data'][0]['dmg_fire']
    char_dmg_earth = char_data['data'][0]['dmg_earth']
    char_dmg_water = char_data['data'][0]['dmg_water']
    char_dmg_air = char_data['data'][0]['dmg_air']
    char_res_fire = char_data['data'][0]['res_fire']
    char_res_earth = char_data['data'][0]['res_earth']
    char_res_water = char_data['data'][0]['res_water']
    char_res_air = char_data['data'][0]['res_air']
    current_char_combat_stats = (f"hp: {char_hp}\n\t"
                                 f"attack_fire: {char_attack_fire}, attack_earth: {char_attack_earth}, attack_water: {char_attack_water}, attack_air: {char_attack_air}\n\t"
                                 f"dmg_fire: {char_dmg_fire}, dmg_earth: {char_dmg_earth}, dmg_water: {char_dmg_water}, dmg_air: {char_dmg_air}\n\t"
                                 f"res_fire: {char_res_fire}, res_earth: {char_res_earth}, res_water: {char_res_water}, res_air: {char_res_air}")

print(f"character combat stats: {current_char_combat_stats}")

goal = "kill yellow slime"

vectorstore = Chroma.from_texts(texts=monster_names, embedding=local_embeddings)
retrieved_docs = vectorstore.similarity_search(goal, k=1)
retrieved_item = retrieved_docs[0].page_content
retrieved_monster_stats = monster_stats[retrieved_item]
print(f"retrieved monster stats: {retrieved_monster_stats}")

system_prompt = """Here are all the stats a player can have:
Hit points (HP)
Elemental attacks (fire, water, earth,air)
Elemental damages (fire, water, earth,air)
Elementals resistance (fire, water, earth,air)
Elemental attacks: Attack is the basic stats. Each attack removes one hit point from its opponent.
Elemental damages: Damage increases the attack of an element, it is given by consumables and equipment.
Here's the formula for calculating the effects of damage: Attack * (Damage * 0.01)
For example, if a player has a base attack of 100 and a damage buff of 30, the output damage will be 130. 1 damage buff = 1% extra base damage (1 extra damage using the example above)
Elemental resistances: Resistance reduces the attack damage of its opponent, the more resistance a player/monster has, the more chance he has of blocking the opponent's attacks, it is given by consumables and equipment.
Here's the formula for calculating the effects of damage reduction: Attack * (Resistance * 0.01)
For example, if a monster has a resistance buff of 30 and the player has 100 attack, the monster will block 30 damage. 1 resistance buff = 1% damage reduction (1 less damage using the example above)

Combat is based on a turn-by-turn system. The player always attacks first.
Fights can take a maximum of 100 turns (i.e. 50 attacks for the player, 50 attacks for the monster), otherwise you've automatically lost the fight.

Based on player stats vs monster stats return True or False depending on whether the player wins the fight based on your deduction. I don't want any code.
Don't forget to calculate total damage dealt by both player and monster over turns.
"""
question = f"""
Goal: {goal}
Player stats: {current_char_combat_stats}
Monster stats: {retrieved_monster_stats}
"""

messages = [
    ("system", system_prompt),
    ("human", f"{question}"),
]

response_message = model.invoke(messages)

print(response_message.content)

math_fix_prompt = """You are a math expert, that checks if math in Deduction is correct if not you fix it.
Check if the resistances are applied correctly - monster resistance should be applied to character attack and vice versa.
Check if damage calculation over turns is correct.
Check if Total damage * turns is calculated correctly.
If damage calculation over turns is not provided do it yourself and change the deduction result if it was wrong!
"""

question = f"""
Deduction: {response_message}
"""

messages = [
    ("system", math_fix_prompt),
    ("human", f"{question}")
]

response_message = model.invoke(messages)

print(response_message.content)