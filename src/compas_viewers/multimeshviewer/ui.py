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
                    'value': 1,
                    'minval': 1,
                    'maxval': 100,
                    'step': 1,
                    'scale': 0.1,
                    'slide': 'slide_size_vertices',
                    'edit': 'edit_size_vertices',
                },
                {
                    'name': 'width_edges',
                    'type': 'slider',
                    'text': 'width edges',
                    'value': 1,
                    'minval': 1,
                    'maxval': 100,
                    'step': 1,
                    'scale': 0.1,
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
                    'value': +30,
                    'minval': -180,
                    'maxval': +180,
                    'step': 1,
                    'scale': 1,
                    'slide': 'slide_azimuth',
                    'edit': 'edit_azimuth'
                },
                {
                    'name': 'elevation',
                    'type': 'slider',
                    'text': 'elevation',
                    'value': -10,
                    'minval': -180,
                    'maxval': +180,
                    'step': 1,
                    'scale': 1,
                    'slide': 'slide_elevation',
                    'edit': 'edit_elevation'
                },
                {
                    'name': 'distance',
                    'type': 'slider',
                    'text': 'distance',
                    'value': +10,
                    'minval': 0,
                    'maxval': +100,
                    'step': 1,
                    'scale': 1,
                    'slide': 'slide_distance',
                    'edit': 'edit_distance'
                },
                {
                    'name': 'fov',
                    'type': 'slider',
                    'text': 'fov',
                    'value': 50,
                    'minval': 10,
                    'maxval': 170,
                    'step': 1,
                    'scale': 1,
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
