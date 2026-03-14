@Domain
Triggered when writing, reviewing, or refactoring Python code. Specifically targeting modern Python 3 development (3.7/3.8+) and prioritizing the idiomatic "Pythonic" style defined by community conventions.

@Vocabulary
- **Pythonic**: The idiomatic style of writing Python that has emerged from the community, preferring explicitness, simplicity, and maximum readability.
- **PEP 8**: Python Enhancement Proposal #8; the official standard style guide for formatting Python code.
- **Unicode Sandwich**: An architectural pattern where Unicode data is encoded/decoded at the furthest boundary of an interface, while the core program strictly operates on `str` types containing Unicode data.
- **F-Strings**: Interpolated format strings (prefixed with an `f`), which evaluate arbitrary Python expressions directly within format specifiers, solving the verbosity and error-prone nature of older formatting methods.
- **Unpacking**: Python's generalized syntax for assigning multiple values from any iterable into discrete variables in a single statement, avoiding explicit indexing.
- **Walrus Operator (`:=`)**: An assignment expression that both assigns a value to a variable and evaluates to that value simultaneously, useful for preventing repetitive computations in conditional logic.

@Objectives
- Exclusively utilize modern Python 3 features and deprecate all Python 2 methodologies.
- Strictly enforce PEP 8 styling, naming, and structural guidelines to maximize code clarity and maintainability.
- Minimize visual noise and indexing operations by using unpacking, `enumerate`, and `zip`.
- Eliminate complex, single-line Boolean tricks; favor readable helper functions and assignment expressions (`:=`).
- Guarantee robust character encoding by explicitly managing boundaries between `bytes` (binary) and `str` (Unicode text).

@Guidelines
- **Item 1: Python Version Restrictions**
  - Always write code targeted at Python 3. Do not include Python 2 compatibility shims, legacy syntax, or backports.

- **Item 2: PEP 8 Conformity**
  - **Whitespace**: Use spaces instead of tabs. Use 4 spaces per indentation level. Keep lines at or below 79 characters. Indent continued multiline expressions by 4 extra spaces. Separate functions/classes by 2 blank lines, and methods by 1 blank line. In dictionaries, omit whitespace before the colon, and put a single space after it. Put exactly one space before and after the `=` operator. For type annotations, put no space before the colon and one space after.
  - **Naming**: Functions/variables/attributes must be `lowercase_underscore`. Protected instance attributes must be `_leading_underscore`. Private instance attributes must be `__double_leading_underscore`. Classes/Exceptions must be `CapitalizedWord`. Module-level constants must be `ALL_CAPS`. Use `self` for instance methods and `cls` for class methods as the first parameter.
  - **Expressions**: Use inline negation (`if a is not b`). Check empty/non-empty sequences using implicit boolean evaluations (`if not somelist` or `if somelist`). Never compare the length of a sequence to zero. Avoid single-line `if`, `for`, `while`, or `except` statements. Use parentheses to surround multiline expressions instead of using the `\` line continuation character.
  - **Imports**: Place all imports at the top of the file. Prefer absolute module names (`from bar import foo`), but explicit relative imports (`from . import foo`) are acceptable when necessary. Group imports in order: 1. standard library, 2. third-party modules, 3. own modules. Alphabetize within subsections.

- **Item 3: Bytes vs. Str**
  - Treat `bytes` (raw 8-bit values) and `str` (Unicode code points) as strictly incompatible. Never mix them using operators (`>`, `==`, `+`, `%`).
  - Implement the "Unicode Sandwich" by converting input boundaries immediately to `str`, operating strictly on `str`, and encoding to `bytes` only at the output boundary.
  - When opening file handles, always use explicitly binary modes (`'rb'`, `'wb'`) for binary data. For text modes (`'r'`, `'w'`), always explicitly pass the `encoding` parameter (e.g., `encoding='utf-8'`) to avoid relying on unpredictable system defaults.

- **Item 4: F-Strings Over C-Style and str.format**
  - Do not use C-style formatting (`%s`) or the `str.format()` method. Both introduce verbosity, repetition, and type incompatibility risks.
  - Always use f-strings (`f'{var}'`) to format text. Embed Python expressions directly inside f-string braces to reduce visual noise (e.g., `f'{item.title():<10s} = {round(count)}'`).

- **Item 5: Helper Functions Over Complex Expressions**
  - Do not use dense, single-line boolean logic tricks (e.g., relying on `or` / `and` to fall back to default values, like `my_dict.get('key', [''])[0] or 0`).
  - Move complex inline expressions into standalone helper functions containing full `if/else` statements.
  - For simpler conditions, use the if/else ternary expression (`a if b else c`), but extract to a function if reused or if visual noise increases.

- **Item 6: Multiple Assignment Unpacking Over Indexing**
  - Avoid accessing items in a tuple or list via explicit integer indices (e.g., `item[0]`).
  - Use unpacking to extract variables (`first, second = item`).
  - Use unpacking to swap variables in place without temporary variables (`a, b = b, a`).
  - Use unpacking directly within `for` loop targets, comprehensions, and generator expressions.

- **Item 7: Enumerate Over Range**
  - Do not loop over a sequence using `range(len(sequence))` to extract indices.
  - Always use `enumerate()` to iterate over a sequence when the loop index is required.
  - Supply the optional second argument to `enumerate()` to specify the starting integer if counting does not start at 0 (e.g., `enumerate(items, 1)`).

- **Item 8: Zip for Parallel Processing**
  - Do not use index tracking (`counts[i]`) to iterate over multiple sequences simultaneously.
  - Use the built-in `zip()` function to wrap multiple iterables, yielding tuples for parallel processing.
  - Beware that `zip()` silently truncates outputs to the shortest iterable. If differing lengths are expected, use `itertools.zip_longest()` to prevent data loss.

- **Item 9: Avoid `else` Blocks After Loops**
  - Never place an `else` block immediately following a `for` or `while` loop's interior block. Its behavior (executing only if the loop completes without hitting a `break`) is counter-intuitive and highly confusing.
  - Instead, use a helper function that returns early when a condition is met, or use an explicitly named boolean tracking variable.

- **Item 10: Assignment Expressions (Walrus Operator)**
  - Utilize the walrus operator (`:=`) to define and evaluate variables simultaneously.
  - Use `:=` in `if` or `elif` statements to prevent repeating variable lookups (e.g., dictionary fetching).
  - Use `:=` to emulate `do/while` loops and avoid the infinite "loop-and-a-half" anti-pattern (`while True: break`).
  - Surround the assignment expression with parentheses when it is a subexpression of a larger condition.

@Workflow
1. **Analyze and Upgrade**: Scan code to strip out any Python 2 patterns. Transition all string formatting to f-strings.
2. **Type and Boundary Audit**: Validate the separation between `bytes` and `str`. Enforce explicit encodings on `open()` calls.
3. **Iterative Simplification**: Scan all loops. Replace `range(len())` with `enumerate()`. Replace manual parallel indexing with `zip()`. Eradicate all instances of `for...else` and `while...else`.
4. **Refactor Indexing**: Convert all hardcoded tuple/list indices (`var[0]`, `var[1]`) into clean, multiple assignment unpacking operations.
5. **Logic De-duplication**: Identify dense, single-line boolean fallback tricks; refactor them into helper functions. Replace repetitive variable initializations just prior to an `if`/`elif` check with the walrus operator (`:=`).
6. **Format**: Format the modified code according to PEP 8 standards (spacing, indentation, implicit boolean checks, parentheses over line continuations).

@Examples (Do's and Don'ts)

**Item 2: Implicit Booleans**
- [DO]
  ```python
  if not somelist:
      handle_empty()
  ```
- [DON'T]
  ```python
  if len(somelist) == 0:
      handle_empty()
  ```

**Item 2: Multiline Expressions**
- [DO]
  ```python
  total = (first_variable
           + second_variable
           + third_variable)
  ```
- [DON'T]
  ```python
  total = first_variable \
          + second_variable \
          + third_variable
  ```

**Item 3: Bytes vs Str and File Handles**
- [DO]
  ```python
  with open('data.bin', 'wb') as f:
      f.write(b'\xf1\xf2\xf3')

  with open('text.txt', 'r', encoding='utf-8') as f:
      text = f.read()
  ```
- [DON'T]
  ```python
  with open('data.bin', 'w') as f:
      f.write(b'\xf1\xf2\xf3')  # Breaks due to text-mode expecting str

  with open('text.txt', 'r') as f:
      text = f.read()  # Relies on unpredictable system default encoding
  ```

**Item 4: F-Strings vs C-Style**
- [DO]
  ```python
  formatted = f'#{i+1}: {item.title():<10s} = {round(count)}'
  ```
- [DON'T]
  ```python
  formatted = '#%d: %-10s = %d' % (i + 1, item.title(), round(count))
  ```

**Item 5: Helper Functions vs Complex Expressions**
- [DO]
  ```python
  def get_first_int(values, key, default=0):
      found = values.get(key, [''])
      if found[0]:
          return int(found[0])
      return default

  red = get_first_int(my_values, 'red')
  ```
- [DON'T]
  ```python
  red = int(my_values.get('red', [''])[0] or 0)
  ```

**Item 6: Unpacking vs Indexing**
- [DO]
  ```python
  for rank, (name, calories) in enumerate(snacks, 1):
      print(f'#{rank}: {name} has {calories} calories')

  a[i-1], a[i] = a[i], a[i-1]
  ```
- [DON'T]
  ```python
  for i in range(len(snacks)):
      item = snacks[i]
      name = item[0]
      calories = item[1]
      print(f'#{i+1}: {name} has {calories} calories')

  temp = a[i]
  a[i] = a[i-1]
  a[i-1] = temp
  ```

**Item 7: Enumerate vs Range/Len**
- [DO]
  ```python
  for i, flavor in enumerate(flavor_list, 1):
      print(f'{i}: {flavor}')
  ```
- [DON'T]
  ```python
  for i in range(len(flavor_list)):
      flavor = flavor_list[i]
      print(f'{i + 1}: {flavor}')
  ```

**Item 8: Zip for Parallel Processing**
- [DO]
  ```python
  for name, count in zip(names, counts):
      if count > max_count:
          longest_name = name
          max_count = count
  ```
- [DON'T]
  ```python
  for i in range(len(names)):
      count = counts[i]
      if count > max_count:
          longest_name = names[i]
          max_count = count
  ```

**Item 9: Avoid Loop Else Blocks**
- [DO]
  ```python
  def coprime(a, b):
      for i in range(2, min(a, b) + 1):
          if a % i == 0 and b % i == 0:
              return False
      return True
  ```
- [DON'T]
  ```python
  for i in range(2, min(a, b) + 1):
      if a % i == 0 and b % i == 0:
          print('Not coprime')
          break
  else:
      print('Coprime')
  ```

**Item 10: Walrus Operator for Repetition**
- [DO]
  ```python
  if (count := fresh_fruit.get('apple', 0)) >= 4:
      make_cider(count)
  else:
      out_of_stock()

  # Do/While emulation
  while fresh_fruit := pick_fruit():
      make_juice(fresh_fruit)
  ```
- [DON'T]
  ```python
  count = fresh_fruit.get('apple', 0)
  if count >= 4:
      make_cider(count)
  else:
      out_of_stock()

  # Loop and a half
  while True:
      fresh_fruit = pick_fruit()
      if not fresh_fruit:
          break
      make_juice(fresh_fruit)
  ```