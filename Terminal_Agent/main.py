from interfaces import MyCharactersAPI
from controller.agent import Agent

if __name__ == "__main__":
    my_characters = MyCharactersAPI().get_all_characters()
    agent = Agent(my_characters[0])
    agent.run()
