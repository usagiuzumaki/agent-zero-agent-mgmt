import json

def try_parse(json_string: str):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return DirtyJson.parse_string(json_string)


def parse(json_string: str):
    return DirtyJson.parse_string(json_string)


def stringify(obj, **kwargs):
    return json.dumps(obj, ensure_ascii=False, **kwargs)


class DirtyJson:
    def __init__(self):
        self._reset()

    def _reset(self):
        self.json_string = ""
        self.index = 0
        self.current_char = None
        self.result = None
        self.stack = []

    @staticmethod
    def parse_string(json_string):
        # Optimization: Try standard json.loads first for performance
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, TypeError):
            pass

        parser = DirtyJson()
        return parser.parse(json_string)

    def parse(self, json_string):
        self._reset()
        self.json_string = json_string

        # Add bounds checking to prevent IndexError
        if not json_string:
            # Return None for empty strings
            return None

        self.index = self.get_start_pos(self.json_string)

        # Ensure index is within bounds
        if self.index >= len(self.json_string):
            # If start position is beyond string length, return None
            return None

        self.current_char = self.json_string[self.index]
        self._parse()
        return self.result

    def feed(self, chunk):
        self.json_string += chunk
        if not self.current_char and self.json_string:
            self.current_char = self.json_string[0]
        self._parse()
        return self.result

    def _advance(self, count=1):
        self.index += count
        if self.index < len(self.json_string):
            self.current_char = self.json_string[self.index]
        else:
            self.current_char = None

    def _skip_whitespace(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self._advance()
            elif (
                self.current_char == "/" and self._peek(1) == "/"
            ):  # Single-line comment
                self._skip_single_line_comment()
            elif (
                self.current_char == "/" and self._peek(1) == "*"
            ):  # Multi-line comment
                self._skip_multi_line_comment()
            else:
                break

    def _skip_single_line_comment(self):
        while self.current_char is not None and self.current_char != "\n":
            self._advance()
        if self.current_char == "\n":
            self._advance()

    def _skip_multi_line_comment(self):
        self._advance(2)  # Skip /*
        while self.current_char is not None:
            if self.current_char == "*" and self._peek(1) == "/":
                self._advance(2)  # Skip */
                break
            self._advance()

    def _parse(self):
        if self.result is None:
            self.result = self._parse_value()
        else:
            self._continue_parsing()

    def _continue_parsing(self):
        while self.current_char is not None:
            if isinstance(self.result, dict):
                self._parse_object_content()
            elif isinstance(self.result, list):
                self._parse_array_content()
            elif isinstance(self.result, str):
                self.result = self._parse_string()
            else:
                break

    def _parse_value(self):
        self._skip_whitespace()
        if self.current_char == "{":
            if self._peek(1) == "{":  # Handle {{
                self._advance(2)
            return self._parse_object()
        elif self.current_char == "[":
            return self._parse_array()
        elif self.current_char in ['"', "'", "`"]:
            if self._peek(2) == self.current_char * 2:  # type: ignore
                return self._parse_multiline_string()
            return self._parse_string()
        elif self.current_char and (
            self.current_char.isdigit() or self.current_char in ["-", "+"]
        ):
            return self._parse_number()
        elif self._match("true"):
            return True
        elif self._match("false"):
            return False
        elif self._match("null") or self._match("undefined"):
            return None
        elif self.current_char:
            return self._parse_unquoted_string()
        return None

    def _match(self, text: str) -> bool:
        # first char should match current char
        if not self.current_char or self.current_char.lower() != text[0].lower():
            return False

        # peek remaining chars
        remaining = len(text) - 1
        if self._peek(remaining).lower() == text[1:].lower():
            self._advance(len(text))
            return True
        return False

    def _parse_object(self):
        obj = {}
        self._advance()  # Skip opening brace
        self.stack.append(obj)
        self._parse_object_content()
        return obj

    def _parse_object_content(self):
        while self.current_char is not None:
            self._skip_whitespace()
            if self.current_char == "}":
                if self._peek(1) == "}":  # Handle }}
                    self._advance(2)
                else:
                    self._advance()
                self.stack.pop()
                return
            if self.current_char is None:
                self.stack.pop()
                return  # End of input reached while parsing object

            key = self._parse_key()
            value = None
            self._skip_whitespace()

            if self.current_char == ":":
                self._advance()
                value = self._parse_value()
            elif self.current_char is None:
                value = None  # End of input reached after key
            else:
                value = self._parse_value()

            self.stack[-1][key] = value

            self._skip_whitespace()
            if self.current_char == ",":
                self._advance()
                continue
            elif self.current_char != "}":
                if self.current_char is None:
                    self.stack.pop()
                    return  # End of input reached after value
                continue

    def _parse_key(self):
        self._skip_whitespace()
        if self.current_char in ['"', "'"]:
            return self._parse_string()
        else:
            return self._parse_unquoted_key()

    def _parse_unquoted_key(self):
        # Optimization: use list join instead of string concatenation
        result = []
        while (
            self.current_char is not None
            and not self.current_char.isspace()
            and self.current_char not in [":", ",", "}", "]"]
        ):
            result.append(self.current_char)
            self._advance()
        return "".join(result)

    def _parse_array(self):
        arr = []
        self._advance()  # Skip opening bracket
        self.stack.append(arr)
        self._parse_array_content()
        return arr

    def _parse_array_content(self):
        while self.current_char is not None:
            self._skip_whitespace()
            if self.current_char == "]":
                self._advance()
                self.stack.pop()
                return
            value = self._parse_value()
            self.stack[-1].append(value)
            self._skip_whitespace()
            if self.current_char == ",":
                self._advance()
                # handle trailing commas, end of array
                self._skip_whitespace()
                if self.current_char is None or self.current_char == "]":
                    if self.current_char == "]":
                        self._advance()
                    self.stack.pop()
                    return
            elif self.current_char != "]":
                self.stack.pop()
                return

    def _parse_string(self):
        # Optimization: use list join instead of string concatenation
        result = []
        quote_char = self.current_char
        self._advance()  # Skip opening quote
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == "\\":
                self._advance()
                if self.current_char in ['"', "'", "\\", "/", "b", "f", "n", "r", "t"]:
                    result.append({
                        "b": "\b",
                        "f": "\f",
                        "n": "\n",
                        "r": "\r",
                        "t": "\t",
                    }.get(self.current_char, self.current_char))
                elif self.current_char == "u":
                    self._advance()  # Skip 'u'
                    unicode_char = ""
                    # Try to collect exactly 4 hex digits
                    for _ in range(4):
                        if self.current_char is None or not self.current_char.isalnum():
                            # If we can't get 4 hex digits, treat it as a literal '\u' followed by whatever we got
                            result.append("\\u" + unicode_char)
                            break # break inner loop
                        unicode_char += self.current_char
                        self._advance()
                    else: # Executed if loop finished normally (found 4 chars)
                        try:
                            result.append(chr(int(unicode_char, 16)))
                        except ValueError:
                            # If invalid hex value, treat as literal
                            result.append("\\u" + unicode_char)
                    continue # Continue to next char in while loop
            else:
                result.append(self.current_char)
            self._advance()
        if self.current_char == quote_char:
            self._advance()  # Skip closing quote
        return "".join(result)

    def _parse_multiline_string(self):
        # Optimization: use find and slicing instead of character-by-character loop
        # This provides O(1) loop overhead vs O(N)
        quote_char = self.current_char
        closing_marker = quote_char * 3

        self._advance(3)  # Skip first quote

        start_index = self.index
        end_index = self.json_string.find(closing_marker, start_index)

        if end_index != -1:
            result = self.json_string[start_index:end_index]
            # Advance to the character after the closing marker
            # We need to update index to end_index + 3 (skip closing quotes)
            # But _advance updates relative to current index.
            # Current index is start_index (because we called _advance(3) before)
            # So we need to advance by (end_index - start_index) + 3
            self._advance(end_index - start_index + 3)
            return result.strip()
        else:
            # If no closing marker found, consume the rest of the string
            result = self.json_string[start_index:]
            self._advance(len(self.json_string) - start_index)
            return result.strip()

    def _parse_number(self):
        number_str = ""
        while self.current_char is not None and (
            self.current_char.isdigit()
            or self.current_char in ["-", "+", ".", "e", "E"]
        ):
            number_str += self.current_char
            self._advance()
        try:
            return int(number_str)
        except ValueError:
            return float(number_str)

    def _parse_unquoted_string(self):
        # Optimization: use list join instead of string concatenation
        result = []
        while self.current_char is not None:
            if self.current_char in [",", "}", "]"]:
                break

            if self.current_char == ":":
                # Check for URL pattern (e.g., http://)
                # If : is followed by //, treat it as part of the string
                if self._peek(2) == "//":
                    result.append(self.current_char)
                    self._advance()
                    continue
                else:
                    break

            result.append(self.current_char)
            self._advance()

        # Do not consume the delimiter (matching _parse_number behavior)
        return "".join(result).strip()

    def _peek(self, n):
        # Optimization: avoid slicing for single char lookahead
        if n == 1:
            idx = self.index + 1
            if idx < len(self.json_string):
                return self.json_string[idx]
            return ""

        # Optimization: use slicing instead of loop
        peek_start = self.index + 1
        peek_end = peek_start + n
        return self.json_string[peek_start:peek_end]

    def get_start_pos(self, input_str: str) -> int:
        chars = ["{", "[", '"']
        indices = [input_str.find(char) for char in chars if input_str.find(char) != -1]
        return min(indices) if indices else 0
