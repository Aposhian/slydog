from eliza import Eliza

class Character:
    def __init__(self, scriptfile, name):
        self.name = name
        self.eliza = Eliza()
        self.outputbox = OutputBox()
        self.inputbox = InputBox()
        self.leadinfulfilled = False

        eliza.load(scriptfile)

    def initiateDialogue(gameState):
        # Put main function of textbox here


    class OutputBox:
        # Call eliza.respond(input)
    
    class InputBox: