import requests
import json
import pandas as pd
import argparse


def retrieve_courses(token, run_slug):
    headers = {
        'ACTIVE-TOKEN': token,
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json, text/plain, */*'
    }
    endpoint = 'https://api.cognomos.com/runs/' + run_slug + '/courses/'
    finished = False
    courses = []
    while(finished is not True):
        r = requests.get(endpoint, headers=headers)
        payload = json.loads(r.content)
        if payload.get('results'):
            courses += payload.get('results')
        if payload.get('next'):
            endpoint = payload.get('next')
        else:
            finished = True
    return courses


parser = argparse.ArgumentParser()
parser.add_argument('token')
parser.add_argument('run_slug')
parser.add_argument('out_file')
args = parser.parse_args()
courses = retrieve_courses(args.token, args.run_slug)

courses_flattened = pd.json_normalize(courses)
courses_flattened.to_csv(args.out_file, index=False)
