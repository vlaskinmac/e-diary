# Electronic school diary


**Script Corrects teachers' grades and comments.**


This script is written as part of the task of the courses [Devman](https://dvmn.org).


## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Python Version

Python 3.6 and later.



## Installing

- Download the main code from the repository: [fork](https://github.com/devmanorg/e-diary/tree/master)
- Data dase downloads here: [schoolbase.zip](https://github.com/vlaskinmac/e-diary/files/7985932/schoolbase.zip)


To install the software, you need to install the dependency packages from the file: **requirements.txt**.

Perform the command:

```

pip3 install -r requirements.txt

```
## Launch code
**Files script.py and settings.py must be in the same directory.**
#### Arguments
- To correct grades use argument: **-n or --name** 
- To correct grades and add teacher praise add argument: **-s, --subject** 


**Examples of commands:**


```python
$ python script.py -n "Голубев Феофан" -s Краеведение
```

```python
$ python script.py -n "Голубев Феофан" 
```


## Authors

**vlaskinmac**  - [GitHub-vlaskinmac](https://github.com/vlaskinmac/)


