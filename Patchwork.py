from graphics import *

def main():
    size, colours = getInputs()
    win = GraphWin("PatchWork", size * 100, size * 100)
    win.setCoords(0, 0, size, size)
    instructions(win, size)
    patches, patchType = drawPatchWork(win, size, colours)
    switchPatches(win, patches, size, patchType, colours)
        
def getInputs():
    #gets the size of the patchwork and the 3 colours
    valid = False
    colours = []
    validcolours = ["red", "green", "blue", "magenta", "cyan", "orange", "brown", "pink"] 
    while not valid:
        size = input("What size patchwork would you like? (5, 7, 9 or 11): ")
        if size.isdigit():
            size = eval(size)
            if size == 5 or size ==7 or size == 9 or size == 11 :
                valid = True
            else: 
                print("please put a valid size")
                print(size)
        else:
            print("please put a valid number, (5, 7, 9 or 11)")
            size = input("What size patchwork would you like? (5, 7, 9 or 11): ")
    print("Please choose 3 colours (red, green, blue, magenta, cyan, orange, brown or pink): ")
    for i in range(3):
        colour = input("Input colour: ")
        while colour not in validcolours or colour in colours:
            colour = input("Please put a valid colour: ")
        colours.append(colour)
    colours = colours * size**2
    return size, colours

def instructions(win, size):
    #displays user instructions
    message = Text(Point(size/2,size/2),"Click two patches to switch them \n or Click the same patch twice to change the design\n\n Click to Continue")
    message.draw(win)
    win.getMouse()
    message.undraw()

def drawPatchWork(win, size, colours):
    #draws the original patch work
    patches = [] #stores each of the patches to be drawn
    patchType = [] #stores the type of each patch (patch1 or patch2) relative to the positions of patches
    count = 0
    for i in range(size):
        for j in range(size):
            if i == j:
                patches.append(patch2(win, j, i,colours[count]))
                patchType.append("patch2")
            else:
                patches.append(patch1(win, j, i,colours[count]))
                patchType.append("patch1")
            count = count + 1
    for patch in patches:
        for part in patch:
            part.draw(win)
    return patches, patchType

def patch1(win, x, y,colour):
    #draws rectangles that increase in height along the x axis
    x1 = x
    y1 = y
    x2 = x1 + 0.1
    y2 = y1 + 0.1
    patch = []
    s = Rectangle(Point(x1, y1), Point(x1 + 1, y1 + 1))
    s.setFill("white")
    s.setOutline("")
    patch.append(s)
    for i in range(10):
        r = Rectangle(Point(x1+(i*0.1), y1), Point(x2 + (i*0.1), y2 + (i*0.1)))
        r.setFill(colour)
        r.setOutline(colour)
        patch.append(r)
    return patch
            
def patch2(win, x, y, colour):
    #draws rectangle first then triangle over it. Rectangle width 0.2, height, 0.1
    colours = [colour, "white"] * 5
    patch = []
    for i in range(10):
        for j in range(0,10,2):
            if colours[i] == colour:
                colour2 = "white"
            else:
                colour2 = colour
            r = Rectangle(Point(x + (j*0.1),y + (i*0.1)), Point(x+((j+2)*0.1),y+((i + 1)*0.1)))
            r.setFill(colours[i])
            r.setOutline("")
            t = Polygon(Point(x+(j*0.1),y+(i*0.1)), Point(x+((j+1)*0.1), y+((i+1)*0.1)), Point(x+((j+2)*0.1), y+(i*0.1)))
            t.setFill(colour2)
            t.setOutline("")
            patch.append(r)
            patch.append(t)
    return patch
    
def switchPatches(win, patches, size, patchType, colours):
    #function to switch patches and patch designs
    exit = False

    while not exit:
        #gets the two points that are clicked 
        point1 = win.getMouse()
        point2 = win.getMouse()
        patchA = Point(int(point1.getX()),int(point1.getY())) 
        patchB = Point(int(point2.getX()), int(point2.getY())) 
        a = locatePatch(size, patchA)
        b = locatePatch(size, patchB)
        if a != b: # if the two patches clicked are different they switch
            colourA = colours[a] #changes the colours of the patches in the colours list
            colours[a] = colours[b]
            colours[b] = colourA
            for part in patches[a]: #undraws the patches so they can be replaced
                part.undraw()
            for part in patches[b]:
                part.undraw()
            if patchType[b] == "patch1": #check the patch type so that the correct function is used to pass the variables
                patches[a] = patch1(win, patchA.getX(), patchA.getY(), colours[a])
                temp = "patch1" #stored to temp as patch a needs to not be changed for the if statement below
            else:
                patches[a] = patch2(win, patchA.getX(), patchA.getY(), colours[a])
                temp = "patch2"
            if patchType[a] == "patch1":
                patches[b] = patch1(win, patchB.getX(), patchB.getY(), colours[b])
                patchType[b] = "patch1"
            else:
                patches[b] = patch2(win, patchB.getX(), patchB.getY(), colours[b])
                patchType[b] = "patch2"
            patchType[a] = temp
            for part in patches[a]: #draws the components f the patch that changed
                part.draw(win)
            for part in patches[b]:
                part.draw(win)
        else: #if the two patches clicked are the same, the patern switches
            for part in patches[a]:
                part.undraw()
            if patchType[a] == "patch1":
                patches[a] = patch2(win, patchA.getX(), patchA.getY(), colours[a])
                patchType[a] = "patch2"
            else:
                patches[a] = patch1(win, patchA.getX(), patchA.getY(), colours[a])
                patchType[a] = "patch1"
            for part in patches[a]:
               part.draw(win)
    
def locatePatch(size, patch):
    #loops through the patches to give an integer location value
    location = 0
    for i in range(size):
        for j in range(size):
            if patch.getX() == j and patch.getY()== i:
                return location
            else:
                location = location + 1
main()