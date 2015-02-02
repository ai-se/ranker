typo: gitting  
	- git status
	- git commit -am "typo"
	- git push origin master

gitting:
	git config --global credential.helper cache
	git config credential.helper 'cache --timeout=3600'

commit:  gitting
	- git status
	- git commit -a
	- git push origin master

update:  gitting
	- git pull origin master

status: gitting
	- git status
	
demo1:
	python ranker.py | tee var/demo1.txt

