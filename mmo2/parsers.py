import requests
import itertools
TOKEN = ''
NAME = ''
MAP = []
def get_resource_map(*args):
    url = "https://api.artifactsmmo.com/maps/"
    headers = {"Accept": "application/json"}
    MAP = []
    
    for i in range(1, 5):
        querystring = {"size": "100", "page": f"{i}"}
        response = requests.get(url, headers=headers, params=querystring)
        response_j = response.json()['data']
        MAP.append(response_j)
    
    response_for_llm = ""
    for map_slice in MAP:
        for tile in map_slice:
            name = tile['name']  # Extract the name of the location
            if tile['content']:
                content_type = tile['content']['code']
                object_type = tile['content']['type']
                X = tile['x']
                Y = tile['y']
                response_for_llm += f'{name}, X: {X}, Y: {Y}, Object on tile: {content_type}, Object type: {object_type}\n'
            
    
    return response_for_llm

def get_resource_map_list(*args):
    url = "https://api.artifactsmmo.com/maps/"
    headers = {"Accept": "application/json"}
    resource_map = []  # List to store formatted map entries
    
    # Fetch map data from the API
    for i in range(1, 5):
        querystring = {"size": "100", "page": str(i)}
        response = requests.get(url, headers=headers, params=querystring)
        response_data = response.json()['data']
        
        # Process each tile in the response data
        for tile in response_data:
            if tile['content']:  # Check if there is any content on the tile
                name = tile['name']  # Name of the location
                x = tile['x']
                y = tile['y']
                content_type = tile['content']['code']
                object_type = tile['content']['type']
                entry = f'{name}, X: {x}, Y: {y}, Object on tile: {content_type}, Object type: {object_type}'
                resource_map.append(entry)
    
    return resource_map

#print(get_resource_map_list())

def get_items_list():
    items = []
    url = "https://api.artifactsmmo.com/items/"
    headers = {"Accept": "application/json"}
    pages_num = requests.get(url, headers=headers, params={"size":"100"}).json()['pages']
    for i in range(1,pages_num+1):
        querystring = {"size":"100","page":f"{i}"}
        response = requests.get(url, headers=headers, params=querystring)
        response_j = response.json()['data']
        items.append(response_j)
    items = list(itertools.chain(*items))
    return items
    
def recursive_crafting(items_list, item_code, indent='\t'):
    item = [i for i in items_list if i['code'] == item_code][0]
    result = f"Item: {item['name']}"
    if item['craft']:
        items_for_craft = [i['code'] for i in item['craft']['items']]
        quantities = [i['quantity'] for i in item['craft']['items']]
        result += f", requires to craft skill {item['craft']['skill']} with level {item['craft']['level']} using items {items_for_craft} with quantities {quantities}"
        for i in items_for_craft:
            next_item = recursive_crafting(items_list, i, indent + '\t')
            result += f"\n{indent}Information about component {i}: {next_item}"
    else:
        result += f", is a raw resource with subtype {item['subtype']}"
    return result

def get_crafting_tree(items_list):
    response_for_llm = ""
    for item in items_list:
        if item['craft']:
            response_for_llm += recursive_crafting(items_list, item['code'])
            response_for_llm += '\n'
                
    return response_for_llm

#items_list = get_items_list()
#test = get_crafting_tree(items_list)

#print("items_list", items_list)
#print("test", test)

def recursive_crafting_dict(items_list, item_code):
    item = [i for i in items_list if i['code'] == item_code][0]
    result = f"Item: {item['name']}"
    if item['craft']:
        items_for_craft = [i['code'] for i in item['craft']['items']]
        quantities = [i['quantity'] for i in item['craft']['items']]
        crafted_items = [recursive_crafting(items_list, i) for i in items_for_craft]
        result += (f", requires to craft skill {item['craft']['skill']} "
                   f"with level {item['craft']['level']} "
                   f"using items {crafted_items} in quantities {quantities}")
    else:
        result += f", is a raw resource with subtype {item['subtype']}"
    return result

def get_crafting_tree_dict():
    items_list = get_items_list()
    crafting_tree = {}
    item_names = []
    
    for item in items_list:
        item_names.append(item['name'])  # Add item name to the list
        if item['craft']:
            crafting_tree[item['name']] = recursive_crafting(items_list, item['code'])
                
    return crafting_tree, item_names


def get_monsters_stats():
    monsters = []
    url = "https://api.artifactsmmo.com/monsters/"
    headers = {"Accept": "application/json"}
    pages_num = requests.get(url, headers=headers, params={"size":"100"}).json()['pages']
    for i in range(1,pages_num+1):
        querystring = {"size":"100","page":f"{i}"}
        response = requests.get(url, headers=headers, params=querystring)
        response_j = response.json()['data']
        monsters.append(response_j)
    monsters = list(itertools.chain(*monsters))
    monsters_lists = []
    for i in monsters:
        monsters_lists.append(i['name'])
    return monsters, monsters_lists

if __name__ == '__main__':
    monsters = get_monsters_stats()
    
    
#print(monsters)
    

#items_list = get_items_list()
#items_dict, items_list = get_crafting_tree_dict()

#print("items_list", items_list)
#print("test", items_list)

def get_character_state():

    url = "https://api.artifactsmmo.com/characters/Zaur"

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)

    #print(response.json())
    return response.json()



