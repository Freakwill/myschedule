# myschedule

My schedule, also your schedule. It is our schedule.

## Featrues

* display the tasks dynamically, currently, only the running task and comming task are shown
* build heavily on python instead of javascript/coffeescript (update.py will be ignored)

## Configuration

* Create 'todolist.txt' under '/Users/*HOME*'
* Edit it, create a task in the form '14:10-15:00, study' (there is an example)
* start up the wigdet.
  
'14:10-15:55, study' == '14:10, study', since the default duration == 45min.
  
## Hicking

Inherit the following classes.
Task: a task
ToDoList: todo list, list of Task

* To create the your own html form, override method `report`
* If you save 'todolist.txt' in another path, you have to set it to argument `path` of `read` method in script.py
* Method `__format__` controls the form of a task

## Framework

It was built by [pyubersicht](https://github.com/Freakwill/pyubersicht).
