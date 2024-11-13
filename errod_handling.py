#gestion des erreurs (syntaxe et grammaire possiblement inutile)
class LexicalError(Exception):
    def __init__(self, message, line=None, column=None):
        # message : Description de l'erreur
        # line, column : Position de l'erreur dans le code source (facultatif)
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.__str__())

    def __str__(self):
        # Affiche un message d'erreur avec la position (s'il est disponible)
        location = f" at line {self.line}, column {self.column}" if self.line is not None and self.column is not None else ""
        return f"LexicalError: {self.message}{location}"


class SyntaxError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.__str__())

    def __str__(self):
        location = f" at line {self.line}, column {self.column}" if self.line is not None and self.column is not None else ""
        return f"SyntaxError: {self.message}{location}"


class RuntimeError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.__str__())

    def __str__(self):
        location = f" at line {self.line}, column {self.column}" if self.line is not None and self.column is not None else ""
        return f"RuntimeError: {self.message}{location}"
