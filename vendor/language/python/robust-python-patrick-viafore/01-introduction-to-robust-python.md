@Domain
This rule file is triggered whenever the AI is developing, refactoring, reviewing, or analyzing Python code. It specifically applies to tasks requiring data structure selection, iteration design, API signature creation, and general code maintainability improvements.

@Vocabulary
- **Robustness**: A codebase that is resilient and error-free in spite of constant change. Robust code is flexible (like a willow tree bending in the wind), not rigid (like a bar of iron).
- **Clean Code**: Code that expresses its intent clearly and concisely, strictly in that order. It avoids clever tricks that hinder readability.
- **Maintainable Code**: Code designed proactively for future developers, making tasks like fixing bugs or extracting libraries frictionless.
- **Asynchronous Communication**: The transfer of information across time and space. Source code is the primary "low cost, low proximity" asynchronous communication tool used to convey intent to future maintainers.
- **Static Indexing**: Using a constant literal to index into a collection (e.g., `my_list[4]`).
- **Dynamic Indexing**: Indexing into a collection using a variable that is unknown until runtime.
- **Pythonic**: Code written in an idiomatic style that emphasizes simplicity and is instantly recognizable to most Python developers.
- **Law of Least Surprise (Law of Least Astonishment)**: A program and its code should always respond in the way that astonishes the reader the least.
- **Necessary Complexity**: Complexity that is inherently required by the problem domain (e.g., deep learning models).
- **Accidental Complexity**: Superfluous, wasteful, or confusing statements born from organic growth rather than deliberate design (e.g., adding a simple command-line option requiring changes across 10 files).

@Objectives
- Ensure every line of code explicitly communicates its intent to future developers through the deliberate selection of types, collections, and iteration constructs.
- Construct software using the simplest possible method so that there are obviously no deficiencies, rather than making it so complicated that there are no obvious deficiencies.
- Treat the codebase as the ultimate asynchronous communication medium, prioritizing readability and discoverability over short-term coding speed.
- Eliminate accidental complexity entirely while isolating and encapsulating necessary complexity.

@Guidelines
- **General Intent & Design**
  - The AI MUST prioritize clarity over conciseness, and conciseness over cleverness.
  - The AI MUST encapsulate abstract concepts into explicit user-defined types (e.g., custom classes) rather than relying on positional data in lists or tuples.
  - The AI MUST NEVER surprise future maintainers. If a block of code requires a surprising workaround, the AI MUST add an explicit comment explaining *why* the code is written that way.
- **Collection Selection**
  - The AI MUST select collections based on the exact behavioral intent:
    - Use `list` ONLY for mutable collections that will be iterated over and may contain duplicates.
    - Use `tuple` for immutable, fixed-size collections where elements are extracted via indices or unpacking, and iteration is rare.
    - Use `set` to explicitly communicate that a collection contains absolutely no duplicates and order does not matter.
    - Use `frozenset` to explicitly communicate an immutable set.
    - Use `dict` for mapping unique keys to values.
    - Use `generator` for collections that are computationally expensive or infinite, communicating that evaluation is lazy.
    - Use `collections.Counter` when the sole intent is to count the occurrences of elements.
    - Use `collections.defaultdict` to communicate that missing keys intrinsically have a fallback default value.
- **Indexing Rules**
  - The AI MUST NOT use static indexing on `list` or `dict` objects UNLESS fulfilling one of these specific exceptions:
    1. Getting the first (`[0]`) or last (`[-1]`) element of a sequence.
    2. Using a dictionary as an intermediate data type (e.g., parsing JSON/YAML).
    3. Operating on sequences in fixed chunks (e.g., always splitting after the third element).
    4. Explicit, proven performance optimizations.
  - The AI MUST use dynamic indexing when accessing lists and dictionaries in all other scenarios.
  - The AI MUST freely use static indexing for `tuple` objects, as they have a fixed size and structure.
- **Iteration Constructs**
  - The AI MUST use `for` loops ONLY for iterating over a collection or range to perform an action or side effect.
  - The AI MUST use `while` loops ONLY for iterating as long as a certain condition remains true. The AI MUST NOT use `while` loops with manual index increments to iterate over a sequence.
  - The AI MUST use list/dict/set `comprehensions` ONLY for transforming one collection into another. The AI MUST NOT use comprehensions if the loop block contains side effects.
  - The AI MUST use `recursion` ONLY when the substructure of a collection is identical to the main structure (e.g., trees).

@Workflow
1. **Analyze Intent**: Before writing or refactoring code, evaluate what real-world concept the code represents. Identify the necessary complexity and plan to isolate it.
2. **Type Replacement**: If the code uses generic types (like a list where the first element is a special value and the rest are tuples), abstract this into a dedicated Class or Type (e.g., converting `recipe[0]` to `recipe.servings`).
3. **Select Collections**: Map the data requirements (mutability, uniqueness, mapping, laziness) strictly to the allowed Python collections (`list`, `set`, `tuple`, `dict`, `Counter`, `generator`).
4. **Select Iteration**: Determine if the loop transforms data (use comprehension), applies side-effects (use `for`), or waits on a condition (use `while`).
5. **Implement and Verify**: Write the code without "clever" hacks. Review the code against the Law of Least Surprise. If the implementation is not immediately obvious to a visual inspection, rewrite it or add an asynchronous communication tool (a highly descriptive comment).

@Examples (Do's and Don'ts)

**Principle: Communicating Intent via Types**
- [DO] 
```python
def adjust_recipe(recipe: Recipe, servings: int) -> Recipe:
    new_ingredients = list(recipe.get_ingredients())
    recipe.clear_ingredients()
    for ingredient in new_ingredients:
        ingredient.adjust_proportion(Fraction(servings, recipe.servings))
    return Recipe(servings, new_ingredients)
```
- [DON'T] (Relies on implicit positional data and mutating variables)
```python
def adjust_recipe(recipe, servings):
    new_recipe = [servings]
    old_servings = recipe[0]
    factor = servings / old_servings
    recipe.pop(0)
    while recipe:
        ingredient, amount, unit = recipe.pop(0)
        new_recipe.append((ingredient, amount * factor, unit))
    return new_recipe
```

**Principle: Selecting the Correct Collection for Counting**
- [DO]
```python
from collections import Counter

def create_author_count_mapping(cookbooks: list[Cookbook]):
    return Counter(book.author for book in cookbooks)
```
- [DON'T] (Uses the wrong collection and requires boilerplate)
```python
def create_author_count_mapping(cookbooks: list[Cookbook]):
    counter = {}
    for cookbook in cookbooks:
        if cookbook.author not in counter:
            counter[cookbook.author] = 0
        counter[cookbook.author] += 1
    return counter
```

**Principle: Iteration Selection**
- [DO] (Using a `for` loop for sequence side-effects)
```python
for character in text:
    print(character)
```
- [DON'T] (Using a `while` loop with a manual index for sequence iteration)
```python
index = 0
while index < len(text):
    print(text[index])
    index += 1
```

**Principle: Transformations via Comprehension**
- [DO]
```python
authors = [cookbook.author for cookbook in cookbooks]
```
- [DON'T] (Using a `for` loop with side-effect appends just to transform a collection)
```python
authors = []
for cookbook in cookbooks:
    authors.append(cookbook.author)
```