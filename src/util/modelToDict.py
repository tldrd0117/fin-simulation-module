import collections
import inspect
def modelToDict(instance, parent_key="" ,sep="_"):
    items = []
    d = vars(instance)
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if inspect.isclass(v):
            v = vars(v)
        
        if isinstance(v, collections.MutableMapping):
            items.extend(modelToDict(v, new_key, sep).items())
        else:
            items.append((new_key, v))

    return dict(items)