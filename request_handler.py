from urllib.parse import urlparse, parse_qs
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_species, get_single_species, get_all_snakes, get_snakes_by_species_id, get_single_snake, create_snake, get_all_owners, get_single_owner


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'snakes', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk) 

    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        
        response = {}  # Default response
        # Parse the URL and capture the tuple that is returned in a variable
        parsed = self.parse_url(self.path)
    #If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "species":
                if id is not None:
                    response = get_single_species(id)
                else:
                    response = get_all_species()
            elif resource == "snakes":
                if id is not None:
                    response = get_single_snake(id)
                else:
                    response = get_all_snakes()
            elif resource == "owners":
                if id is not None:
                    response = get_single_owner(id)
                else:
                    response = get_all_owners()
            else:
                response = {}
        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed
            # see if the query dictionary has a species key
            if query.get('species') and resource == 'snakes':
                response = get_snakes_by_species_id(query['species'][0])
        
        # Send a JSON formatted string as a response
        if not response:
            self._set_headers(404)
        elif isinstance(response, dict) and response.get('msg'):
            self._set_headers(405)
        else:
            self._set_headers(200)
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        if content_len == 0:
            self._set_headers(404)
            response = {
                "message": "No content sent"
            }
            self.wfile.write(json.dumps(response).encode())
            return
        post_body = self.rfile.read(content_len)
        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)
        parsed = self.parse_url(self.path)
        (resource, id) = parsed

        # Initialize new snake
        new_snake = None
        if resource == "snakes":
            # if all keys are in post-body:
            keys = ['name', 'owner_id', 'species_id', 'gender', 'color']
            if has_all_keys(post_body, keys):
                self._set_headers(201)
                new_snake = create_snake(post_body)
            else:
                self._set_headers(400)
                # create a dictionary with one key called message and store it in new_animal using a Python version of a ternary statement

                # make a list of the keys in post_body using the built-in keys() function and convert it into python list using list(...). Call this post_body_keys
                post_body_keys = list(post_body.keys())
                print(post_body_keys)
                # use a list comprehension to find those keys in "keys" that are not present in post_body_keys
                missing_keys = [
                    key for key in keys if key not in post_body_keys]
                msg = ", ".join(missing_keys) + " missing. Please update."

                new_snake = {
                    "message": msg
                }
                self.wfile.write(json.dumps(new_snake).encode())
        else:
            new_snake = {}
            self._set_headers(404)

        # Encode the new animal and send in response
            self.wfile.write(json.dumps(new_snake).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handles PUT requests to the server"""
        self.do_PUT()

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


def has_all_keys(dict, key_list):
    '''Checks if the dictionary dict has all the keys in the list key_list. Returns false if any of the keys are not found, and true if all the keys are found'''
    for key in key_list:
        if key not in dict:
            return False
    return True

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
