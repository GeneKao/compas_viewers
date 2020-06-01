from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from random import randint

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# get shaders
from OpenGL.GL import shaders
# import the vertext buffer object
from OpenGL.arrays import vbo

from compas.utilities import hex_to_rgb
from compas.utilities import rgb_to_hex

from compas.utilities import flatten
from compas_viewers.core import GLWidget
from compas_viewers.core import Grid
from compas_viewers.core import Axes
import numpy as np

__all__ = ['View']


hex_to_rgb = partial(hex_to_rgb, normalize=True)

SHIFT = 16777248
CTRL = 16777249


def flist(items):
    return list(flatten(items))


class View(GLWidget):
    """"""

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller
        self.n = 0
        self.v = 0
        self.e = 0
        self.f = 0

        self.selecting = False
        self.deselecting = False
        self.selected = set()

    @property
    def nodes(self):

        # print(list(self.controller.scene.traverse()))
        # return [self.controller.scene.nodes[key] for key in self.controller.scene.nodes]
        return self.controller.scene.traverse()

    @property
    def settings(self):
        return self.controller.settings

    # ==========================================================================
    # CAD
    # ==========================================================================

    def setup_grid(self):
        grid = Grid()
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)
        grid.draw()
        glEndList()
        self.display_lists.append(index)

    def setup_axes(self):
        axes = Axes()
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)
        axes.draw()
        glEndList()
        self.display_lists.append(index)

    # ==========================================================================
    # selecting
    # ==========================================================================

    def mousePressEvent(self, event):
        super(View, self).mousePressEvent(event)
        if self.isActiveWindow() and self.underMouse():
            self.mouse.last_pos = event.pos()
            x = self.mouse.last_pos.x()
            y = self.mouse.last_pos.y()

            if self.mouse.buttons['left']:
                rgb = self.instance_map[y][x]
                selected_hex = rgb_to_hex(rgb)

                # when clicked on objects
                if selected_hex in self.intances:
                    for hex_key in self.intances:
                        if selected_hex == hex_key:
                            if not self.deselecting:
                                self.select(self.intances[hex_key])
                            else:
                                self.deselect(self.intances[hex_key])
                        elif not self.selecting and not self.deselecting:
                            self.deselect(self.intances[hex_key])
                    print('selected:', self.selected)

                # when clicked on blank area
                elif not self.selecting and not self.deselecting:
                    for item in list(self.selected):
                        self.deselect(item)

    def keyPressAction(self, key):
        if key == SHIFT:
            self.selecting = True
            print('start selecting')
        elif key == CTRL:
            self.deselecting = True
            print('start deselecting')

    def keyReleaseAction(self, key):
        if key == SHIFT:
            self.selecting = False
            print('stop selecting')
        elif key == CTRL:
            self.deselecting = False
            print('stop deselecting')

    def select(self, item):
        if isinstance(item, dict):
            print('seleted attribute: ', item)
        else:
            self.selected.add(item)
            item.widget.setSelected(True)

    def deselect(self, item):
        if isinstance(item, dict):
            pass
        else:
            if item in self.selected:
                self.selected.remove(item)
            item.widget.setSelected(False)

    # ==========================================================================
    # painting
    # ==========================================================================

    def paint(self):

        self.draw_instances()

        glDisable(GL_DEPTH_TEST)
        for dl in self.display_lists:
            glCallList(dl)

        glEnable(GL_DEPTH_TEST)
        self.draw_buffers()
        self.draw_rotation_center()

    def random_hex(self):
        while True:
            unique_hex = '#%02x%02x%02x' % (randint(0, 255), randint(0, 255), randint(0, 255))
            if unique_hex not in self.intances and unique_hex != '#ffffff':
                return unique_hex

    def make_buffers(self):

        # create instances map only at first time
        if not hasattr(self, 'intances'):
            self.intances = {}
            for i, m in enumerate(self.nodes):
                m.instance_color = self.random_hex()
                self.intances[m.instance_color] = m

                vertices = list(m.view.vertices)
                m.vertices_instance_color = []
                for v in vertices:
                    _hex = self.random_hex()
                    m.vertices_instance_color.append(_hex)
                    self.intances[_hex] = {'vertex': v, 'mesh': i}

                edges = list(m.view.edges)
                m.edge_instance = []
                m.edges_instance_color = []
                m.edge_xyz = []
                for j, e in enumerate(edges):

                    v1, v2 = e
                    m.edge_xyz.extend(m.view.xyz[v1])
                    m.edge_xyz.extend(m.view.xyz[v2])

                    m.edge_instance.extend([j * 2, j * 2 + 1])

                    _hex = self.random_hex()
                    m.edges_instance_color.append(_hex)
                    m.edges_instance_color.append(_hex)
                    self.intances[_hex] = {'edge': e, 'mesh': i}

        self.buffers = []
        for node in self.nodes:
            xyz = flist(node.view.xyz)
            vertices = list(node.view.vertices)
            edges = flist(node.view.edges)
            faces = flist(node.view.faces)
            faces_back = flist(face[::-1] for face in node.view.faces)
            vertices_instance_color = flist(hex_to_rgb(vc) for vc in node.vertices_instance_color)
            edges_instance_color = flist(hex_to_rgb(c) for c in node.edges_instance_color)
            instance_color = flist(hex_to_rgb(node.instance_color) for key in node.view.xyz)

            if hasattr(node.view, 'vertices_color'):
                vertices_color = flist(vc for vc in node.view.vertices_color)
            else:
                vertices_color = flist(hex_to_rgb('#000000') for key in node.view.vertices)
            edges_color = '#000000'
            face_color = node.settings.get("color", "#cccccc")

            edges_color = flist(hex_to_rgb(edges_color) for key in edges)
            faces_color = flist(hex_to_rgb(face_color) for key in node.view.xyz)
            faces_color_back = flist(hex_to_rgb(face_color) for key in node.view.xyz)

            vertices_selected_color = flist(hex_to_rgb('#999900') for key in node.view.vertices)
            edges_selected_color = flist(hex_to_rgb('#aaaa00') for key in edges)
            faces_selected_color = flist(hex_to_rgb('#ffff00') for key in node.view.xyz)
            faces_selected_color_back = flist(hex_to_rgb('#ffff00') for key in node.view.xyz)

            self.buffers.append({

                'isSelected': node.widget.isSelected,

                'xyz': self.make_vertex_buffer(xyz),
                'vertices': self.make_index_buffer(vertices),
                'edges': self.make_index_buffer(edges),
                'edges.instance': self.make_index_buffer(node.edge_instance),
                'faces': self.make_index_buffer(faces),
                'faces:back': self.make_index_buffer(faces_back),
                'vertices.color': self.make_vertex_buffer(vertices_color, dynamic=True),
                'vertices.instance.color': self.make_vertex_buffer(vertices_instance_color, dynamic=True),
                'vertices.selected.color': self.make_vertex_buffer(vertices_selected_color, dynamic=True),
                'edges.color': self.make_vertex_buffer(edges_color, dynamic=True),
                'edges.xyz': self.make_vertex_buffer(node.edge_xyz),
                'edges.instance.color': self.make_vertex_buffer(edges_instance_color, dynamic=True),
                'edges.selected.color': self.make_vertex_buffer(edges_selected_color, dynamic=True),
                'faces.color': self.make_vertex_buffer(faces_color, dynamic=True),
                'faces.color:back': self.make_vertex_buffer(faces_color_back, dynamic=True),
                'faces.selected.color': self.make_vertex_buffer(faces_selected_color, dynamic=True),
                'faces.selected.color:back': self.make_vertex_buffer(faces_selected_color_back, dynamic=True),
                'instance.color': self.make_vertex_buffer(instance_color),
                'n': len(xyz),
                'v': len(vertices),
                'e': len(edges),
                'f': len(faces)})

        self.create_shader()

    def draw_buffers(self):
        if not self.buffers:
            return

        for buffer in self.buffers:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, buffer['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            selected = buffer['isSelected']()

            if self.settings['faces.on']:
                if selected:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['faces.selected.color'])
                else:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['faces.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['faces'])
                glDrawElements(GL_TRIANGLES, buffer['f'], GL_UNSIGNED_INT, None)

                if selected:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['faces.selected.color:back'])
                else:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['faces.color:back'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['faces:back'])
                glDrawElements(GL_TRIANGLES, buffer['f'], GL_UNSIGNED_INT, None)

            if self.settings['edges.on']:
                glLineWidth(self.settings['edges.width:value'])
                if selected:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['edges.selected.color'])
                else:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['edges.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['edges'])
                glDrawElements(GL_LINES, buffer['e'], GL_UNSIGNED_INT, None)

            if self.settings['vertices.on']:
                glPointSize(self.settings['vertices.size:value'])
                if selected:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['vertices.selected.color'])
                else:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['vertices.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['vertices'])
                glDrawElements(GL_POINTS, buffer['v'], GL_UNSIGNED_INT, None)

            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

        self.draw_shader()

    def draw_rotation_center(self):

        if self.mouse.buttons['right']:

            self.sphere_buffer = {
                'xyz': self.make_vertex_buffer(self.camera.target),
                'vertices': self.make_index_buffer([0]),
                'vertices.color': self.make_vertex_buffer([0.7, 1, 0], dynamic=True),
                'v': 1
            }

            # draw sphere
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, self.sphere_buffer['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            glPointSize(15)
            glBindBuffer(GL_ARRAY_BUFFER, self.sphere_buffer['vertices.color'])
            glColorPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.sphere_buffer['vertices'])
            glDrawElements(GL_POINTS, self.sphere_buffer['v'], GL_UNSIGNED_INT, None)

            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

    def draw_instances(self):
        # save out a instance map in background
        if not self.buffers:
            return
        for buffer in self.buffers:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, buffer['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            if self.settings['faces.on']:
                glBindBuffer(GL_ARRAY_BUFFER, buffer['instance.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['faces'])
                glDrawElements(GL_TRIANGLES, buffer['f'], GL_UNSIGNED_INT, None)

                glBindBuffer(GL_ARRAY_BUFFER, buffer['instance.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['faces:back'])
                glDrawElements(GL_TRIANGLES, buffer['f'], GL_UNSIGNED_INT, None)

            if self.settings['vertices.on']:
                glPointSize(self.settings['vertices.size:value'])
                glBindBuffer(GL_ARRAY_BUFFER, buffer['vertices.instance.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['vertices'])
                glDrawElements(GL_POINTS, buffer['v'], GL_UNSIGNED_INT, None)

            if self.settings['edges.on']:
                glBindBuffer(GL_ARRAY_BUFFER, buffer['edges.xyz'])
                glVertexPointer(3, GL_FLOAT, 0, None)
                glLineWidth(self.settings['edges.width:value'])
                glBindBuffer(GL_ARRAY_BUFFER, buffer['edges.instance.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['edges.instance'])
                glDrawElements(GL_LINES, buffer['e'], GL_UNSIGNED_INT, None)

            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

        instance_buffer = glReadPixels(0, 0, self.GL_width, self.GL_height, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
        instance = np.frombuffer(instance_buffer, dtype=np.uint8).reshape(self.GL_height, self.GL_width, 3)

        # for heigh-res screens
        size = self.size()
        ratioH = int(self.GL_height / size.height())
        ratioW = int(self.GL_width / size.width())
        instance = instance[::ratioH, ::ratioW, :]

        instance = np.flip(instance, 0)
        self.instance_map = instance

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def create_shader(self):
        # create a vertex and fragment shader
        # apparently verterx shaders only need
        # to return a gl_Position, an fragment
        # shaders only need to return a color
        vshader = '''#version 120
        varying vec3 ec_pos;

        void main(){
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            ec_pos = (gl_ModelViewMatrix * gl_Vertex).xyz;
        }
        '''
        fshader = '''#version 120
        varying vec3 ec_pos;
        void main(){

            vec3 light = vec3(0.5, 0.2, 1.0);
            light = normalize(light);

            vec4 color = vec4( 1,0,0,1 );
            vec3 ec_normal = normalize(cross(dFdx(ec_pos), dFdy(ec_pos)));

            float dProd = max(0.0,
                    dot(ec_normal, light));

            color = vec4(ec_normal, 1);
            //color = vec4(dProd, dProd, dProd, 1);
            gl_FragColor = color;
            
        }

        
        '''
        # compile our shaders
        VERTEX_SHADER = shaders.compileShader(vshader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(fshader, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        # create a vbo (stored actual data for our triangles)

        # for node in self.nodes:
        #     xyz = np.array(node.view.xyz)[:3]

        # vertices = np.array([[1.78149199, 0.32750149, 0.],
        #                      [1.32750149, 1.21850801, 0.],
        #                      [2.21850801, 1.67249851, 0.]],'f')
        # print(vertices.dtype)
        
        # # vertices = np.array([[1.78, 0.327, 0.],
        # #                      [1.32, 1.21, 0.],
        # #                      [2.21, 1.67, 0.]],'f')

        # # vertices = xyz

        vertices = np.concatenate([np.array(node.view.xyz, dtype=np.float32) for node in self.nodes])
        faces = np.concatenate([np.array(node.view.faces) for node in self.nodes])
        print(faces.shape)
        
        vertex_buffer = [[ [node.view.xyz[index] for index in face] for face in node.view.faces] for node in self.nodes]
        vertex_buffer = np.array(vertex_buffer, dtype=np.float32)
        print(vertex_buffer.shape)
        vertex_buffer = np.reshape(vertex_buffer,(vertex_buffer.shape[0]*vertex_buffer.shape[1]*vertex_buffer.shape[2],vertex_buffer.shape[3]))
        self.vertex_buffer = vertex_buffer

        print(np.array(vertex_buffer).shape)

        self.vbo = vbo.VBO(vertex_buffer)

    def draw_shader(self):
        '''render the geometry of the scene'''
        # tell opengl to use our shader
        shaders.glUseProgram(self.shader)
        try:
            # bind data into gpu
            self.vbo.bind()
            try:
                # tells opengl to access vertex once
                # we call a draw function
                glDisable(GL_POLYGON_SMOOTH)
                glEnableClientState(GL_VERTEX_ARRAY)
                
                # point at our vbo data
                glVertexPointerf(self.vbo)
                # actually tell opengl to draw
                # the stuff in the VBO as a series
                # of triangles
                glDrawArrays(GL_TRIANGLES, 0, self.vertex_buffer.shape[0])
            finally:
                # cleanup, unbind the our data from gpu ram
                # and tell opengl that it should not
                # expect vertex arrays anymore
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)
        finally:
            # stop using our shader
            shaders.glUseProgram(0)

# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    pass
