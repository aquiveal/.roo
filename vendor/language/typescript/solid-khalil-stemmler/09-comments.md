# @Domain
Trigger these rules whenever the AI is tasked with writing, refactoring, reviewing, or documenting source code. This applies to any programming language, particularly when the AI is asked to add comments, explain code, or improve code readability.

# @Vocabulary
- **Declarative Code**: Code that expresses its intent (the *what* and *how*) natively through expressive class, method, and variable names, eliminating the need for explanatory comments.
- **Imperative Code**: Detailed, step-by-step logic that often obscures the higher-level intent, frequently prompting developers to write "What" or "How" comments.
- **Redundant Comment**: A comment that repeats what is already explicitly clear from the code's syntax, method signature, or variable naming.
- **Log/Journal Comment**: A comment tracking the history of changes, dates, or author information within the source code.
- **Closing Brace Comment**: A comment placed at the end of a scope block (e.g., `// end of if`) to help navigate large, poorly structured code blocks.
- **Single Layer of Abstraction**: A design structure where a function or method reads like a high-level "table of contents", with all lower-level imperative details pushed downwards into respective private helper methods.

# @Objectives
- Ensure the code itself explains *What* it does and *How* it does it through declarative naming and structure.
- Restrict the use of comments exclusively to explaining *Why* a specific technical or business decision was made.
- Aggressively eliminate code clutter by removing redundant comments, commented-out code, and journal entries.
- Force the transformation of comment-reliant imperative code into self-documenting declarative code.

# @Guidelines
- **Code Explains What and How; Comments Explain Why**: The AI MUST NOT write comments to explain what a block of code is doing or how it operates. The AI MUST only write comments to explain the *Why* (e.g., performance optimizations, algorithm choices, or business-domain context that cannot be expressed via code).
- **Refactor Over Commenting**: When encountering code that is complex enough to seemingly require a comment, the AI MUST first attempt to refactor the code (e.g., extracting logic into well-named variables or functions) before resorting to writing a comment.
- **Eradicate Redundant Comments**: The AI MUST delete any comment that says something already adequately expressed by the code (e.g., `/** This method gets the user by user id */ getUserByUserId()`).
- **Eradicate Log/Journal Entries**: The AI MUST NOT generate or preserve comments describing when, what, or by whom code was changed. Version control handles this.
- **Eradicate Commented-Out Code**: The AI MUST delete any commented-out code rather than preserving it.
- **Eradicate Closing Brace Comments**: The AI MUST delete comments like `// end of inner if`. If the code requires such comments to be readable, the AI MUST refactor the block into smaller, separate functions.
- **Turn Comments into Variables/Methods**: The AI MUST translate explanatory comments that precede complex conditional statements into intermediate, descriptively named variables or private methods.
- **Maintain a Single Layer of Abstraction**: The AI MUST structure methods so they present a single level of abstraction. Complex, multi-step operations (often annotated with inline comments like `// 1. Do X`, `// 2. Do Y`) MUST be abstracted into private helper methods.

# @Workflow
1. **Analyze Code for Complexity**: Scan the target code block or feature request.
2. **Evaluate Existing Comments**: Identify all comments in the provided code. Categorize them as explaining *What*, *How*, or *Why*.
3. **Purge "Bad Comments"**: Immediately delete commented-out code, journal/log headers, redundant method descriptions, and closing brace comments.
4. **Refactor "What/How" Comments into Code**: 
   - If a comment explains a complex boolean condition, extract the condition into a variable named after the comment.
   - If a comment explains a block of imperative logic (e.g., inside a `.reduce()` or `for` loop), extract that block into a private method named after the comment.
5. **Enforce Single Layer of Abstraction**: Review the main method. Ensure it reads declaratively. Push any remaining low-level imperative details down into separate methods.
6. **Inject "Why" Comments (If Necessary)**: Only if the code implements a highly specific workaround, an unexpected algorithm (e.g., a Splay Tree for >5000 entries), or a counter-intuitive business requirement, write a concise comment explaining *Why* this approach was taken.

# @Examples (Do's and Don'ts)

### 1. Handling Complex Conditions
**[DON'T]** Use a comment to explain a complex imperative boolean check.
```typescript
// Check to see if buyer eligible for loan for property
// if the buyers credit score is greater than the minimal approval
// and the last job they were at, they were there for longer than the
// minimum employment length
// AND, their downpayment preferred value is the minimum downpayment
// based on the type of property it is,
// THEN, we will approve their loan
if (
  (buyer.creditScore >= MIN_APPROVAL_SCORE) &&
  (buyer.jobHistory.getLast().getEmploymentLength() >= MIN_EMPLOYMENT_LENGTH) &&
  (downpayment.value >= getMinimumDownpayment(property, downpaymentPercentage))
) {
  // ...
}
```

**[DO]** Refactor the comment into a declarative method or variable.
```typescript
if (buyer.isEligibleForLoan(property, downpaymentPercentage)) {
  // ...
}
```

### 2. Handling Imperative Math/Logic
**[DON'T]** Leave messy imperative code with inline comments explaining what it does.
```typescript
const _x: number = abs(x - deviceInfo.position.x) / scale;
let directionCode;
if (0 < _x & x != deviceInfo.position.x) {
  if (0 > x - deviceInfo.position.x) {
    directionCode = 0x04 /*left*/;
  } else if (0 < x - deviceInfo.position.x) {
    directionCode = 0x02 /*right*/;
  }
}
```

**[DO]** Remove the comments and use clean structure and constant variables to express the logic.
```typescript
const DIRECTIONCODE_RIGHT: number = 0x02;
const DIRECTIONCODE_LEFT: number = 0x04;
const DIRECTIONCODE_NONE: number = 0x00;

const oldX = deviceInfo.position.x;
const directionCode = (x > oldX) 
  ? DIRECTIONCODE_RIGHT 
  : (x < oldX) 
    ? DIRECTIONCODE_LEFT 
    : DIRECTIONCODE_NONE;
```

### 3. Redundant Comments
**[DON'T]** Write JSDoc or inline comments that just repeat the method signature.
```typescript
export class UserService {
  /**
   * This method gets the user by user id.
   */
  getUserByUserId (userId: string): Promise<User> { 
    // ...
  }
}
```

**[DO]** Rely on the declarative naming to speak for itself. Delete the comment entirely.
```typescript
export class UserService {
  getUserByUserId (userId: string): Promise<User> { 
    // ...
  }
}
```

### 4. Adding "Why" Context
**[DON'T]** Write code that behaves strangely without explaining the business or technical reasoning.
```typescript
function warnAboutDataLoss(
  existingRef: Reference,
  incomingObj: StoreObject,
  storeFieldName: string,
  store: NormalizedCache,
) {
  // ...
}
```

**[DO]** Add a comment to explain *Why* a specific structural reality exists that the reader cannot infer from the code.
```typescript
// Note that this function is unused in production, and thus should be
// pruned by any well-configured minifier.
function warnAboutDataLoss(
  existingRef: Reference,
  incomingObj: StoreObject,
  storeFieldName: string,
  store: NormalizedCache,
) {
  // ...
}
```

### 5. Single Layer of Abstraction vs Inline Comments
**[DON'T]** Leave a massive function block littered with comments explaining the steps.
```typescript
get formConfig () {
  return this.fields.reduce((fields, field) => {
    if (!Array.isArray(fields)) {
      field = [field]
    }
    // Currently last field in section
    const last = fields.slice(-1)[0];
    const lastValue = this.values[last.id];

    if (this.values[field.id]) {
      // answered fields always show
      return [...fields, field]
    } else if (this.values[last.id] && lastValue.next_field_id === field.id) {
      // this is the next field depending on the previous value
      return [...fields, field]
    } else {
      // this field shouldn't be visible yet
      return fields;
    }
  })
}
```

**[DO]** Extract the imperative steps into private methods, leaving only the "Why" comment if absolutely necessary.
```typescript
get formConfig () {
  return this.fields.reduce((fields, field) => {
    if (this.isSectionFirstInArray(fields)) {
      fields = this.makeArray(fields);
    }

    if (this.shouldAddToFieldsList(fields, field)) {
      return [...fields, field]
    }
    
    // Shouldn't be visible yet - I left this, as it explains what cannot
    // reasonably be refactored to be said in words
    return fields;
  })
}
```