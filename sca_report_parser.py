#!/usr/bin/python3

import csv, optparse, json

def capitalize(input: str):
    if not input:
        return input
    return input[0].upper() + input[1:]

def generate_HTML(csv_filename: str, html_filename: str):

    csv_data = []

    with open(csv_filename, "r") as csv_file:
        csv_data_dict = csv.DictReader(csv_file)
        for row in csv_data_dict:
            csv_data.append(row)

    html = """<html>
    <head>
        <title>SCA Result</title>
        <style>
            .failed {
                color: rgb(255,0,0);
            }

            .passed {
                color: rgb(46,139,87);
            }

            .link {
                color: rgb(65, 105, 225);
            }

            body {
            }
                padding: 10pt;

            td {
                padding: 0pt 5pt 0pt 0pt;
            }
            
            h1, h3 {
                color: rgb(53,133,248);
            }

            h1 {
                padding-top: 10pt;
                padding-bottom: 10pt;
            }
        </style>
    </head>
    <body>
    <div>
        <table width='100%'>
            <tr>
                <td align='left'>
                    <h1>Security Configuration Assessment Report</h1>
                </td>
                <td width='20%' align='right'>
                    <img src="data:image/png;base64,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" width='128pt'/>
                </td>
            </tr>
        </table>
    </div>"""
    counter = 1
    passed = 0
    failed = 0
    na = 0
    total = 0
    #dict_keys(['condition', 'Rationale', 'Title', 'ID', 'Remediation', 'Result', 'Policy ID', 'Description', 'command', 'References', 'Compliance', 'Rules'])
    for check in csv_data:
        html += f"<h3>{counter}. {check['Title']}</h3>"
        html += f"<span class={check['Result']}><b>{capitalize(check['Result'])}</b></span>"
        if check['Result'] == 'passed':
            passed += 1
        elif check['Result'] == 'failed':
            failed += 1
        else:
            na += 1
        html += f"<p><table width='50%'><tr><td><b>ID:</b></td><td>{check['ID']}</td><td><b>Policy:</b></td><td>{check['Policy ID']}</td></tr></table></p>"
        html += f"<p align='justify'><b>Description:</b> {check['Description']}</p>"
        html += f"<p align='justify'><b>Rationale:</b> {check['Rationale']}</p>"
        html += f"<p align='justify'><b>Remediation:</b> {check['Remediation']}</p>"
        html += f"<p align='justify'><b>Command:</b> {check['command']}</p>"
        compliances = json.loads(check['Compliance'])
        html += f"<p align='justify'><b>Compliance:</b><ul>"
        for compliance in compliances:
            html += f"<li>{compliance['key'].upper().replace("_", " ")} - {compliance['value']}</li>"
        html += "</ul></p>"
        rules = json.loads(check['Rules'])
        html += f"<p align='justify'><b>Rules:</b><ul>"
        for rule in rules:
            html += f"<li>{rule['type']}: {rule['rule']}</li>"
        html += "</ul></p>"
        html += f"<p align='justify'><b>Condition:</b> {capitalize(check['condition'])}</p>"
        references = check['References'].split(",")
        if references[0] != "-":
            html += f"<p align='justify'><b>References:</b><ul>"
            for reference in references:
                html += f"<li><a href={reference} target='_blank' class='link'>{reference}</a></li>"
            html += "</ul></p><br />"
        counter += 1
    total = passed + failed + na
    html += "<h3>Summary:</h3>"
    html += f"<table><tr><td><b>Passed:</b></td><td class='passed' align='right'>{passed}</td></tr><tr><td><b>Failed:</b></td><td class='failed' align='right'>{failed}</td></tr><tr><td><b>Not Applicable:</b></td><td align='right'>{na}</td></tr><tr><td><b>Total:<b></td><td align='right'><b>{total}</b></td></tr></table>"
    html += "</body></html>"

    with open(html_filename, "w") as output_html:
        output_html.write(html)
    


def main():
    parser = optparse.OptionParser("Script to convert Wazuh CSV to HTML report for SCA.")
    parser.add_option("-i", dest="input_file", default="checks.csv", help="CSV Input File")
    parser.add_option("-o", dest="output_file", default="output.html", help="HTML Output File")
    (options, args) = parser.parse_args()

    generate_HTML(options.input_file, options.output_file)

if __name__ == "__main__":
    main()