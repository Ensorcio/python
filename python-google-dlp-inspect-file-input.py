import os
import sys
# Import the client library
import google.cloud.dlp
# Import argument library
import argparse
#Import mimetypes to read files
import mimetypes
#Import json library
import json

# Edit this with your Google Cloud Project ID.
project = 'Project-ID'

# Instantiate a client.
dlp = google.cloud.dlp.DlpServiceClient()

# Specify CLI Arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Specify file to inspect with DLP API")
    parser.add_argument('-f', '--file', nargs='?', required=False, help='Absolute path to read the file.')
    args = parser.parse_args()
    return args

def main(custom_dictionaries=None, custom_regexes=None, mime_type=None):
    args = parse_arguments()

    # If mime_type is not specified, guess it from the filename.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(args.file)
        mime_type = mime_guess[0]
    # Select the content type index from the list of supported types.
    supported_content_types = {
        None: 0, # "Unspecified"
        'image/jpeg': 1,
        'image/bmp': 2,
        'image/png': 3,
        'image/svg': 4,
        'text/plain': 5,
    }
    content_type_index = supported_content_types.get(mime_type, 0)

    # The file to inspect
    with open(args.file, mode='rb') as f:
        item = {'byte_item': {'type': content_type_index, 'data': f.read()}}

    # The info types to search for in the content. Required.
    info_types = [{'name': 'FIRST_NAME'}, {'name': 'LAST_NAME'}, {'name': 'CREDIT_CARD_NUMBER'} ]

    # Prepare custom_info_types by parsing the dictionary word lists and
    # regex patterns.
    if custom_dictionaries is None:
        custom_dictionaries = []
    dictionaries = [{
        'info_type': {'name': 'CUSTOM_DICTIONARY_{}'.format(i)},
        'dictionary': {
            'word_list': {'words': custom_dict.split(',')}
        }
    } for i, custom_dict in enumerate(custom_dictionaries)]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [{
        'info_type': {'name': 'CUSTOM_REGEX_{}'.format(i)},
        'regex': {'pattern': custom_regex}
    } for i, custom_regex in enumerate(custom_regexes)]
    custom_info_types = dictionaries + regexes

    # The minimum likelihood to constitute a match. Optional.
    min_likelihood = 'LIKELIHOOD_UNSPECIFIED'

    # The maximum number of findings to report (0 = server maximum). Optional.
    max_findings = 0

    # Whether to include the matching string in the results. Optional.
    include_quote = True

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        'info_types': info_types,
        'custom_info_types': custom_info_types,
        'min_likelihood': min_likelihood,
        'include_quote': include_quote,
        'limits': {'max_findings_per_request': max_findings},
    }

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Call the API.
    response = dlp.inspect_content(parent, inspect_config, item)

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            try:
                print('Quote: {}'.format(finding.quote))
            except AttributeError:
                pass
            print('Info type: {}'.format(finding.info_type.name))
            # Convert likelihood value to string respresentation.
            print('Likelihood: {}'.format(finding.likelihood))
    else:
        print('No findings.')

if __name__ == '__main__':
  main()