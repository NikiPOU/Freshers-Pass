from db import execute_query

def get_fresher_id(username):
    sql = "SELECT id FROM fresher_profile WHERE username = %s"
    result = execute_query(sql, (username,))
    return result[0][0] if result else None