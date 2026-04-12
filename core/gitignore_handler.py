import pathspec
from pathlib import Path

class GitignoreHandler:
    def __init__(self, patterns=None):
        self.patterns = patterns or []
        self.spec = None
        if self.patterns:
            self._compile()

    def add_patterns(self, patterns_text, scope_path=None):
        if not patterns_text:
            return
            
        new_patterns = []
        for line in patterns_text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if scope_path:
                # Scope the pattern to the subdirectory
                # scope_path should be relative to source root
                prefix = str(scope_path).replace("\\", "/")
                if not prefix.endswith('/'):
                    prefix += '/'
                
                if line.startswith('/'):
                    new_patterns.append(f"{prefix}{line[1:]}")
                else:
                    # If it's a relative pattern, match it within the scope
                    new_patterns.append(f"{prefix}**/{line}")
            else:
                new_patterns.append(line)
                
        self.patterns.extend(new_patterns)
        self._compile()

    def _compile(self):
        self.spec = pathspec.PathSpec.from_lines('gitwildmatch', self.patterns)

    def is_ignored(self, file_path, base_path):
        if not self.spec:
            return False
        
        # pathspec expects paths relative to the root
        try:
            relative_path = Path(file_path).relative_to(base_path)
            return self.spec.match_file(str(relative_path))
        except ValueError:
            # Not in base path, so not ignored by these rules
            return False

    @staticmethod
    def detect_and_load(directory):
        gitignore_path = Path(directory) / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
