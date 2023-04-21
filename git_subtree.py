#!/usr/bin/python

DOCUMENTATION = '''
module: git_subtree
short_description: Ansible module to execute the git subtree command.
description:
    - This module mimics the functionality of the git subtree command by adding a subtree from a source repository to a subdirectory in the main repository.
version_added: "2.9"
author:
    - Your Name (@your_username)
options:
    source:
        description:
            - The source repository to pull the subtree from.
        required: true
    ref:
        description:
            - The repository ref while adding or pulling subtree. Example a branch (main,develop..) of a specific tag
        required: true
    subdirectory:
        description:
            - The subdirectory of the source repository to include in the main repository.
        required: true
    prefix:
        description:
            - The prefix to use for the subtree directory in the main repository.
        required: true
    squash:
        description:
            - A boolean flag indicating whether to squash the subtree history into a single commit in the main repository.
        type: bool
        default: false
    commit_message:
        description:
            - The commit message to use when committing the subtree changes to the main repository.
        default: ''
    working_directory:
        description:
            - The working directory in which to execute the git command.
        default: null
    username:
        description:
            - The username to connect to the git repository.
        default: null
    password:
        description:
            - The git token to connect to the git repository.
        default: null
    ssh_key:
        description:
            - The path to the private ssh key if using ssh connection to the git repo.
        default: null
'''

EXAMPLES = '''
- name: Add a subtree to the main repository
  git_subtree:
    source: https://github.com/example/repo.git
    ref: main
    subdirectory: path/to/subdirectory
    prefix: subtree/prefix
    squash: true
    commit_message: "Add subtree from example/repo"
    working_directory: /path/to/main/repository
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

def main():
    module = AnsibleModule(
        argument_spec=dict(
            source=dict(required=True),
            ref=dict(required=True),
            subdirectory=dict(required=False),
            prefix=dict(required=True),
            squash=dict(type='bool', default=False),
            commit_message=dict(default=''),
            working_directory=dict(default=None),
            username=dict(default=None),
            password=dict(default=None, no_log=True),
            ssh_key=dict(default=None)
        ),
        supports_check_mode=False,
    )

    source = module.params['source']
    ref = module.params['ref']
    subdirectory = module.params['subdirectory']
    prefix = module.params['prefix']
    squash = module.params['squash']
    commit_message = module.params['commit_message']
    working_directory = module.params['working_directory']
    username = module.params['username']
    password = module.params['password']
    ssh_key = module.params['ssh_key']

    check_command = ['git', 'subtree', 'split', '--prefix', prefix]
    try:
        subprocess.check_output(check_command, stderr=subprocess.DEVNULL, cwd=working_directory, text=True)
    except subprocess.CalledProcessError:
        # the subtree does not exist yet, add it
        command = ['git', 'subtree', 'add', '--prefix', prefix, source, ref]
        if squash:
            command.append('--squash')
        if commit_message:
            command.extend(['-m', commit_message])

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory, check=True, text=True)
        except subprocess.CalledProcessError as e:
            module.fail_json(msg=f"Error running command {e.cmd}: {e.stderr.strip()}", rc=e.returncode)

        module.exit_json(
            changed=True,
            msg=result.stdout.strip(),
            rc=result.returncode
        )

    # the subtree already exists, update it
    command = ['git', 'subtree', 'pull', '--prefix', prefix, source, ref]
    if squash:
        command.append('--squash')
    if commit_message:
        command.extend(['-m', commit_message])

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory, check=True, text=True)
    except subprocess.CalledProcessError as e:
        module.fail_json(msg=f"Error running command {e.cmd}: {e.stderr.strip()}", rc=e.returncode)
    if 'is already at commit' in result.stderr:
        module.exit_json(
            changed=False,
            msg=result.stdout.strip(),
            rc=result.returncode
        )
    else:

        module.exit_json(
            changed=True,
            msg=result.stdout.strip(),
            rc=result.returncode
        )


if __name__ == '__main__':
    main()
