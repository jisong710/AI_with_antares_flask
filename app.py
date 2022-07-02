from flask import Flask, render_template, request
from module.database import Database
from module.algoritma_pso import algoritma_pso
from module.algoritma_genetika import algoritma_genetik

genetik = algoritma_genetik()
app = Flask(__name__)
pso = algoritma_pso()
db = Database()
@app.route('/login',methods = ['POST', 'GET'])
def login():
    style = "style.css"
    return render_template('login.html',style = style)

@app.route('/register',methods = ['POST', 'GET'])
def register():
    style = "style.css"
    if(request.method == 'POST'):
        print(request.form)
        datalogin = db.register(request.form);
        if(datalogin != "kosong"):
            return render_template('login.html',username = datalogin)
        else:
            message = "error saat login"
            return render_template('register.html',style = style)
    else:
        return render_template('register.html',style = style)



@app.route('/',methods = ['POST', 'GET'])
def index():
    style = "style.css"
    if(request.method == 'POST'):
        print(request.form)
        datalogin = db.login(request.form);
        if(datalogin != "kosong"):
            return render_template('index.html',username = datalogin)
        else:
            message = "error saat login"
            return render_template('login.html',style = style)
    else:
        datalogin = db.login(request.form);
        return render_template('index.html',style = style, username = datalogin)

@app.route('/akun/',methods = ['POST', 'GET'])
def akun():
    user = db.cekakun(request.args.get('id'))
    style = "style.css"
    return render_template('akun.html',style = style,user = user)

@app.route('/device/',methods = ['POST', 'GET'])
def device():
    if(request.method == "POST"):
        db.insertdevice(request.form)
        username = db.cekakun(0)
        return render_template('index.html',username = username)
    data1 = db.readgedung(None)
    data2 =db.readdevice(None)
    style = "style.css"
    return render_template('device.html',style = style, data2 = data2, data1 = data1)


@app.route('/gedung/',methods = ['POST', 'GET'])
def gedung():
    if(request.method == "POST"):
        db.insertGedung(request.form)
        username = db.cekakun(0)
        return render_template('index.html',username = username)
    style = "style.css"
    data1 = db.readgedung(None)
    return render_template('gedung.html',style = style, data1 = data1)

@app.route('/waktu/',methods = ['POST', 'GET'])
def waktu():
    if(request.method == "POST"):
        db.masukWaktu(request.form)
        username = db.cekakun(0)
        return render_template('index.html',username = username)
    data2 =db.readdevice(None)
    style = "style.css"
    return render_template('waktu.html',style=style, data2 = data2)

@app.route('/olah/',methods = ['POST', 'GET'])
def olah():
    if(request.method == "POST"):
        if(request.form['algoritma'] == "pso"):
            db.pso(request.form)
        elif(request.form['algoritma'] == "genetic"):
            db.genetik(request.form)
    data1 =db.readgedung(None)
    data2 =db.readdevice(None)
    style = "style.css"
    return render_template('machinelearn.html',style=style, data2 = data2, data1 = data1)
@app.route('/machinelearn/',methods = ['POST', 'GET'])
def ML():
    if(request.method == "POST"):
        if(request.form['algoritma'] == "pso"):
            data2,biaya,nama_device = pso.algoritma(request.form)
        elif(request.form['algoritma'] == "genetic"):
            data2,biaya,nama_device = genetik.algoritma(request.form)
    data1 =db.readgedung(None)
    style = "style.css"
    datalogin = db.login(request.form);
    return render_template('hasil.html',len= len(data2), data2 = data2, biaya= biaya, nama_device = nama_device, data1 = data1)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 