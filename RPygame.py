import pygame
import numpy as np
class IEvent:
    def check(self, event) -> bool:
        raise NotImplementedError('abstract method')
    def callback(self) -> bool:
        raise NotImplementedError('abstract method')
class IPyGameObject:
    def add(self, screen):
        raise NotImplementedError('abstract method')
class IEventable:
    def get_event(self) -> IEvent:
        raise NotImplementedError('abstract method')
class IPositionable:
    def set_position(self, pos):
        raise NotImplementedError('abstract method')
class PositionableObj(IPositionable, IPyGameObject):
    pass
class NeutralEvent(IEvent):
    def check(self, event):
        return False
class Colorable:
    def set_color(self, color):
        self._color = color
class ICanvas:
    def add_object(self, pos: tuple, obj: IPyGameObject):
        raise NotImplementedError('abstract method')
    def next_frame(self, event):
        raise NotImplementedError('abstract method')
    def get(self):
        raise NotImplementedError('abstract method')
class Game:
    def __init__(self):
        pygame.init()
    def start(self):
        self._func()
        pygame.quit()
    def _func(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                self._screen.next_frame(event)
    def add_screen(self, screen: ICanvas):
        self._screen = screen
class PCircle(IPyGameObject, IPositionable, Colorable):
    def __init__(self):
        self.set_radius(6)
        self.set_set_color((0,0,255))
    def set_radius(self, rad):
        self._radius = rad
    def add(self, screen: ICanvas):
        pygame.draw.circle(screen.get(), self._color, self._pos, self._radius)
    def set_position(self, pos):
        self._pos = pos
class StaticScreen(ICanvas):
    def __init__(self, resolution):
        self._resolution = resolution
        self._screen = pygame.display.set_mode(self._resolution)
        self.set_background_color((255, 255, 255))
        self._objs = []
        self._clock = None
    def set_background_color(self, color: tuple):
        self._screen.fill(color)
    def add_object(self, pos: tuple, obj: PositionableObj):
        self._objs.append((pos, obj))
    def get(self):
        return self._screen
    def next_frame(self, event):
        for pos, obj in self._objs:
            if isinstance(obj, IPositionable):
                obj.set_position(pos)
            if isinstance(obj, IEventable):
                obj_event = obj.get_event()
                if obj_event.check(event):
                    obj_event.callback()
            obj.add(self)
        pygame.display.flip()
        if self._clock is not None:
            self._clock.tick(self._rate)
    def clear(self):
        self._objs.clear()
    def setframerate(self, frame_rate):
        self._rate = frame_rate
        self._clock = pygame.time.Clock()
class RectangularScreen(IPyGameObject, IPositionable, Colorable):
    def __init__(self, size):
        self._size = size
        self._surface = None
        self._pos_rect = None
        self._pos = (0,0)
        self.set_color((255,255,255))
    def set_image(self, img_path):
        from pygame.locals import RLEACCEL
        self._img_path = img_path
        self._surface = pygame.image.load(self._img_path).convert()
        self._surface.set_colorkey((255, 255, 255), RLEACCEL)
    def add(self, screen: ICanvas):
        surface = self.get_surface()
        screen.get().blit(surface, self.get_rect())
    def get_rect(self):
        if self._pos_rect is None:
            self._pos_rect = self._surface.get_rect(center=self._pos)
        return self._pos_rect
    def set_position(self, pos):
        self._pos = pos
    def get_surface(self):
        if self._surface is None:
            self._surface = pygame.surface(self._size)
            self._pos_rect = self.get_rect()
        return self._surface
class NonRegularPolygon(IPyGameObject, Colorable):
    def __init__(self, points):
        self._points = points
        self.set_color((0,0,0))
        from shapely.geometry import Polygon as Poly
        self._poly_model = Poly(self._points)
    def add(self, screen: ICanvas):
        pygame.draw.polygon(screen.get(), self._color, self._points)
    def lies(self, point: tuple):
        from shapely.geometry import Point
        return self._poly_model.intersects(Point(point))
class RegularPolygon(IPyGameObject, IPositionable, Colorable, IEventable):
    def __init__(self, nr_of_sides, one_point_loc = None):
        self.set_color((0,0,0))
        self._n_side = nr_of_sides
        self._one_point = one_point_loc
        self._poly = None
        self._event = NeutralEvent()
    def add(self, screen: ICanvas):
        self._make_poly()
        self._poly.set_color(self._color)
        self._poly.add(screen)
    def set_position(self, pos):
        self._pos = pos
    def _make_points(self):
        from shapely.geometry import LineString
        if self._one_point is None:
            self._one_point = self._radius * np.array(self._dir) + np.array(self._pos)
        rot_angle = 360 / self._n_side
        line  = LineString([self._one_point, self._pos])
        self._points = []
        from shapely import affinity
        for i in range(self._n_side):
            an = rot_angle* (i+1)
            self._points.append(affinity.rotate(line, an, self._pos).coords[0])
    def set_one_point_location(self, length, direction=(1,0)):
        self._radius = length
        self._dir = np.array(direction) / np.linalg.norm(direction)
    def set_event(self, event: IEvent):
        self._event = event
    def get_event(self):
        return self._event
    def _make_poly(self):
        if self._poly is None:
            self._make_points()
            self._poly = NonRegularPolygon(self._points)
    def lies(self, pos):
        self._make_poly()
        return self._poly.lies(pos)
class MouseClick(IEvent):
    def __init__(self, parent):
        self._parent = parent
    def check(self, event):
        from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
        val = event.type == MOUSEBUTTONDOWN
        if val:
            self._point = pygame.mouse.get_pos()
        return val
    def callback(self):
        pass
class PolyColorChange(MouseClick):
    def __init__(self, parent: RegularPolygon):
        self._parent = parent
    def check(self, event):
        if super().check(event):
            return self._parent.lies(self._point)
        return False
    def callback(self):
        import random
        self._parent.set_color((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
class GEventable(IEvent):
    def set_event_func(self, func):
        self._func = func
    def set_check_func(self,check_func):
        self._check_func = check_func
    def check(self, event):
        return self._check_func(self, event)
    def set_data(self, data):
        self._data = data
    def callback(self):
        self._func(self)
    def set_parent(self, parent):
        self._parent = parent
class PButton(IPyGameObject, IEventable, Colorable, IPositionable):
    def __init__(self):
        self._event = None
        self._poly = None
        self._height = None
        self._width = None
        self._top_left = None
        self._center = None
        self._pytext = None
        self._background_color = (170,170,170) # gray
        self.set_text("")
    def set_top_left_position(self, pos):
        self._top_left = pos
        self._set_points()
    def set_center(self, pos):
        self._center = pos
    def set_size(self, height, width):
        self._height = height
        self._width = width
        self._set_points()
    def set_text(self, text, font="arial", size= 35, pos = (2,2)):
        self._text = text
        self._font = font
        self._font_size = size
        self._text_pos = pos
    def get_event(self):
        if self._event is None:
            self._event = GEventable()
            self._event.set_check_func(lambda st, x: False)
            self._event.set_parent(self)
        return self._event
    def add(self, screen):
        a,b = self._top_left
        pygame.draw.rect(screen.get(), self._background_color, [a,b,self._width,self._height])
        i, j = self._text_pos
        if self._pytext is None:
            smallfont = pygame.font.SysFont(self._font, self._font_size)
            self._pytext = smallfont.render(self._text , True , (255,255,255))
        screen.get().blit(self._pytext, (a + i,b +j))
    def lies(self, pos):
        if self._poly is None:
            a, b = self._center
            h_2, w_2 = self._height/2, self._width/2
            self._top_left = (a-h_2, b - w_2)
            self._poly = NonRegularPolygon([self._top_left, (a-h_2, b + w_2),
                                            (a + h_2, b + w_2), (a + h_2, b-w_2)])
        return self._poly.lies(pos[::-1])
    def _set_points(self):
        if self._height is not None and self._top_left is not None:
            a, b = self._top_left
            self._center =  a + self._height/2, b + self._width /2
    def set_position(self, pos):
        self.set_top_left_position(pos)