from string import Template


class BaseStringTemplate(Template):
    delimiter = "$"

    def safe_loads(self, mapping=None, **kwargs):
        if mapping is None:
            mapping = {}

        combine_kwargs = {**mapping, **kwargs}

        class DefaultDict(dict):
            def __missing__(self, key):
                # return f"<{key}>"
                return "" # suppress missing keys Error

        safe_mappings = DefaultDict(**combine_kwargs)
        return self.safe_substitute(safe_mappings)

__all__ = [BaseStringTemplate]
