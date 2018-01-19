from flask import Flask
import requests
import json
import math
from flask import jsonify
import base64


app = Flask(__name__)
#user = base64.b64decode('c3VubnlrdW1hcnNAZ21haWwuY29t')
token = '54254cb1d9c5807684350a4411fa0f9b46326894'
headers = {'Authorization':'token' + token}
@app.route('/openissues/')
def open_issues():
  data = requests.get("https://api.github.com/orgs/att/repos", headers = headers)
  data = json.loads(data.content)
  repos = []
  open_issue_count = []
  
  for i in range(0, len(data)):
    repos.append(data[i]['name'])
    open_issue_count.append(data[i]['open_issues_count'])
  
  repo_issues = {}
  
  for i in range(0, len(repos)):
    issue_numbers = []
    loop = int(open_issue_count[i]/100)
    for j in range(1, loop + 2):
      issues = requests.get("https://api.github.com/repos/att/" + repos[i] + "/issues?state=open&page=" + str(j) + "&per_page=100", headers = headers)
      issues = json.loads(issues.content)
      for k in range(0, len(issues)):
        issue_numbers.append(str(issues[k]['number']) + ':' + issues[k]['title'])
    repo_issues[repos[i]]=issue_numbers
  
  new_list = []
    
  for key, value in repo_issues.iteritems():
    pobj = {}
    pobj['repo'] = key	
    open_issues = []
    for i in range(0, len(value)):
      obj = {}
      bdy = requests.get("https://api.github.com/repos/att/" + key + "/issues/" + str(value[i].split(':')[0]) + "/comments", headers = headers)
      bdy = json.loads(bdy.content)
      #obj['repo'] = key
      obj['number'] = str(value[i].split(':')[0])
      obj['title'] = str(value[i].split(':')[1])
      obj['comments'] = []
      for j in range(0, len(bdy)):
        try:
          if(bdy[j]):
            if(bdy[j]['body']):
              obj['comments'].append(bdy[j]['body'])
        except KeyError:
          continue
      open_issues.append(obj)
    pobj['open_issues'] = open_issues
    new_list.append(pobj)
  return jsonify(new_list)

if __name__ == '__main__':
  app.run()
