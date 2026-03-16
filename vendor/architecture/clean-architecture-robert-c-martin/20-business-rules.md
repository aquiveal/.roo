# @Domain
These rules MUST be activated whenever the AI is tasked with designing, implementing, modifying, or refactoring business logic, domain models, application core features, entities, or use cases. They also apply when decoupling application logic from databases, user interfaces (UIs), or third-party frameworks.

# @Vocabulary
*   **Critical Business Rules:** Rules or procedures that make or save the business money, irrespective of whether they are implemented on a computer or executed manually.
*   **Critical Business Data:** The core data required by the Critical Business Rules to operate.
*   **Entity:** An object or software module that encapsulates a small set of Critical Business Rules operating on Critical Business Data. 
*   **Use Case:** An object or description containing application-specific business rules that specify how and when an automated system operates. It orchestrates the "dance of the Entities."
*   **Request and Response Models:** Simple, framework-independent data structures used exclusively to pass input data into a Use Case and output data out of a Use Case.
*   **Tramp Data:** Extraneous data passed through a system simply because objects (like Entities) were heavily coupled to request/response models.

# @Objectives
*   Keep the business rules pristine, unsullied by baser concerns such as user interfaces, databases, or third-party frameworks.
*   Establish a rigid dependency hierarchy enforcing the Dependency Inversion Principle: Lower-level application rules (Use Cases) depend on higher-level generalizations (Entities), while Entities depend on absolutely nothing.
*   Isolate the core business domain from external volatility by enforcing strict boundaries using simple, independent Request and Response models.

# @Guidelines
*   **Entity Construction:** The AI MUST encapsulate Critical Business Data and Critical Business Rules together into `Entity` objects or modules.
*   **Entity Purity:** The AI MUST NOT allow Entities to contain dependencies on databases, user interfaces, or third-party frameworks. Entities MUST be plain, standalone objects representing pure business logic.
*   **Use Case Responsibilities:** The AI MUST implement `Use Case` objects to define application-specific business rules. Use Cases MUST solely orchestrate the retrieval, validation, and interaction of Entities.
*   **I/O Agnosticism:** The AI MUST ensure Use Cases have zero knowledge of how data is communicated to the user or stored. Use Cases MUST NOT contain SQL, HTML, or routing logic.
*   **Dependency Direction:** The AI MUST enforce that Entities have absolutely no knowledge of the Use Cases that control them. Use Cases MUST depend on Entities; Entities MUST NEVER depend on Use Cases.
*   **Request/Response Models:** The AI MUST use simple data structures to pass data into and out of Use Cases.
*   **Framework Independence in Models:** The AI MUST NOT use standard framework interfaces (e.g., `HttpRequest`, `HttpResponse`) as input or output structures for Use Cases.
*   **Entity Segregation in Models:** The AI MUST NOT include references to `Entity` objects within Request or Response models. Tying them together violates the Common Closure Principle (CCP) and the Single Responsibility Principle (SRP). The AI MUST manually map data between Entities and Response Models.

# @Workflow
1.  **Analyze the Domain:** Evaluate the requirement to separate Critical Business Rules (rules that exist even without a computer system) from application-specific business rules (rules defining the automated system's constraints).
2.  **Define Entities:** Group the Critical Business Data and Critical Business Rules into an `Entity`. Verify that this Entity requires no external imports related to I/O, web, or persistence.
3.  **Define Request/Response Models:** Create simple data structures (`RequestModel` and `ResponseModel`) consisting only of primitive types or simple data bags. Ensure neither structure references the `Entity`.
4.  **Construct the Use Case:** Create a `UseCase` class/module that accepts the `RequestModel`.
5.  **Orchestrate:** Inside the Use Case, retrieve the necessary state, invoke the Critical Business Rules on the relevant `Entity` objects, and compute the result. 
6.  **Map and Return:** Map the resultant data from the `Entity` into the `ResponseModel` and return it.
7.  **Audit Dependencies:** Perform a final check to ensure the Dependency Inversion Principle is intact: I/O Delivery -> Use Case -> Entity.

# @Examples (Do's and Don'ts)

## Entity Design
*   **[DO]** Create an Entity as a plain object focused strictly on business calculations and state.
    ```java
    public class Loan {
        private double balance;
        private double interestRate;

        public Loan(double balance, double interestRate) {
            this.balance = balance;
            this.interestRate = interestRate;
        }

        public double calculateMonthlyPayment() {
            // Pure Critical Business Rule calculation
            return (balance * interestRate) / 12;
        }
    }
    ```
*   **[DON'T]** Mix database or framework concerns into the Entity.
    ```java
    import javax.persistence.Entity;
    import javax.persistence.Table;

    @Entity
    @Table(name = "loans")
    public class Loan extends ActiveRecord {
        // Anti-pattern: The Entity now depends on a database framework.
        public void saveToDatabase() {
            this.save(); 
        }
    }
    ```

## Use Case Implementation
*   **[DO]** Use independent data structures for Use Case boundaries and orchestrate the Entity.
    ```java
    public class CalculateLoanPaymentUseCase {
        public LoanPaymentResponse execute(LoanPaymentRequest request) {
            // 1. Application-specific validation
            if (request.creditScore < 500) {
                throw new LowCreditScoreException();
            }
            
            // 2. Orchestrate the Entity
            Loan loan = new Loan(request.balance, request.interestRate);
            double payment = loan.calculateMonthlyPayment();
            
            // 3. Map to independent Response Model
            return new LoanPaymentResponse(payment);
        }
    }
    ```
*   **[DON'T]** Pass web-specific objects into the Use Case or leak HTML/SQL logic.
    ```java
    public class CalculateLoanPaymentUseCase {
        // Anti-pattern: Use case depends on the web framework (HttpRequest)
        public void execute(HttpRequest request, HttpResponse response) {
            double balance = Double.parseDouble(request.getParameter("balance"));
            // Anti-pattern: SQL inside the use case
            database.executeSql("INSERT INTO logs (action) VALUES ('loan_calc')");
            response.write("<html><body>Payment Calculated</body></html>");
        }
    }
    ```

## Request and Response Models
*   **[DO]** Create plain data structures that decouple the Use Case from both the UI and the Entity.
    ```java
    public class LoanPaymentResponse {
        public final double monthlyPayment;
        
        public LoanPaymentResponse(double monthlyPayment) {
            this.monthlyPayment = monthlyPayment;
        }
    }
    ```
*   **[DON'T]** Embed the Entity inside the Request or Response model.
    ```java
    public class LoanPaymentResponse {
        // Anti-pattern: Returning the Entity object directly in the response model.
        // This couples the UI to the Critical Business Rules and invites tramp data.
        public final Loan loanEntity;
        
        public LoanPaymentResponse(Loan loanEntity) {
            this.loanEntity = loanEntity;
        }
    }
    ```