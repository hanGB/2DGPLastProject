
# layer 0: Background Objects
# layer 1: Foreground Objects
# layer 2: Ui Objects
# layer 3: auto

objects = [[], [], [], []]


def add_object(o, layer):
    if layer != 3:
        objects[layer].append(o)
    else:
        if len(objects[3]) == 0:
            objects[3].append(o)


def add_objects(l, layer):
    objects[layer] += l


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def remove_object_processor():
    if len(objects[3]) != 0:
        objects[3].clear()


def clear():

    for i in range(len(objects)):
        for o in objects[i]:
            objects[i].remove(o)
            del o

# 처음에 삭제시 완전 삭제가 안되는 버그 존재하여 한 번 더 탐색하여 나머지 삭제

    for i in range(len(objects)):
        for o in objects[i]:
            objects[i].remove(o)
            del o


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

