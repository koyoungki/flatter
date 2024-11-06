# Flatter

Flatter is a Python script designed to calculate file dependencies in C/C++ projects and flatten code by replacing `#include "header"` style includes with the actual content of the included files. This process helps in creating a standalone, single-file version of the code, ideal for testing, submission, or distribution.

## Features

- Recursively processes and resolves dependencies for files included via `#include "header.h"`.
- Maintains standard library includes (`#include <header>`) without expanding them.
- Outputs the final flattened code in a single file.

## Usage

```bash
python flatter.py <target_file> <output_file>
```
