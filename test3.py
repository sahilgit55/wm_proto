z =  {'Set Top Left':"position_5:5", "Set Top Right": "position_main_w-overlay_w-5:5", "Set Bottom Left": "position_5:main_h-overlay_h", "Set Bottom Right": "position_main_w-overlay_w-5:main_h-overlay_h-5"}

s = {}

ss = list(z.keys())
for key in ss:
    value = z[key]
    s[value.replace('position_', '')] = key
    
{'5:5': 'Set Top Left', 'main_w-overlay_w-5:5': 'Set Top Right', '5:main_h-overlay_h': 'Set Bottom Left', 'main_w-overlay_w-5:main_h-overlay_h-5': 'Set Bottom Right'}
print(s)