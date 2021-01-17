import os

def replace_username(username:str) -> str:
    if username.strip().upper().count('AKIZMINET'):
        return 'akizminet (phake)'
    elif username == os.environ.get('akizminet'):
        return 'akizminet'
    elif username.strip().upper() == 'Nhung':
        return 'Nhung (phake)'
    elif username == os.environ.get('nhung'):
        return 'Nhung'
    else:
        return username
