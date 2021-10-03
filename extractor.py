import requests
import json
import re

COLOR_REGISTRY = 'https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/platform/theme/common/colorRegistry.ts'


def get_color_registry():
    """
    Get the color registry from the color registry file.
    """
    response = requests.get(COLOR_REGISTRY)
    if response.status_code != 200:
        raise Exception('Failed to get color registry')
    return response.text



if __name__ == '__main__':
    lines = get_color_registry().split('\n')
    jsonstring = {
        'variables': [],
    }
    for line in lines:
        regex = re.compile(r'export const \w+ = registerColor\((\S+)')
        match = regex.search(line)
        if match:
            matchGroup = re.sub(r'\'|,', '', match.group(1))
            jsonstring['variables'].append(matchGroup)
    
    with open('color-variables.json', 'w') as f:
        json.dump(jsonstring, f, indent=4)