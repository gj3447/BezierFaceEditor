import parameter as pt
import random as rd
import pygame as pg
import besierline as bl
import parameter as pt
def random_map():
    x= int(rd.random()*pt.MAP_X)
    y= int(rd.random()*pt.MAP_Y)
    return [x,y]
def random_array(count):
    result = []
    for e in range(count):
        result.append(random_map())
    return result
def face_list():
    key_list = [pg.K_0,pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5,pg.K_6,pg.K_7,pg.K_8,pg.K_9]
    result = {}
    for e in key_list:
        result[e] = FACE()
    return result
class FACE:
    def __init__(self):
        self.ore = {"pos":random_array(pt.OUT_EYE_BROW),"key":pg.K_q,"color":[0,0,0],"width":4,"name":"out_right_eyebrow"}
        self.ole = {"pos":random_array(pt.OUT_EYE_BROW),"key":pg.K_w,"color":[0,0,0],"width":4,"name":"out_left_eyebrow"}
        self.ire = {"pos":random_array(pt.IN_EYE_BROW),"key":pg.K_e,"color":[0,0,0],"width":4,"name":"in_right_eyebrow"}
        self.ile = {"pos":random_array(pt.IN_EYE_BROW),"key":pg.K_r,"color":[0,0,0],"width":4,"name":"in_left_eyebrow"}
        self.ure = {"pos":random_array(pt.EYE),"key":pg.K_a,"color":[0,0,0],"width":4,"name":"up_right_eye"}
        self.ule = {"pos":random_array(pt.EYE),"key":pg.K_s,"color":[0,0,0],"width":4,"name":"up_left_eye"}
        self.dre = {"pos":random_array(pt.EYE),"key":pg.K_d,"color":[0,0,0],"width":4,"name":"down_right_eye"}
        self.dle = {"pos":random_array(pt.EYE),"key":pg.K_f,"color":[0,0,0],"width":4,"name":"down_left_eye"}
        self.um = {"pos":random_array(pt.MOUSE),"key":pg.K_z,"color":[0,0,0],"width":4,"name":"up_mouse"}
        self.dm = {"pos":random_array(pt.MOUSE),"key":pg.K_x,"color":[0,0,0],"width":4,"name":"down_mouse"}
        
        self.list = [self.ore,
                  self.ole,
                  self.ire,
                  self.ile,
                  self.ure,
                  self.ule,
                  self.dre,
                  self.dle,
                  self.um,
                  self.dm]
        self.movingpoint = None
        self.modify = None
        
    def key_down(self,state):
        key = pg.key.get_pressed()
        for e in self.list:
            if key[e['key']]:
                self.modify = e
                state["bar_r"].value_update(value = self.modify["color"][0])
                state["bar_g"].value_update(value = self.modify["color"][1])
                state["bar_b"].value_update(value = self.modify["color"][2])
                state["bar_s"].value_update(value = self.modify["width"])
                print(self.modify["name"])
                return self.modify['name']
    def mouse_down(self):
        if self.modify !=None:
            pos = pg.mouse.get_pos()
            for e in range(len(self.modify['pos'])):
                
                dis = ((self.modify['pos'][e][0] - pos[0])**2 + (self.modify['pos'][e][1] - pos[1])**2)**(1/2)
                if dis < pt.POINT_SIZE:
                    self.movingpoint = e
                    return e
        self.movingpoint = None
        return None
    def mouse_update(self):
        if self.modify !=None:
            if self.movingpoint !=None:
                pos = pg.mouse.get_pos()
                self.modify['pos'][self.movingpoint][0] = pos[0]
                self.modify['pos'][self.movingpoint][1] = pos[1]
                
    def mouse_up(self):
        self.movingpoint = None
        
    def draw(self,screen):
        for e in self.list:
            pg.draw.lines(screen,e["color"],False,bl.besierline(e["pos"],pt.BL_COUNT),e["width"])
        if self.modify!= None:
            for e in self.modify["pos"]:
                pg.draw.circle(screen,(0,0,0),e,pt.POINT_SIZE)
    def change_draw(self,change_face,percent,screen):
        for e in range(len(self.list)):
            points_1 = self.list[e]["pos"]
            points_2 = change_face.list[e]["pos"]
            width = int(self.list[e]["width"] * percent + change_face.list[e]["width"] *(float(1)-percent))
            besierpoint = bl.besierline_percent(points_1,points_2,percent,pt.BL_COUNT)
            colortemp = []
            for a in range(3):
                cell = int(self.list[e]["color"][a] *percent + change_face.list[e]["color"][a]*(float(1)-percent))
                if cell>=255:
                    cell = 255
                if cell <=0:
                    cell = 0
                colortemp.append(cell)
            print(colortemp)
            pg.draw.lines(screen,colortemp,False,besierpoint,width)