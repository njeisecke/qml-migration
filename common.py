def path_to_uri(path):
    if path == ".":
        return 'ui'
    else:
        return f'ui.{path.replace("./", "").replace("/", ".")}'

def path_to_module_name(path):
    if path == ".":
        return 'ui'
    else:
        return f'ui_{path.replace("./", "").replace("/", "_")}'
