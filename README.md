# Lineinfile Python

I often find myself wanting similar features of the lineinfile module from Ansible, which is why I decided to make a 
Python adaptation of the [lineinfile module](https://docs.ansible.com/ansible/latest/modules/lineinfile_module.html)
in [Ansible](https://www.ansible.com/).


## List of features

The list of features supported in this adaptation is directly taken from the `lineinfile` module documentation.

- [ ] Attributes
- [ ] Backrefs
- [ ] Backup
- [x] Create
- [ ] Firstmatch
- [ ] Group
- [ ] Insertafter
- [ ] Insertbefore
- [ ] Mode
- [ ] Other
- [ ] Owner
- [x] Regexp
- [ ] Selevel
- [ ] Serole
- [ ] Setype
- [ ] Seuser
- [ ] Unsafe_writes
- [ ] Validate

## Development
```
git clone git@github.com:AlexanderGrooff/lineinfile-python.git
cd lineinfile-python
mkvirtualenv -a . -p python3 $(basename $(pwd))
```
