# checks for diff, if any then commit all and save
git -C ~/SpaceMonkey/Documents/todos diff --exit-code || git -C ~/SpaceMonkey/Documents/todos commit --all -m "autocommit"

## TODO: make it so cron either sends to my proper email upon changes
## or does not mail results at all.


# git -C $HOME/Spacemonkey/Documents/todos diff --exit-code --quiet && git -C $HOME/Spacemonkey/Documents/todos commit --all -m "autocommit"
# possible the above didn't work as a cron because I capital-typed a directory
# Lahwran says he never manages to make commands work, just files.


## make sure this script is executable
# chmod +x AutosaveNotes.sh
# crontab $HOME/SpaceMonkey/Documents/todos/AutosaveCron.txt

###########

## log here
# vim /var/log/cron.log

## setup by adding
# cron.*      /var/log/cron.log
## to /etc/syslog.conf
## Then restart syslog

# sudo launchctl unload /System/Library/LaunchDaemons/com.apple.syslogd.plist
# sudo launchctl load /System/Library/LaunchDaemons/com.apple.syslogd.plist
## http://superuser.com/questions/134864/log-of-cron-actions-on-os-x

