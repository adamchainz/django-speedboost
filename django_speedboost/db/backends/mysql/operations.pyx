def quote_name(name):
    if name[0] == "`" and name[-1] == "`":
        return name  # Quoting once is enough.
    else:
        return "`" + name + "`"
