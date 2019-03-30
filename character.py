from eliza import Eliza

class Character:
    def __init__(self, name, avatar, sprite, scriptfile):
        self.name = name
        self.avatar = avatar
        self.sprite = sprite
        self.eliza = Eliza()
        #self.outputbox = OutputBox()
        #self.inputbox = InputBox()
        self.leadinfulfilled = False
        with open(scriptfile) as character_script:
            content = character_script.read()
            eliza.combined_script.append(content)
    
    def load(self):
        eliza.load()

    def initiateDialogue(self, gameState):
        # Put main function of textbox here

"""
    class OutputBox:
        # Call eliza.respond(input)
    
    class InputBox:
    
"""