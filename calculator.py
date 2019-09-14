#!/usr/bin/env python

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback

def intro(*args):
    """Introduces the calculator to the user"""
    page = """
        <html>
        <h1>WSGI Calculator</h1>
        <body>
            This page provides the user with the ability to add, subtract,
            multiply, and divide two numbers.

        <h2>Instructions</h2>
        In the url, please enter the arithmetic operation you would like to perform
        followed by the two values involved in the operation. The available
        arithmetic operations are as follows:<br></br>
        add<br></br>
        subtract<br></br>
        multiply<br></br>
        divide
        <h3>Example</h3>
        Url Entry:  /add/3/4/<br></br>
        Result: 3 + 4 = 7
        </body>
        </html>
    """
    return page

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum_num = 0
    operands = []
    try:
        for i in range(0, len(args)):
            sum_num = sum_num + int(args[i])
            operands.append(f'{args[i]}')

        operand_string = ' + '.join(operands)
        return f'{operand_string} = {sum_num}'
    except IndexError:
        raise IndexError

def subtract(*args):
    """Returns a STRING with the difference of the arguments."""
    difference = int(args[0])
    operands = [f'{args[0]}']
    try:
        for i in range(1, len(args)):
            difference = difference - int(args[i])
            operands.append(f'{args[i]}')

        operand_string = ' - '.join(operands)
        return f'{operand_string} = {difference}'
    except IndexError:
        return IndexError

def multiply(*args):
    """Returns a STRING with the product of the agruments."""
    product = int(args[0])
    operands = [f'{args[0]}']
    try:
        for i in range(1, len(args)):
            product = product * int(args[i])
            operands.append(f'{args[i]}')

        operand_string = ' * '.join(operands)
        return f'{operand_string} = {product}'
    except IndexError:
        raise IndexError

def divide(*args):
    """Returns a STRING with the quotient of the arguments."""
    quotient = int(args[0])
    operands = [f'{args[0]}']
    try:
        for i in range(1, len(args)):
            try:
                quotient = quotient / int(args[i])
                operands.append(f'{args[i]}')
            except ZeroDivisionError:
                raise ZeroDivisionError

        operand_string = ' / '.join(operands)
        return f'{operand_string} = {quotient}'
    except IndexError:
        raise IndexError

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    path = path.strip('/').split('/')
    funcs = {'': intro,
             'add': add,
             'subtract': subtract,
             'multiply': multiply,
             'divide': divide
             }

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
      raise NameError

    return func, args

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Invalid Result. A number can't be divided by zero.</h1>"
    except IndexError:
        status = "400 Bad Request"
        body = "<h1>Insufficient Operands"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(("Content-length", str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
