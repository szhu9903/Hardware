

def format_menu(menus, up_menu):
    result = [menu for menu in menus if menu['sm_menuupid'] == up_menu and menu['id'] is not None]
    if not result: return []
    for menu in result:
        menu['sub'] = format_menu(menus, menu['id'])
    return result



