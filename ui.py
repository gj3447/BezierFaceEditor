import pygame as pg

class BAR:
    def __init__(self,value,position , color , callback):
        self.value_max= value
        self.value = 0
        self.value_position = min([position[0][1],position[1][1]])
        self.value_callback = callback
        self.position = position
        self.color = color
        self.click = False
        self.x_max = max([self.position[0][0],self.position[1][0]])
        self.x_min = min([self.position[0][0],self.position[1][0]])
        self.y_min = min([self.position[0][1],self.position[1][1]])
        self.y_max = max([self.position[0][1],self.position[1][1]])
        self.height = self.y_max - self.y_min
        self.width = self.x_max - self.x_min
    def value_update(self,value):
        self.value = value
        percent = float(self.value)/float(self.value_max)
        self.value_position = percent*self.height + self.y_min
    def mouse_down(self):
        pos = pg.mouse.get_pos()
        if self.inside(pos):
            self.click = True
    def mouse_update(self,state):
        pos = pg.mouse.get_pos()
        if self.click :
            self.value_position = pos[1]
            if self.value_position <self.y_min:
                self.value_position = self.y_min
            if self.value_position > self.y_max:
                self.value_position = self.y_max
            percent = float(self.value_position - self.y_min)/float(self.height)
            self.value = percent * self.value_max
            if self.value_callback!=None:
                self.value_callback(self.value,state)
    def mouse_up(self):
        self.click = False
    def inside(self,pos):
        x= (pos[0]-self.position[0][0]) * (pos[0]-self.position[1][0])
        y = (pos[1]-self.position[0][1]) * (pos[1]-self.position[1][1])
        if x<=0 and y<=0:
            return True
        else:
            return False
    def draw(self,screen):
        pg.draw.rect(screen,[0,0,0], pg.Rect(int(self.x_min),int(self.y_min),int(self.width),int(self.height)))
        pg.draw.rect(screen, self.color, pg.Rect(int(self.x_min), int(self.y_min), int(self.width),int(self.value_position-self.y_min)))
        
    
    