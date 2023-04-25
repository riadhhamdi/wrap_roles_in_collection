# wrap_roles_in_collection

The following repo contains a set of ansible modules, playbooks and configuration to package multiple roles located in different git repositories into a collection repo. 

# Prerequisites

- `git subtree` command should be available on your system or on your execution environment

# Usage

- Configure the roles and their repos in the variables file `vars/roles_repos.yml`
- Init a collection repository. You can create a new git repo and use the command `ansible-galaxy collection init demo.collection` to generate a collection skeleton 
- Use the playbook.yml to add each role in roles_repos.yml into the collection repository

- Configure Your roles repos in the file `vars/roles_repos.yml`

```yaml
subtrees:
  - source: git@github.com:riadhhamdi/demo_role1.git  ## Change with your own role (https or ssh) 
    squash: true 
    ref: main
    prefix: roles/role1
  - source: git@github.com:riadhhamdi/demo_role2.git  ## Change with your own role (https or ssh) 
    squash: true 
    ref: main
    prefix: roles/role2
main_collection:
  repo: git@github.com:riadhhamdi/demo_collection.git
  clone_dir: /tmp/demo_collection
```

- Run the playbook to add each repo to the collection main directory

```bash
ansible-playbook playbook.yml -vv
```

# Variables

- `subtrees`: A list of dictionaries containing the roles repos. 

- `Collection`: The target repository of your  collection . galaxy.yml and other collection files should be added manually.


