from controllers.Renderable import Renderable

class Scene:
    """
    Manages a collection of renderable objects within a 3D environment.

    The Scene class is responsible for holding all objects that can be drawn
    (i.e., instances of classes implementing the Renderable interface).
    """
    def __init__(self):
        self._objects = []
        
    def add(self, obj:Renderable):
        if obj not in self._objects:
            self._objects.append(obj)
        
    def remove(self, obj:Renderable):
        if obj in self._objects:
            self._objects.remove(obj)
        
    def render_all(self, target_stage):
        for obj in self._objects:
            obj.render(target_stage)
            