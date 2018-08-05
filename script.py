# -*- coding: utf-8 -*-

import re
import pathlib
import pickle

import pendulum


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
            return 'To prepare task: %s [%s ~ %s]!' % (self.name, begin, end)
        elif spec == 'finished':
            return 'Finished task: %s [%s ~ %s]?' % (self.name, begin, end)
        else:
            return 'Started task: %s [%s ~ %s].' % (self.name, begin, end)

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

    def __getstate__(self):
        return self.name, self.begin.to_time_string(), self.end.to_time_string()

    def __setstate__(self, state):
        name, begin, end = state
        self.name, self.begin, self.end = name, pendulum.parse(begin, tz='local'), pendulum.parse(end, tz='local')


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

    def comming_task(self, fromWhen=pendulum.now()):
        # Get the comming task
        tasks = self.future_tasks(fromWhen)
        if tasks:
            return min(tasks, key=lambda t: t.begin)

    def have_a_rest(self):
        return not self.running_task

    def del_past_tasks(self):
        for task in self:
            if task.end > pendulum.now():
                self.remove(task)

    def __getstate__(self):
        return self

    def __setstate__(self, tasks):
        self[:] = tasks

    def report(self):
        now = pendulum.now()
        lst = '<div class="time">%s </div><ul>' % now.format('YYYY-MM-DD dddd')
        if self.running_task:
            lst += '<li class="running">{rt}</li>\n'.format(rt=self.running_task)
        else:
            lst += '<li class="rest">Have a rest, take a coffee.</li>\n'
        if self.comming_task():
            if (self.comming_task().begin - now).total_minutes() > 90:
                lst += '<li class="comming">{ct:prepare} (Don\'t hurry.)</li>'.format(ct=self.comming_task())
            else:
                lst += '<li class="comming">{ct:prepare}</li>'.format(ct=self.comming_task())
        else:
            lst += '<li class="rest">No more tasks. Have a long rest.</li>'
        lst += '</ul>'
        return '<div class="list">%s</div>' % lst

    @staticmethod
    def load(fname='todolist'):
        pklPath = pathlib.Path('./%s.pkl' % fname)
        if pklPath.exists():
            with open(pklPath, 'rb') as fo:
                todolist = pickle.load(fo)
        else:
            txtPath = pathlib.Path('~/%s.txt' % fname).expanduser()
            todolist = ToDoList.read(txtPath)
            with open(pklPath, 'wb') as fo:
                pickle.dump(todolist, fo)
        return todolist


todolist = ToDoList.load()

if __name__ == '__main__':
    print(todolist.report())
