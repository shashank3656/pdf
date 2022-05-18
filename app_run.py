#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import camelot
import os
from flask import Flask, flash, request, send_file
from werkzeug.utils import secure_filename

from flask import jsonify
from flask_cors import CORS


import camelot
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(["pdf"])
app = Flask(__name__)

CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if os.path.isdir('uploads'):
    pass
else:
    os.mkdir('uploads')


@app.route('/pdf', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return "fail"

        file = request.files['file']

        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        print(path)

        tables = camelot.read_pdf(path, flavor='lattice', pages='1-end')
        D= []
        for t in tables:
            D.append(t.df.to_dict("dict"))
        d1 = tables[0].parsing_report
        os.remove(path)
        return jsonify({"performance": d1, "table": D})

        # return "success"


if __name__ == '__main__':
    app.run()

