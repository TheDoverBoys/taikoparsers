import sys, os, json, pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet.app import run
from pyglet import image

width, height= 640, 480
window = Window(caption="Taiko 3 Chart Viewer", width=width,height=height)
batch = pyglet.graphics.Batch()
batchtwo = pyglet.graphics.Batch()
sprites = []

measure_no = 0
beat_no = 0
toggle_help = False
screenshot_no = 0
bar_no = 0

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

                has_bar = bindata[14+increment] == 1

                tempo = bindata[15+increment]

                balloon1_quantity = bindata[32+increment:34+increment]
                balloon1_length = bindata[34+increment:36+increment]
                balloon2_quantity = bindata[36+increment:38+increment]
                balloon2_length = bindata[38+increment:40+increment]
                if (balloon1_quantity == b'\xFF\xFF'):
                    balloon1_quantity = None
                    balloon1_length = None
                else:
                    balloon1_quantity = int.from_bytes(balloon1_quantity, "little")
                    balloon1_length = int.from_bytes(balloon1_length, "little")
                if (balloon2_quantity == b'\xFF\xFF'):
                    balloon2_quantity = None
                    balloon2_length = None
                else:
                    balloon2_quantity = int.from_bytes(balloon2_quantity, "little")
                    balloon2_length = int.from_bytes(balloon2_length, "little")
                
                norbranch1 = branchparser(bindata[40+increment:88+increment])
                expbranch1 = branchparser(bindata[88+increment:136+increment])
                masbranch1 = branchparser(bindata[136+increment:184+increment])
                norbranch2 = branchparser(bindata[184+increment:232+increment])
                expbranch2 = branchparser(bindata[232+increment:280+increment])
                masbranch2 = branchparser(bindata[280+increment:328+increment])
                jsony = json.dumps({'ABQ':branch1, 'MBQ':branch2, 'FOF':offset, 'BAR':has_bar, 'TMP':tempo, 'BQO':balloon1_quantity, 'BLO':balloon1_length, 'BQT':balloon2_quantity, 'BLT':balloon2_length, 'ONB':norbranch1, 'OAB':expbranch1, 'OMB':masbranch1, 'TNB':norbranch2, 'TAB':expbranch2, 'TMB':masbranch2})

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
                imt = image.ImageGrid(image.load('notes.png'), 4, 4)
                match imgdefine:
                    case (1 | 2 | 3): imgdefined = imt[0]
                    case (5 | 6 | 7): imgdefined = imt[1]
                    case (9 | 10 | 11): imgdefined = imt[2]
                    case (13 | 14 | 15): imgdefined = imt[3]
                    case (17 | 18 | 19): imgdefined = imt[4]
                    case 21: imgdefined = imt[5]
                    case 22:
                        if j == 47:
                            if (i < len(a)-1 and a[i+1].get(chartlookup[k])[0]) == 22: imgdefined = imt[7]
                            else: imgdefined = imt[8]
                        elif(j != 47 and a[i].get(chartlookup[k])[j+1] != 22 and a[i].get(chartlookup[k])[j-1] == 22): imgdefined = imt[8]
                        elif j == 0:
                            if (i > 0 and a[i-1].get(chartlookup[k])[47]) == 22: imgdefined = imt[7]
                            else: imgdefined = imt[6]
                        elif(j != 0 and a[i].get(chartlookup[k])[j-1] != 22 and a[i].get(chartlookup[k])[j+1] == 22): imgdefined = imt[6]
                        else: imgdefined = imt[7]
                    case 23:
                        if j == 47:
                            if (i < len(a)-1 and a[i+1].get(chartlookup[k])[0]) == 23: imgdefined = imt[10]
                            else: imgdefined = imt[11]
                        elif(j != 47 and a[i].get(chartlookup[k])[j+1] != 23 and a[i].get(chartlookup[k])[j-1] == 23): imgdefined = imt[11]
                        elif j == 0:
                            if (i > 0 and a[i-1].get(chartlookup[k])[47]) == 23: imgdefined = imt[10]
                            else: imgdefined = imt[9]
                        elif(j != 0 and a[i].get(chartlookup[k])[j-1] != 23 and a[i].get(chartlookup[k])[j+1] == 23): imgdefined = imt[9]
                        else: imgdefined = imt[10]
                    case 24: imgdefined = imt[12]
                    case 25: imgdefined = imt[13]
                    case 26: imgdefined = imt[14]
                    case 27: imgdefined = imt[15]
                    case 0: imgdefined = None
                    case _:
                        print("Invalid note type!")
                        exit()
                if (imgdefined != None):
                    pic = imgdefined
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

def masstextrender():
    global chart
    global measure_no
    global beat_no
    global toggle_help
    global bar_no
    bar_values = [1, 2, 4, 8, 12, 16, 24, 48]
    advbr = chart[measure_no].get('ABQ')
    masbr = chart[measure_no].get('MBQ')
    advbrt = "Advanced Quota: " + str(advbr)
    masbrt = "Master Quota:   " + str(masbr)
    
    tempo = 14400/(chart[measure_no].get('TMP'))
    bint = 60/tempo
    mint = bint*4
    pint = mint+(bint*(beat_no/12))
    divis = "Beat: " + str(beat_no) + "/48"
    tempot = "BPM:           " + str(tempo)
    quantt = "Quantization: 1/" + str(bar_values[bar_no])
    offset = (chart[measure_no].get('FOF'))/98.438121
    if measure_no < len(chart)-1:
        nxtint = (((chart[measure_no+1].get('FOF'))/98.438121)+(60/(14400/(chart[measure_no+1].get('TMP')))*4))-(offset+pint)
    else:
        nxtint = (bint*8)-pint
    offsett = "First Offset:  " + str(offset)
    roffset = "Reach Offset:  " + str(offset+mint)
    poffset = "Posit Offset:  " + str(offset+pint)
    meast = "Measure: " + str(measure_no+1) + " / " + str(len(chart))
    nxtintt = "Next Interval: " + str(nxtint)
    
    ubalq = chart[measure_no].get('BQO')
    uball = chart[measure_no].get('BLO')
    dbalq = chart[measure_no].get('BQT')
    dball = chart[measure_no].get('BLT')
    ubalqt = "1P Bal. Quant.: " + str(ubalq)
    uballt = "1P Bal. Length: " + str(uball)
    if uball != None: uballt += " / " + str(uball/60)
    dbalqt = "2P Bal. Quant.: " + str(dbalq)
    dballt = "2P Bal. Length: " + str(dball)
    if dball != None: dballt += " / " + str(dball/60)
    
    textrender(meast, 10, 460)
    textrender(divis, 330, 460)
    textrender(quantt, 330, 450)
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
    textrender("v", 40+(12*beat_no), 422)
    textrender("Press H for help", 10, 10)
    
    if toggle_help == True: helprender()

def helprender():
    rect = pyglet.shapes.Rectangle(0, 0, width, height, color=(0, 0, 0, 204))
    rect.draw()
    textrender("Taiko 3 Chart Viewer v1.1", 80, 285)
    textrender("program by TheDoverBoys", 80, 275)
    textrender("2023", 80, 265)
    textrender("UP - Previous measure", 80, 245)
    textrender("DOWN - Next measure", 80, 235)
    textrender("LEFT - Previous beat unit", 80, 225)
    textrender("RIGHT - Next beat unit", 80, 215)
    textrender("A - Increase quantization", 320, 245)
    textrender("D - Decrease quantization", 320, 235)
    textrender("P - Take screenshot", 320, 225)
    textrender("ESC - Exit program", 320, 215)

def bgrender():
    bars = []
    global chart
    global measure_no
    global bar_no
    bar_values = [1, 2, 4, 8, 12, 16, 24, 48]
    for i in range(2):
        n1bar = pyglet.shapes.Rectangle(0,383-(i*153),width,37, color=(56, 56, 56), batch = batchtwo)
        n2bar = pyglet.shapes.Rectangle(0,332-(i*153),width,37, color=(48,88,112), batch = batchtwo)
        n3bar = pyglet.shapes.Rectangle(0,281-(i*153),width,37, color=(128,48,112), batch = batchtwo)
        bars.append(n1bar)
        bars.append(n2bar)
        bars.append(n3bar)
    for j in range(6):
        wtbar = pyglet.shapes.Rectangle(0,370-(j*51),width,12, color=(248, 248, 248), batch=batchtwo)
        bars.append(wtbar)
    for number in range(bar_values[bar_no]+1):
        if number != 0:
            beat_divide = pyglet.shapes.Rectangle(44+(576/bar_values[bar_no])+((number-1)*(576/bar_values[bar_no])), 128, 1, 292, color=(0, 0, 0, 102), batch = batchtwo)
            bars.append(beat_divide)
    linet = chart[measure_no].get('BAR')
    if linet == True:
        bar = pyglet.shapes.Rectangle(44, 128, 1, 292, color=(176, 176, 176), batch = batchtwo)
    batchtwo.draw()

def init():
    try:
        global chart
        chart = everything(sys.argv[1])
    except IndexError:
        print("There's no file here!")
        print("Usage: ", os.path.basename(__file__), "[file]")
        exit()
    viewer(chart, measure_no)

@window.event
def on_key_press(symbol, modifiers):
    global measure_no
    global beat_no
    global toggle_help
    global bar_no
    
    if toggle_help == False:
        if symbol == key.RIGHT:
            if beat_no >= 47 and measure_no < len(chart)-1:
                measure_no += 1
                beat_no = 0
                refresh()
            elif beat_no < 47:
                beat_no += 1
        if symbol == key.LEFT:
            if beat_no <= 0 and measure_no > 0:
                measure_no -= 1
                beat_no = 47
                refresh()
            elif beat_no > 0:
                beat_no -= 1
        if symbol == key.UP and measure_no > 0:
            measure_no -= 1
            refresh()
        if symbol == key.DOWN and measure_no < len(chart)-1:
            measure_no += 1
            refresh()
        if symbol == key.H:
            toggle_help = True
        if symbol == key.P:
            screenshot_name = 'screenshot_' + str(os.path.basename(sys.argv[1])) + '_m' + str(measure_no+1) + '.png'
            pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
        if symbol == key.D:
            if bar_no < 7: bar_no += 1
            #print(bar_no)
        if symbol == key.A:
            if bar_no > 0: bar_no -= 1
            #print(bar_no)
            
    else:
        if symbol == key.H: toggle_help = False
    
    if symbol == key.ESCAPE:
        window.close()

@window.event
def on_draw():
    window.clear()
    bgrender()
    batch.draw()
    masstextrender()

def refresh():
    global sprites
    sprites = []
    init()

@window.event
def on_deactivate():
    window.clear()
    
if __name__ == "__main__":
    init()
    run()