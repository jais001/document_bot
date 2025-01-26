import re

from constants import substrings


class SimplePreprocessor:
    """Text Preprocessor"""

    def __init__(self) -> None:
        self.substrings = substrings

    def _replace_substrings_with_space(self, text: str) -> str:
        """method to replace substrings with space

        Args:
            text (str): input text

        Returns:
            str: preprocessed text
        """
        for substring in self.substrings:
            text = text.replace(substring, " ")
        return text

    def _remove_multiple_space(self, text: str) -> str:
        """method to remove multiple spaces from a given text

        Args:
            text (str): input text as string

        Returns:
            str: returns a cleaned text after removing multiple spaces
        """
        text = re.sub("\\s\\s+", " ", text)
        return text

    def _remove_repeated_symbols(self, text: str) -> str:
        """Method to remove repeating multiple symbols from a given text

        Args:
            text (str): input text as string

        Returns:
            str: returns a cleaned text after removing multiple spaces
        """
        # regex operation removes multiple dash or dot
        text = re.sub(r"\-{2,}|\.{2,}", " ", text)
        # removes repeated ". ."
        text = re.sub(r"(\.\s?){2,}", " ", text)
        return text

    def _remove_non_ascii(self, text: str) -> str:
        """Remove characters outside the ASCII range of 0-127 from a string.

        Args:
            text (str): Input text as a string.

        Returns:
            str: Returns the text with non-ASCII characters removed.
        """
        cleaned_text = "".join(
            [(char if 0 <= ord(char) <= 127 else " ") for char in text]
        )
        return cleaned_text

    def preprocess_document(self, document_text: str) -> str:
        """method to perform text preprocessing

        Returns:
            str: preprocessed string
        """

        # removing non-ascii characters
        non_ascii_removed_text = self._remove_non_ascii(text=document_text)
        # remove substrings
        text = self._replace_substrings_with_space(text=non_ascii_removed_text)
        cleaned_text = self._remove_repeated_symbols(text=text)
        new_text = self._remove_multiple_space(text=cleaned_text)

        return new_text
