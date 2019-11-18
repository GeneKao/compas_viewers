from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .view import View
from .controller import Controller

import os

here = os.path.abspath(os.path.dirname(__file__))

CONFIG = {
    'menubar': [
        {
            'type'  : 'menu',
            'text'  : 'View',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Mesh',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Tools',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'OpenGL',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Window',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Help',
            'items' : []
        }
    ],
    'toolbar': [
        {'text': 'Zoom Extents', 'action': 'zoom_extents', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-to-extents-50.png')},
        {'text': 'Zoom In', 'action': 'zoom_in', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-in-50.png')},
        {'text': 'Zoom Out', 'action': 'zoom_out', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-out-50.png')},
        {'text': 'View:Perspective', 'action': 'set_view', 'args' : [View.VIEW_PERSPECTIVE], 'image': None},
        {'text': 'View:Front', 'action': 'set_view', 'args' : [View.VIEW_FRONT], 'image': None},
        {'text': 'View:Left', 'action': 'set_view', 'args' : [View.VIEW_LEFT], 'image': None},
        {'text': 'View:Top', 'action': 'set_view', 'args' : [View.VIEW_TOP], 'image': None},
        {'text': 'View:Capture', 'action': 'capture_image', 'args' : [], 'image': None},
    ],
    'sidebar': [
        {
            'type' : 'group',
            'text' : None,
            'items': [
                {
                    'type'   : 'textedit',
                    'text'   : None,
                    'value'  : None,
                    'edit'   : 'select_command'
                },
            ],
        },
        {
            'type'  : 'group',
            'text'  : None,
            'items' : [
                {'type' : 'checkbox', 'text' : 'vertices', 'action' : 'toggle_vertices', 'state' : True, },
                {'type' : 'checkbox', 'text' : 'edges', 'action' : 'toggle_edges', 'state' : True, },
                {'type' : 'checkbox', 'text' : 'faces', 'action' : 'toggle_faces', 'state' : True, },
            ]
        },
        {
            'type' : 'group',
            'text' : None,
            'items': [
                {
                    'type'  : 'colorbutton',
                    'text'  : 'color vertices',
                    'value' : Controller.settings['vertices.color'],
                    'action': 'change_vertices_color',
                    'size'  : (16, 16),
                },
                {
                    'type'  : 'colorbutton',
                    'text'  : 'color edges',
                    'value' : Controller.settings['edges.color'],
                    'action': 'change_edges_color',
                    'size'  : (16, 16),
                },
            ]
        },
        {
            'type' : 'group',
            'text' : None,
            'items': [
                {
                    'name'   : 'size_vertices',
                    'type'   : 'slider',
                    'text'   : 'size vertices',
                    'value'  : Controller.settings['vertices.size:value'],
                    'minval' : Controller.settings['vertices.size:minval'],
                    'maxval' : Controller.settings['vertices.size:maxval'],
                    'step'   : Controller.settings['vertices.size:step'],
                    'scale'  : Controller.settings['vertices.size:scale'],
                    'slide'  : 'slide_size_vertices',
                    'edit'   : 'edit_size_vertices',
                },
                {
                    'name'   : 'width_edges',
                    'type'   : 'slider',
                    'text'   : 'width edges',
                    'value'  : Controller.settings['edges.width:value'],
                    'minval' : Controller.settings['edges.width:minval'],
                    'maxval' : Controller.settings['edges.width:maxval'],
                    'step'   : Controller.settings['edges.width:step'],
                    'scale'  : Controller.settings['edges.width:scale'],
                    'slide'  : 'slide_width_edges',
                    'edit'   : 'edit_width_edges',
                },
            ]
        },
        {
            'type' : 'group',
            'text' : None,
            'items': [
                {
                    'name'   : 'azimuth',
                    'type'   : 'slider',
                    'text'   : 'azimuth',
                    'value'  : Controller.settings['camera.azimuth:value'],
                    'minval' : Controller.settings['camera.azimuth:minval'],
                    'maxval' : Controller.settings['camera.azimuth:maxval'],
                    'step'   : Controller.settings['camera.azimuth:step'],
                    'scale'  : Controller.settings['camera.azimuth:scale'],
                    'slide'  : 'slide_azimuth',
                    'edit'   : 'edit_azimuth'
                },
                {
                    'name'   : 'elevation',
                    'type'   : 'slider',
                    'text'   : 'elevation',
                    'value'  : Controller.settings['camera.elevation:value'],
                    'minval' : Controller.settings['camera.elevation:minval'],
                    'maxval' : Controller.settings['camera.elevation:maxval'],
                    'step'   : Controller.settings['camera.elevation:step'],
                    'scale'  : Controller.settings['camera.elevation:scale'],
                    'slide'  : 'slide_elevation',
                    'edit'   : 'edit_elevation'
                },
                {
                    'name'   : 'distance',
                    'type'   : 'slider',
                    'text'   : 'distance',
                    'value'  : Controller.settings['camera.distance:value'],
                    'minval' : Controller.settings['camera.distance:minval'],
                    'maxval' : Controller.settings['camera.distance:maxval'],
                    'step'   : Controller.settings['camera.distance:step'],
                    'scale'  : Controller.settings['camera.distance:scale'],
                    'slide'  : 'slide_distance',
                    'edit'   : 'edit_distance'
                },
                {
                    'name'   : 'fov',
                    'type'   : 'slider',
                    'text'   : 'fov',
                    'value'  : Controller.settings['camera.fov:value'],
                    'value'  : Controller.settings['camera.fov:value'],
                    'minval' : Controller.settings['camera.fov:minval'],
                    'maxval' : Controller.settings['camera.fov:maxval'],
                    'step'   : Controller.settings['camera.fov:step'],
                    'scale'  : Controller.settings['camera.fov:scale'],
                    'slide'  : 'slide_fov',
                    'edit'   : 'edit_fov'
                },
            ]
        },
        {
            'type'   : 'stretch',
        }
    ]
}

STYLE = """
QMainWindow {}

QDockWidget#Sidebar {
}

QGroupBox, QSlider, QLabel, QDockWidget {
background-color: rgba(255, 255, 255, 0.0);
}

QGroupBox, QSlider, QLabel, QLineEdit, QColorButton {
margin: 0;
padding: 0;
border: 0;
}

QGroupBox {
    border-bottom: 1px solid white;
    padding-top: 12px;
    padding-bottom: 12px;
    padding-left: 12px;
    padding-right: 12px;
}

QSlider::groove:horizontal {
    border: 1px solid #999999;
    height: 2px;
    background-color: #999999;
}

QSlider::handle:horizontal {
    background-color: #333333;
    border: 1px solid #333333;
    width: 3px;
    margin: -4px 0;
}


"""

from .app import MultiMeshViewer


__all__ = ['MultiMeshViewer']

