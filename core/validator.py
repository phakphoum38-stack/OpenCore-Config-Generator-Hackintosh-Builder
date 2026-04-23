def validate(config):
    errors = []

    if "Kernel" not in config:
        errors.append("Missing Kernel section")

    return errors
