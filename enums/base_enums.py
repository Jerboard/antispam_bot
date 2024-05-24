from enum import Enum


class ListEx(str, Enum):
    WL_USERS = 'wl_users'
    WL_PHRASE = 'wl_phrase'
    WL_URL = 'wl_url'
    BL_PHRASE = 'bl_phrase'


lists_ex = {
    ListEx.WL_USERS.value: 'wl_users.json',
    ListEx.WL_URL.value: 'wl_url.json',
    ListEx.WL_PHRASE.value: 'wl_phrase.json',
    ListEx.BL_PHRASE.value: 'bl_phrase.json'
}