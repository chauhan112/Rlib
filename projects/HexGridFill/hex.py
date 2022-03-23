from RPygame import IPyGameObject, IPositionable, IEventable, MouseClick, ICanvas, \
    IEvent, Game, StaticScreen,RegularPolygon, PolyColorChange, NonRegularPolygon, PButton
import numpy as np
import pygame
from OpsDB import IOps
BOARD_SIZE = 500, 500
class ITile:
    def get_nebors(self):
        raise NotImplementedError('abstract method')
    def get_position(self):
        raise NotImplementedError('abstract method')
DIRECTIONS = [(1, -1, 0), (-1, 1, 0),
              (0, 1, -1), (0, -1, 1),
              (1, 0, -1), (-1, 0, 1)]
class IHexBoard:
    def get_tile(self, pos):
        raise NotImplementedError('abstract method')
    def set_radius(self, radius):
        raise NotImplementedError('abstract method')
class PosCalculator:
    def __init__(self):
        self._direction_map = {
            '-a': (1, -1, 0), 'a': (-1, 1, 0),
            'b': (0, 1, -1), '-b': (0, -1, 1),
            'c': (1, 0, -1), '-c': (-1, 0, 1)
        }
    def get_pos(self, steps = []):
        pos = (0,0,0)
        for f in steps:
            pos = ADD(pos, self._direction_map[f])
        return pos
    def get_pos_direction(self, x, y, z):
        steps = []
        dirs = ['a', 'b', 'c']
        for i, val in enumerate([x,y,z]):
            step = dirs[i]
            if val < 0:
                step = f'-{step}'
            steps += [step]*abs(val)
        return self.get_pos(steps)
def ADD(tup1, tup2):
    a,b,c = tup1
    a2,b2,c2 = tup2
    return (a+a2, b+b2, c+c2)
def MULTIPLY(tup, fac):
    a,b,c = tup
    return a*fac, b*fac, c*fac
class HexTile(ITile):
    def __init__(self, q_pos, r_pos, s_pos):
        self._pos = (q_pos, r_pos, s_pos)
        self._value = None
    def get_nebors(self):
        return [ADD(self._pos, dire) for dire in DIRECTIONS]
    def set_value(self, val):
        self._value = val
    def get_value(self):
        return self._value
class HexBoard(IHexBoard):
    def __init__(self, radius = 1):
        self.set_radius(radius)
        self._board = {}
    def set_tile_value(self, tile_pos, value):
        self.get_tile(tile_pos).set_value(value)
    def set_tiles_value(self, tiles_pos, value):
        for tile_pos in tiles_pos:
            self.set_tile_value(tile_pos, value)
    def get_tile(self, pos):
        if not self.lies_in_board(pos):
            raise IOError("Out of board")
        if pos not in self._board:
            if sum(pos) != 0:
                raise IOError("Invalid index")
            self._board[pos] = HexTile(*pos)
        return self._board[pos]
    def lies_in_board(self, pos):
        res = True
        for va in pos:
            res = res and abs(va) <= self._radius
        return res
class IGame:
    def solve(self):
        pass
class HexTileGameSolver(IGame):
    def set_data(self, board: IHexBoard, initial_pos, obstacles_pos = []):
        self._board = board
        self._initial_pos = initial_pos
        self._obstacles_pos = obstacles_pos
        self._board.set_tiles_value(obstacles_pos,"wall")
    def solve(self):
        pass
    def set_board(self, board: IHexBoard):
        self._board = board
    def export(self, name):
        if not name.endswith(".pkl"):
            name += '.pkl'
        SerializationDB.pickleOut({'initial_pos': self._initial_pos,
                                   'walls': self._obstacles_pos,
                                   'radius': self._board._radius}, name)
    def load_from_pickle(self, name):
        vals = SerializationDB.readPickle(name)
        self.set_data(HexBoard(vals['radius']), vals['initial_pos'], vals['walls'])
        
    def partition_check(nebors):
        if len(nebors) == 1:
            return True
        vertices = [tile._pos for tile in gam._grid_model.get_all_tiles()]
        graph = {}
        for tile in vertices:
            if gam.is_passable(tile):
                nebors = gam.get_nebors(tile)
                graph[tile] = {tar: 1 for tar in (filter(gam.is_passable, nebors))}
        return vertices, graph
        
class HexTileForRendering:
    def __init__(self, coordinate):
        self._pos = coordinate
        self._center = None
    def get_pixel_center(self, grid_center, radius):
        if self._center is None:
            arr = np.array([0.5 * np.sqrt(3)*radius, -1.5* radius])
            self._center = arr * self._pos + grid_center
        return self._center
class HexGridModel(IHexBoard):
    def __init__(self, center = (0,0)):
        self.set_radius(1)
        self._pos_indices = None
        self._grid_center = center
        self._grid_model = None
    def set_radius(self, radius):
        self._radius = radius
    def grid_center(self):
        return self._grid_center
    def get_tile(self, pos):
        if self._pos_indices is None:
            self._make_tiles()
        return self._pos_indices[pos]
    def _make_tiles(self):
        self._pos_indices = {}
        for i in range(-2 * self._radius, 2 * (self._radius + 1)):
            for j in range(-1*self._radius, self._radius+ 1):
                if self.lies_inside_grid((i,j)):
                    self._pos_indices[(i,j)] = HexTileForRendering((i,j))
    def get_all_tiles(self):
        if self._pos_indices is None:
            self._make_tiles()
        return list(self._pos_indices.values())
    def lies_inside_grid(self, pos):
        i, j = pos
        if self._grid_model is None:
            r = self._radius
            val = [(2*r,0),(r,r), (-r,r)]
            pnts = np.array(val)
            val += list(map(lambda x: tuple(x), -1* pnts))
            self._grid_model = NonRegularPolygon(val)
        return self._grid_model.lies(pos) and (i+j) % 2 == 0
class HexGridRender(IPyGameObject, IPositionable, IEventable):
    def __init__(self):
        self._polygons = None
        self._event = None
        self.set_direction_of_tiles((1,0))
    def set_position(self, pos):
        self._pos = pos
    def add(self, screen: ICanvas):
        polygons = self.get_polygons()
        for poly in polygons:
            poly.add(screen)
    def get_polygons(self):
        if self._polygons is None:
            self._polygons = []
            for tile in self._board.get_all_tiles():
                center = tile.get_pixel_center(self._board.grid_center(), self._rad)
                hexagonal = 6
                reg = RegularPolygon(hexagonal)
                reg.set_position(center)
                reg.set_one_point_location(self._rad-2, self._dir)
                pcc = PolyColorChange(reg)
                reg.set_event(pcc)
                reg.coordinate = tile._pos
                self._polygons.append(reg)
        return self._polygons
    def set_grid_model(self, board: IHexBoard):
        self._board = board
    def set_tile_radius(self, radius):
        self._rad = radius
    def get_event(self):
        return self._event
    def set_event(self, event: IEvent):
        self._event = event
    def set_direction_of_tiles(self, dire):
        self._dir = dire
class GridObjClick(MouseClick):
    def callback(self):
        for poly in self._parent.get_polygons():
            event = poly.get_event()
            if poly.lies(self._point):
                event.callback()
                break
class GameModel:
    def __init__(self):
        self.current = (0,0)
        self._nebor_of_origin = np.array([(2,0), (1,1), (-1, 1), (-2,0), (-1,-1), (1,-1)])
        self._grid_model = HexGridModel(np.array(BOARD_SIZE)/2)
        self._grid_model.set_radius(4)
        self._info = {}
        self.color = self._get_color()
        self._visited = {}
        self._obstacles_pos = set()
    def load_from_pickle(self, pkl):
        from SerializationDB import SerializationDB
        val = SerializationDB.readPickle(pkl)
        self.current = val['start-point']
        self._obstacles_pos = set(val['obstacles'])
        self._grid_model.set_radius(val['radius'])
    def export(self, name):
        from SerializationDB import SerializationDB
        if not name.endswith(".pkl"):
            name += '.pkl'
        SerializationDB.pickleOut({'obstacles': self._obstacles_pos, 'start-point': self.current,
            'radius': self._grid_model._radius}, name)
    def is_obstacle(self, pos):
        return pos in self._obstacles_pos
    def is_visited(self, pos):
        if pos in self._visited:
            return self._visited[pos]
        return False
    def set_visited(self, pos):
        self._visited[pos] = True
    def is_passable(self, pos):
        return not self.is_obstacle(pos) and not self.is_visited(pos) and self._grid_model.lies_inside_grid(pos)
    def get_nebors(self, pos):
        nebors = self._nebor_of_origin + pos
        return [tuple(va) for va in nebors]
    def get_position_in_direction(self, pos, pos2):
        pos = np.array(pos)
        direction = pos2 - pos
        res = []
        while self._grid_model.lies_inside_grid(pos):
            res.append(tuple(pos))
            pos += direction
            if not self.is_passable(tuple(pos)):
                break
        return res
    def _get_color(self):
        from modules.Explorer.personalizedWidgets import EmptyClass
        ec = EmptyClass()
        ec.head = (255, 0, 0)
        ec.unvisited = (0,0, 0)
        ec.obstacle = (255,255, 0)
        ec.visited = (0,0,255)
        return ec
class DnSAction(MouseClick):
    def __init__(self, parent):
        self._parent = parent
        self._pos_poly_map = None
        self._path = []
    def check(self, event):
        if not super().check(event):
            return False
        for poly in self._parent.get_polygons():
            event = poly.get_event()
            if poly.lies(self._point):
                self._selected_pos = poly.coordinate
                return True
        return False
    def callback(self):
        current = self._model.current
        nebors_of_current = self._model.get_nebors(current)
        not_visited_nebors = list(filter(lambda x: not self._model.is_visited(x), nebors_of_current))
        if self._selected_pos in not_visited_nebors:
            line_of_movement = self._model.get_position_in_direction(current, self._selected_pos)
            poly = None
            for pos in line_of_movement:
                poly = self._get_poly_for_position(pos)
                poly.set_color(self._model.color.visited)
                self._model.set_visited(pos)
            if poly is not None:
                poly.set_color(self._model.color.head)
                self._model.current = pos
                self._path.append(line_of_movement)
    def set_model(self, model: GameModel):
        self._model = model
    def _get_poly_for_position(self, pos):
        if self._pos_poly_map is None:
            self._pos_poly_map = {}
            for poly in self._parent.get_polygons():
                self._pos_poly_map[poly.coordinate] = poly
        return self._pos_poly_map[pos]
class BackButton:
    def __init__(self):
        self._mouse_click = MouseClick(None)
        self._btn = PButton()
        self._btn.set_text("back", size=20)
        self._btn.set_size(40, 80)
        event = self._btn.get_event()
        event.set_check_func(self.check_func)
        event.set_event_func(self.callback)

    def callback(self, state):
        dgm = self._dgm
        if len(dgm._event._path) == 0:
            return
        last_path = dgm._event._path.pop()
        first= last_path[0]
        for val in last_path:
            dgm._model._visited[val] = False
            poly = dgm._event._get_poly_for_position(val)
            poly.set_color(dgm._model.color.unvisited)
        dgm._model.set_visited(first)
        dgm._model.current = first
        dgm._event._get_poly_for_position(first).set_color(dgm._model.color.head)
        
    def check_func(self, state, event):
        clicked = self._mouse_click.check(event)
        return clicked and self._btn.lies(self._mouse_click._point)
    
    def get_button(self):
        return self._btn 
    
    def set_model(self, game_model):
        self._dgm = game_model
class DarkNShadowGameMock(IOps):
    def __init__(self):
        self._game = None
        self._screen = None
        self.tile_radius = 30
        self._model = GameModel()
        self._gr = HexGridRender()
        self._gr.set_grid_model(self._model._grid_model)
        self._gr.set_tile_radius(self.tile_radius)
        self._event = DnSAction(self._gr)
        self._event.set_model(self._model)
        self._gr.set_event(self._event)
        self._gr.set_direction_of_tiles((0,1))
        self._game = Game()
        self._back_btn = BackButton()
        self._back_btn.set_model(self)
    def execute(self):
            self._load_initial_state()
        # try:
            sc = StaticScreen(BOARD_SIZE)
            self._game.add_screen(sc)
            sc.setframerate(30)
            sc.add_object(np.array(BOARD_SIZE)/2, self._gr)
            sc.add_object((0,0), self._back_btn.get_button())
            self._game.start()
        # except Exception as e:
            # print(e)
            # pygame.quit()
    def load(self, pkl):
        self._model.load_from_pickle(pkl)
    def _load_initial_state(self):
        self._event._get_poly_for_position(self._model.current).set_color(self._model.color.head)
        for pos in self._model._obstacles_pos:
            self._event._get_poly_for_position(pos).set_color(self._model.color.obstacle)
class ClickInfo(PolyColorChange):
    def callback(self):
        super().callback()
        self._func(self)
    def set_func(self, func):
        self._func = func
class Main:
    def grid_test(radius, tile_radius = 30, callback=None):
        hgm = HexGridModel(np.array(BOARD_SIZE)/2)
        hgm.set_radius(radius)
        gr = HexGridRender()
        gr.set_grid_model(hgm)
        gr.set_tile_radius(tile_radius)
        gr.set_direction_of_tiles((0,1))
        goc = GridObjClick(gr)
        gr.set_event(goc)
        if callback is not None:
            for p in gr.get_polygons():
                cf = ClickInfo(p)
                cf.set_func(callback)
                p.set_event(cf)
        g = Game()
        sc = StaticScreen(BOARD_SIZE)
        g.add_screen(sc)
        sc.setframerate(30)
        sc.add_object(np.array(BOARD_SIZE)/2, gr)
        g.start()
    def game(file):
        dgm = DarkNShadowGameMock()
        dgm.load(file)
        dgm.execute()