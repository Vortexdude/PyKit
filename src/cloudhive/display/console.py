""""
Example -
template_mapping = dict(
    default="Downloading $file from url $url",
    flora="# => [Downloading] $file from url $url"
)

cs = ConsoleFormatter(template_mapping)
default_console = cs.Trooper("default")
flora_console = cs.Trooper("flora")
line1 = default_console.inject(file="file1", url="https://example.com")
line2 = flora_console.inject(file="file2", url="https://example.com")
print(line1)
print(line2)


"""
from template import BaseStringTemplate

MAX_CHAR_LENGTH = 50
MIN_FILLER = 5


class ConsoleFormatter:
    def __init__(
            self,
            tp_map: dict,
            delimiter: str | None = None,
            filler: str | None = None,
            add_filler: bool = True
    ):
        """
        Initialize the ConsoleFormatter.

        :param tp_map: A dictionary of templates mapped to styles.
        :param delimiter: The delimiter used for string templates.
        :param filler: The character to use for fillers.
        :param add_filler: Whether to add filler characters to the output.
        """

        if not tp_map or not isinstance(tp_map, dict):
            raise ValueError("'tp_map' must be non empty dictionary")

        self._tp_map = tp_map
        self.style = None
        self.add_filler: bool = add_filler
        self.filler = filler or "*"
        self.delimiter = delimiter or "$"

    def Trooper(self, style: str):
        if style not in self._tp_map:
            raise KeyError(f"Style '{style}' not found in `tp_map`.")

        template_str = self._tp_map[style]
        if self.add_filler:
            template_str += " $filler"
        return TemplateFormatter(BaseStringTemplate(template_str), self.filler, self.add_filler)


class TemplateFormatter:

    def __init__(self, template, filler: str, add_filer: bool):
        self._template: BaseStringTemplate = template
        self._filler = filler
        self._add_filler = add_filer

    def inject(self, **kwargs):
        if self._add_filler:
            total_chars = sum(len(values) for values in kwargs.values())
            total_dots = max(0, MAX_CHAR_LENGTH - total_chars)
            if total_dots >= MIN_FILLER:  # threshold
                kwargs['filler'] = self._filler * total_dots

        return self._template.safe_loads(kwargs)
