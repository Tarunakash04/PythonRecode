from flask import Flask, request, send_file, render_template_string
import pandas as pd
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def convert_to_json(filepath):
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
        df = pd.read_excel(filepath)
    else:
        return None

    json_filepath = os.path.splitext(filepath)[0] + '.json'
    df.to_json(json_filepath, orient='records', lines=True)
    return json_filepath

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            json_filepath = convert_to_json(filepath)

            if json_filepath:
                return send_file(json_filepath, as_attachment=True)
            else:
                return 'Error: Unsupported file type. Please upload a CSV or Excel file.', 400
        else:
            return 'Error: Please upload a valid CSV or Excel file.', 400
    
    return render_template_string('''
        <!doctype html>
        <title>Upload CSV or Excel to Convert to JSON</title>
        <h1>Upload a CSV or Excel file to convert it to JSON</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv, .xlsx, .xls" required>
            <button type="submit">Upload</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
