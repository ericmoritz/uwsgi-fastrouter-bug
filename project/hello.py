import time

def hello(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plan")])
    time.sleep(0.5)
    return ["Hello, World"]
                  

application = hello
