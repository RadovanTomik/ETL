import csv
import json
import os
from flask import Flask, flash, request, redirect, url_for, make_response, Response, render_template
from werkzeug.utils import secure_filename

import converter
from settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == "__main__":
    global file_name
    global frequency
    app.run(port=5000)


# Root URL
@app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template('upload.html')


@app.route("/mapping/<file_name>", methods=['GET'])
def mapping(file_name):
    # map the headers to FHIR attributes
    headers = []
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name)) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader)
    return render_template('show_file.html', headers=headers)


@app.route('/background_process_test/', methods=['GET', 'POST'])
def save_blueprint():
    num = len([name for name in os.listdir('/Users/radot/Projects/ETL/Blueprints') if os.path.isfile(name)])
    personId = request.form.get('comp_select')
    sampleId = request.form.get('comp_select2')
    mappings = {
        "personID": personId,
        "sampleID": sampleId
    }
    blueprint_name = "/Users/radot/Projects/ETL/Blueprints/b-" + str(num) + ".json"
    blueprint = open(blueprint_name, "w")
    json.dump(mappings, blueprint)
    blueprint.close()
    converter.createFhir(file_name, blueprint_name)

    return 'Thanks, upload is set'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
    # save the file
    global frequency
    if request.method == 'POST':
        frequency = request.form['time']
        print(frequency)
    global file_name
    file_name = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    return redirect(url_for('mapping', file_name=uploaded_file.filename))

# Upload file DONE
# Load all headers from the file DONE
# Display FHIR attributes(start with personId, sampleID) DONE
# Add dropdown menus containing headers DONE
# Save selection as a blueprint DONE
# Map attributes accoridng to the blueprint/create FHIR transaction DONE
