# @Domain
This rule file is triggered whenever the user requests the AI to add new features to an existing system, refactor code for future growth, modify core business logic to support new workflows, resolve tight coupling/spaghetti code, or explicitly asks for implementation of the Open-Closed Principle (OCP), extensibility, or SOLID principles.

# @Vocabulary
- **Extensibility:** The property of a software system that allows new functionality to be added without modifying existing parts of the system.
- **Shotgun Surgery:** An anti-pattern where a single conceptual change spreads out in a blast pattern, requiring modifications across a wide variety of unrelated files and functions.
- **Necessary Complexity:** The intrinsic complexity inherent to the problem domain (e.g., multiple notification types, methods, and users).
- **Accidental Complexity:** Superfluous complexity introduced by poor implementation, tight coupling, and tangled dependencies.
- **Open-Closed Principle (OCP):** A software design principle stating that code should be open for extension but closed for modification.
- **Extension Points:** Specific, deliberately designed areas in the codebase (using duck typing, subtyping, protocols, or unions) where future developers can inject new functionality without altering core logic.
- **Coupling:** The degree of interdependence between software modules; highly extensible systems often introduce a shared common subsystem that acts as a central coupled mechanism.

# @Objectives
- The AI MUST design software that embraces change by enabling the addition of new features through new code rather than altering existing code.
- The AI MUST actively identify and eliminate Accidental Complexity while carefully containing Necessary Complexity.
- The AI MUST prevent Shotgun Surgery by decoupling unrelated concerns and consolidating shared logic into extensible mechanisms.
- The AI MUST pragmatically balance the flexibility of the Open-Closed Principle against the drawbacks of reduced readability and increased coupling by documenting abstractions thoroughly.

# @Guidelines

## Identifying Extensibility Smells
- When evaluating an existing codebase, the AI MUST flag code for an extensibility redesign if any of the following OCP violations are detected:
  - **The easy things are hard to do:** Simple configuration changes or additions require modifying multiple files.
  - **High estimates/Pushback:** The user indicates that adding a seemingly simple, similar feature to an existing one is taking too long or carries high risk.
  - **Large changesets:** Commits or proposed changes touch a massive number of files to implement one feature (Shotgun Surgery).

## Enforcing the Open-Closed Principle (OCP)
- The AI MUST NOT implement new variations of a feature by adding arbitrary parameters (e.g., `email: Email`, `send_to_customer: bool`, `texts: list`) to an existing core function.
- The AI MUST separate independent axes of change (e.g., What is happening vs. How it is transported vs. Who receives it) into distinct, independent types (e.g., separate Dataclasses for `Notification` and `NotificationMethod`).
- The AI MUST utilize Pythonic extension mechanisms such as duck typing, structural subtyping (Protocols), nominal subtyping (Base Classes), or Type Unions to define Extension Points.
- The AI MUST replace deeply nested, continuously growing `if/elif` blocks within core business logic with dynamic dispatch mechanisms (e.g., mapping dictionaries, polymorphism, or overloaded handler functions).

## Mitigating the Drawbacks of Extensibility
- Because extensibility introduces extra layers of abstraction that hurt readability, the AI MUST heavily document the code structure and explain the routing of the abstracted logic.
- Because extensibility introduces coupling to a shared central subsystem, the AI MUST mandate or generate a strong set of isolated tests for the new shared subsystem.
- The AI MUST apply OCP in moderation: only define extension points in areas of the codebase that are reasonably expected to change or have a proven history of churn. The AI MUST NOT over-abstract static, unchanging domain logic.

# @Workflow
When tasked with adding a new feature to an existing workflow or refactoring a brittle system, the AI MUST follow this exact algorithm:

1. **Analyze Complexity:** Separate the feature's Necessary Complexity (business rules) from its Accidental Complexity (messy implementation details).
2. **Identify OCP Violations:** Review the target functions for parameter bloat, tangled intents, and potential Shotgun Surgery.
3. **Decouple Concerns:** 
   - Extract distinct domain concepts into independent types (e.g., `@dataclass class NewSpecial`, `@dataclass class Email`).
   - Group related types using `Union` or `Protocol` to create generic type hints.
4. **Define Extension Points:** Create a unified entry function that accepts the generic type (e.g., `send_notification(notification: Notification)`) and routes it without needing to know the internal data of the implementation.
5. **Implement Dispatch/Routing:** Create specific handler functions (e.g., `send_email()`, `send_text()`) and a routing mechanism (e.g., a dictionary mapping types to users, or a factory) to connect the decoupled types.
6. **Extend (Do Not Modify):** Implement the new user request by creating new types/classes and registering them to the dispatch mechanism, ensuring the core function remains untouched.
7. **Mitigate Drawbacks:** Generate documentation explaining the abstraction layers and write tests for the newly created shared subsystem.

# @Examples (Do's and Don'ts)

## [DON'T]
Do not introduce Accidental Complexity by appending parameters and modifying existing core functions to handle new use cases. This causes Shotgun Surgery.

```python
# ANTI-PATTERN: Modifying the core function directly, adding parameters, 
# and mixing business logic with notification mechanisms.
def declare_special(
    dish: Dish, 
    start_date: datetime.datetime, 
    end_time: datetime.datetime, 
    emails: list[Email], 
    texts: list[PhoneNumber], 
    send_to_customer: bool
):
    # ... snip setup in local system ...
    
    # Tangled mechanism logic inside policy code
    for email in emails:
        send_email(email, dish)
    for text in texts:
        send_text(text, dish)
    if send_to_customer:
        notify_customer(dish)
```

## [DO]
Do decouple concerns using distinct types, Type Unions, and a shared routing mechanism so the core function remains closed to modification but open to extension.

```python
# BEST PRACTICE: Decouple intents into distinct types
@dataclass
class NewSpecial:
    dish: Dish
    start_date: datetime.datetime
    end_date: datetime.datetime

@dataclass
class IngredientsOutOfStock:
    ingredients: Set[Ingredient]

Notification = Union[NewSpecial, IngredientsOutOfStock]

@dataclass
class Text:
    phone_number: str

@dataclass
class Email:
    email_address: str

NotificationMethod = Union[Text, Email]

# Define an extensible mapping (Routing Mechanism)
users_to_notify: Dict[type, List[NotificationMethod]] = {
    NewSpecial: [Email("boss@company.org"), Text("555-2345")],
    IngredientsOutOfStock: [Email("inventory@company.org")]
}

# The routing function handles the dispatch (Extension Point)
def send_notification(notification: Notification):
    try:
        users = users_to_notify[type(notification)]
    except KeyError:
        raise ValueError("Unsupported Notification Method")
    
    for notification_method in users:
        notify(notification_method, notification)

# The core function remains pristine and closed to modification
def declare_special(dish: Dish, start_date: datetime.datetime, end_time: datetime.datetime):
    # ... snip setup in local system ...
    send_notification(NewSpecial(dish, start_date, end_time))
```