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
            self.eliza.combined_script += content
    
    def load(self):
        self.eliza.load()

    def initiateDialogue(self, gameState):
        # Put main function of textbox here
        pass

"""
    class OutputBox:
        # Call eliza.respond(input)
    
    class InputBox:
    
"""