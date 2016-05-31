from re import search

def valid_user(username, password, repeat_password, users):
    usernames = []
    for user in users:
        usernames.append(user[0])
    if username in usernames:
        return [False, "Username is already taken."]
    #if password != repeat_password:
    #    return [False, "Passwords do not match."]
    #if len(password) < 8:
    #    return [False, "Your password must be at least 8 characters."]
    #if not (bool(search(r'\d', password)) and bool(search('[a-z]', password)) and bool(search('[A-Z]', password)) and bool(search(r'[!@#$%^*]', password))):
    #    return [False, "Your password must include a lowercase letter, an uppercase letter, a number, and at least of one the following symbols: '!@#$%^*'."]
    return [True, "Your information has been validated."]
