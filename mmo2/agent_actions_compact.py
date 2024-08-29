import requests
import time
import json
class agent_actions_compact():
    
    def __init__(self,character_name,token):
        self.token = token
        self.character_name = character_name
        
    def sleep(self,response_json):
        cooldown = response_json['data']['cooldown']['total_seconds']
        cooldown = int(cooldown)  
        time.sleep(cooldown)
    
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
        
    def unequip_item(self,slot_name):
        NAME = self.character_name
        TOKEN = self.token          
        url = f"https://api.artifactsmmo.com/my/{NAME}/action/unequip"
        payload = {
            "slot": f"{slot_name}",
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
            return 'Item removed from slot'
        
        if 'error' in response_j:
            err_code = response_j['error']['code']
            err_code = int(err_code)      
            
            if err_code == 404:
                return 'No such item in your equipment'
            if err_code == 478:
                return 'Missing item or insufficient quantity'   
            if err_code == 491:
                return 'This slot already empty, update your State information'  
            if err_code == 497:
                return 'Your inventory is full'
            
        return 'Unexpected error, try again'   
    
    def equip_item(self,slot_name,item_name):
        
        NAME = self.character_name
        TOKEN = self.token  
        url = f"https://api.artifactsmmo.com/my/{NAME}/action/equip"

        payload = {
            "code": f"{item_name}",
            "slot": f"{slot_name}",
            "quantity": 1
            }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {TOKEN}"
                    }

        response = requests.post(url, json=payload, headers=headers)
        response_j = response.json()
        
        #print(response_j)

        if 'data' in response_j:
            self.sleep(response_j)
            return 'Item equiped in slot'
        
        if 'error' in response_j:
            err_code = response_j['error']['code']
            err_code = int(err_code)

            if err_code == 404 or err_code == 478: #Пока не очень ясна разница между ошибками
                return 'Cant equip item,no such item in your inventory'
            if err_code == 485:
                return 'This item already equiped'
            if err_code == 472:
                return 'This item is not valid for this slot'
            if err_code == 491:
                return 'This slot is not empty, empty it, then try equiping item again'
            if err_code == 496:
                return 'Character level to low'
            if err_code == 422:
                return 'Provided input not valid for this action'
            
        return 'Unexpected error, try again'                              
    
    def fight(self):
        NAME = self.character_name
        TOKEN = self.token
        url = f"https://api.artifactsmmo.com/my/{NAME}/action/fight"
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization":f"Bearer {TOKEN}"
                    }   
        response = requests.post(url, headers=headers)
        response_j = response.json()
        if 'data' in response_j:
            self.sleep(response_j)
            fight_result = response_j['data']['fight']['result']
            if fight_result == 'lose':
                return 'Fight lost'
            else:
                return 'Fight won'
            
        if 'error' in response_j:
            err_code = response_j['error']['code']
            err_code = int(err_code)
            
            if err_code == 598:
                return 'Mob not found on this tile'
            
        return 'Unexpected error, try again'
    
    def get_map_content(self): 
        MAP = []
        url = "https://api.artifactsmmo.com/maps/"
        headers = {"Accept": "application/json"}
        for i in range(1,5):
            querystring = {"size":"100","page":f"{i}"}
            response = requests.get(url, headers=headers, params=querystring)
            response_j = response.json()['data']
            MAP.append(response_j)
            response_for_llm = ""
        for map_slice in MAP:
            for tile in map_slice:
                if tile['content']:
                    content_type = tile['content']['code']
                    object_type = tile['content']['type']
                    X = tile['x']
                    Y = tile['y']
                    response_for_llm += f'X: {X}, Y: {Y}, Object on tile: {content_type}, Object type: {object_type} \n'
        return response_for_llm
    
    def get_character_info(self): # Распарсить перед подачей в LLM
        NAME = self.character_name
        url = f"https://api.artifactsmmo.com/characters/{NAME}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def check_inventory(self): # Распарсить перед подачей в LLM
        NAME = self.character_name
        url = f"https://api.artifactsmmo.com/characters/{NAME}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        inventory = response.json()['data']['inventory']
        return inventory
    
    def check_craftable_items(self): 
        avaliavle_upgrades = "Items avaliable for crafting: copper_dagger"
        return avaliavle_upgrades
    
    def check_equiped_items(self):
        NAME = self.character_name
        url = f"https://api.artifactsmmo.com/characters/{NAME}"

        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()
        equipment_keys = [
    'weapon_slot', 'shield_slot', 'helmet_slot', 'body_armor_slot', 
    'leg_armor_slot', 'boots_slot', 'ring1_slot', 'ring2_slot', 
    'amulet_slot', 'artifact1_slot', 'artifact2_slot', 'artifact3_slot',
    'consumable1_slot', 'consumable1_slot_quantity', 'consumable2_slot', 'consumable2_slot_quantity'
    ]
        equipment_info = {key: data['data'][key] if data['data'][key] else None for key in equipment_keys}

        # Convert the equipment information to JSON for output
        equipment_json = json.dumps(equipment_info, indent=4)
        return f'Equiped items: {str(equipment_info)}'
    
    def craft_item(self, item):
        # Move to mining location
        result = self.move(2, 0)
        if result != 'Success':
            return f"Failed to move to mining location: {result}"
        
        # Gather Copper Ore
        for _ in range(48):  # You need to mine 48 Copper Ore
            gather_result = self.gather()
            if "Resource gathered" not in gather_result:
                return f"Failed to gather resources: {gather_result}"
        
        # Move to crafting location for Copper
        result = self.move(1, 5)
        if result != 'Success':
            return f"Failed to move to crafting location for Copper: {result}"
        
        # Craft Copper from Copper Ore
        for _ in range(6):  # You need 6 Copper, and each requires 8 Ore
            craft_result = self.craft('copper')
            if "Item crafted" not in craft_result:
                return f"Failed to craft Copper: {craft_result}"
        
        # Move to crafting location for Copper Dagger
        result = self.move(2, 1)
        if result != 'Success':
            return f"Failed to move to crafting location for Copper Dagger: {result}"
        
        # Craft Copper Dagger
        craft_result = self.craft('copper_dagger')
        if "Item crafted" not in craft_result:
            return f"Failed to craft Copper Dagger: {craft_result}"
        
        return "Copper Dagger crafted successfully!"
    
    def craft_item1(self, item):
        print("copper dagger crafted")

    def equip_item1(self, slot, item):
        NAME = self.character_name
        TOKEN = self.token
        url = f"https://api.artifactsmmo.com/my/{NAME}/action/move"
        payload = {
            'x':2,
            'y':1
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
        
        print("copper dagger equiped")
        return 'Unexpected error, try again'    

def execute_action(action_string, agent):
    # Splitting the action and its arguments
    action, args = action_string.split('(')
    args = args.strip(')').split(', ') if args.strip(')') else []  # Clean up and split arguments

    # Converting arguments to their appropriate types, here assumed all to integers
    args = [int(arg) if arg.isdigit() else arg for arg in args]

    # Getting the method from the class based on the action
    method = getattr(agent, action, None)
    
    # If the method exists, call it with the arguments
    if method:
        return method(*args)
    else:
        return "Action not supported"    
    


#character_name = "Zaur"
#token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFub2tpbSIsInBhc3N3b3JkX2NoYW5nZWQiOiIifQ.OsCHHHu137HfnNhZS_51h-9lazB7zGb_mDeCi00pXqE"
#agent_actions = agent_actions_compact(character_name, token)

#print(execute_action('craft_copper_dagger()', agent_actions))