# -*- coding:utf-8 -*-
import xml.dom.minidom as minidom


def write_xml(points):
    dom = minidom.getDOMImplementation().createDocument(None, '任务', None)
    root = dom.documentElement
    points.sort(key=lambda x: (round(x[0]), x[1]))
    i = 0
    while i < len(points):
        point = points[i]
        bomb = 1
        while i < len(points) - 1 and points[i] == points[i + 1]:
            bomb += 1
            i += 1
        element = dom.createElement('瞄准点')
        element.setAttribute('x', str(round(point[0])))
        element.setAttribute('y', str(round(point[1])))
        element.setAttribute('成爆弹量', str(bomb))
        root.appendChild(element)
        i += 1
    with open('out.xml', 'w', encoding='utf-8') as f:
        dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')


if __name__ == '__main__':
    write_xml([(-49.0, -68.0), (-39.0, -48.0), (-40.0, -19.0), (-40.0, -19.0), (-40.0, -19.0), (-40.0, -19.0)])
