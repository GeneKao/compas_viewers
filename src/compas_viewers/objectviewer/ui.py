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
    'sidebar': []
}
