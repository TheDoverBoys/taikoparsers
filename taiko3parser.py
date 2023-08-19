import sys, os, json, pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet.app import run
from pyglet import image

width, height= 640, 480
window = Window(caption="Taiko 3 Chart Viewer", width=width,height=height)
batch = pyglet.graphics.Batch()
helpbatch = pyglet.graphics.Batch()
sprites = []

temp1 = 0
temp2 = 0
temp3 = False

def everything(file):
    if os.path.isfile(file):
        arquivo = open(file,"rb")
        bindata = arquivo.read()
        jsonx = []
        chunksize = 324
        measure = 1
        if bindata[:4] != b'\x25\x10\x01\x00':
            print('Header mismatch! Are you sure this is a Taiko 3 chart?')
            exit()
        else:
            while True:
                jsony = ''
                increment = chunksize*(measure-1)

                branch1 = bindata[4+increment:8+increment]
                branch2 = bindata[8+increment:12+increment]

                if branch1 == b'\xFE\xFF\xFF\xFF':
                    return jsonx
                elif branch1 == b'\xFF\xFF\xFF\xFF':
                    branch1 = None
                else:
                    branch1 = int.from_bytes(branch1, "little")


                if branch2 == b'\xFF\xFF\xFF\xFF':
                    branch2 = None
                else:
                    branch2 = int.from_bytes(branch2, "little")

                offset = int.from_bytes(bindata[12+increment:14+increment], "little")

                barvis = bindata[14+increment] == 1

                tempo = bindata[15+increment]

                bal1quan = bindata[32+increment:34+increment]
                bal1leng = bindata[34+increment:36+increment]
                bal2quan = bindata[36+increment:38+increment]
                bal2leng = bindata[38+increment:40+increment]
                if (bal1quan == b'\xFF\xFF'):
                    bal1quan = None
                    bal1leng = None
                else:
                    bal1quan = int.from_bytes(bal1quan, "little")
                    bal1leng = int.from_bytes(bal1leng, "little")
                if (bal2quan == b'\xFF\xFF'):
                    bal2quan = None
                    bal2leng = None
                else:
                    bal2quan = int.from_bytes(bal2quan, "little")
                    bal2leng = int.from_bytes(bal2leng, "little")
                
                norbranch1 = branchparser(bindata[40+increment:88+increment])
                expbranch1 = branchparser(bindata[88+increment:136+increment])
                masbranch1 = branchparser(bindata[136+increment:184+increment])
                norbranch2 = branchparser(bindata[184+increment:232+increment])
                expbranch2 = branchparser(bindata[232+increment:280+increment])
                masbranch2 = branchparser(bindata[280+increment:328+increment])
                jsony = json.dumps({'ABQ':branch1, 'MBQ':branch2, 'FOF':offset, 'BAR':barvis, 'TMP':tempo, 'BQO':bal1quan, 'BLO':bal1leng, 'BQT':bal2quan, 'BLT':bal2leng, 'ONB':norbranch1, 'OAB':expbranch1, 'OMB':masbranch1, 'TNB':norbranch2, 'TAB':expbranch2, 'TMB':masbranch2})

                jsonx.append(json.loads(jsony))
                measure+=1
    else:
        print("This is not a file!")
        exit()

def branchparser(area):
    split = [area[i] for i in range (0, len(area))]
    return split

def viewer(a, mn):
    chartlookup = {
        0: 'ONB',
        1: 'OAB',
        2: 'OMB',
        3: 'TNB',
        4: 'TAB',
        5: 'TMB'
    }
    
    for i in [mn]:
        for j in range(47, -1, -1):
            for k in range(6):
                imgdefine = a[i].get(chartlookup[k])[j]
                match imgdefine:
                    case (1 | 2 | 3): imgdefined = 'note01.png'
                    case (5 | 6 | 7): imgdefined = 'note05.png'
                    case (9 | 10 | 11): imgdefined = 'note09.png'
                    case (13 | 14 | 15): imgdefined = 'note13.png'
                    case (17 | 18 | 19): imgdefined = 'note17.png'
                    case 21: imgdefined = 'note21.png'
                    case 22:
                        if j == 47:
                            if (i < len(a)-1 and a[i+1].get(chartlookup[k])[0]) == 22: imgdefined = 'note22b.png'
                            else: imgdefined = 'note22c.png'
                        elif(j != 47 and a[i].get(chartlookup[k])[j+1] != 22 and a[i].get(chartlookup[k])[j-1] == 22): imgdefined = 'note22c.png'
                        elif j == 0:
                            if (i > 0 and a[i-1].get(chartlookup[k])[47]) == 22: imgdefined = 'note22b.png'
                            else: imgdefined = 'note22a.png'
                        elif(j != 0 and a[i].get(chartlookup[k])[j-1] != 22 and a[i].get(chartlookup[k])[j+1] == 22): imgdefined = 'note22a.png'
                        else: imgdefined = 'note22b.png'
                    case 23:
                        if j == 47:
                            if (i < len(a)-1 and a[i+1].get(chartlookup[k])[0]) == 23: imgdefined = 'note23b.png'
                            else: imgdefined = 'note23c.png'
                        elif(j != 47 and a[i].get(chartlookup[k])[j+1] != 23 and a[i].get(chartlookup[k])[j-1] == 23): imgdefined = 'note23c.png'
                        elif j == 0:
                            if (i > 0 and a[i-1].get(chartlookup[k])[47]) == 23: imgdefined = 'note23b.png'
                            else: imgdefined = 'note23a.png'
                        elif(j != 0 and a[i].get(chartlookup[k])[j-1] != 23 and a[i].get(chartlookup[k])[j+1] == 23): imgdefined = 'note23a.png'
                        else: imgdefined = 'note23b.png'
                    case 24: imgdefined = 'note24.png'
                    case 25: imgdefined = 'note25.png'
                    case 26: imgdefined = 'note26.png'
                    case 27: imgdefined = 'note27.png'
                    case 0: imgdefined = None
                    case _:
                        print("Invalid note type!")
                        exit()
                if (imgdefined != None):
                    pic = image.load(imgdefined)
                    posx = 2+(12*j)
                    posy = height-60-((k+1)*51)
                    spri = pyglet.sprite.Sprite(pic, posx, posy, batch = batch)
                    sprites.append(spri)

def textrender(a, xpos, ypos):
    label = pyglet.text.Label(a,
                            font_name = 'Courier New',
                            font_size = 10,
                            color = (255,255,255,255),
                            x = xpos, y = ypos)
    label.draw()

def masstrender():
    global chart
    global temp1
    global temp2
    global temp3
    advbr = chart[temp1].get('ABQ')
    masbr = chart[temp1].get('MBQ')
    advbrt = "Advanced Quota: " + str(advbr)
    masbrt = "Master Quota:   " + str(masbr)
    
    tempo = 14400/(chart[temp1].get('TMP'))
    bint = 60/tempo
    mint = bint*4
    pint = mint+(bint*(temp2/12))
    divis = "Beat: " + str(temp2) + "/48"
    tempot = "BPM:           " + str(tempo)
    offset = (chart[temp1].get('FOF'))/98.438121
    if temp1 < len(chart)-1:
        nxtint = (((chart[temp1+1].get('FOF'))/98.438121)+(60/(14400/(chart[temp1+1].get('TMP')))*4))-(offset+pint)
    else:
        nxtint = (bint*8)-pint
    offsett = "First Offset:  " + str(offset)
    roffset = "Reach Offset:  " + str(offset+mint)
    poffset = "Posit Offset:  " + str(offset+pint)
    meast = "Measure: " + str(temp1+1) + " / " + str(len(chart))
    nxtintt = "Next Interval: " + str(nxtint)
    
    ubalq = chart[temp1].get('BQO')
    uball = chart[temp1].get('BLO')
    dbalq = chart[temp1].get('BQT')
    dball = chart[temp1].get('BLT')
    ubalqt = "1P Bal. Quant.: " + str(ubalq)
    uballt = "1P Bal. Length: " + str(uball)
    if uball != None: uballt += " / " + str(uball/60)
    dbalqt = "2P Bal. Quant.: " + str(dbalq)
    dballt = "2P Bal. Length: " + str(dball)
    if dball != None: dballt += " / " + str(dball/60)
    
    textrender(meast, 10, 460)
    textrender(divis, 330, 460)
    textrender(advbrt, 10, 450)
    textrender(masbrt, 10, 440)
    textrender(tempot, 10, 80)
    textrender(offsett, 10, 70)
    textrender(roffset, 10, 60)
    textrender(poffset, 10, 50)
    textrender(nxtintt, 10, 40)
    textrender(ubalqt, 330, 70)
    textrender(uballt, 330, 60)
    textrender(dbalqt, 330, 50)
    textrender(dballt, 330, 40)
    textrender("v", 40+(12*temp2), 420)
    textrender("Press H for help", 10, 10)
    
    if temp3 == True: helprender()

def helprender():
    rect = pyglet.shapes.Rectangle(0, 0, width, height, color=(0, 0, 0, 204))
    rect.draw()
    textrender("Taiko 3 Chart Viewer", 80, 280)
    textrender("program by tikal.", 80, 270)
    textrender("2023", 80, 260)
    textrender("UP - Previous measure", 80, 240)
    textrender("DOWN - Next measure", 80, 230)
    textrender("ESC - Exit program", 80, 220)
    textrender("LEFT - Previous beat unit", 320, 240)
    textrender("RIGHT - Next beat unit", 320, 230)
    
def bgrender():
    global chart
    global temp1
    linet = chart[temp1].get('BAR')
    if linet == True:
        bar = pyglet.shapes.Rectangle(44, 120, 1, 296, color=(176, 176, 176, 255))
        bar.draw()

@window.event
def on_activate():
    try:
        global chart
        chart = everything(sys.argv[1])
    except IndexError:
        print("There's no file here!")
        print("Usage: ", os.path.basename(__file__), "[file]")
        exit()
    viewer(chart, temp1)

@window.event
def on_key_press(symbol, modifiers):
    global temp1
    global temp2
    global temp3
    
    if temp3 == False:
        if symbol == key.RIGHT:
            if temp2 >= 47 and temp1 < len(chart)-1:
                temp1 += 1
                temp2 = 0
                refresh()
            elif temp2 < 47:
                temp2 += 1
        if symbol == key.LEFT:
            if temp2 <= 0 and temp1 > 0:
                temp1 -= 1
                temp2 = 47
                refresh()
            elif temp2 > 0:
                temp2 -= 1
        if symbol == key.UP and temp1 > 0:
            temp1 -= 1
            refresh()
        if symbol == key.DOWN and temp1 < len(chart)-1:
            temp1 += 1
            refresh()
        if symbol == key.H:
            temp3 = True
    else:
        if symbol == key.H: temp3 = False
    
    if symbol == key.ESCAPE:
        window.close()

@window.event
def on_draw():
    window.clear()
    bgrender()
    batch.draw()
    masstrender()

def refresh():
    global sprites
    sprites = []
    viewer(chart, temp1)

run()