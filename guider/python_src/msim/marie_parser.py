from collections import OrderedDict


class Parser:

    KEYWORDS = [
        'load', 'store', 'add', 'subt',
        'input', 'output', 'halt',
        'skipcond', 'jump', 'clear',
        'addi', 'jumpi', 'loadi', 'storei',
        'hex', 'dec', 'ascii',
    ]

    def __init__(self, program=None):
        self.variables = {}
        self.instructions = {}
        self.lines = None
        self._maxes = OrderedDict({'variable': 0, 'func': 0, 'operand': 0, 'comments': 0})

        if program is not None:
            self.parse(program)

    def parse(self, program):
        self.lines = list(map(self._parse_line, program.split('\n')))
        self.revise_operands()

    def _parse_line(self, original_line):
        var, func, operand, comments, operand_is_var = None, None, None, None, False

        line = original_line.strip()

        if '//' in line:
            idx = line.index('/')
            comments = line[idx::]
            line = line[:idx]

        if ',' in line:
            idx = line.index(',')
            var = line[0: idx]
            self.variables[var] = Variable(var)
            line = line[(idx + 1)::]
            if len(var) + 1 > self._maxes['variable']:
                self._maxes['variable'] = len(var) + 1

        chunks = line.split()

        if len(chunks) > 0:
            func = chunks[0]
            if len(func) > self._maxes['func']:
                self._maxes['func'] = len(func)
            if len(chunks) > 1:
                operand = chunks[1]
                if operand in self.variables.keys():
                    operand_is_var = True
                if len(operand) > self._maxes['operand']:
                    self._maxes['operand'] = len(operand)

        return Line(original_line, func, var, operand, comments, operand_is_var)

    def revise_operands(self):
        def check(l):
            if not l.operand_is_var and l.operand in self.variables.keys():
                l.operand_is_var = True

        list(map(check, self.lines))

    def render(self, for_html=False):
        return '\n'.join([self.render_line(line, for_html=for_html) for line in self.lines])

    def render_line(self, line, for_html=False):
        return line.rendered(self._maxes, for_html=for_html)

    def render_html(self):
        return self.render(for_html=True).split('\n')

    def html_line_numbers(self):
        return [line.render_line_number() for line in self.lines]


class Line:

    _colors = {
        'func': 'rgb(191, 63, 63)',
        'variable': 'rgb(127, 63, 191)',
        'comments': 'rgb(119,136,153)',
        'operand': 'rgb(0, 0, 0)',
    }

    _numbers = '0x0'

    def __init__(self, line, func=None, variable=None, operand=None, comments=None, operand_is_var=None):
        self.func = func
        self.line = line
        self.variable = variable
        self.operand = operand
        self.comments = comments
        self.operand_is_var = operand_is_var
        self.number = None
        if func is not None or variable is not None or operand is not None:
            self.number = Line._numbers
            Line._numbers = hex(int(Line._numbers, 16) + int('1', 16))

    def rendered(self, maxes, for_html=False):
        def line_wrap(l):
            wrapper = '<a style="white-space: pre;">{}</a>'
            if for_html:
                l = wrapper.format(l.strip())
            return l

        def color_wrap(f, s):
            wrapper = '<a style="color: {c}; white-space: pre;">{str_}</a>'
            f = f if f in ['func', 'variable', 'comments'] or f == 'operand' and not self.operand_is_var else 'variable'
            if f is not 'comments' and self.number is None:
                return s
            return wrapper.format(c=Line._colors[f], str_=s)

        def get(f, m):
            if self.__dict__[f] is None:
                str_ = ''
            else:
                str_ = self.__dict__[f] + (',' if f == 'variable' else '')
            pad = ' ' * (m - len(str_))
            str_ = (pad if f == 'variable' else '') + str_ + (pad if f != 'variable' else '')
            if for_html:
                return color_wrap(f, str_)
            else:
                return str_

        return line_wrap(' '.join([get(field, max_) for field, max_ in maxes.items()]))

    def render_line_number(self):
        def extract(n, i=1):
            return hex_split(n)[i]

        def hex_split(n):
            return n.split('x')

        def add_pad(n):
            return extract(self.number, 0) + ('0' * n) + extract(self.number)

        if self.number is not None:
            padn = len(extract(Line._numbers)) - len(extract(self.number))
            return '<a style="color: rgb(169,169,169); white-space: pre;">{}</a>'.format(add_pad(padn))
        else:
            return ''


class Variable:

    def __init__(self, name):
        self.name = name
        self.color = None

