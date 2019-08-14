from flask import Flask
import os

vlc = '/usr/bin/vlc'

main_page = """
<!DOCTYPE html>
<html>
<body>

<h2>Button</h2>
<form action="button">
    <button type="submit">Press Button!</button>
<form>
 
</body>
</html>
"""

app = Flask(__name__)

@app.route('/button')
def button():
    os.system(vlc)
    return main_page
    

@app.route('/')
def index():
    return main_page

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')