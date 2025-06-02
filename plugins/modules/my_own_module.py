#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Module for creating files with content

version_added: "1.0.0"

description: Module creates a file at specified path with given content.

options:
    path:
        description: Path to the file to be created
        required: true
        type: str
    content:
        description: Content to write to the file
        required: false
        type: str
        default: ""
author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create a file with content
- name: Create a file
  my_namespace.my_collection.my_own_module:
    path: /tmp/testfile.txt
    content: "Hello World!"

# Create an empty file
- name: Create empty file
  my_namespace.my_collection.my_own_module:
    path: /tmp/emptyfile.txt
'''

RETURN = r'''
file_path:
    description: Path to the created file
    type: str
    returned: always
    sample: '/tmp/testfile.txt'
content:
    description: Content written to the file
    type: str
    returned: always
    sample: 'Hello World!'
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default="")
    )

    result = dict(
        changed=False,
        file_path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['file_path'] = path
    result['content'] = content

    if module.check_mode:
        module.exit_json(**result)

    if os.path.exists(path):
        with open(path, 'r') as f:
            existing_content = f.read()
        if existing_content == content:
            module.exit_json(**result)

    try:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
    except Exception as e:
        module.fail_json(msg=f"Failed to create file: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
