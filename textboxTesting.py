import pygame as pg
from pygame.locals import *
import sys
import time
from threading import Timer

pg.init()

WHITE=(255,255,255)
blue=(0,0,255)
black = (0, 0, 0)

screen = pg.display.set_mode((640, 480),0, 32)
screen.fill(WHITE)
pg.display.update()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
textSize = 25
FONT = pg.font.Font(None, textSize)
screenWidth, screenHeight = pg.display.get_surface().get_size()
textEdgeBufferW = 40
textEdgeBufferH = 20
backspacePressed = False
backspaceStart = time.time()
currentDialogue = 1
script = {1:"i want to talk to you",2:"its important",3:"i think you are pregnant"}

class OutputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    #args = self, dialgue, letter_i
    
    def scrolling(args):
        #myself = args.self
        dialogue = args.dialogue
        letter_i = args.letter_i

        print(self.text)
        self.text = dialogue[:letter_i]
        # Re-render the text.
        self.txt_surface = FONT.render(self.text, True, self.color)

        if len(self.text) < len(dialogue):
            #time.sleep(.5)
            #self.scrolling(dialogue, letter_i+1)
            
            t = Timer(0.5, self.scrolling(),args=(self, dialogue, letter_i+1)).start()

    def handle_event(self, event):

        global currentDialogue

        #load the next dialogue text if available
        if event.type == pg.KEYDOWN:   
  
            if event.key == pg.K_q:
                #Timer(0.5, self.scrolling(),args=(self, dialogue, letter_i+1)).start()
                
                
                self.text = ""
                # erase the text
                pg.draw.rect(screen, (50,50,50), self.rect)
                if currentDialogue <= len(script):
                    for letter in script[currentDialogue]:
                        self.text = self.text + letter
                    
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.color)
                    #    time.sleep(.1)

                    currentDialogue += 1
                else:
                    bob = True
                    #what to do when they are done talking?

    def update(self):
        global backspaceStart
        # Resize the box if the text is too long.
        #if self.txt_surface.get_width() < screenWidth - textEdgeBufferW/2:
        #    width = max(200, self.txt_surface.get_width()+10)
        #    self.rect.w = width
                
    def draw(self, screen):
        pg.draw.rect(screen, (50,50,50), self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global backspacePressed, backspaceStart
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text) #<<<<<<<<<<<<<<<<<<<<<<< here is where a character's eliza responds
                    #handleAI(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    backspacePressed = True
                    backspaceStart = time.time()
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        if event.type == pg.KEYUP:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    backspacePressed = False

    def update(self):
        global backspacePressed, backspaceStart
        # Resize the box if the text is too long.
        #if self.txt_surface.get_width() < screenWidth - textEdgeBufferW/2:
        #    width = max(200, self.txt_surface.get_width()+10)
        #    self.rect.w = width

        #for debugging backspace
        #print(str(backspacePressed)+" "+str(backspaceStart))

        #delete characters when holding backspace down
        if time.time() - backspaceStart > 0.35:
            if backspacePressed:
                backspaceStart += .05
                self.text = self.text[:-1]
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def main():

    #DISPLAY=pg.display.set_mode((640, 480),0,32)

    screen.fill(WHITE)
    me = pg.image.load('assets/princess.png')
    screen.blit(me, (200,150,25,25))
    pg.display.update()

    done = False
    #overlay the dialogue tools onto the screen
    def overlay():
        global screenWidth, screenHeight

        #fade in to black
        for i in range(1, 100):
            s=pg.Surface((screenWidth,screenHeight), pg.SRCALPHA)
            s.fill((0,0,0,i/20))
            screen.blit(s, (0,0))
            pg.display.update()
            time.sleep(.00001)

        #instantiate text boxes
        clock = pg.time.Clock()
        output_box = OutputBox(textEdgeBufferW/2, screenHeight - textEdgeBufferH - textSize*3, screenWidth - textEdgeBufferW, textSize*2)
        input_box2 = InputBox(textEdgeBufferW/2, screenHeight - textEdgeBufferH - textSize, screenWidth - textEdgeBufferW, textSize)
        text_boxes = [output_box, input_box2]   
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        done = True
                        #hide overlay after done with loop

                for box in text_boxes:
                    box.handle_event(event)

            for box in text_boxes:
                box.update()

            #screen.fill((30, 30, 30))
            for box in text_boxes:
                box.draw(screen)

            pg.display.flip()
            clock.tick(30)
            print(done)
        return


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    #give controls to overlay textbox
                    overlay()
                    #give controls to movement
                    s=pg.Surface((screenWidth,screenHeight))
                    s.fill(WHITE)
                    screen.blit(s, (0,0))
                    #screen.fill(WHITE)
                    pg.display.update()
                    break


                


if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()











    #this function brings up the dialogue
    #littlegirl.initiateDialogue(gameState)

    #def initiateDialogue(thisGameState, who):

