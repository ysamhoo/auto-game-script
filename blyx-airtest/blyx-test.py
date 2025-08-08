# -*- encoding=utf8 -*-
__author__ = "yuyu"

from airtest.core.api import *
import logging
import sys

controller_pos=[320, 725]
buttons={
"home_teleportation":Template(r"tpl1754340188642.png", record_pos=(0.1, -0.146), resolution=(542, 1008)),
"promotion_tips":Template(r"tpl1754643186148.png", record_pos=(0.003, 0.715), resolution=(599, 1109)),
"home_bottom":[260, 900],
"teleportation":Template(r"tpl1754339519623.png", record_pos=(0.27, -0.063), resolution=(599, 1109)),
"back": Template(r"tpl1754338045737.png", record_pos=(0.413, 0.697), resolution=(599, 1109)),
"confirm":Template(r"tpl1754337431599.png", record_pos=(0.148, 0.184), resolution=(599, 1109)),
 "map":Template(r"tpl1754398721915.png", record_pos=(0.008, 0.598), resolution=(599, 1109)),
}
place_buttons = {
    "教堂山谷": (
        Template(r"tpl1754338327899.png", record_pos=(-0.23, -0.395), resolution=(599, 1109)),
        Template(r"tpl1754338348491.png", record_pos=(0.138, -0.201), resolution=(599, 1109))
    ),
    "贫瘠营地": (
        Template(r"tpl1754338382738.png", record_pos=(-0.228, -0.286), resolution=(599, 1109)),
        Template(r"tpl1754338392042.png", record_pos=(0.143, -0.37), resolution=(599, 1109))
    ),
    "双峰山谷": (
        Template(r"tpl1754338382738.png", record_pos=(-0.228, -0.286), resolution=(599, 1109)),
        Template(r"tpl1754338472803.png", record_pos=(0.146, -0.199), resolution=(599, 1109))
    ),
    "污染哨站": (
        Template(r"tpl1754338489972.png", record_pos=(-0.231, -0.179), resolution=(599, 1109)),
        Template(r"tpl1754338589851.png", record_pos=(0.144, -0.368), resolution=(599, 1109))
    ),
    "腐烂沼泽": (
        Template(r"tpl1754338489972.png", record_pos=(-0.231, -0.179), resolution=(599, 1109)),
        Template(r"tpl1754338506474.png", record_pos=(0.143, -0.201), resolution=(599, 1109))
    ),
    "寒风营地": (
        Template(r"tpl1754338489972.png", record_pos=(-0.231, -0.179), resolution=(599, 1109)),
        Template(r"tpl1754338606771.png", record_pos=(0.143, -0.038), resolution=(599, 1109))
    ),
    "魔力之环": (
        Template(r"tpl1754338622526.png", record_pos=(-0.226, -0.073), resolution=(599, 1109)),
        Template(r"tpl1754338630620.png", record_pos=(0.146, -0.365), resolution=(599, 1109))
    ),
    "北风营地": (
        Template(r"tpl1754338622526.png", record_pos=(-0.226, -0.073), resolution=(599, 1109)),
        Template(r"tpl1754338650683.png", record_pos=(0.144, -0.203), resolution=(599, 1109))
    ),
    "王座大厅": (
        Template(r"tpl1754338662076.png", record_pos=(-0.228, 0.038), resolution=(599, 1109)),
        Template(r"tpl1754338672659.png", record_pos=(0.143, -0.365), resolution=(599, 1109))
    ),
    "冰冠禁区": (
        Template(r"tpl1754338662076.png", record_pos=(-0.228, 0.038), resolution=(599, 1109)),
        Template(r"tpl1754338693117.png", record_pos=(0.144, -0.034), resolution=(599, 1109))
    ),
    "炽热哨站": (
        Template(r"tpl1754338704979.png", record_pos=(-0.228, 0.25), resolution=(599, 1109)),
        Template(r"tpl1754338717940.png", record_pos=(0.144, -0.205), resolution=(599, 1109))
    ),
}
pos_cache={}
def reload():
    global tryReloadTimes
    global pos_cache
    tryReloadTimes = 0
    try:
        pos_cache={}
        #touch more button
        touch(Template(r"tpl1754328018641.png", record_pos=(0.285, -0.892), resolution=(661, 1219)))
        #touch the reload icon
        touch(Template(r"tpl1754328042184.png", record_pos=(0.24, -0.498), resolution=(661, 1219)))
        sleep(10)
        connect_device("Windows:///?title_re=百炼英雄")
#         connect_device("Wdows:///853218")
        # wait for the game to load
        # home_bottom_pos=wait(buttons["home_bottom"], timeout=10)
        # pos_cache["home_bottom"]=home_bottom_pos
        touch(buttons["home_bottom"])
        # wait for the home teleportation button to appear
        times = 0
        while times < 15 :
            home_teleportation_button_pos=exists(buttons["home_teleportation"])
            if(home_teleportation_button_pos):
                # pos_cache["home_teleportation_button_pos"]=home_teleportation_button_pos
                tryReloadTimes = 0
                return home_teleportation_button_pos
            touch(buttons["home_bottom"])
            times += 1
#         thorw Exception("Failed to find home teleportation button after 15 attempts")
    except:
        sleep(1)
        tryReloadTimes += 1
        if tryReloadTimes < 3: 
            print("try reload times: ", tryReloadTimes)
            reload()
            
def is_outdoor():
    return exists(buttons["back"])

def is_athome():
    return exists(buttons["home_teleportation"])

def go_home():
    go_home_button_pos=is_outdoor()
    if go_home_button_pos:
        touch(go_home_button_pos)
#         confirm_button_pos=exists(buttons["confirm"])
#         if confirm_button_pos:
#             touch(confirm_button_pos) 
        sleep(6) #转场动画   
        home_teleportation_button_pos = wait(buttons["home_teleportation"],interval=0.6,timeout=10)
        return home_teleportation_button_pos;
    return exists(buttons["home_teleportation"])

def find_teleportation_button():
    return exists(buttons["teleportation"]) or exists(buttons["home_teleportation"]) or  go_home()


def get_place_button(place):
    return place_buttons.get(place, (None, None))

def teleport_to(place,teleportation_pos=None):
    teleportation_pos = teleportation_pos or find_teleportation_button()
    touch(teleportation_pos)
    wait(buttons["map"])
    button1, button2 = get_place_button(place)
    if button1 and button2:
        button1_pos = exists(button1)
        button2_pos = button2
        if button1_pos:
            touch(button1_pos)
            button2_pos = wait(button2)
        touch(button2_pos)    
    sleep(6)#等待转场动画
    return wait(buttons["teleportation"],interval=0.6,timeout=10)

def make_money(teleportation_pos=None):
    teleportation_pos=teleport_to("寒风营地",teleportation_pos)
    swipe(controller_pos, vector=[0.09, -0.018], duration=1.5)
    sleep(1)
    swipe(controller_pos, vector=[-0.09, 0.018], duration=1.5)

    
    teleportation_pos=teleport_to("贫瘠营地",teleportation_pos)
    swipe(controller_pos, vector=[0.05,-0.001], duration=0.8)
    # sleep(0.2)
    swipe(controller_pos, vector=[-0.05,0], duration=0.8)
    
    teleportation_pos=teleport_to("教堂山谷",teleportation_pos)
    swipe(controller_pos, vector=[0.02, -0.03], duration=4.4)
    swipe(controller_pos, vector=[-0.019, 0.07], duration=4)
    
    teleport_to("污染哨站")
    swipe(controller_pos, vector=[0.05, 0.0035], duration=0.8)
    swipe(controller_pos, vector=[-0.046, 0.04], duration=3.3)
    swipe(controller_pos, vector=[0.005, 0.06], duration=6.2)
    # sleep(0.4)
    teleportation_pos=go_home()
    teleportation_pos=teleport_to("王座大厅",teleportation_pos)
    return teleportation_pos
    

    
def main():
    
    print("程序开始运行...")
    auto_setup(__file__,devices=["Windows:///?title_re=百炼英雄"])
    # logger = logging.getLogger("blyx-test")
    # logger.setLevel(logging.WARNING)
    reload()
    teleportation_pos=None
    while True:
        try:
            teleportation_pos=make_money(teleportation_pos)
        except KeyboardInterrupt:
            print("收到中断信号，程序退出。")
            sys.exit(0)
        except Exception as e:
            print("发生异常：", e)
            reload()
#     make_money()
    print("finished!")        

if __name__ == "__main__":
    main()















