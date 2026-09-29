# Factory: one place decides which parser to build from the file name.
import json
from abc import ABC, abstractmethod
from typing import ClassVar

# --- original function-based version ---

# def parse_csv(text):
#    header, *body = [line.split(",") for line in text.strip().splitlines()]
#    #return [dict(zip(header, row)) for row in body]
#    result = []
#    for row in body:
#        result.append(dict(zip(header, row)))
#    return result

# def parse_json(text):
#    return json.loads(text)

# def get_parser(file_name):
#     if file_name.endswith(".csv"):
#         return parse_csv
#     elif file_name.endswith(".json"):
#         return parse_json
#     else:
#         raise ValueError(f"Unsupported file type: {file_name}")


# csv_data = "name,qty\nrice,3\nflour,1"
# print(get_parser("stock.csv")(csv_data))
# print(get_parser("stock.json")('{"rice": 3}'))

# --- class-based version ---


class Parser(ABC):
    @abstractmethod
    def parse(self, text):
        ...


class CsvParser(Parser):
    def parse(self, text):
        header, *body = [line.split(",") for line in text.strip().splitlines()]
        result = []
        for row in body:
            result.append(dict(zip(header, row)))
        return result


class JsonParser(Parser):
    def parse(self, text):
        return json.loads(text)


class ParserFactory:
    _parsers: ClassVar[dict] = {
        ".csv": CsvParser,
        ".json": JsonParser,
    }

    @classmethod
    def get_parser(cls, file_name):
        for suffix, parser_cls in cls._parsers.items():
            if file_name.endswith(suffix):
                return parser_cls()
        raise ValueError(f"Unsupported file type: {file_name}")


if __name__ == "__main__":
    csv_data = "name,qty\nrice,3\nflour,1"
    print(ParserFactory.get_parser("stock.csv").parse(csv_data))
    print(ParserFactory.get_parser("stock.json").parse('{"rice": 3}'))

