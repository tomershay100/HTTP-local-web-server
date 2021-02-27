# HTTP-local-web-server
1. [Introduction](#introduction)
2. [Dependencies](#dependencies)  
3. [Installation](#installation)


## Introduction
a python TCP web server that works with a browser as a client. After a client sends to the server a path of a file that he wants to download (in the format of an HTTP/1.1 message), the server will search and find the file and send it back to the client. The server supports a ```keep-alive``` connection but does not use concurrency - therefore, a maximum ```accpet()``` time of 1 sec is set.

Additionally,
* If it asks for the path `/` - the server will return the ```index.html``` file.
* If it asks for the path `/redirect` - the server will return 301 Moved Permanently error with the file path ```/result.html```.
* If it requests a path that does not exist - the server will return a ```404 Not Found``` error.

## Dependencies
* Windows / Linux / macOS with python
* Git
* Web browser (e.g. Chrome)

## Installation
1. Clone the repository:  
    ```
    $ git clone https://github.com/tomershay100/HTTP-local-web-server.git
    ```
2. Run the server using python3:
    ```
    $ python3 server.py 12345
    ```
    with "12345" as port number (you can choose a free port as you like).
3. Open the browser and type as URL the files from the "Files" folder that you want to download in the following format. for example:
    ```
    http://localhost:12345/a/b/ref.html
    ```
    or
    ```
    http://localhost:12345/
    ```
    or
    ```
    http://localhost:12345/redirect
    ```
    
