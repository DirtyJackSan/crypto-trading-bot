# 👑 Администраторы (полный доступ)
ADMINS = {
    8445673077  # <-- ЗАМЕНИ НА СВОЙ chat_id
}

# 👤 Пользователи (только чтение)
USERS = {
    6781280324  # chat_id брата
}

def is_admin(chat_id: int) -> bool:
    return chat_id in ADMINS

def is_user(chat_id: int) -> bool:
    return chat_id in USERS or chat_id in ADMINS

def all_users():
    return ADMINS.union(USERS)