from .settings import SETTINGS

UI = {
    'menubar': [
        {
            'type': 'menu',
            'text': 'View',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Mesh',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Tools',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'OpenGL',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Window',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Help',
            'items': []
        }
    ],
    'toolbar': [
        # {'text': 'Zoom Extents', 'action': 'zoom_extents', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-to-extents-50.png')},
        # {'text': 'Zoom In', 'action': 'zoom_in', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-in-50.png')},
        # {'text': 'Zoom Out', 'action': 'zoom_out', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-out-50.png')},
        {'text': 'View:Perspective', 'action': 'set_view', 'args': [1], 'image': None},
        {'text': 'View:Front', 'action': 'set_view', 'args': [2], 'image': None},
        {'text': 'View:Left', 'action': 'set_view', 'args': [3], 'image': None},
        {'text': 'View:Top', 'action': 'set_view', 'args': [4], 'image': None},
        {'text': 'View:Capture', 'action': 'capture_image', 'args': [], 'image': None},
    ],
    'sidebar': [
        {
            'type': 'group',
            'text': None,
            'items': [
                {
                    'type': 'textedit',
                    'text': None,
                    'value': None,
                    'edit': 'select_command'
                },
            ],
        },
        {
            'type': 'group',
            'text': None,
            'items': [
                {'type': 'checkbox', 'text': 'vertices', 'action': 'toggle_vertices', 'state': True, },
                {'type': 'checkbox', 'text': 'edges', 'action': 'toggle_edges', 'state': True, },
                {'type': 'checkbox', 'text': 'faces', 'action': 'toggle_faces', 'state': True, },
            ]
        },
        {
            'type': 'group',
            'text': None,
            'items': [
                {
                    'type': 'colorbutton',
                    'text': 'color vertices',
                    'value': '#222222',
                    'action': 'change_vertices_color',
                    'size': (16, 16),
                },
                {
                    'type': 'colorbutton',
                    'text': 'color edges',
                    'value': '#666666',
                    'action': 'change_edges_color',
                    'size': (16, 16),
                },
            ]
        },
        {
            'type': 'group',
            'text': None,
            'items': [
                {
                    'name': 'size_vertices',
                    'type': 'slider',
                    'text': 'size vertices',
                    'value': SETTINGS['camera.azimuth:value'],
                    'minval': SETTINGS['camera.azimuth:minval'],
                    'maxval': SETTINGS['camera.azimuth:maxval'],
                    'step': SETTINGS['camera.azimuth:step'],
                    'scale': SETTINGS['camera.azimuth:scale'],
                    'slide': 'slide_size_vertices',
                    'edit': 'edit_size_vertices',
                },
                {
                    'name': 'width_edges',
                    'type': 'slider',
                    'text': 'width edges',
                    'value': SETTINGS['edges.width:value'],
                    'minval': SETTINGS['edges.width:minval'],
                    'maxval': SETTINGS['edges.width:maxval'],
                    'step': SETTINGS['edges.width:step'],
                    'scale': SETTINGS['edges.width:scale'],
                    'slide': 'slide_width_edges',
                    'edit': 'edit_width_edges',
                },
            ]
        },
        {
            'type': 'group',
            'text': None,
            'items': [
                {
                    'name': 'azimuth',
                    'type': 'slider',
                    'text': 'azimuth',
                    'value': SETTINGS['camera.azimuth:value'],
                    'minval': SETTINGS['camera.azimuth:minval'],
                    'maxval': SETTINGS['camera.azimuth:maxval'],
                    'step': SETTINGS['camera.azimuth:step'],
                    'scale': SETTINGS['camera.azimuth:scale'],
                    'slide': 'slide_azimuth',
                    'edit': 'edit_azimuth'
                },
                {
                    'name': 'elevation',
                    'type': 'slider',
                    'text': 'elevation',
                    'value': SETTINGS['camera.elevation:value'],
                    'minval': SETTINGS['camera.elevation:minval'],
                    'maxval': SETTINGS['camera.elevation:maxval'],
                    'step': SETTINGS['camera.elevation:step'],
                    'scale': SETTINGS['camera.elevation:scale'],
                    'slide': 'slide_elevation',
                    'edit': 'edit_elevation'
                },
                {
                    'name': 'distance',
                    'type': 'slider',
                    'text': 'distance',
                    'value': SETTINGS['camera.distance:value'],
                    'minval': SETTINGS['camera.distance:minval'],
                    'maxval': SETTINGS['camera.distance:maxval'],
                    'step': SETTINGS['camera.distance:step'],
                    'scale': SETTINGS['camera.distance:scale'],
                    'slide': 'slide_distance',
                    'edit': 'edit_distance'
                },
                {
                    'name': 'fov',
                    'type': 'slider',
                    'text': 'fov',
                    'value': SETTINGS['camera.fov:value'],
                    'minval': SETTINGS['camera.fov:minval'],
                    'maxval': SETTINGS['camera.fov:maxval'],
                    'step': SETTINGS['camera.fov:step'],
                    'scale': SETTINGS['camera.fov:scale'],
                    'slide': 'slide_fov',
                    'edit': 'edit_fov'
                },
            ]
        },
        {
            'type': 'stretch',
        }
    ]
}
