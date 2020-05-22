import requests
import constants

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    def getToken():
        resp = s.get(constants.BASE_URL+"/admin/")
        return s.cookies['csrftoken'] #csrf token

    def login(token):
        login_data = {
            "username": constants.USERNAME,
            "password": constants.PASSWORD,
            "csrfmiddlewaretoken": token,
            "next": constants.BASE_URL+"/admin/"
        }

        resp = s.post(constants.BASE_URL+"/admin/login/",
            data=login_data, headers=dict(Referer=constants.BASE_URL))

    def get(url):
        resp = s.get(constants.BASE_URL+url)
        if resp.status_code != 200: print("Something Went Wrong")
        else: return resp.json()

    token = getToken()
    login(token)
    token = getToken()
    print(get('/api/_teams/?active=1&limit=10000&o=-elo_mean'))
    print(get('/api/teams/active/by/elo_mean'))


'''
FOR DOCUMENTATION PURPOSES (UNUSED)
def post(number, name, token):
    data = {
        "number": number,
        "name": name,
        "csrfmiddlewaretoken": token,
        "next": constants.BASE_URL+"/api/teams/"
    }

    resp = s.post(constants.BASE_URL+'/api/teams/',
        data=data, headers=dict(Referer=constants.BASE_URL))
    if resp.status_code != 201: print("Something Went Wrong")
    else: print("Successful POST")
'''
