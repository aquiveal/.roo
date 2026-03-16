# @Domain
These rules MUST be activated and strictly adhered to whenever the AI is tasked with generating, reviewing, refactoring, modifying, or explaining Python code (`.py` files). These rules apply to all general Python development tasks, standard library usage, algorithm implementation, and code formatting requests.

# @Vocabulary
- **Pythonic**: Code that follows the unique, emergent idioms of the Python community, emphasizing explicitness, simplicity, and readability.
- **PEP 8**: Python Enhancement Proposal #8, the official style guide for formatting Python code.
- **Unicode Sandwich**: A design pattern where a program does encoding and decoding of Unicode data at the furthest boundary of its interfaces, operating exclusively on `str` types at its core.
- **Interpolated F-Strings (f-strings)**: A Python 3.6+ syntax (`f'...'`) for formatting strings that allows arbitrary Python expressions to be directly embedded within format specifiers.
- **Unpacking**: Python's syntax for assigning multiple values from an iterable to distinct variables in a single statement.
- **Walrus Operator (`:=`)**: An assignment expression introduced in Python 3.8 that simultaneously assigns a value to a variable and evaluates that value within a larger expression.
- **Catch-all Unpacking**: Using a starred expression (`*variable`) to receive all remaining values that didn't match any other part of an unpacking pattern.
- **Generator**: A function that uses `yield` expressions to incrementally produce a stream of values, returning an iterator.

# @Objectives
- The AI MUST write highly idiomatic (Pythonic) code that leverages Python 3's unique features to maximize expressivity and minimize visual noise.
- The AI MUST prioritize code readability and simplicity over overly dense "clever" one-liners.
- The AI MUST completely strictly adhere to PEP 8 style formatting and naming conventions.
- The AI MUST prevent common data-type and boundary bugs by strictly managing string/byte encodings and explicit sequence parsing.
- The AI MUST proactively refactor redundant code using assignment expressions, multiple unpacking, and specialized built-in functions.

# @Guidelines

## 1. Python Version Constraints
- The AI MUST use Python 3 syntax exclusively. Code MUST be compatible with Python 3.8+ idioms.
- The AI MUST NOT use legacy Python 2 syntax, modules, or workarounds (e.g., do not use `six` or `2to3` concepts).

## 2. Strict PEP 8 Compliance
- **Whitespace**: 
  - The AI MUST use 4 spaces for each level of indentation. The AI MUST NOT use tabs.
  - The AI MUST restrict line lengths to 79 characters or less.
  - The AI MUST indent continuations of long expressions onto additional lines by four extra spaces from their normal indentation level.
  - The AI MUST separate functions and classes by two blank lines in a file.
  - The AI MUST separate methods within a class by one blank line.
  - The AI MUST NOT place whitespace between a dictionary key and the colon. The AI MUST place a single space before the corresponding value if it fits on the same line.
  - The AI MUST put exactly one space before and after the `=` operator in variable assignments.
  - The AI MUST format type annotations with no separation between the variable name and the colon, and a single space before the type information.
- **Naming**:
  - The AI MUST use `lowercase_underscore` for functions, variables, and attributes.
  - The AI MUST use `_leading_underscore` for protected instance attributes.
  - The AI MUST use `__double_leading_underscore` for private instance attributes.
  - The AI MUST use `CapitalizedWord` for classes and exceptions.
  - The AI MUST use `ALL_CAPS` for module-level constants.
  - The AI MUST name the first parameter of instance methods `self`.
  - The AI MUST name the first parameter of class methods `cls`.
- **Expressions and Statements**:
  - The AI MUST use inline negation (e.g., `if a is not b`) instead of negating positive expressions (e.g., `if not a is b`).
  - The AI MUST NOT check for empty/non-empty containers by comparing their length to zero (e.g., `if len(somelist) == 0`). The AI MUST use implicit boolean evaluation (e.g., `if not somelist` or `if somelist`).
  - The AI MUST avoid single-line `if` statements, `for` and `while` loops, and `except` compound statements. Spread them across multiple lines.
  - The AI MUST prefer surrounding multiline expressions with parentheses over using the `\` line continuation character.
- **Imports**:
  - The AI MUST place all `import` statements at the top of the file.
  - The AI MUST use absolute import paths over relative paths (e.g., `from bar import foo` instead of `import foo`). If relative imports are unavoidable, the AI MUST use explicit syntax (`from . import foo`).
  - The AI MUST group imports in three alphabetical sections: standard library modules, third-party modules, and your own modules.

## 3. String and Byte Management
- The AI MUST distinctly separate the usage of `bytes` (sequences of 8-bit values) and `str` (sequences of Unicode code points).
- The AI MUST NOT attempt to concatenate (`+`), compare (`<`, `>`, `==`), or format (`%`) `bytes` instances with `str` instances.
- The AI MUST employ the "Unicode sandwich" pattern: convert `bytes` to `str` (using `.decode()`) at the furthest boundary of interfaces, operate internally strictly on `str`, and convert back to `bytes` (using `.encode()`) upon output.
- The AI MUST explicitly use binary mode (`'rb'` or `'wb'`) when opening files to read/write binary data.
- The AI MUST explicitly pass the `encoding` parameter (e.g., `encoding='utf-8'`) when opening files to read/write Unicode data to prevent system-default encoding bugs.

## 4. String Formatting
- The AI MUST use interpolated f-strings (`f'{variable}'`) for string formatting.
- The AI MUST NOT use C-style format strings (`%s`, `%d`) due to type conversion incompatibilities, readability issues with long tuples, and dictionary verbosity.
- The AI MUST NOT use the `str.format()` method, as it shares the verbosity drawbacks of C-style formatting.
- The AI MUST utilize f-string inline expression capabilities to format and modify data concurrently (e.g., `f'{item.title():<10s} = {round(count)}'`).

## 5. Expression Complexity
- The AI MUST NOT write dense, complex single-line expressions (e.g., using boolean `or` and `and` evaluation hacks like `my_values.get('key', [''])[0] or 0`).
- The AI MUST use `if/else` ternary conditional expressions for simple logic.
- The AI MUST extract complex logic into separate, well-named helper functions, especially if the logic is reused. Follow the DRY (Don't Repeat Yourself) principle.

## 6. Multiple Assignment Unpacking
- The AI MUST prefer multiple assignment unpacking over explicit numeric indexing to extract values from tuples, lists, or dictionary items.
- The AI MUST use unpacking to swap variables in-place without temporary variables (e.g., `a[i-1], a[i] = a[i], a[i-1]`).
- The AI MUST use unpacking within the target list of `for` loops (e.g., `for rank, (name, calories) in enumerate(snacks):`).

## 7. Looping over Iterables
- The AI MUST use the `enumerate()` built-in function when iterating over a data structure and an index is simultaneously required.
- The AI MUST NOT loop over a sequence using `range(len(sequence))` and subsequent array indexing.
- The AI MUST utilize the second parameter of `enumerate(iterable, start)` if the index count needs to begin at a number other than zero (e.g., `1`).
- The AI MUST use the `zip()` built-in function to iterate over two or more iterators in parallel instead of indexing them manually.
- The AI MUST use `itertools.zip_longest()` if the iterators passed to parallel processing might be of unequal lengths and truncation is unacceptable.

## 8. Anti-Patterns to Avoid
- The AI MUST NOT use `else` blocks immediately following `for` or `while` loop interior blocks. The AI MUST extract the loop into a helper function and use early `return` statements or flag variables to represent the target logic.

## 9. Assignment Expressions (Walrus Operator)
- The AI MUST use the walrus operator (`:=`) to assign a value to a variable and evaluate it simultaneously when an expression is repeated.
- The AI MUST use assignment expressions in `if` and `elif` blocks to avoid noisy variable assignments immediately preceding the conditional check.
- The AI MUST wrap assignment expressions in parentheses when they are subexpressions of larger expressions (e.g., `if (count := fruit.get('apple', 0)) >= 4:`).
- The AI MUST use assignment expressions to replace the "loop-and-a-half" idiom (infinite `while True:` loop with an internal `if not var: break` statement). 

# @Workflow
1. **Validation**: Check if the requested Python script logic requires parsing/handling I/O. If so, implement the "Unicode sandwich" pattern (`bytes`/`str` separation). Ensure file access explicitly declares binary/text modes and encodings.
2. **Structuring**: Lay out the necessary classes and functions. Ensure two blank lines between functions/classes and one blank line between methods. 
3. **Implementation (Logic)**: 
   - Write the core logic avoiding deep single-line expressions. Break complex boolean math or dictionary/list extractions into multi-line `if/else` statements or distinct helper functions.
   - If swapping variables, use tuple unpacking.
   - If looping and an index is needed, use `enumerate`.
   - If looping multiple lists, use `zip`.
4. **Refactoring (Optimization)**:
   - Scan the generated code for any C-style (`%`) or `.format()` strings. Convert all to f-strings.
   - Scan for variable assignments that are exclusively used to test a condition immediately afterward. Combine them using the `:=` walrus operator.
   - Scan for `for/else` or `while/else` constructs. Move the loop to a helper function utilizing an early return.
   - Scan for manual list indexing (`obj[0]`, `obj[1]`). Replace with multiple assignment unpacking.
5. **PEP 8 Compliance Check**: Review line lengths (max 79 chars), indentation (4 spaces), naming conventions, and import sorting before finalizing output.

# @Examples (Do's and Don'ts)

### String Formatting
[DON'T]
```python
old_style = '#%d: %-10s = %d' % (i + 1, item.title(), round(count))
new_style = '#{}: {:<10s} = {}'.format(i + 1, item.title(), round(count))
```
[DO]
```python
f_string = f'#{i+1}: {item.title():<10s} = {round(count)}'
```

### Complex Expressions vs Helper Functions
[DON'T]
```python
red = int(my_values.get('red', [''])[0] or 0)
```
[DO]
```python
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

red = get_first_int(my_values, 'red')
```

### Indexing vs Unpacking
[DON'T]
```python
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name} has {calories} calories')
```
[DO]
```python
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} has {calories} calories')
```

### Iterating Sequences (enumerate / zip)
[DON'T]
```python
for i in range(len(names)):
    count = counts[i]
    if count > max_count:
        longest_name = names[i]
        max_count = count
```
[DO]
```python
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count
```

### Else Blocks After Loops
[DON'T]
```python
for i in range(2, min(a, b) + 1):
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')
```
[DO]
```python
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True
```

### Assignment Expressions (Walrus Operator)
[DON'T]
```python
count = fresh_fruit.get('banana', 0)
if count >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
else:
    count = fresh_fruit.get('apple', 0)
    if count >= 4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get('lemon', 0)
        if count:
            to_enjoy = make_lemonade(count)
        else:
            to_enjoy = 'Nothing'
```
[DO]
```python
if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('apple', 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get('lemon', 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = 'Nothing'
```

### Loop-and-a-Half Anti-Pattern
[DON'T]
```python
while True:
    fresh_fruit = pick_fruit()
    if not fresh_fruit:
        break
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
```
[DO]
```python
while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
```