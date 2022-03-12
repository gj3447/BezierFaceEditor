from pkg_resources import IResourceProvider
import pygame as pg
import besierline as bl
import pickle as pk
import parameter as pt
import random as rd
import face
import ui

def bar_r_callback(value,state):
    state["face_current"].modify["color"][0] = int(value)
def bar_g_callback(value,state):
    state["face_current"].modify["color"][1] = int(value)
def bar_b_callback(value,state):
    state["face_current"].modify["color"][2] = int(value)
def bar_s_callback(value,state):
    state["face_current"].modify["width"] = int(value)
    
def start():
    pg.init()
    screen = pg.display.set_mode([pt.MAP_X, pt.MAP_Y])
    face_list = face.face_list()
    face_current = face_list[pg.K_0]
    bar_r = ui.BAR(value=255,position=[[10,10],[25,100]],color=[255,0,0],callback=bar_r_callback)
    bar_g = ui.BAR(value=255,position=[[30,10],[45,100]],color=[0,255,0],callback=bar_g_callback)
    bar_b = ui.BAR(value=255,position=[[50,10],[65,100]],color=[0,0,255],callback=bar_b_callback)
    bar_s = ui.BAR(value=100,position=[[70,10],[85,100]],color=[100,100,100],callback=bar_s_callback)
    font = pg.font.SysFont(pg.font.get_fonts()[0],20) 
    state = {
        "screen" : screen,
        "running" : True,
        "face_list" : face_list,
        "face_current" : face_current,
        "face_change" : None,
        "change_time" : float(0),
        "last_tick" : float(0),
        "delta_time" : float(0),
        "bar_r" : bar_r,
        "bar_g" : bar_g,
        "bar_b" : bar_b,
        "bar_s" : bar_s,
        "bar_list" : [bar_r,bar_g,bar_b,bar_s],
        "font" : font
    }
    update(state=state)
    pg.quit()
    
def update(state):
    while state["running"]:
        for event in pg.event.get():
            state["running"] = event_action(event=event,state=state)
        tick=pg.time.get_ticks()
        state["delta_time"] = float(tick - state["last_tick"])
        state["last_tick"] = tick
        if state["face_change"]!=None:
            if state["change_time"] > 0:
                state["change_time"] =float(state["change_time"]- (state["delta_time"] / float(pt.CHANGE_TIME)))
            else:
                state["change_time"] = 0
                state["face_current"] = state["face_change"]
                state["face_change"] = None
        draw(state=state)
        
def draw(state):
    state["screen"].fill((255,255,255))
    if state["face_change"] ==None:
        state["face_current"].draw(state["screen"])
        if state["face_current"].modify !=None:
            text = state["font"].render(state["face_current"].modify["name"],True,(0,0,0)) 
            state["screen"].blit(text,(pt.CENTER[0],0))    
            for e in state["bar_list"]:
                e.draw(screen=state["screen"])
    else:
        state["face_current"].change_draw(change_face=state["face_change"],percent=state["change_time"],screen=state["screen"])
    pg.display.flip()
def event_action(event,state):
    if event.type == pg.QUIT:
        return False
    event_mouse(event=event,state=state)
    event_key(event=event,state=state)
    return True
def event_mouse(event,state):
    if state['face_current'].modify !=None:
        if event.type == pg.MOUSEBUTTONDOWN:
            state['face_current'].mouse_down()
            for e in state["bar_list"]:
                e.mouse_down()
        if event.type == pg.MOUSEBUTTONUP:
            state['face_current'].mouse_up()
            for e in state["bar_list"]:
                e.mouse_up()
        if event.type == pg.MOUSEMOTION:
            state['face_current'].mouse_update()
            for e in state["bar_list"]:
                e.mouse_update(state=state)
def event_key(event,state):
    if event.type == pg.KEYDOWN:
        face_change = None
        state['face_current'].key_down(state=state)
        key = pg.key.get_pressed()
        if state['face_change'] == None:
            for e in state['face_list'].keys():
                if key[e]:
                    face_change = state['face_list'][e]
                if (face_change != None)and(state['face_current'] != face_change):
                    state['face_change'] = face_change
                    state['change_time'] = float(1)
                    state['face_change'].modify = None
                    state['face_change'].movingpoint = None
start()
