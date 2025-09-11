from enum import Enum


class AdminCB(str, Enum):
    BACK_MAIN = 'back_main'
    ADD_WL = 'admin_add_wl'
    DEL_WL = 'admin_delete_wl'
    DEL_USER_WL = 'admin_delete_user_wl'