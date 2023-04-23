# wrap_roles_in_collection

The following repo contains a set of ansible modules, playbooks and configuration to package multiple roles located in different git repositories into a collection repo. 

# Usage

- Configure the roles and their repos in the variables file `vars/roles_repos.yml`
- Init a collection repository. You can create a new git repo and use the command `ansible-galaxy collection init demo.collection` to generate a collection skeleton 
- Use the playbook.yml to add each role in roles_repos.yml into the collection repository

# Example

