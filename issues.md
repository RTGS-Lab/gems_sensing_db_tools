### Issues

1. Logging happens on whatever branch you are working out of. Create logging branch and put all logs there.
2. update configuration uses a wrapper on old GitLogger class
3. error analysis is using backwards methods and outdated classes
4. Lot of bloat in each module, analyze each one, and make sure only neccesary functions exist. Make sure there are no unsued functions or repeated code
5. every module has multiple paramter definitions for some reason.
6. create a requirements document for each module and a list of arguments that makes each module useful
7. add a link to the notes of the device to the logfile