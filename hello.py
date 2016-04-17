from flask import Flask, url_for, render_template, request
from openpyxl import load_workbook
app = Flask(__name__)

@app.route("/")
def form():
    return render_template("form.html")

@app.route('/hello/', methods=['POST'])
def hello():
    mno=request.form['mno']
    akey=request.form['akey']
    uid=request.form['uid']
    
    wb = load_workbook('userdata.xlsx')
    sheet = wb.get_sheet_by_name('Sheet1')
    sheet.append([mno,akey,uid])
    wb.save('userdata.xlsx')    
    return render_template('result.html',mno=mno,akey=akey,uid=uid)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=80)