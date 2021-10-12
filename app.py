from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/createuser')
def createuser():
    return render_template('createuser.html')


@app.route('/createproduct')
def createproduct():
    return render_template('createproduct.html')


@app.route('/createprovider')
def createprovider():
    return render_template('createprovider.html')

#dsdsd
if __name__ == '__main__':
    app.run()
