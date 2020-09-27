#!/usr/bin/env python3

import argparse
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import jinja2
import json
import sys

def filePath(vulnerability):
    return vulnerability['location']['file']

def countSeverities(vulnerabilities):
    # Pre-define severities we expect so we don't have to sort later
    frequencies = {
        'Critical': 0,
        'High': 0,
        'Medium': 0,
        'Low': 0,
        'Unknown': 0
    }

    for vulnerability in vulnerabilities:
        if vulnerability['severity'] in frequencies:
            frequencies[vulnerability['severity']] += 1
        else: # If we don't have a category for a severity create it here
            frequencies[vulnerability['severity']] = 1

    return frequencies

parser = argparse.ArgumentParser(description='Parse a GitLab SAST report to HTML')
parser.add_argument('files', metavar='files', nargs='+',
                    help='The files that should be converted to HTML.')
parser.add_argument('--only-severities', type=str, required=False,
                    help='A comma delimited list of the vulnerabilities to keep (defaults to all)')
parser.add_argument('--jsonpath-filter', type=str, required=False,
                    help='Provide a custom jsonpath filter to apply to all JSON files')
args = parser.parse_args()

if args.jsonpath_filter is not None:
    try:
        jsonpath_expr = parse(args.jsonpath_filter)
    except:
        print('Invalid jsonpath filter provided')
        sys.exit(1)
# Build a filter based on severities
elif args.only_severities is not None:
    severities = args.only_severities.split(',')
    filters = list()
    for severity in severities:
        filters.append("$.vulnerabilities[?(@.severity == '" + severity + "')]")
    filter = ' | '.join(filters)
    jsonpath_expr = parse(filter)
else:
    jsonpath_expr = parse("$.vulnerabilities[*]")

vulnerabilities = list()

# Iterate over all the JSON files provided
for json_file in args.files:
    with open(json_file) as f:
        data = json.load(f)

        if float(data['version']) >= 4.0:
            print('We don\'t know how to parse this version of SAST report')
            sys.exit(1)

        vulns = jsonpath_expr.find(data)
        for vuln in vulns:
            vulnerabilities.append(vuln.value)

frequencies=countSeverities(vulnerabilities)

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
template = env.get_template('vulnerability_report.html')
rendered = template.render(vulnerabilities=vulnerabilities, frequencies=countSeverities(vulnerabilities))
print(rendered)