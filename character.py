from eliza import Eliza

class Character:
    def __init__(self, scriptfile):
        self.eliza = Eliza()
        self.outputbox = OutputBox()
        self.inputbox = InputBox()
        eliza.load(scriptfile)

    def initiateDialogue(gameState):
        # Put main function of textbox here


    class OutputBox:
        # Call eliza.respond(input)
    
    class InputBox: