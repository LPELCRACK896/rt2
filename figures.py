import lpmath as lpm
import numpy as np
from math import pi
WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, sceneObj, textCoords):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObj = sceneObj
        self.textCoords = textCoords

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0, matType = OPAQUE, texture = None):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.matType = matType
        self.texture = texture


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = lpm.suma_o_resta_vectores(self.center, orig, True)
        tca = lpm.productoPunto(L, dir)
        d = (lpm.magnitud_vector(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        P = lpm.suma_o_resta_vectores(orig, [t0 * d for d in dir])
        normal = lpm.suma_o_resta_vectores(P, self.center, True)
        normal = lpm.normalizaVector(normal)

        u = np.arctan2(normal[2], normal[0])/ (2 * pi) + 0.5
        v = np.arccos(-normal[1])/pi
        uvs  = (u, v)
        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         sceneObj = self,
                         textCoords=uvs)
