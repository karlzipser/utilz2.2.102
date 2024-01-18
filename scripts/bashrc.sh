
alias gacp="git add .;git commit -m 'gacp';git push origin master"
alias sshok='sudo service ssh restart'
alias rgrep='grep -r -n -I '
alias enablescripts='chmod -R u+x ~/utilz2/scripts/'
alias rse='rsync -ravL --exclude *.pth --exclude *.png --exclude *.pth_'

git config --global credential.helper "cache --timeout=86400"

alias ipy="ipython --no-banner --no-confirm-exit"

export PYTHONPATH=~:$PYTHONPATH

# mogrify -format jpg *.HEIC

export PATH=~/utilz2/scripts:$PATH
export PATH=~/utilz2/scripts/osx:$PATH

export COMPUTER_NAME=$HOSTNAME #'' #
PS1="$HOSTNAME\[\033[01;35m\]\w\[\033[00m\] $ "

export HISTSIZE=100000
export PYTHONUNBUFFERED=1 
# needed for time.sleep() to work properly

alias enable_scripts='chmod -R u+x utilz2/scripts/'

export PYTHONSTARTUP=~/utilz2/scripts/__start__.py

alias nfiles="ls -l | wc -l"
#EOF
