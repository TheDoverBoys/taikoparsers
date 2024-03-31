import sys, os, json, pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet.app import run
from pyglet import image

width, height= 640, 480
window = Window(caption="Taiko 2 Chart Viewer", width=width,height=height)
batch = pyglet.graphics.Batch()
batchtwo = pyglet.graphics.Batch()
sprites = []

measure_no = 0
beat_no = 0
toggle_help = False
screenshot_no = 0
bar_no = 0
toggle_stats = True

def everything(file):
    if os.path.isfile(file):
        arquivo = open(file,"rb")
        bindata = arquivo.read()
        jsonx = []
        chunksize = 1164
        measure = 1
        if bindata[:4] != b'\x16\x11\x00\x00':
            print('Header mismatch! Are you sure this is a Taiko 2 chart?')
            exit()
        else:
            offset = int.from_bytes(bindata[4:8], "little")
            while True:
                jsony = ''
                increment = chunksize*(measure-1)
                tempo = bindata[8+increment:12+increment]
                if tempo == b'\xff\xff\xff\xff': return jsonx
                else: tempo = int.from_bytes(tempo, "little")
                branch1 = bindata[12+increment:16+increment]
                branch2 = bindata[16+increment:20+increment]
                
                if branch1 == b'\xFF\xFF\xFF\xFF': branch1 = None
                else: branch1 = int.from_bytes(branch1, "little")

                if branch2 == b'\xFF\xFF\xFF\xFF': branch2 = None
                else: branch2 = int.from_bytes(branch2, "little")

                norbranch1 = branchparser(bindata[20+increment:212+increment])
                norbranch2 = branchparser(bindata[212+increment:404+increment])
                expbranch1 = branchparser(bindata[404+increment:596+increment])
                expbranch2 = branchparser(bindata[596+increment:788+increment])
                masbranch1 = branchparser(bindata[788+increment:980+increment])
                masbranch2 = branchparser(bindata[980+increment:1172+increment])
                
                jsony = json.dumps({'FOF':offset, 'TMP':tempo, 'ABQ':branch1, 'MBQ':branch2, 'ONB':norbranch1, 'TNB':norbranch2, 'OAB':expbranch1, 'TAB':expbranch2, 'OMB':masbranch1, 'TMB':masbranch2})
                jsonx.append(json.loads(jsony))
                measure+=1
    else:
        print("This is not a file!")
        exit()
        
def branchparser(area):
    split = [area[i] for i in range(0, len(area), 4)]
    return split
    
def viewer(a, measurenumber):
    chartlookup = {
        0: 'ONB',
        1: 'TNB',
        2: 'OAB',
        3: 'TAB',
        4: 'OMB',
        5: 'TMB'
    }
    for i in [measurenumber]:
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
                    case 0: imgdefined = None
                    case _:
                        print("Invalid note type!")
                        exit()
                if (imgdefined != None):
                    pic = imgdefined
                    posx = 23+(12*j)
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
    global toggle_stats
    bar_values = [1, 2, 4, 8, 12, 16, 24, 48]
    advbr = chart[measure_no].get('ABQ')
    masbr = chart[measure_no].get('MBQ')
    advbrt = "Advanced Quota: " + str(advbr)
    masbrt = "Master Quota:   " + str(masbr)
    
    tempo = (14400/(chart[measure_no].get('TMP')))*0.997101631
    divis = "Beat: " + str(beat_no) + "/48"
    tempot = "BPM:           " + str(tempo)
    quantt = "Quantization: 1/" + str(bar_values[bar_no])
    offset = (chart[0].get('FOF'))*0.016715113
    offsett = "First Offset:  " + str(offset)
    toffsett = "True Offset:   " + str(offset+(240/((14400/(chart[0].get('TMP')))*0.997101631)))
    meast = "Measure: " + str(measure_no+1) + " / " + str(len(chart))
    
    textrender(meast, 10, 460)
    textrender(divis, 330, 460)
    textrender(quantt, 330, 450)
    textrender(advbrt, 10, 450)
    textrender(masbrt, 10, 440)
    textrender(tempot, 10, 80)
    textrender(offsett, 10, 70)
    textrender(toffsett, 10, 60)
    textrender("v", 40+(12*beat_no), 422)
    textrender("Press H for help", 10, 10)
    
    if toggle_help == True: helprender()
    if toggle_stats == True: statsrender(chart)

def helprender():
    rect = pyglet.shapes.Rectangle(0, 0, width, height, color=(0, 0, 0, 204))
    rect.draw()
    textrender("Taiko 2 Chart Viewer v1.0", 80, 285)
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

def statsrender(chart):
    global toggle_stats
    twoplayer_verify = False
    branch_verify = False
    unusedbranch_verify = False
    firstbranch = None
    
    for chart_index in range(len(chart)):
        advancedbranch = chart[chart_index].get('ABQ')
        masterbranch = chart[chart_index].get('MBQ')
        if not advancedbranch: advancedbranch = 0
        if not masterbranch: masterbranch = 0
        if (advancedbranch > 0 or masterbranch > 0) and not branch_verify:
            firstbranch = chart_index
            branch_verify = True
    for chart_index in range(len(chart)):
        playeronesideone = chart[chart_index].get('ONB')
        playertwosideone = chart[chart_index].get('TNB')
        playeronesidetwo = chart[chart_index].get('OAB')
        playeronesidethr = chart[chart_index].get('OMB')
        playertwosidetwo = chart[chart_index].get('TAB')
        playertwosidethr = chart[chart_index].get('TMB')
        if (playeronesideone != playertwosideone) and not twoplayer_verify:
            twoplayer_verify = True
        if branch_verify:
            if chart_index < firstbranch:
                for tick_index in range(len(playeronesideone)):
                    if (playeronesidetwo[tick_index] or playeronesidethr[tick_index] or playertwosidetwo[tick_index] or playertwosidethr[tick_index]) and not unusedbranch_verify:
                        unusedbranch_verify = True
            if ((playeronesidetwo != playertwosidetwo) or (playeronesidethr != playertwosidethr)) and not twoplayer_verify:
                twoplayer_verify = True
        else:
            for tick_index in range(len(playeronesideone)):
                if (playeronesidetwo[tick_index] or playeronesidethr[tick_index] or playertwosidetwo[tick_index] or playertwosidethr[tick_index]) and not unusedbranch_verify:
                        unusedbranch_verify = True
    print("Branches: ", branch_verify, " /  Unused Branch Sections: ", unusedbranch_verify, " /  Two Player: ", twoplayer_verify)
    toggle_stats = False

def bgrender():
    bars = []
    global chart
    global measure_no
    global bar_no
    bar_values = [1, 2, 4, 8, 12, 16, 24, 48]
    for i in range(2):
        n1bar = pyglet.shapes.Rectangle(0,383-(i*51),width,37, color=(56, 56, 56), batch = batchtwo)
        n2bar = pyglet.shapes.Rectangle(0,281-(i*51),width,37, color=(48,88,112), batch = batchtwo)
        n3bar = pyglet.shapes.Rectangle(0,179-(i*51),width,37, color=(128,48,112), batch = batchtwo)
        bars.append(n1bar)
        bars.append(n2bar)
        bars.append(n3bar)
    for number in range(bar_values[bar_no]+1):
        if number != 0:
            beat_divide = pyglet.shapes.Rectangle(44+(576/bar_values[bar_no])+((number-1)*(576/bar_values[bar_no])), 128, 1, 292, color=(0, 0, 0, 102), batch = batchtwo)
            bars.append(beat_divide)
    bar = pyglet.shapes.Rectangle(44, 128, 1, 292, color=(176, 176, 176), batch = batchtwo)
    for j in range(6):
        wtbar = pyglet.shapes.Rectangle(0,370-(j*51),width,12, color=(248, 248, 248), batch=batchtwo)
        bars.append(wtbar)
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
            screenshot_measure_no = str(measure_no+1)
            if int(screenshot_measure_no) < 10: screenshot_measure_no = "00" + screenshot_measure_no
            elif 10 <= int(screenshot_measure_no) < 100: screenshot_measure_no = "0" + screenshot_measure_no
            screenshot_name = 'screenshot_' + str(os.path.basename(sys.argv[1])) + '_m' + str(screenshot_measure_no) + '.png'
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