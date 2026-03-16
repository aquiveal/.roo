# @Domain
Parsing, validating, and modeling dynamic or external data (e.g., from configuration files, network requests, databases, JSON, YAML) in Python codebases where static typechecking is insufficient to guarantee runtime data integrity.

# @Vocabulary
- **Validation Logic**: Complex, sprawling procedural code (nested `if` statements) historically used to verify data integrity. To be avoided in favor of declarative models.
- **Pydantic**: A Python parsing and validation library that enforces type hints at runtime, throwing a `ValidationError` when data is malformed.
- **Constrained Types**: Built-in pydantic types (e.g., `constr`, `PositiveInt`, `conlist`) that enforce boundary limits (length, size, regular expressions) declaratively.
- **Custom Validator**: A class method decorated with `@validator` used to enforce complex, interdependent, or domain-specific business logic on model fields.
- **Parsing vs. Validation**: Pydantic's default behavior is parsing (coercing data, such as string `"123"` to integer `123`) rather than strict validation.
- **Strict Fields**: Pydantic types like `StrictInt` that disable automatic type coercion, forcing an exact type match.

# @Objectives
- Shift errors left by catching invalid external data immediately at the injection point (runtime), rather than later in the application's execution.
- Maximize readability by replacing sprawling procedural validation logic with declarative data models.
- Provide strong, documented guarantees about the structure and validity of data coming out of data sources.

# @Guidelines
- When reading data from external sources (YAML, JSON, APIs), the AI MUST NOT rely solely on static type annotations like `TypedDict`, as they provide zero runtime validation.
- The AI MUST use `pydantic` to model data that requires runtime validation.
- The AI MUST define models using `pydantic.dataclasses.dataclass` (or inherit from `pydantic.BaseModel`) to ensure validation occurs upon object construction.
- The AI MUST NOT write manual `if`-based validation for basic properties (length, bounds, regex matching). Instead, the AI MUST use Pydantic's built-in constrained types (e.g., `constr(min_length=1)`, `PositiveInt`, `conlist(min_items=2)`).
- For complex validation logic (e.g., checking if a list of employees contains at least one specific role), the AI MUST use the `@validator` decorator.
- When writing custom validators, the AI MUST raise a `ValueError` if the data violates the defined business constraints.
- The AI MUST evaluate whether implicit type coercion is safe for the specific domain. If exact type matching is strictly required (e.g., rejecting the string `"123"` when an `int` is expected), the AI MUST use Pydantic's strict fields (e.g., `StrictInt`).
- The AI MUST handle or expect `pydantic.error_wrappers.ValidationError` when constructing models with external data.

# @Workflow
1. **Identify Vulnerable Injection Points**: Locate areas where external data enters the system (e.g., `yaml.safe_load()`, `json.loads()`).
2. **Define the Model**: Create a class representing the expected data structure and decorate it with `@dataclass` from `pydantic.dataclasses`.
3. **Apply Constrained Types**: Analyze the fields and replace standard Python types with Pydantic constrained types (`constr`, `conlist`, `PositiveInt`) to enforce basic data boundaries (e.g., string lengths, list sizes).
4. **Implement Custom Validators**: Identify interdependent constraints or complex business rules. Implement these as class methods decorated with `@validator('field_name')`, raising `ValueError` on failure.
5. **Enforce Strictness**: Review the model for fields where type coercion (parsing) could introduce bugs (e.g., truncating floats to ints). Replace standard types with Strict types (e.g., `StrictInt`) where necessary.
6. **Construct and Catch**: Pass the raw dictionary data into the Pydantic model (e.g., `Model(**data)`). Ensure the application is prepared to surface the resulting `ValidationError` if the data is invalid.

# @Examples (Do's and Don'ts)

### External Data Modeling
[DO] Use pydantic dataclasses for external data to ensure runtime validation.
```python
from pydantic.dataclasses import dataclass

@dataclass
class Dish:
    name: str
    price_in_cents: int
    description: str

def load_dish(data: dict) -> Dish:
    return Dish(**data) # Validates at runtime
```

[DON'T] Use `TypedDict` for external data, as it allows invalid data to pass silently at runtime.
```python
from typing import TypedDict

class Dish(TypedDict):
    name: str
    price_in_cents: int
    description: str

def load_dish(data: dict) -> Dish:
    return data # No runtime validation occurs! Invalid data causes bugs later.
```

### Basic Constraints
[DO] Use Pydantic's constrained types to declaratively enforce data boundaries.
```python
from pydantic.dataclasses import dataclass
from pydantic import constr, PositiveInt, conlist

@dataclass
class Restaurant:
    name: constr(regex=r'^[a-zA-Z0-9 ]*$', min_length=1, max_length=16)
    number_of_seats: PositiveInt
    dishes: conlist(Dish, min_items=3)
```

[DON'T] Write procedural validation logic in `__init__` or standalone functions.
```python
@dataclass
class Restaurant:
    name: str
    number_of_seats: int
    dishes: list

    def __post_init__(self):
        if not (1 <= len(self.name) <= 16):
            raise ValueError("Name too long")
        if self.number_of_seats <= 0:
            raise ValueError("Seats must be positive")
        if len(self.dishes) < 3:
            raise ValueError("Must have at least 3 dishes")
```

### Complex Business Logic
[DO] Use the `@validator` decorator for complex, interdependent constraints.
```python
from pydantic import validator
from pydantic.dataclasses import dataclass

@dataclass
class Restaurant:
    employees: list[Employee]

    @validator('employees')
    def check_chef_and_server(cls, employees):
        if (any(e for e in employees if e.position == 'Chef') and 
            any(e for e in employees if e.position == 'Server')):
            return employees
        raise ValueError('Must have at least one chef and one server')
```

[DON'T] Leave complex validation up to the consumer of the class.
```python
@dataclass
class Restaurant:
    employees: list[Employee]

# Bad: Forcing caller to validate
def process_restaurant(restaurant: Restaurant):
    if not has_chef_and_server(restaurant.employees):
        raise ValueError("Invalid employees")
```

### Strict Parsing vs Validation
[DO] Use strict fields when implicit data coercion is dangerous or undesirable.
```python
from pydantic.dataclasses import dataclass
from pydantic import StrictInt

@dataclass
class Model:
    value: StrictInt

# Model(value="123") will raise a ValidationError
```

[DON'T] Use standard types if you want to strictly reject coerced types.
```python
from pydantic.dataclasses import dataclass

@dataclass
class Model:
    value: int

# Model(value="123") silently coerces to integer 123
# Model(value=5.5) silently truncates to integer 5
```