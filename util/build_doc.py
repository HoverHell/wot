#!/usr/bin/env python
# coding: utf8
"""
A script to convert convenient text to markdown to html.

"""


import os
import sys
import re
import pyaux


def repl_header(match):
    """ Replace '=' header with '#' header """
    lh, text, rh = match.groups()
    res = '%s %s %s' % ('#' * len(lh), text, '#' * len(rh))
    return res


class Worker:
    result = None
    state = None
    state__list = None

    simple_replacements = (
        # header
        (r'^(=+) (.+) (=+)$', repl_header),
        # trailing whitespaces
        (r' *$', ''),
    )

    header = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      ol { padding: 0 0 0 2em; }
      ol[manual] { padding: 0 0 0 1em; list-style: none; }
      li[value]:before { content: attr(value) ". " }
    </style>
  </head>
  <body>
    '''

    footer = '''
  </body>
</html>
    '''

    list_header = '<ol manual=1>'
    list_footer = '</ol>'
    item_footer = '</li>'  # non-item-specific

    def process(self, lines):
        self.state = None
        self.result = []

        # self.result.append(self.header)

        lines = (self.handle_simple_replacements(line) for line in lines)
        line_iter = pyaux.window(lines, fill_left=True, fill=None)
        
        for prev_line, line in line_iter:
            self.check_state(prev_line, line)
            if self.state == 'list':
                self.process_list(line)
            else:
                self.result.append(line)

        # self.result.append(self.footer)

        return self.result

    def handle_simple_replacements(self, line):
        # simple replacements
        for rex, repl in self.simple_replacements:
            line = re.sub(rex, repl, line)
        return line

    def check_state(self, prev_line, line):
        """ State changes handler """
        if self.state == 'list':
            # empty line and then a non-list.
            # Almost markdown-like behaviour for lists: single empty
            # lines will not break the list; but unlike markdown, two
            # empty lines will.
            if not prev_line and not re.search(r'^ +[0-9].*\. ', line):
                # Not a list anymore
                self.result, prev_line_x = self.result[:-1], self.result[-1]
                self.unwind_list()
                self.result.append(prev_line_x)
                self.state = ''
                self.state__list = None
        elif not prev_line and line.startswith(' 1. '):
            # note the very specific list starter
            self.state = 'list'
            self.state_list = []

    def process_list(self, line):
        # any line should match
        match = re.search(
            r'^(?P<spaces> *)(?:(?P<num>[0-9a-z.]+)\. )?(?P<text>.*)$',
            line)
        data = match.groupdict()
        spaces = data['spaces']
        indent = len(spaces)
        num = data.get('num')
        text = data['text']

        if not num:
            # put as-is
            # e.g.: empty lines
            self.result.append(line)
            return

        item_header = '<li value="%s">' % (num,)
        item_footer = self.item_footer
        item_info = dict(data, indent=indent)

        # else:  if num:
        if not self.state__list:
            # starting a list
            self.result.extend((
                self.list_header,  # <ol>
                spaces + item_header,  # <li>
                spaces + text))
            self.state__list = [item_info]
            return

        # else: if within a list already:
        last_info = self.state__list[-1]
        if last_info['indent'] == indent:
            # same indent, i.e. continuing the list
            self.result.extend((
                spaces + item_footer,  # </li>
                spaces + item_header,  # <li>
                spaces + text))
            last_info.update(item_info)  # replace the num for possible recursion
        elif 0 < indent - last_info['indent'] <= 3:
            # going deeper
            # ol-li-ol-li chain
            self.result.extend((
                spaces + self.list_header,  # <ol>
                spaces + item_header,  # <li>
                spaces + text))
            self.state__list.append(item_info)
        elif indent - last_info['indent'] < 0:
            # returning
            state_closing, state_remain = pyaux.split_list(
                self.state__list, lambda info: info['indent'] > indent)
            self.unwind_list(state_closing)  # </li></ol>
            self.state__list = state_remain
            self.result.extend((
                spaces + item_footer,  # </li>
                spaces + item_header,  # <li>
                spaces + text))

    def unwind_list(self, infos=None):
        if infos is None:
            infos = self.state__list or []
        for info in reversed(infos):
            spaces = info['spaces']
            self.result.extend((
                spaces + self.item_footer,  # </li>
                spaces + self.list_footer))  # </ol>


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = os.path.join(os.path.dirname(__file__), '..', 'doc.txt')

    with open(filename) as fo:
        data = fo.read()


    lines = data.splitlines()

    worker = Worker()
    result = worker.process(lines)
    result_s = '\n'.join(result)

    with open('doc.md', 'w') as fo:
        fo.write(result_s)

    import markdown
    result_html_base = markdown.Markdown().convert(result_s)
    result_html = worker.header + result_html_base + worker.footer
    # with open('doc_xx.html', 'w') as fo:
    #     fo.write(result_html_base)
    with open('doc.html', 'w') as fo:
        fo.write(result_html)


if __name__ == '__main__':
    main()
