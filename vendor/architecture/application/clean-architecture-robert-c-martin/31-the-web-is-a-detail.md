# @Domain

These rules MUST be activated whenever the AI is tasked with creating, refactoring, or reviewing any system architecture, frontend-to-backend integrations, user interface (UI) layers, web controllers, or core business logic. They apply to all web applications, desktop applications, and mobile applications where a boundary must exist between the delivery mechanism (the GUI/Web) and the application's core use cases.

# @Vocabulary

- **The Web**: A mere delivery mechanism and an IO (Input/Output) device. It is a detail, not an architecture. 
- **Detail**: An element (such as the Web or GUI) that must be kept entirely separate from and external to the core business logic.
- **GUI (Graphical User Interface)**: A detail that dictates the visual and interactive presentation. The Web is classified strictly as a GUI.
- **The Dance**: The specific, chatty interaction loop between the application and the GUI (e.g., JavaScript validation, drag-and-drop, AJAX calls). This interaction is highly specific to the GUI type and cannot be easily abstracted.
- **Use Case**: A class or function representing the core business logic, executed on behalf of a user. It is defined strictly by its input data, the processing performed, and its output data.
- **Data Structure**: A plain, independent object or struct used to pass complete input values into a Use Case, and to pass resultant output values back to the UI. It MUST NOT contain any GUI or Web dependencies.
- **Device Independence**: The architectural principle that the core application (Use Cases) must operate completely unaware of the IO device (the Web/GUI) driving it.

# @Objectives

- The AI MUST treat the Web and all GUIs strictly as peripheral details, never as the central organizing principle of the architecture.
- The AI MUST protect the core business logic from arbitrary UI changes driven by trends or "marketing geniuses" by establishing rigid architectural boundaries.
- The AI MUST NOT attempt to abstract "The Dance" (the intricate back-and-forth UI interactions); instead, it MUST abstract the boundary where the UI hands off complete data to the application.
- The AI MUST achieve device independence by enforcing communication between the UI and Use Cases exclusively through plain Data Structures.

# @Guidelines

- **Isolate the Web/GUI**: The AI MUST place all Web technologies (HTTP requests, HTML, DOM manipulation, framework-specific UI bindings) behind a boundary that keeps them separate from core business logic.
- **Ignore the Pendulum of Trends**: The AI MUST NOT allow architectural decisions to be driven by short-term industry oscillations (e.g., centralizing vs. distributing computing power, server-side vs. client-side rendering). The core architecture must remain agnostic to these shifts.
- **Accept the Specificity of "The Dance"**: When writing UI code, the AI MUST handle the specific intricacies of the GUI (e.g., AJAX, specific widget behaviors) entirely within the UI layer. Do not leak these chatty interactions into the business rules.
- **Abstract at the Use Case Boundary**: The AI MUST define the boundary between the UI and the application at the exact point where the input data from the user is considered complete.
- **Enforce Data Structure Communication**: The AI MUST NOT pass raw UI/Web objects (like HTTP Requests, DOM events, or framework-specific context objects) into a Use Case. Instead, the AI MUST map these into independent Data Structures.
- **Return Independent Data**: Upon completion of a Use Case, the AI MUST return the resultant data in an independent Data Structure, leaving the UI layer responsible for translating that data into the specific format required by the Web/GUI (e.g., JSON, HTML views).
- **Expect Iteration**: The AI MUST anticipate that drawing this abstract boundary perfectly will take several iterations and MUST continuously refactor to ensure no UI details leak into the Use Cases.
- **Ensure Swap-ability**: The AI MUST write Use Cases such that the entire Web GUI could be deleted and replaced with a Console GUI or Desktop GUI without altering a single line of Use Case code.

# @Workflow

When implementing a feature that spans from the user interface to the core logic, the AI MUST follow this exact sequence:

1. **Define the Use Case Identity**: Identify the specific business function to be performed on behalf of the user, independent of how the user triggers it.
2. **Design the Input Data Structure**: Create a plain data structure (e.g., a simple DTO or struct) that represents the *complete* set of data required to execute the Use Case.
3. **Design the Output Data Structure**: Create a plain data structure that represents the *complete* result of the Use Case execution.
4. **Implement the Use Case**: Write the business logic to accept only the Input Data Structure, perform the required processing, and return the Output Data Structure. Ensure absolutely zero imports or references to Web or GUI libraries exist in this file.
5. **Implement "The Dance" (UI Layer)**: Write the Web/GUI controller to handle the chatty interactions (validation, HTTP parsing, routing).
6. **Bridge the Boundary**: In the UI layer, compile the gathered UI data into the Input Data Structure. Invoke the Use Case. Receive the Output Data Structure. Translate the Output Data Structure into the appropriate Web/GUI response (e.g., an HTTP 200 JSON response or HTML template).

# @Examples (Do's and Don'ts)

### [DO]

**Do** abstract the boundary using independent data structures, keeping the Use Case completely ignorant of the Web.

```python
# --- Core Business Logic (Completely Web-Agnostic) ---

# 1. Independent Data Structures
class CreateOrderInputData:
    def __init__(self, item_id: str, quantity: int, user_id: str):
        self.item_id = item_id
        self.quantity = quantity
        self.user_id = user_id

class CreateOrderOutputData:
    def __init__(self, order_id: str, total_price: float, status: str):
        self.order_id = order_id
        self.total_price = total_price
        self.status = status

# 2. The Use Case
class CreateOrderUseCase:
    def execute(self, input_data: CreateOrderInputData) -> CreateOrderOutputData:
        # Core business rules applied here
        total = calculate_total(input_data.item_id, input_data.quantity)
        order_id = save_order(input_data)
        return CreateOrderOutputData(order_id=order_id, total_price=total, status="SUCCESS")

# --- Web/GUI Detail (Handles "The Dance") ---

# 3. The Web Controller
from flask import request, jsonify

@app.route('/order', methods=['POST'])
def create_order():
    # Handle the Web specific "dance"
    raw_json = request.get_json()
    user_id = request.headers.get('X-User-Id')
    
    # Map to independent Data Structure
    input_data = CreateOrderInputData(
        item_id=raw_json['item_id'],
        quantity=raw_json['quantity'],
        user_id=user_id
    )
    
    # Execute Use Case
    use_case = CreateOrderUseCase()
    output_data = use_case.execute(input_data)
    
    # Map Output Data Structure back to Web specific response
    return jsonify({
        "order_id": output_data.order_id,
        "total": output_data.total_price,
        "status": output_data.status
    }), 201
```

### [DON'T]

**Don't** pass Web/GUI objects into the business logic, and **Don't** allow the Use Case to know about the HTTP request or response. This couples the application to the Web detail.

```python
# ANTI-PATTERN: Business logic coupled to the Web detail

from flask import request, jsonify, make_response

class CreateOrderUseCase:
    # DON'T pass the HTTP request object into the Use Case
    def execute(self, http_request):
        # DON'T let the Use Case parse JSON or read HTTP headers
        raw_json = http_request.get_json()
        item_id = raw_json['item_id']
        quantity = raw_json['quantity']
        user_id = http_request.headers.get('X-User-Id')
        
        # Core business rules
        total = calculate_total(item_id, quantity)
        order_id = save_order(item_id, quantity, user_id)
        
        # DON'T let the Use Case format the HTTP response
        return make_response(jsonify({
            "order_id": order_id,
            "total": total,
            "status": "SUCCESS"
        }), 201)

@app.route('/order', methods=['POST'])
def create_order():
    use_case = CreateOrderUseCase()
    # Passing the Web detail directly into the core logic
    return use_case.execute(request)
```