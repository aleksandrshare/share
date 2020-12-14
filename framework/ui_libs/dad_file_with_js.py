#!/usr/bin/env python
# -*- coding: utf-8 -*-

# JS скрипт для использования drag and drop HTML5
JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""


def drag_and_drop_file(web_element, path):
    """ функция исользует JS скрипт, чтобы передать файл с локальной машины в элемент drag and drop
    :argument
        web_element (webelement): элемент для drag_and_drop
        path (str): путь до локального файла
    """
    driver = web_element.parent
    file_input = driver.execute_script(JS_DROP_FILE, web_element, 0, 0)
    file_input.send_keys(path)
