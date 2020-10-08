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

    def __init__(self, controller, activate_selection=False):
        super(View, self).__init__()
        self.controller = controller
        self.n = 0
        self.v = 0
        self.e = 0
        self.f = 0
        self.activate_selection = activate_selection

        self.selecting = False
        self.deselecting = False
        self.selected = set()
        self.use_shaders = True

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

            if self.activate_selection:
                # perform object selection through instance color
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
        if self.activate_selection:
            if key == SHIFT:
                self.selecting = True
                print('start selecting')
            elif key == CTRL:
                self.deselecting = True
                print('start deselecting')

    def keyReleaseAction(self, key):
        if self.activate_selection:
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

        if self.activate_selection:
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

            # print(node.settings)
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
                vertices_color = node.settings.get("vertices.color", "#000000")
                vertices_color = flist(hex_to_rgb(vertices_color) for key in node.view.vertices)
            
            
            edges_color = node.settings.get("edges.color", "#000000")
            face_color = node.settings.get("color", "#cccccc")

            edges_color = flist(hex_to_rgb(edges_color) for key in edges)
            faces_color = flist(hex_to_rgb(face_color) for key in node.view.xyz)
            faces_color_back = flist(hex_to_rgb(face_color) for key in node.view.xyz)

            vertices_selected_color = flist(hex_to_rgb('#999900') for key in node.view.vertices)
            edges_selected_color = flist(hex_to_rgb('#ffff00') for key in edges)
            faces_selected_color = flist(hex_to_rgb('#ffff00') for key in node.view.xyz)
            faces_selected_color_back = flist(hex_to_rgb('#ffff00') for key in node.view.xyz)

            if self.activate_selection:
                is_selected = node.widget.isSelected
            else:
                is_selected = lambda: False

            buffer = {
                'isSelected': is_selected,
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
                'instance.color': self.make_vertex_buffer(instance_color),
                'edges.width': node.settings.get("edges.width", self.settings['edges.width:value']),
                'vertices.size': node.settings.get("vertices.size", self.settings['vertices.size:value']),

                'vertices.on': node.settings.get("vertices.on", self.settings['vertices.on']),
                'edges.on': node.settings.get("edges.on", self.settings['edges.on']),
                'faces.on': node.settings.get("faces.on", self.settings['faces.on']),

                'n': len(xyz),
                'v': len(vertices),
                'e': len(edges),
                'f': len(faces)
                }

            if not self.use_shaders:
                buffer.update({
                    'faces.color': self.make_vertex_buffer(faces_color, dynamic=True),
                    'faces.color:back': self.make_vertex_buffer(faces_color_back, dynamic=True),
                    'faces.selected.color': self.make_vertex_buffer(faces_selected_color, dynamic=True),
                    'faces.selected.color:back': self.make_vertex_buffer(faces_selected_color_back, dynamic=True),
                })

            self.buffers.append(buffer)

        if self.use_shaders:
            self.create_shader()

    def draw_buffers(self):
        if not self.buffers:
            return

        for buffer in self.buffers:
            glDisable(GL_POLYGON_SMOOTH)
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, buffer['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            selected = buffer['isSelected']()

            if buffer['faces.on'] and not self.use_shaders:
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

            if buffer['edges.on']:
                glDisable(GL_LINE_SMOOTH)
                glLineWidth(buffer['edges.width'])
                if selected:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['edges.selected.color'])
                else:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['edges.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['edges'])
                glDrawElements(GL_LINES, buffer['e'], GL_UNSIGNED_INT, None)

            if buffer['vertices.on']:
                glPointSize(buffer['vertices.size'])
                if selected:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['vertices.selected.color'])
                else:
                    glBindBuffer(GL_ARRAY_BUFFER, buffer['vertices.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['vertices'])
                glDrawElements(GL_POINTS, buffer['v'], GL_UNSIGNED_INT, None)

            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

        if self.use_shaders:
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
        uniform vec3 face_color;
        uniform float opacity;

        void main(){

            vec3 light = vec3(0.5, 0.2, 1.0);
            light = normalize(light);

            vec3 ec_normal = normalize(cross(dFdx(ec_pos), dFdy(ec_pos)));

            float dProd = max(0.0,
                    dot(ec_normal, light));

            gl_FragColor = vec4(face_color * dProd, opacity);
            
        }

        
        '''
        # compile our shaders
        VERTEX_SHADER = shaders.compileShader(vshader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(fshader, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        for node in self.nodes:

            node.shader_uniforms = {
                'face_color': glGetUniformLocation( self.shader, 'face_color' ),
                'opacity': glGetUniformLocation( self.shader, 'opacity' ),
            }

            vertex_buffer = [ [node.view.xyz[index] for index in face] for face in node.view.faces]
            vertex_buffer = np.array(vertex_buffer, dtype=np.float32)
            if len(vertex_buffer.shape) == 3:
                vertex_buffer = np.reshape(vertex_buffer,(vertex_buffer.shape[0]*vertex_buffer.shape[1],vertex_buffer.shape[2]))
                vertex_buffer = np.concatenate((vertex_buffer,vertex_buffer[::-1]))
                node.vertex_buffer = vertex_buffer
                node.vbo = vbo.VBO(vertex_buffer)

    def draw_shader(self):

        if not self.settings['faces.on']:
            return
        
        for node in self.nodes:
            if not hasattr(node,'vbo'):
                continue

            if not node.settings.get("faces.on", self.settings['faces.on']):
                continue

            shaders.glUseProgram(self.shader)
            try:
                # bind data into gpu
                node.vbo.bind()
                try:
                    # tells opengl to access vertex once
                    # we call a draw function
                    glDisable(GL_POLYGON_SMOOTH)
                    glEnableClientState(GL_VERTEX_ARRAY)
                    
                    # point at our vbo data
                    glVertexPointerf(node.vbo)
                    # actually tell opengl to draw
                    # the stuff in the VBO as a series
                    # of triangles
                    if self.activate_selection and node.widget.isSelected():
                        glUniform3f( node.shader_uniforms['face_color'],1,1,0)
                    else:
                        rgb = hex_to_rgb(node.settings.get("color", "#ffffff"))
                        glUniform3f( node.shader_uniforms['face_color'], *rgb)

                    glUniform1f( node.shader_uniforms['opacity'], node.settings.get("opacity", 1))
    
                    glDrawArrays(GL_TRIANGLES, 0, node.vertex_buffer.shape[0])
                finally:
                    # cleanup, unbind the our data from gpu ram
                    # and tell opengl that it should not
                    # expect vertex arrays anymore
                    node.vbo.unbind()
                    glDisableClientState(GL_VERTEX_ARRAY)
            finally:
                # stop using our shader
                shaders.glUseProgram(0)

# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    pass
