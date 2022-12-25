from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
# short import
for module in ['os', 'json', 'time', 'datetime', 'requests', 'pytz']:
    globals()[module] = __import__(module)

class SubmitForm(BaseModel):
    projectKey: str
    scanTime: str
    scanType: str

# app init
app = FastAPI(
    docs_url = '',
    openapi_url = ''
)

# get envs
SC_TOKEN = os.getenv('SC_TOKEN')
SC_ORG = os.getenv('SC_ORGANIZATION')

# root page
@app.get('/')
def root():
    return {'detail': 'Nothing Here'}

# define api root
api = APIRouter(prefix='/api/v1/sonarcloud')

@api.get('/')
def root_api():
    return {'detail': 'API for create storing and gathering data for Sonarcloud', 'author': 'phucdc'}

def to_seconds(scanTime: str):
    _time = scanTime.split(':')
    #just have seconds
    if len(_time) == 1:
        return float(_time[0])
    # m:s
    elif len(_time) == 2:
        return float(_time[0]) * 60 + float(_time[1])
    else:
        return float(_time[0]) * 3600 + float(_time[1]) * 60 + float(_time[2])

def getmeasures(projectKey: str, scanType: str):
    url = f'https://sonarcloud.io/api/measures/component?metricKeys=ncloc,vulnerabilities,bugs&componentKey={projectKey}'
    headers = {
        'Authorization': f'Bearer {SC_TOKEN}'
    }
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        return
    result = {
        'ncloc': 0,
        'bugs': 0,
        'vulnerabilities': 0
    }
    for measure in r.json()['component']['measures']:
        result[measure['metric']] = int(measure['value']) 
    if scanType == 'full':
        result['ncloc'] = 0
    return result

def get_full_info(projectKey: str):
    url = f'https://sonarcloud.io/api/issues/search?s=FILE_LINE&resolved=false&types=VULNERABILITY&ps=100&facets=severities%2CsonarsourceSecurity%2Ctypes&componentKeys={projectKey}&organization={SC_ORG}&additionalFields=_all'
    headers = {
        'Authorization': f'Bearer {SC_TOKEN}'
    }
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        return
    save_data(dict(r.json()), f'data/{projectKey}/vulnerabilities')
    
def save_data(data: dict, spath: str = ''):
    if not spath:
        spath = f"data/{data['projectKey']}"
    if not os.path.exists(spath):
        os.mkdir(spath)
        os.mkdir(f'{spath}/vulnerabilities')
    curtime = time.strftime("%Y%m%d-%H%M%S")
    fpath = f"{spath}/{curtime}.json"
    with open(fpath, 'w') as f:
        f.write(json.dumps(data, indent=4))

@api.post('/submit')
def submit(req: SubmitForm):
    time.sleep(60)
    measures = getmeasures(req.projectKey, req.scanType)
    if not measures:
        return {'status': 'error', 'message': 'There was an error, pls check your $SC_TOKEN or projectKey'}
    d = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    data = {'projectKey': req.projectKey, 'scanDate': d.isoformat('T'), 'scanTime': to_seconds(req.scanTime), **measures}
    save_data(data)
    get_full_info(req.projectKey)
    return {'status': 'success', 'data': data}

@api.get('/get-data')
def get_data(projectKey: str, dtype: str = 'measures'): # measures or full?
    if not dtype:
        spath = f"data/{projectKey}"
    else:
        spath = f"data/{projectKey}/vulnerability"
    if not os.path.exists(spath):
        return {'status': 'error', 'message': f'No data for {projectKey}'}
    alldata = []
    for file in os.listdir(spath):
        data = json.load(open(f'{spath}/{file}'))
        alldata.append(data)
    return alldata

app.include_router(api)
