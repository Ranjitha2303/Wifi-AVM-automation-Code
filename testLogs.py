ENABLE = True


def INFO(data):
    if ENABLE:
        print ("---INFO: {}".format(data))


def ERROR(data):
    if ENABLE:
        print ("---ERROR: {}".format(data))


def SUCCESS(data):
    if ENABLE:
        print ("---SUCCESS: {}".format(data))


def STATUS(data):
    if ENABLE:
        print ("---STATUS: {}".format(data))
