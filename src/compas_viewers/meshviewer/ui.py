UI = {
    'menubar': [
        {
            'type': 'menu',
            'text': 'View',
            'items': [
                {
                    'type': 'menu',
                    'text': 'Set View',
                    'items': [
                        {
                            'type': 'radio',
                            'items': [
                                {
                                    'text': 'Perspective',
                                    'action': 'set_view',
                                    'args': [1],
                                    'checked': True
                                },
                                {
                                    'text': 'Front',
                                    'action': 'set_view',
                                    'args': [2],
                                    'checked': False
                                },
                                {
                                    'text': 'Left',
                                    'action': 'set_view',
                                    'args': [3],
                                    'checked': False
                                },
                                {
                                    'text': 'Top',
                                    'action': 'set_view',
                                    'args': [4],
                                    'checked': False
                                },
                            ]
                        }
                    ]
                },
                {'type': 'separator'},
                {'text': 'Camera', 'action': 'update_camera_settings'},
                {'type': 'separator'},
                {'text': 'Capture Image', 'action': 'capture_image'},
                {'text': 'Capture Video', 'action': 'capture_video'},
                {'type': 'separator'}
            ]
        },
        {
            'type': 'menu',
            'text': 'Mesh',
            'items': [
                {'text': 'From OBJ', 'action': 'from_obj'},
                {'text': 'From JSON', 'action': 'from_json'},
                {'text': 'From STL', 'action': 'from_stl'},
                {'text': 'From PLY', 'action': 'from_ply'},
                {'type': 'separator'},
                {'text': 'To OBJ', 'action': 'to_obj'},
                {'text': 'To JSON', 'action': 'to_json'},
                {'text': 'To STL', 'action': 'to_stl'},
                {'text': 'To PLY', 'action': 'to_ply'},
                {'type': 'separator'},
                {
                    'type': 'menu',
                    'text': 'Polyhedrons',
                    'items': [
                        {'text': 'Tetrahedron', 'action': 'from_polyhedron', 'args': [4]},
                        {'text': 'Hexahedron', 'action': 'from_polyhedron', 'args': [6]},
                        {'text': 'Octahedron', 'action': 'from_polyhedron', 'args': [8]},
                        {'text': 'Dodecahedron', 'action': 'from_polyhedron', 'args': [12]},
                    ]
                },
                {'type': 'separator'},
            ]
        },
        {
            'type': 'menu',
            'text': 'Tools',
            'items': [
                {'text': 'Flip Normals', 'action': 'flip_normals'},
                {'type': 'separator'},
                {
                    'type': 'menu',
                    'text': 'Subdivision',
                    'items': [
                        {'text': 'Catmull-Clark', 'action': 'subdivide', 'args': ['catmullclark', 1]}
                    ]
                }
            ]
        },
        {
            'type': 'menu',
            'text': 'OpenGL',
            'items': [
                {'text': 'Version Info', 'action': 'opengl_version_info'},
                {'type': 'separator'},
                {
                    'type': 'radio',
                    'items': [
                        {
                            'text': 'Version 2.1',
                            'action': 'opengl_set_version',
                            'args': [(2, 1)],
                            'checked': True
                        },
                        {
                            'text': 'Version 3.3',
                            'action': 'opengl_set_version',
                            'args': [(3, 3)],
                            'checked': False
                        },
                        {
                            'text': 'Version 4.1',
                            'action': 'opengl_set_version',
                            'args': [(4, 1)],
                            'checked': False
                        }
                    ]
                },
            ]
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
                {'type': 'checkbox', 'text': 'normals', 'action': 'toggle_normals', 'state': False, },
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
                # {
                #     'type'  : 'colorbutton',
                #     'text'  : 'color faces (front)',
                #     'value' : Controller.settings['faces.color:front'],
                #     'action': 'change_faces_color_front',
                #     'size'  : (16, 16),
                # },
                # {
                #     'type'  : 'colorbutton',
                #     'text'  : 'color faces (back)',
                #     'value' : Controller.settings['faces.color:back'],
                #     'action': 'change_faces_color_back',
                #     'size'  : (16, 16),
                # },
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
