from flask import Flask, render_template, request, session, send_from_directory, g, flash
from generator import Generator
import subprocess
import tempfile
import os
import flat_api
import base64

gen = Generator()
app = Flask(__name__)
app.config['FILES_FOLDER'] = os.path.join(os.getcwd(), '.workspace')
app.config['BINS_FOLDER'] = os.path.join(os.getcwd(), 'bin')
app.config['BIN_ABC2MIDI'] = os.path.join(app.config['BINS_FOLDER'], 'abc2midi')
app.config['VOCABULARY'] = ['(3', '(4', '-', '/2', '/4', '2', '3', '3/2', '4', '6', '8', '=A', '=A,', '=B', '=B,', '=C', '=D', '=E', '=F', '=G', '=G,', '=a', '=b', '=c', "=c'", '=d', "=d'", '=e', "=e'", '=f', '=g', 'H', 'T', '[', ']', '^A', '^A,', '^C', '^D', '^F', '^G', '^G,', '^a', '^c', "^c'", '^d', '^f', '^g', 'z', '~']
app.config['MULS'] = ['/2', '/4', '2', '3', '3/2', '4', '6', '8']
app.config['SYMBOLS'] = ['~', 'T', 'H']

configuration = flat_api.Configuration()
configuration.access_token = '<<flat_access_token>>'
flat_api_client = flat_api.ApiClient(configuration)
if not os.path.exists(app.config['FILES_FOLDER']):
    os.makedirs(app.config['FILES_FOLDER'])
app.debug = False


# Decorator for post-request callback
def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response


# Translate to valid ABC code
def parseCode(code):
    return ''.join(code.split())


def writeABC(code, title, program):
    code = parseCode(code)
    # Temp ABC file
    tmpfileabc = tempfile.NamedTemporaryFile(dir=app.config['FILES_FOLDER'],
        suffix='.abc', delete=False)
    tmpfileabc.write(b'X:1\n')
    tmpfileabc.write(bytes('T:' + title + '\n', encoding='utf-8'))
    tmpfileabc.write(b'K:C\n')
    tmpfileabc.write(bytes('%%MIDI program ' + str(program) + '\n', encoding='utf-8'))
    tmpfileabc.write(bytes(code+'\n', encoding='utf-8'))
    tmpfileabc.close()
    return tmpfileabc.name

def createMidi(abcfile):
    subprocess.run([app.config['BIN_ABC2MIDI'], abcfile, '-o', abcfile+'.mid'])
    return abcfile+'.mid'


def createFiles(data, title, program):
    # Temp abc file
    tmpfileabc = writeABC(data, title, program)

    # Midi file
    midifile = createMidi(tmpfileabc)

    # Delete files after request
    @after_this_request
    def remove_files(response):
        os.remove(tmpfileabc)
        os.remove(midifile)
        return response

    return tmpfileabc, midifile

def uploadMidiToFlat(midifile, title):
    with open(midifile , 'rb') as f:
        data = f.read()

    data = base64.b64encode(data).decode('utf-8')

    new_score = flat_api.ScoreCreation(
        title=title,
        privacy='public',
        data=data,
        data_encoding='base64'
    )
    try:
        # Check limit account (max 15 scores)
        scores = flat_api.ScoreApi(flat_api_client).get_user_scores('me')
        if len(scores) == 15:
            deleteScore(scores[-1].id)

        score = flat_api.ScoreApi(flat_api_client).create_score(new_score)
        return score.id
    except flat_api.rest.ApiException as e:
        print(e)

def checkInputScore(score):
    for pal in score.split():
        if not (pal in app.config['VOCABULARY']):
            return False
    return True

def deleteScore(id):
    try:
        flat_api.ScoreApi(flat_api_client).delete_score(id)
    except flat_api.rest.ApiException as e:
        print(e)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/generar', methods=['POST','GET'])
def generar():
    # From form
    if(request.method == 'POST'):
        # Get data:
        # Actions
        new_session = len(request.form.getlist('new-session'))
        save_session = len(request.form.getlist('save-session'))
        download = len(request.form.getlist('download'))
        run = len(request.form.getlist('run'))

        # Values
        notes = request.form['scoreNotes']
        if not checkInputScore(notes):
            flash("Datos de composición inválidos")
            return render_template('generar.html')
        save_title = request.form['saveTitle']
        if save_title == '':
            save_title = 'AutoScore composition'
        run_title = request.form['runTitle']
        if run_title == '':
            run_title = 'AutoScore generation'
        if len(request.form.getlist('timesteps')):
            timesteps = int(request.form['timesteps'])
            # Check timesteps
            try:
                steps = int(timesteps)
                if steps < 0:
                    flash('Número de pasos inválido')
                    return render_template('generar.html')
            except Exception:
                flash('Número de pasos inválido')
                return render_template('generar.html')
        mode = len(request.form.getlist('mode')) > 0
        program = request.form['program']


        # Process data
        if new_session:
            # New session: delete cookies
            session['score'] = ''
            session['flat_id'] = ''
        elif save_session:
            # Save session
            session['score'] = notes
            _, midifile = createFiles(notes, save_title, program)
            if session.get('flat_id'):
                deleteScore(session['flat_id'])
            flat_id = uploadMidiToFlat(midifile, save_title)
            session['flat_id'] = flat_id
        elif download:
            # Download MIDI
            _, midifile = createFiles(notes, "AutoScore composition", program)
            (directory, file) = os.path.split(midifile)
            return send_from_directory(directory, file, as_attachment=True)
        elif run:
            # Generate data
            session['score'] = gen.predict(notes, get_best=(not mode), steps=steps)
            _, midifile = createFiles(session['score'], run_title, program)
            if session.get('flat_id'):
                deleteScore(session['flat_id'])
            flat_id = uploadMidiToFlat(midifile, run_title)
            session['flat_id'] = flat_id

    return render_template('generar.html')


@app.route('/explorar')
def explorar():
    try:
        scores = flat_api.ScoreApi(flat_api_client).get_user_scores('me')
    except flat_api.rest.ApiException:
        render_template('explorar.html', scores=[])
    return render_template('explorar.html', scores=scores)

if __name__ == '__main__':
    app.secret_key="<<flask_secret>>"
    app.run(host='0.0.0.0', port=5000, use_reloader=False, threaded=True)

