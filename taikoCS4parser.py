import sys, os, json, pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet.app import run
from pyglet import image

width, height= 640, 480
window = Window(caption="Taiko CS4 Chart Viewer", width=width,height=height)
batch = pyglet.graphics.Batch()
batchtwo = pyglet.graphics.Batch()
sprites = []

measure_number = 0
beat_number = 0
toggle_help = False
screenshot_no = 0
bar_number = 2
toggle_stats = True

def everything(file):
    if os.path.isfile(file):
        arquivo = open(file,"rb")
        bindata = arquivo.read()
        chunksize = 92
        measure = 1
        number_of_measures = int.from_bytes(bindata[:4], byteorder='little')
        definition_offset = int.from_bytes(bindata[4:8], byteorder='little')
        definition_number = int.from_bytes(bindata[8:12], byteorder='little')
        section_area = bindata[16:(chunksize*number_of_measures)]
        definition_area = bindata[definition_offset:definition_offset+(definition_number*16)]
        section_areas = section_parse(section_area, chunksize, number_of_measures)
        definition_areas = definition_parse(definition_area, definition_number)
        return [section_areas, combination_parse(section_areas, definition_areas)]
    else:
        print("This is not a file!")
        exit()



def section_parse(data, chunksize, measures):
    __json_measures = []
    for measure in range(measures):
        __json_measure = ''
        __measure_offset = int.from_bytes(data[measure*chunksize:4+(measure*chunksize)], byteorder='little')
        __measure_bpm = int.from_bytes(data[4+(measure*chunksize):8+(measure*chunksize)], byteorder='little')
        __measure_barline = int.from_bytes(data[8+(measure*chunksize):12+(measure*chunksize)], byteorder='little')
        __measure_advquota = None
        if data[12+(measure*chunksize):16+(measure*chunksize)] != b'\xFF\xFF\xFF\xFF':
            __measure_advquota = int.from_bytes(data[12+(measure*chunksize):16+(measure*chunksize)], byteorder='little')

        __measure_masquota = None
        if data[16+(measure*chunksize):20+(measure*chunksize)] != b'\xFF\xFF\xFF\xFF':
            __measure_masquota = int.from_bytes(data[16+(measure*chunksize):20+(measure*chunksize)], byteorder='little')
        
        __measure_definition_offset_one_nor = int.from_bytes(data[20+(measure*chunksize):24+(measure*chunksize)], byteorder='little')
        __measure_definition_length_one_nor = int.from_bytes(data[24+(measure*chunksize):28+(measure*chunksize)], byteorder='little')
        #__measure_definition_remain_one_nor = int.from_bytes(data[28+(measure*chunksize):32+(measure*chunksize)], byteorder='little')
        __measure_definition_offset_one_adv = int.from_bytes(data[32+(measure*chunksize):36+(measure*chunksize)], byteorder='little')
        __measure_definition_length_one_adv = int.from_bytes(data[36+(measure*chunksize):40+(measure*chunksize)], byteorder='little')
        #__measure_definition_remain_one_adv = int.from_bytes(data[40+(measure*chunksize):44+(measure*chunksize)], byteorder='little')
        __measure_definition_offset_one_mas = int.from_bytes(data[44+(measure*chunksize):48+(measure*chunksize)], byteorder='little')
        __measure_definition_length_one_mas = int.from_bytes(data[48+(measure*chunksize):52+(measure*chunksize)], byteorder='little')
        #__measure_definition_remain_one_mas = int.from_bytes(data[52+(measure*chunksize):56+(measure*chunksize)], byteorder='little')
        __measure_definition_offset_two_nor = int.from_bytes(data[56+(measure*chunksize):60+(measure*chunksize)], byteorder='little')
        __measure_definition_length_two_nor = int.from_bytes(data[60+(measure*chunksize):64+(measure*chunksize)], byteorder='little')
        #__measure_definition_remain_two_nor = int.from_bytes(data[64+(measure*chunksize):68+(measure*chunksize)], byteorder='little')
        __measure_definition_offset_two_adv = int.from_bytes(data[68+(measure*chunksize):72+(measure*chunksize)], byteorder='little')
        __measure_definition_length_two_adv = int.from_bytes(data[72+(measure*chunksize):76+(measure*chunksize)], byteorder='little')
        #__measure_definition_remain_two_adv = int.from_bytes(data[76+(measure*chunksize):80+(measure*chunksize)], byteorder='little')
        __measure_definition_offset_two_mas = int.from_bytes(data[80+(measure*chunksize):84+(measure*chunksize)], byteorder='little')
        __measure_definition_length_two_mas = int.from_bytes(data[84+(measure*chunksize):88+(measure*chunksize)], byteorder='little')
        #__measure_definition_remain_two_mas = int.from_bytes(data[88+(measure*chunksize):92+(measure*chunksize)], byteorder='little')
        __json_measure = json.dumps({'MOF':__measure_offset, 'BPM':__measure_bpm, 'BAR':__measure_barline, 'ABQ':__measure_advquota, 'MBQ':__measure_masquota, 'ONO':__measure_definition_offset_one_nor, 'ONL':__measure_definition_length_one_nor, 'OAO':__measure_definition_offset_one_adv, 'OAL':__measure_definition_length_one_adv, 'OMO':__measure_definition_offset_one_mas, 'OML':__measure_definition_length_one_mas, 'TNO':__measure_definition_offset_two_nor, 'TNL':__measure_definition_length_two_nor, 'TAO':__measure_definition_offset_two_adv, 'TAL':__measure_definition_length_two_adv, 'TMO':__measure_definition_offset_two_mas, 'TML':__measure_definition_length_two_mas})
        __json_measures.append(json.loads(__json_measure))

    return __json_measures

def definition_parse(data, number):
    __json_definitions = []
    for definition in range(number):
        __json_definition = ''
        __note_type = int.from_bytes(data[definition*16:4+(definition*16)], byteorder='little')
        __note_position = int.from_bytes(data[4+(definition*16):8+(definition*16)], byteorder='little')
        __note_hit = None
        if data[8+(definition*16):12+(definition*16)] != b'\xFF\xFF\xFF\xFF':
            __note_hit = int.from_bytes(data[8+(definition*16):12+(definition*16)], byteorder='little')
        __note_length = None
        if data[12+(definition*16):16+(definition*16)] != b'\xFF\xFF\xFF\xFF':
            __note_length = int.from_bytes(data[12+(definition*16):16+(definition*16)], byteorder='little')
        __json_definition = json.dumps({'TYP':__note_type, 'POS':__note_position, 'HIT':__note_hit, 'LEN':__note_length})
        __json_definitions.append(json.loads(__json_definition))
    return __json_definitions

def combination_parse(sections, definitions):
    __offset_lookup = {
        0: 'ONO',
        1: 'OAO',
        2: 'OMO',
        3: 'TNO',
        4: 'TAO',
        5: 'TMO'
    }
    __length_lookup = {
        0: 'ONL',
        1: 'OAL',
        2: 'OML',
        3: 'TNL',
        4: 'TAL',
        5: 'TML'
    }
    
    __all_measures = []
    
    for __section in range(len(sections)):
        __measure_data = []
        for __lookup_id in range(6):
            __measure_data.append([sections[__section].get(__offset_lookup[__lookup_id]), sections[__section].get(__length_lookup[__lookup_id])])
        __all_measures.append(__measure_data)

    __measure_notes = []

    for __measure in range(len(__all_measures)):
        __note_data = []
        for __section in range(6):
            __note_data2 = []
            if __all_measures[__measure][__section][1] > 0:
                for __length in range(__all_measures[__measure][__section][1]):
                    __note_data2.append(definitions[__all_measures[__measure][__section][0]+__length])
            __note_data.append(__note_data2)
        __measure_notes.append(__note_data)
    return __measure_notes


def viewer(chart, measure_no):
    for area_index in range(6):
        if chart[1][area_index]:
            for note_index in range(len(chart[1][measure_no][area_index])-1, -1, -1):
                image_define = chart[1][measure_no][area_index][note_index].get('TYP')
                image_tiles = image.ImageGrid(image.load('notes.png'), 4, 4)
                posx = 23+(12*chart[1][measure_no][area_index][note_index].get('POS'))
                posy = height-60-((area_index+1)*51)
                match image_define:
                    case 1: image_defined = image_tiles[0]
                    case 2: image_defined = image_tiles[1]
                    case 3: image_defined = image_tiles[2]
                    case 4: image_defined = image_tiles[3]
                    case 5: image_defined = image_tiles[4]
                    case 6: image_defined = image_tiles[6]
                    case 7: image_defined = image_tiles[5]
                    case 8: image_defined = image_tiles[12]
                    case 9: image_defined = image_tiles[9]
                    case 10: image_defined = image_tiles[15]
                    case 11: image_defined = image_tiles[13]
                    case _:
                        print("Invalid note type!")
                        exit()
                picture = image_defined
                spri = pyglet.sprite.Sprite(picture, posx, posy, batch = batch)
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
    global measure_number
    global beat_number
    global toggle_help
    global bar_number
    global toggle_stats
    
    for area_index in range(6):
        if chart[1][area_index]:
            for note_index in range(len(chart[1][measure_number][area_index])-1, -1, -1):
                text_define = chart[1][measure_number][area_index][note_index].get('TYP')
                match text_define:
                    case (6 | 9): display_area_text(text_define, None, str(chart[1][measure_number][area_index][note_index].get('LEN')/1000), 23+(12*chart[1][measure_number][area_index][note_index].get('POS')), height-60-((area_index+1)*51))
                    case 10: display_area_text(text_define, str(chart[1][measure_number][area_index][note_index].get('HIT')), str(chart[1][measure_number][area_index][note_index].get('LEN')/1000), 23+(12*chart[1][measure_number][area_index][note_index].get('POS')), height-60-((area_index+1)*51))
    
    bar_values = [1, 2, 4, 8, 12, 16, 24, 48]
    
    advanced_quota = chart[0][measure_number].get('ABQ')
    master_quota = chart[0][measure_number].get('MBQ')
    advanced_text = "Advanced Quota: " + str(advanced_quota)
    master_text = "Master Quota:   " + str(master_quota)
    
    tempo = chart[0][measure_number].get('BPM')
    beat_interval = 60/tempo
    measure_interval = beat_interval*4
    position_interval = measure_interval+(beat_interval*(beat_number/12))
    
    beat_division_text = "Beat: " + str(beat_number) + "/48"
    tempo_text = "BPM:           " + str(tempo)
    quantization_text = "Quantization: 1/" + str(bar_values[bar_number])
    
    offset = chart[0][measure_number].get('MOF')/1000
    if measure_number < len(chart[1])-1:
        next_interval = ((chart[0][measure_number+1].get('MOF')/1000)+(60/(chart[0][measure_number+1].get('BPM'))*4))-(offset+position_interval)
    else:
        next_interval = (beat_interval*8)-position_interval
    offset_text = "First Offset:  " + str(offset)
    reach_offset_text = "Reach Offset:  " + str(offset+measure_interval)
    position_offset_text = "Posit Offset:  " + str(offset+position_interval)
    measure_text = "Measure: " + str(measure_number+1) + " / " + str(len(chart[1]))
    next_interval_text = "Next Interval: " + str(next_interval)

    textrender(measure_text, 10, 460)
    textrender(beat_division_text, 330, 460)
    textrender(quantization_text, 330, 450)
    textrender(advanced_text, 10, 450)
    textrender(master_text, 10, 440)
    textrender(tempo_text, 10, 80)
    textrender(offset_text, 10, 70)
    textrender(reach_offset_text, 10, 60)
    textrender(position_offset_text, 10, 50)
    textrender(next_interval_text, 10, 40)

    textrender("v", 40+(12*beat_number), 422)
    textrender("Press H for help", 10, 10)
    
    if toggle_help == True: helprender()
    if toggle_stats == True: statsrender(chart)

def display_area_text(type, hitvalue, lengthvalue, x_position, y_position):
    textrender(lengthvalue, x_position+36, y_position+16)
    if type == 10:
        textrender(hitvalue, x_position+36, y_position+41)

def helprender():
    rect = pyglet.shapes.Rectangle(0, 0, width, height, color=(0, 0, 0, 204))
    rect.draw()
    textrender("Taiko CS4 Chart Viewer v1.001", 80, 285)
    textrender("program by TheDoverBoys", 80, 275)
    textrender("2024", 80, 265)
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
    __twoplayer_verify = False
    __branch_verify = False
    __unusedbranch_verify = False
    __firstbranch = None

    for __chart_index in range(len(chart[0])):
        __advancedbranch = chart[0][__chart_index].get('ABQ')
        __masterbranch = chart[0][__chart_index].get('MBQ')
        if not __advancedbranch: __advancedbranch = 0
        if not __masterbranch: __masterbranch = 0
        if (__advancedbranch > 0 or __masterbranch > 0) and not __branch_verify:
            __firstbranch = __chart_index
            __branch_verify = True
    for __chart_index in range(len(chart[1])):
        __player1side1 = chart[1][__chart_index][0]
        __player1side2 = chart[1][__chart_index][1]
        __player1side3 = chart[1][__chart_index][2]
        __player2side1 = chart[1][__chart_index][3]
        __player2side2 = chart[1][__chart_index][4]
        __player2side3 = chart[1][__chart_index][5]
        if (__player1side1 != __player2side1) and not __twoplayer_verify:
            __twoplayer_verify = True
        if __branch_verify:
            if __chart_index < __firstbranch:
                if not __unusedbranch_verify:
                    if ((len(__player1side1) != len(__player1side2) or len(__player1side1) != len(__player1side3)) or (len(__player2side1) != len(__player2side2) or len(__player2side1) != len(__player2side3))):
                        __unusedbranch_verify = True
                    else:
                        for __tick_index in range(len(__player1side1)):
                            if __player1side2[__tick_index] != __player1side1[__tick_index] or __player1side3[__tick_index] != __player1side1[__tick_index]:
                                __unusedbranch_verify = True
                        for __tick_index in range(len(__player2side1)):
                            if __player2side2[__tick_index] != __player2side1[__tick_index] or __player2side3[__tick_index] != __player2side1[__tick_index]:
                                __unusedbranch_verify = True
            if ((__player1side2 != __player2side2) or (__player1side3 != __player2side3)) and not __twoplayer_verify:
                __twoplayer_verify = True
        else:
            for __tick_index in range(len(__player1side1)):
                if (__player1side2 or __player1side3 or __player2side2 or __player2side3) and not __unusedbranch_verify:
                        __unusedbranch_verify = True
    print("Branches: ", __branch_verify, " /  Unused Branch Sections: ", __unusedbranch_verify, " /  Two Player: ", __twoplayer_verify)
    
    toggle_stats = False


def bgrender():
    bars = []
    global chart
    global measure_number
    global bar_number
    bar_values = [1, 2, 4, 8, 12, 16, 24, 48]
    for i in range(2):
        n1bar = pyglet.shapes.Rectangle(0,383-(i*153),width,37, color=(56, 56, 56), batch = batchtwo)
        n2bar = pyglet.shapes.Rectangle(0,332-(i*153),width,37, color=(48,88,112), batch = batchtwo)
        n3bar = pyglet.shapes.Rectangle(0,281-(i*153),width,37, color=(128,48,112), batch = batchtwo)
        bars.append(n1bar)
        bars.append(n2bar)
        bars.append(n3bar)
    for number in range(bar_values[bar_number]+1):
        if number != 0:
            beat_divide = pyglet.shapes.Rectangle(44+(576/bar_values[bar_number])+((number-1)*(576/bar_values[bar_number])), 128, 1, 292, color=(0, 0, 0, 102), batch = batchtwo)
            bars.append(beat_divide)
    lineverify = chart[0][measure_number].get('BAR')
    for j in range(6):
        if lineverify:
            bar = pyglet.shapes.Rectangle(44, 128+(51*j), 1, 37, color=(176, 176, 176), batch = batchtwo)
            bars.append(bar)
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
    viewer(chart, measure_number)

@window.event
def on_key_press(symbol, modifiers):
    global measure_number
    global beat_number
    global toggle_help
    global toggle_stats
    global bar_number
    
    if toggle_help == False:
        if symbol == key.RIGHT:
            if beat_number >= 47 and measure_number < len(chart[1])-1:
                measure_number += 1
                beat_number = 0
                refresh()
            elif beat_number < 47:
                beat_number += 1
        if symbol == key.LEFT:
            if beat_number <= 0 and measure_number > 0:
                measure_number -= 1
                beat_number = 47
                refresh()
            elif beat_number > 0:
                beat_number -= 1
        if symbol == key.UP and measure_number > 0:
            measure_number -= 1
            refresh()
        if symbol == key.DOWN and measure_number < len(chart[1])-1:
            measure_number += 1
            refresh()
        if symbol == key.H:
            toggle_help = True
        if symbol == key.P:
            screenshot_measure_no = str(measure_number+1)
            if int(screenshot_measure_no) < 10: screenshot_measure_no = "00" + screenshot_measure_no
            elif 10 <= int(screenshot_measure_no) < 100: screenshot_measure_no = "0" + screenshot_measure_no
            screenshot_name = 'm' + str(screenshot_measure_no) + '.png' # 'screenshot_' + str(os.path.basename(sys.argv[1])) + '_m' + str(screenshot_measure_no) + '.png'
            pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
        if symbol == key.D:
            if bar_number < 7: bar_number += 1
        if symbol == key.A:
            if bar_number > 0: bar_number -= 1
        
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