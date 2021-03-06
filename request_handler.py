
from posts import create_post, delete_post
from http.server import BaseHTTPRequestHandler, HTTPServer
from comments import create_comment, delete_comment, update_comment, get_all_comments
from users import create_user, login_user
import json
from categories import create_category, get_all_categories, get_single_category, delete_category, update_category
from posts import get_all_posts
from posts import get_posts_by_user
from posts import get_single_post
from posts import create_post
from posts import update_post
from comments import get_comments_by_post
import json


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

            if resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            if resource == "comments":
                if id is not None:
                    response = f"{get_all_comments()}"
                else:
                    response = f"{get_all_comments()}"

                  
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "user_id" and resource == "posts":
                response = f"{get_posts_by_user(value)}"

            if key == "post_id" and resource == "comments":
                response = f"{get_comments_by_post(int(value))}"

        self.wfile.write(response.encode())


    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new = None

        if resource == "register":
            new = create_user(post_body)
        elif resource == "categories":
            new = create_category(post_body)
        elif resource == "posts":
            new = create_post(post_body)
        elif resource == "comments":
            new = create_comment(post_body)

        elif resource == "login":
            new = login_user(post_body)

        self.wfile.write(f"{new}".encode())


    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "posts":
            success = update_post(id, post_body)
        elif resource == "comments":
            success = update_comment(id, post_body)

        if resource == "categories":
            success = update_category(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())
        


    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "comments":
            delete_comment(id)
        elif resource == "posts":
            delete_post(id)
            
        elif resource == "categories":
            delete_category(id)

        self.wfile.write("".encode())


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
