from os.path import exists as _exists
from glob import glob
import json

from flask import Flask, request, render_template, redirect

app = Flask(__name__)


def _startval(schema, id):
    fn = f'{schema}/{id}.json'
    if _exists(fn):
        with open(fn) as fp:
            startval = fp.read()
    else:
        startval = 'null'
    return startval


@app.route('/catalog/<schema>')
def catalog(schema):
    fns = glob(f'{schema}/*.json')
    ids = [fn.replace('.json', '') for fn in fns]
    return render_template('catalog.htm', schema=schema, ids=ids)


@app.route('/render/<schema>/<id>')
def render(schema, id):
    startval = _startval(schema, id)
    obj = json.loads(startval)

    return render_template(f'render/{schema}/index.htm', obj=obj)


@app.route('/editor/<schema>/<id>')
def editor(schema, id):
    startval = _startval(schema, id)

    with open(f'schemas/{schema}.json') as fp:
        schema_js = fp.read()

    return render_template('editor.htm',
                           schema=schema,  schema_js=schema_js,
                           id=id, startval=startval)


@app.route('/editor-submit/<schema>/<id>', methods=['POST'])
def editor_submit(schema, id):
    js = request.form.get('json')

    print(js)
    obj = json.loads(js)
    with open(f'{schema}/{id}.json', 'w') as fp:
        json.dump(obj, fp, indent=2)

    return redirect(f'/editor/{schema}/{id}')


if __name__ == '__main__':
    app.run()
