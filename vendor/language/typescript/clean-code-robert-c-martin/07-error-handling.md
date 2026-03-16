@Domain
These rules MUST be triggered whenever the AI is tasked with writing, refactoring, or reviewing error-handling logic, managing exceptions, validating input/output data, handling null values, or integrating with third-party APIs that can throw exceptions.

@Vocabulary
- **Return Code / Error Flag**: A primitive or enum value returned by a function to indicate failure, which the caller is forced to check.
- **Checked Exception**: An exception that must be explicitly declared in a method signature (e.g., Java's `throws` clause), forcing all higher-level callers to handle or declare it.
- **Unchecked Exception**: An exception that does not need to be declared in a method signature (e.g., `RuntimeException`), avoiding modifications to the calling hierarchy.
- **Open/Closed Principle (OCP)**: A principle stating that software entities should be open for extension but closed for modification.
- **Transaction Scope**: The conceptual boundary defined by a `try-catch-finally` block, ensuring the program is left in a consistent state regardless of failures inside the `try` block.
- **Exception Wrapper**: A custom class that encapsulates a third-party API to catch its multiple specific exceptions and rethrow a single, common exception type.
- **Special Case Pattern**: A design pattern where a class is created or configured to handle a special/default case, allowing the client to ignore exceptional behavior and treat the object normally.

@Objectives
- Separate business logic cleanly and completely from error-handling logic so that neither obscures the other.
- Prevent the proliferation of error-checking conditionals scattered throughout the codebase.
- Maintain the encapsulation and stability of method signatures by avoiding checked exceptions.
- Completely eliminate `NullPointerException` risks by systematically avoiding the passing and returning of `null`.
- Define exception classes based on how they will be caught and handled, rather than their origin.

@Guidelines

**Exceptions over Return Codes**
- The AI MUST NEVER use return codes, error flags, or status enums to indicate an error.
- The AI MUST throw an exception immediately upon encountering an error condition.

**Scope and Structure**
- The AI MUST write the `try-catch-finally` statement first when writing code that could throw an exception. This defines the transaction scope.
- The AI MUST ensure that the `catch` block leaves the program in a consistent state.

**Exception Types and Context**
- The AI MUST exclusively use unchecked exceptions. Checked exceptions MUST NOT be used because they break the Open/Closed Principle by forcing signature changes up the call chain.
- The AI MUST provide context with every exception thrown. The exception MUST include an informative error message mentioning the operation that failed, the type of failure, and sufficient data for logging.

**Exception Classification and Third-Party APIs**
- The AI MUST define exception classes based on the caller's needs (i.e., how the caller will handle them), not by the source of the error.
- When calling a third-party API that throws multiple exceptions, the AI MUST wrap the API in a custom class and translate the multiple exceptions into a single, common exception type.

**Normal Flow and Special Cases**
- The AI MUST NOT use exceptions to control regular business logic or "normal flow."
- The AI MUST use the Special Case Pattern (returning an object that encapsulates the default behavior) instead of throwing exceptions for missing but non-fatal data (e.g., returning a `PerDiemMealExpenses` object instead of throwing `MealExpensesNotFound`).

**Null Handling Constraints**
- The AI MUST NEVER return `null` from a method. If a collection is requested and no items exist, the AI MUST return an empty collection (e.g., `Collections.emptyList()`). For standard objects, return a Special Case object.
- The AI MUST NEVER pass `null` into a method as an argument. The AI MUST treat passing `null` as an invalid action by default. The AI MUST NOT litter methods with `if (arg == null)` checks; instead, design the system to forbid passing `null` entirely.

@Workflow
When the AI implements error handling or deals with potential failures, it MUST follow this step-by-step process:
1. **Define the Scope**: Write the `try-catch-finally` block before writing the logic that goes inside the `try`.
2. **Test the Exception**: Write a unit test that forces the code to throw the expected exception.
3. **Narrow the Exception**: Catch the most specific exception possible in the `catch` block, but rethrow it as a custom unchecked exception if necessary.
4. **Provide Context**: Ensure the thrown exception includes a descriptive string and relevant variables for logging.
5. **Wrap APIs**: If utilizing an external library that throws various exceptions, immediately create a Wrapper class. Map the external exceptions to a single custom unchecked exception.
6. **Eliminate Nulls**: Scan the method for `return null;` or passing `null`. Replace `return null` with an empty list or a Special Case object. Remove logic that passes `null` into functions.
7. **Clean up Flow**: Review the code to ensure exceptions are not being used for normal control flow. If they are, extract a Special Case object to handle the alternative flow.

@Examples (Do's and Don'ts)

**1. Using Exceptions Instead of Return Codes**
- [DON'T] Return an error code and force the caller to check it:
  ```java
  public void sendShutDown() {
      DeviceHandle handle = getHandle(DEV1);
      if (handle != DeviceHandle.INVALID) {
          if (record.getStatus() != DEVICE_SUSPENDED) {
              closeDevice(handle);
          } else {
              logger.log("Device suspended.");
          }
      } else {
          logger.log("Invalid handle.");
      }
  }
  ```
- [DO] Throw an exception, separating business logic from error handling:
  ```java
  public void sendShutDown() {
      try {
          tryToShutDown();
      } catch (DeviceShutDownError e) {
          logger.log(e);
      }
  }

  private void tryToShutDown() throws DeviceShutDownError {
      DeviceHandle handle = getHandle(DEV1);
      DeviceRecord record = retrieveDeviceRecord(handle);
      pauseDevice(handle);
      closeDevice(handle);
  }
  ```

**2. Wrapping Third-Party APIs**
- [DON'T] Catch multiple third-party exceptions directly in the business logic:
  ```java
  ACMEPort port = new ACMEPort(12);
  try {
      port.open();
  } catch (DeviceResponseException e) {
      logger.log("Device response exception", e);
  } catch (ATM1212UnlockedException e) {
      logger.log("Unlock exception", e);
  } catch (GMXError e) {
      logger.log("Device response exception", e);
  }
  ```
- [DO] Wrap the API to throw a single, common exception class:
  ```java
  public class LocalPort {
      private ACMEPort innerPort;

      public LocalPort(int portNumber) {
          innerPort = new ACMEPort(portNumber);
      }

      public void open() {
          try {
              innerPort.open();
          } catch (DeviceResponseException e) {
              throw new PortDeviceFailure(e);
          } catch (ATM1212UnlockedException e) {
              throw new PortDeviceFailure(e);
          } catch (GMXError e) {
              throw new PortDeviceFailure(e);
          }
      }
  }
  ```

**3. Defining the Normal Flow (Special Case Pattern)**
- [DON'T] Use exceptions to handle default business logic scenarios:
  ```java
  try {
      MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
      m_total += expenses.getTotal();
  } catch(MealExpensesNotFound e) {
      m_total += getMealPerDiem();
  }
  ```
- [DO] Return a Special Case object that encapsulates the default behavior:
  ```java
  // ExpenseReportDAO now returns a PerDiemMealExpenses object if no meals are found.
  MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
  m_total += expenses.getTotal();
  ```

**4. Returning Null**
- [DON'T] Return `null` when no items are found, forcing the caller to perform a null check:
  ```java
  public List<Employee> getEmployees() {
      if (noEmployeesFound) {
          return null;
      }
  }
  // Caller must do: if (employees != null) { ... }
  ```
- [DO] Return an empty collection to eliminate the null check:
  ```java
  public List<Employee> getEmployees() {
      if (noEmployeesFound) {
          return Collections.emptyList();
      }
  }
  // Caller can safely iterate: for (Employee e : employees) { ... }
  ```

**5. Passing Null**
- [DON'T] Pass `null` into methods, forcing the method to use assertions or throw new exceptions:
  ```java
  calculator.xProjection(null, new Point(12, 13)); // Leads to NullPointerException or cluttered guard clauses.
  ```
- [DO] Forbid the passing of `null` entirely. The architecture must assume `null` is an invalid parameter, preventing it from reaching method calls in the first place.