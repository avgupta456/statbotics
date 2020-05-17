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

    def get():
        resp = s.get(constants.BASE_URL+'/api/teams/')
        if resp.status_code != 200: print("Something Went Wrong")
        else: return resp.json()

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

    token = getToken()
    login(token)
    token = getToken()
    print(get())
    post(179, "Children of the Swamp", token)
    print(get())
