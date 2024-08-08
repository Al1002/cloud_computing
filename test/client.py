import requests
from time import sleep
from os.path import basename

class WebClient:
    def __init__(self, user_name: str, password: str, server_url: str):
        self.user_name = user_name
        self.password = password
        self.server_url = server_url
        self.auth_header = None
        try:
            requests.get(server_url, timeout=3)
        except:
            print("Server not found!")


    def sign_in(self):
        responce = requests.post(
            self.server_url + '/user',
            json =
            {
                'user_name': self.user_name,
                'password': self.password
            }
        )

        return responce


    def log_in(self):
        responce = requests.post(
            self.server_url + '/token',
            json = 
            {
                'user_name': self.user_name,
                'password': self.password
            }
        )

        if responce.status_code != 200:
            return responce

        token = responce.json()['access_token']
        self.auth_header = {"Authorization": f"Bearer {token}"}
        return responce


    def read(self):
        responce = requests.get(
            self.server_url + '/user',
            headers = self.auth_header
        )
        return responce


    def rename(self, new_name: str):
        if not self.auth_header:
            return
        
        responce = requests.put(
            self.server_url + '/user',
            json =
            {
                'user_name': new_name,
                'password': self.password
            },
            headers = self.auth_header
        )

        if self.log_in().status_code == 200:
            self.user_name = new_name

        return responce


    def change_password(self, new_password):
        if not self.auth_header:
            return
        
        responce = requests.put(
            self.server_url + '/user',
            json =
            {
                'user_name': self.user_name,
                'password': new_password
            },
            headers = self.auth_header
        )

        if self.log_in().status_code == 200:
            self.password = new_password

        return responce


    def delete(self):
        responce = requests.delete(
            self.server_url + '/user',
            headers = self.auth_header
        )

        return responce


    def create_project(self, project_name):
        if not self.auth_header:
            return

        responce = requests.post(
            self.server_url + f'/project/{project_name}',
            headers = self.auth_header
        )

        return responce


    def read_project(self, project_name):
        responce = requests.get(
            self.server_url + f'/project/{project_name}',
            headers = self.auth_header
        )
        return responce


    def delete_project(self, project_name):
        if not self.auth_header:
            return

        responce = requests.delete(
            self.server_url + f'/project/{project_name}',
            headers = self.auth_header
        )

        return responce


    def upload_file(self, project_name, file_path, is_entry):
        with open(file_path, 'rb+') as file:
            response = requests.put(
                self.server_url + f"/project/{project_name}/upload?is_entry={is_entry}",
                files = {"file_upload": (basename(file.name), file, "text/plain")},
                headers = self.auth_header
            )
        return response


    def run_project(self, project_name):
        response = requests.post(
            self.server_url + f'/run/{project_name}',
            headers = self.auth_header
        )
        if not response.status_code == 200:
            return response
        
        result_id = response.json()['id']
        response = requests.get(
                self.server_url + f'/result/{result_id}'
        )
        while(response.json()['status'] == 'running'):
            response = requests.get(
                self.server_url + f'/result/{result_id}'
            )
            sleep(1)
        return response