# -*- coding: utf-8 -*-

import re
import pendulum
import pathlib


_DefualtDuration = 45    # 45 minutes
_DefualtPath = pathlib.Path('~').expanduser()


task_rx = re.compile(r' *(?P<begin>\d{1,2}:\d{1,2})(-(?P<end>\d{1,2}:\d{1,2}))?, (?P<name>.+) *')

class Task(object):
    """class of Task.

    A job should be done at certain time.
    """
    def __init__(self, name, begin, end=None):
        self.name = name
        if isinstance(begin, str):
            self.begin = pendulum.parse(begin, tz='local')
        else:
            self.begin = begin
        if end is None:
            self.end = self.begin.add(minutes=_DefualtDuration)
        elif isinstance(end, str):
            self.end = pendulum.parse(end, tz='local')
        else:
            self.end = end

    def __str__(self):
        begin = self.begin.to_datetime_string()
        if self.in_1day():
            end = self.end.to_time_string()
        else:
            end = self.end.to_datetime_string()
        return '[%s ~ %s] %s.' % (begin, end, self.name)

    def __format__(self, spec=''):
        if self.at_today():
            begin = self.begin.to_time_string()
            end = self.end.to_time_string()
        else:
            begin = self.begin.to_datetime_string()
            if self.in_1day():
                end = self.end.to_time_string()
            else:
                end = self.end.to_datetime_string()
        if spec == 'prepare':
            return 'To prepare task: %s [%s ~ %s]!' % (begin, end, self.name)
        elif spec == 'finished':
            return 'Finished task: %s [%s ~ %s]?' % (begin, end, self.name)
        else:
            return 'Started task: %s [%s ~ %s].' % (begin, end, self.name)

    def in_1day(self):
        return self.begin.date() == self.end.date()

    def at_today(self):
        return self.begin.date() == self.end.date() == pendulum.now().date()

    @staticmethod
    def parse(s:str):
        # parse a string to a `Task` object
        m = task_rx.match(s)
        name = m['name']
        if 'end' in m.groupdict():
            begin, end = m['begin'], m['end']
        else:
            begin, end = m['begin'], None
        return Task(name, begin, end)

    def is_running(self):
        return self.begin <= pendulum.now() < self.end


class ToDoList(list):
    '''To do list
    
    Extends:
        list
    
    Variables:
        quote {str} -- quote display under the list
    '''

    quote = 'Control Yourself'

    @staticmethod
    def parse(s:str):
        return ToDoList([Task.parse(todo) for todo in s.split('\n') if todo.strip() and not todo.startswith('#')])

    @staticmethod
    def read(f=_DefualtPath):
        if isinstance(f, str):
            f = pathlib.Path(f).expanduser()
        s = f.read_text(encoding='utf-8')
        return ToDoList.parse(s)

    @property
    def running_task(self):
        # Get the funning task
        for task in self:
            if task.is_running():
                return task

    def future_tasks(self, fromWhen=pendulum.now()):
        '''Get the list of future tasks from `fromWhen`
        
        Keyword Arguments:
            fromWhen {[pendulum.datetime]} -- (default: {pendulum.now()})
        '''
        return [task for task in self if task.begin > fromWhen]

    @property
    def comming_task(self):
        # Get the comming task
        if self.future_tasks():
            return min(self.future_tasks(), key=lambda t: t.begin)

    def have_a_rest(self):
        return not self.running_task

    def report(self):
        head = '<h1>TO DO LIST</br>(%s)</h1>' % pendulum.now().to_date_string()
        lst = '<ul>'
        if self.running_task:
            lst = '<li class="running">{rt}</li>\n'.format(rt=self.running_task)
        else:
            lst = '<li class="rest">Have a rest, take a coffee.</li>\n'
        if self.comming_task:
            lst += '<li class="comming">{ct:prepare}</li>'.format(ct=self.comming_task)
        else:
            lst += '<li class="rest">No more tasks. Have a long rest.</li>'
        lst += '</ul>'
        return '<html>\n%s\n<div class="list">%s</div>\n</br><div class="quote">%s</div></html>' % (head, lst, ToDoList.quote)

if __name__ == '__main__':

    todolist = ToDoList.read('~/todolist.txt')
    print(todolist.report())
