from http.server import BaseHTTPRequestHandler, HTTPServer
from users import create_user
import json
from posts import get_all_posts
from posts import get_posts_by_user
from posts import get_single_post


class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):

        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:

            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return (resource, key, value)

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"

        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "user_id" and resource == "posts":
                response = get_posts_by_user(value)

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new = None

        if resource == "register":
            new = create_user(post_body)

            self.wfile.write(f"{new}".encode())

    # def do_PUT(self):
    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)
    #     post_body = json.loads(post_body)

    #     # Parse the URL
    #     (resource, id) = self.parse_url(self.path)

    #     success = False

    #     if resource == "animals":
    #         success = update_animal(id, post_body)
    #     # rest of the elif's

    #     if success:
    #         self._set_headers(204)
    #     else:
    #         self._set_headers(404)

    #     self.wfile.write("".encode())

    # def do_DELETE(self):
    #     # Set a 204 response code
    #     self._set_headers(204)

    #     # Parse the URL
    #     (resource, id) = self.parse_url(self.path)

    #     # Delete a single animal from the list
    #     if resource == "animals":
    #         delete_animal(id)

    #     # Encode the new animal and send in response
    #     self.wfile.write("".encode())

    #     if resource == "customers":
    #         delete_customer(id)

    #     self.wfile.write("".encode())

    #     if resource == "employees":
    #         delete_employee(id)

    #     self.wfile.write("".encode())

    #     if resource == "locations":
    #         delete_location(id)

    #     self.wfile.write("".encode())

    #     # This function is not inside the class. It is the starting
    #     # point of this application.


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
