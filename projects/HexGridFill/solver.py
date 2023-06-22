def has_partition(dgm: DarkNShadowGameMock):
    from nice_design.iteration import GraphIterator
    vertices = [t._pos for t in dgm._model._grid_model.get_all_tiles() if dgm._model.is_passable(t._pos)]
    if len(vertices) == 0:
        return False
    one_val = vertices[-1]
    gi = GraphIterator()
    gi.set_child_func(lambda st, pos: list(filter(dgm._model.is_passable, dgm._model.get_nebors(pos))))
    gi.set_initial_value(one_val)
    return len([*gi]) != len(vertices)
def empty_spaces(pos, dgm):
    return list(filter(dgm._model.is_passable, dgm._model.get_nebors(pos)))
def has_finished(dgm):
    vertices = [t._pos for t in dgm._model._grid_model.get_all_tiles() if dgm._model.is_passable(t._pos)]
    return len(vertices) == 0
def move(pos, dgm):
    dgm._event._selected_pos = pos
    dgm._event.callback()
def solve(dgm):
    while not has_finished(dgm):
        head = dgm._model.current
        moveable_pos(head, dgm)
def moveable_pos(pos, dgm):
    move(pos, dgm)
    for val in empty_spaces(dgm._model.current, dgm):
        if has_partition(dgm):
            goback(dgm)
        else:
            moveable_pos(val, dgm)
def goback(dgm):
    dgm._back_btn.callback(None)