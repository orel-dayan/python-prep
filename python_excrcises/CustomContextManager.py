from contextlib import contextmanager

@contextmanager
def temporary_config_override(config_dict: dict, key: str, temp_value):
    original_value = config_dict.get(key)
    config_dict[key] = temp_value
    try:
        yield config_dict  # use the modified config within the context
    finally:
       # Restore the original value after exiting the context
        if original_value is not None:
            config_dict[key] = original_value
        else:
            config_dict.pop(key, None)

# Example usage of the temporary_config_override context manager
system_config = {"timeout": 30, "retry_count": 3}

with temporary_config_override(system_config, "timeout", 5):
    print("Inside with block:", system_config)  # timeout = 5

print("Outside with block:", system_config)     # timeout = 30