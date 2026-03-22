# @Domain

These rules MUST be triggered whenever the AI is tasked with writing, modifying, debugging, or analyzing unit tests for React applications, specifically those utilizing Jest, React Testing Library, and `@testing-library/user-event`. This includes testing pure functions, testing React components, simulating user interactions, and configuring or interpreting code coverage.

# @Vocabulary

- **Pure Function**: A function that has a consistent output value for a given set of parameter values, depends only on its parameters, and does not cause side effects or mutate its arguments.
- **Jest**: The core testing framework used to define tests, expectations, and matchers.
- **React Testing Library (RTL)**: A companion library for testing React components by rendering them to a virtual DOM and querying their elements without relying on implementation details.
- **jest-dom**: A companion library providing specialized DOM matchers (e.g., `toBeInTheDocument`, `toBeChecked`).
- **Matcher**: A method on the object returned by Jest's `expect()` function used to validate results (e.g., `toBe`, `toStrictEqual`, `toThrow`).
- **Query**: An RTL method used to select DOM elements (e.g., `getByText`, `findByRole`).
- **Query Variants**:
  - `getBy...`: Synchronous. Returns a single element. Throws an error if not found.
  - `getAllBy...`: Synchronous. Returns multiple elements. Throws an error if none found.
  - `findBy...`: Asynchronous. Returns a single element. Retries for up to 1 second. Throws if not found.
  - `findAllBy...`: Asynchronous. Returns multiple elements. Retries for up to 1 second. Throws if none found.
  - `queryBy...`: Synchronous. Returns a single element or `null` if not found. Used for asserting non-existence.
  - `queryAllBy...`: Synchronous. Returns an array of elements or an empty array if none found.
- **user-event**: An RTL companion library (`@testing-library/user-event` v14+) that simulates realistic user interactions rather than dispatching raw DOM events.
- **Code Coverage Metrics**:
  - `% Stmts`: Statement coverage (how many source code statements executed).
  - `% Branch`: Branch coverage (how many branches of conditional logic executed).
  - `% Funcs`: Function coverage (how many functions called).
  - `% Lines`: Line coverage (how many lines of source code executed).

# @Objectives

- Ensure all tests are robust, implementation-agnostic, and focus on user-centric behavior rather than internal code structure.
- Mandate the use of `@testing-library/user-event` over `fireEvent` to accurately simulate user interactions.
- Enforce strict and semantic test naming conventions.
- Guarantee the correct usage of query variants (`getBy`, `queryBy`, `findBy`) based on the synchronous or asynchronous nature of the element's appearance.
- Apply the appropriate Jest and `jest-dom` matchers based on data types and DOM assertions.

# @Guidelines

## Test Organization and Naming
- **File Placement**: The AI MUST place test files directly adjacent to the source file being tested (e.g., `src/Checklist/Checklist.test.tsx` for `src/Checklist/Checklist.tsx`).
- **File Extensions**: Use `.test.ts` for pure functions and `.test.tsx` for React components. Alternatively, `.spec.ts` or `.spec.tsx` are acceptable.
- **Test Naming Convention**: The AI MUST name tests using the exact pattern: `should {expected output / behaviour} when {input / state condition}` (e.g., `should return true when in checkedIds`).

## Matcher Selection
- **Primitives**: Use `toBe()` ONLY for primitive values (strings, numbers, booleans).
- **Objects/Arrays**: Use `toStrictEqual()` for objects and arrays to recursively check every property. NEVER use `toBe()` for objects or arrays.
- **Exceptions**: Use `toThrow()`. The AI MUST wrap the function execution inside an anonymous function within the `expect` block to properly catch exceptions (e.g., `expect(() => { myFunc(); }).toThrow('error');`).
- **Null Checks**: Combine `.not` with `.toBeNull()` to check that a variable isn't null, or use `.toBe(null)`.
- **DOM Elements**: Use `jest-dom` matchers like `toBeInTheDocument()`, `toBeChecked()`, and `toBeDisabled()` instead of checking raw HTML attributes.

## Component Querying
- Prefer querying by accessibility markers (`ByRole`, `ByLabelText`, `ByText`, `ByPlaceholderText`).
- Use `data-testid` attributes and the `getByTestId` query ONLY when other semantic queries are impossible or impractical.
- **Synchronous Elements**: Use `getBy...` to assert an element is present.
- **Non-Existent Elements**: Use `queryBy...` paired with `not.toBeInTheDocument()` to assert an element is NOT in the DOM. NEVER use `getBy...` for non-existence checks, as it will throw an error and fail the test before the assertion.
- **Asynchronous Elements**: Use `findBy...` (with `await`) for elements that appear after a delay, data fetch, or state update.

## Simulating User Interactions
- The AI MUST use `@testing-library/user-event` (v14 or later) to simulate user interactions.
- The AI MUST NOT use `fireEvent` (e.g., `fireEvent.click`, `fireEvent.mouseDown`) because it couples tests to specific DOM events rather than realistic user behavior.
- Always initialize the user simulation at the top of the test using `const user = userEvent.setup();`.
- Always `await` the interaction methods (e.g., `await user.click(element);`), and ensure the test callback is marked as `async`.

## Code Coverage
- Exclude files that do not contain logic (e.g., `types.ts`, `index.ts`) from code coverage reports to prevent false lower percentages. 
- Configure this exclusion in `package.json` under the `"jest": { "coveragePathIgnorePatterns": ["types.ts", "index.ts"] }` field.

# @Workflow

1. **Identify the Target**: Determine if the subject is a pure function or a React component.
2. **Setup the Test File**: Create the `.test.ts` or `.test.tsx` file in the exact same directory as the target file.
3. **Draft the Test Shell**: Define the test using the `should...when...` naming convention. Add the `async` keyword to the callback if user interactions or async queries are required.
4. **Arrange**: 
   - For pure functions: Prepare the arguments.
   - For components: Call `render(<TargetComponent {...props} />)`.
   - For interactions: Call `const user = userEvent.setup();`.
5. **Act**:
   - For pure functions: Call the function and capture the result.
   - For interactions: Query the element and perform the interaction via `await user.click(element);` (or similar).
6. **Assert**:
   - Query the DOM (using `getBy`, `findBy`, or `queryBy`) or evaluate the pure function result.
   - Apply the correct matcher (`toBe`, `toStrictEqual`, `toBeInTheDocument`, `toThrow`).
7. **Coverage Review**: When instructed to improve coverage, analyze the uncovered lines and write specific test cases targeting unexecuted branches, statements, or functions.

# @Examples (Do's and Don'ts)

## Object Comparison
- **[DO]**:
  ```typescript
  expect(resultObject).toStrictEqual({ name: 'Bob' });
  ```
- **[DON'T]**:
  ```typescript
  // Will fail because toBe checks object reference, not values
  expect(resultObject).toBe({ name: 'Bob' });
  ```

## Testing Exceptions
- **[DO]**:
  ```typescript
  test('should raise exception when value is invalid', () => {
    expect(() => {
      assertValueCanBeRendered(true);
    }).toThrow('value is not a string or a number');
  });
  ```
- **[DON'T]**:
  ```typescript
  test('should raise exception when value is invalid', () => {
    // Will fail because the exception is thrown before expect can catch it
    expect(assertValueCanBeRendered(true)).toThrow('value is not a string or a number');
  });
  ```

## Simulating Interactions
- **[DO]**:
  ```typescript
  import userEvent from '@testing-library/user-event';

  test('should check items when clicked', async () => {
    const user = userEvent.setup();
    render(<Checklist data={data} id="id" primary="name" secondary="role" />);
    
    const checkbox = screen.getByTestId('Checklist__input__1');
    await user.click(checkbox);
    
    expect(checkbox).toBeChecked();
  });
  ```
- **[DON'T]**:
  ```typescript
  import { fireEvent } from '@testing-library/react';

  test('should check items when clicked', () => {
    render(<Checklist data={data} id="id" primary="name" secondary="role" />);
    
    const checkbox = screen.getByTestId('Checklist__input__1');
    // DON'T use fireEvent, it couples to implementation details
    fireEvent.click(checkbox); 
    
    expect(checkbox).toBeChecked();
  });
  ```

## Checking for Non-Existence
- **[DO]**:
  ```typescript
  // queryBy returns null if not found, allowing the assertion to pass
  expect(screen.queryByText('Save')).not.toBeInTheDocument();
  ```
- **[DON'T]**:
  ```typescript
  // getBy throws an error immediately if not found, crashing the test
  expect(screen.getByText('Save')).not.toBeInTheDocument();
  
  // DON'T check against null directly using getBy
  expect(screen.getByText('Save')).toBe(null); 
  ```

## Asynchronous Queries
- **[DO]**:
  ```typescript
  // Use findBy and await it
  expect(await screen.findByText('Save')).toBeInTheDocument();
  ```
- **[DON'T]**:
  ```typescript
  // Missing await, findBy returns a Promise which will not match properly
  expect(screen.findByText('Save')).toBeInTheDocument();
  ```

## DOM Assertions
- **[DO]**:
  ```typescript
  expect(screen.getByText('Save')).toBeDisabled();
  ```
- **[DON'T]**:
  ```typescript
  expect(screen.getByText('Save').hasAttribute('disabled')).toBe(true);
  ```