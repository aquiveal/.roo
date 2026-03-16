# @Domain
Trigger these rules whenever generating, refactoring, evaluating, or documenting code identifiers. This includes naming variables, functions, methods, classes, interfaces, types, parameters, namespaces, files, and directories. These rules apply across all programming languages, particularly strictly-typed languages like TypeScript and object-oriented environments.

# @Vocabulary
- **Thesaurus Names**: Different words used to express the exact same concept or behavior (e.g., `get`, `fetch`, `show`, `present`).
- **Knowledge in the World**: Knowledge that does not have to be learned or memorized because it maps directly to physical or cultural realities (e.g., real-world domain concepts).
- **Knowledge in the Head**: Knowledge that requires logical processing, memory, or learning to use (e.g., arbitrary technical implementations or math).
- **CQS (Command Query Separation)**: The principle that a method is either a Command (performs an action/side-effect, returns no data) or a Query (returns data, performs no side-effects).
- **Blob Parameters**: Untyped or highly generic parameter objects (e.g., `args: any`) that do not explicitly declare their contents.
- **Over-specification**: Packing too much context, logic, or variant information into a name (e.g., `userHasAuthenticatedAndVerifiedEmailShouldTheyBeNonAdmins`).
- **Under-specification**: Using a generic name that fails to describe the contents or intended use case of the identifier (e.g., `Option` instead of `FoodOption`).
- **Compression vs. Context**: The balance in naming where *compression* increases discoverability but reduces context, and *context* increases understanding but makes names unreadable. Names communicate *what*, while context/grouping/comments communicate *why*.

# @Objectives
- Ensure every concept is represented by a single, consistent, and unique name throughout the codebase.
- Bridge the gap between the code and the real world by heavily favoring domain-specific terminology.
- Guarantee that all names clearly express their contents, behaviors, and return types without requiring the reader to analyze the underlying implementation.
- Maximize search-ability by avoiding typos, misspellings, arbitrary abbreviations, and raw numeric constants.
- Maintain professional austerity by strictly avoiding jokes, temporary concepts, or pop-culture references.

# @Guidelines

### 1. Consistency & Uniqueness
- **AI MUST** enforce a single vocabulary term per concept. Never use "thesaurus names" (e.g., do not mix `get`, `fetch`, and `retrieve` for the same operation).
- **AI MUST** rigidly adhere to language and project casing conventions (e.g., `PascalCase` for types/classes, `camelCase` for variables/functions).
- **AI MUST NOT** misspell names to create unique identifiers, nor use alternate spellings (e.g., `color`/`colour`).
- **AI MUST NOT** recycle variable names. Always initialize a new explicitly named temporary variable rather than reusing an existing one for a different purpose.
- **AI MUST NOT** rely on casing to differentiate variables (e.g., `empName`, `EmpName`, and `Empname` in the same scope is strictly forbidden).

### 2. Understandability
- **AI MUST** use domain concepts to refer to business rules. The code must reflect real-world processes.
- **AI MUST** use correct architectural construct names for technical layers (e.g., `Controller`, `Repo`, `Mapper`, `Factory`).
- **AI MUST NOT** use vague, "tech-y" sounding names that add no meaning (e.g., avoid `Processor`, `Manager`, `Helper`, `Dealie`).
- **AI MUST NOT** randomly capitalize syllables within words (e.g., `PaidJobDeTails`).
- **AI MUST NOT** use digits in names where they resemble letters (e.g., `10l`). Write out the word instead (`ThirdCard`, not `3rdCard`).
- **AI MUST** document notable side effects within the method name (e.g., `createUserAndSendAccountVerificationEmail`).
- **AI MUST** avoid misleading names. A method claiming to validate something MUST return a boolean.
- **AI MUST NOT** use negatives in boolean names. Use `!isEmailValid` instead of `isEmailNotValid`.

### 3. Specificity
- **AI MUST** ensure a name describes exactly what is inside the variable—nothing more, nothing less. Remove conversational context regarding *why* it exists.
- **AI MUST** properly differentiate single items from collections. Use plural names (`todos`), or collection suffixes (`todoList`) for arrays/lists. Use singular names for single instances.
- **AI MUST NOT** append the identifier type to the name unless strictly necessary for meta-programming (e.g., `user` instead of `userVariable` or `userObject`).
- **AI MUST** name human actors by their specific roles (e.g., `Admin`, `Editor`, `Visitor`, `Trader`) rather than defaulting to the generic term `User`, unless in a strict Identity & Access Management context.
- **AI MUST** specify unions in variable names if the variable can hold multiple types (e.g., `userOrUserId`).
- **AI MUST NOT** use Blob parameters. Define strict interfaces/types for object parameters.
- **AI MUST NOT** use number series parameters (e.g., `arr1`, `arr2`). Use intention-revealing names like `source` and `destination`.

### 4. Brevity
- **AI MUST** omit needless words from names (e.g., replace `inOrderTo` with `to`, `aNumberOf` with `some`).
- **AI MUST NOT** use non-conventional single-letter variables. Single letters are ONLY permitted in standard math or localized loop counters (`i`, `x`, `y`).
- **AI MUST** rely on contextual grouping. If a method is inside `StudentRepo`, name it `create(props)`, NOT `createStudent(props)`.
- **AI MUST NOT** use unnecessary member prefixes (e.g., `_firstName` or `vmFirstName`). Rely on access modifiers (`private`, `protected`) and object encapsulation (`this.model.firstName`).

### 5. Search-ability & Pronounceability
- **AI MUST NOT** use inline numeric constants. Extract them into expressively named constant variables (e.g., `const DEFAULT_MOVIE_RATING = 8`).
- **AI MUST** use camel case to signal word breaks to ensure readability (`prepareARead`, not `preparearead`).
- **AI MUST** format boolean variables/methods as questions (`isPostEmpty()`) or assertions (`potIsEmpty()`).
- **AI MUST NOT** omit vowels or use arbitrary abbreviations (e.g., `Controller` not `Cntrllr`, `timeStamp` not `tmStmp`). Very standard, culturally ubiquitous abbreviations (`ssn`, `id`) are permitted.

### 6. Austerity
- **AI MUST NOT** use culturally restricted references, memes, jokes, or historical events in code identifiers. The code must be understandable globally and longitudinally.

# @Workflow
When generating or reviewing code, the AI must process naming via the following rigid algorithmic steps:

1. **Concept Identification**: Identify the exact domain concept, behavior, or architectural construct the identifier represents.
2. **Context Check**: Determine the identifier's location (e.g., inside a class, inside a loop). Strip out words that are already implied by the surrounding context (e.g., class name, module name).
3. **Role & Type Mapping**: 
   - If human, assign a role-based name (`Customer`, not `User`).
   - If a collection, make it explicitly plural.
   - If a boolean, formulate it as a question (`is...`, `has...`, `can...`) or assertion.
   - If a method, apply CQS. Is it a Command (verb, side-effect) or a Query (noun/verb, returns data)?
4. **Vocabulary Standardization**: Check against established patterns in the current codebase. Ensure no "thesaurus names" are being introduced.
5. **Sanitization**: 
   - Remove digits.
   - Remove abbreviations lacking vowels.
   - Remove negative booleans.
   - Remove meta-words (`Variable`, `Object`, `Helper`, `Manager`).
   - Remove prefixes (`_`, `vm`).
6. **Formatting**: Apply the language-specific casing standard strictly.
7. **Final Validation**: Is it pronounceable? Is it searchable? Is it austere? If no, return to step 3.

# @Examples (Do's and Don'ts)

### Consistency (Thesaurus Names)
- **[DON'T]**: Mixing verbs for the same action across a class.
  ```typescript
  export class PostAPI {
    getAuthor(): Promise<Author>;
    fetchPosts(): Promise<Posts>;
    showTags(): Promise<Tags>;
    presentCategories(): Promise<Categories>;
  }
  ```
- **[DO]**: Standardize on a single verb.
  ```typescript
  export class PostAPI {
    getAuthor(): Promise<Author>;
    getPosts(): Promise<Posts>;
    getTags(): Promise<Tags>;
    getCategories(): Promise<Categories>;
  }
  ```

### Variable Recycling
- **[DON'T]**: Reusing a temporary variable for different purposes.
  ```typescript
  let sum = 0;
  // ... loop calculating category sum using sum
  console.log(sum);
  sum = 0;
  // ... loop calculating tag sum using sum
  ```
- **[DO]**: Creating distinct, specific variables.
  ```typescript
  let categorySum = 0;
  // ... loop calculating category sum
  let tagSum = 0;
  // ... loop calculating tag sum
  ```

### Avoid Digits and Random Capitalization
- **[DON'T]**: Using characters that look like digits, or randomly capitalizing.
  ```typescript
  const 10l = 101;
  const 3rdCard = true;
  const PaidJobDeTails = {};
  ```
- **[DO]**: Spelling out words and using proper casing.
  ```typescript
  const oneIota = 101;
  const thirdCard = true;
  const paidJobDetails = {};
  ```

### Avoid Negative Booleans
- **[DON'T]**: Encoding the negation in the variable name.
  ```typescript
  if (isEmailNotValid(email)) { return; }
  ```
- **[DO]**: Using logical negation operators on a positive boolean name.
  ```typescript
  if (!isEmailValid(email)) { return; }
  ```

### Specificity vs Over-Specification
- **[DON'T]**: Encoding conditional execution paths or conversational context into the name.
  ```typescript
  public userHasAuthenticatedAndVerifiedEmailShouldTheyBeNonAdmins(user: User): boolean {}
  const tempUserToDetermineIfExistsOrNot = await this.userRepo.getUser();
  ```
- **[DO]**: Describing exactly what the variable holds or extracting conditionals into separate methods.
  ```typescript
  public userIsAdmin(user: User): boolean {}
  const userExists = !!(await this.userRepo.getUser());
  ```

### Context and Grouping
- **[DON'T]**: Repeating the context in the method name when the class already provides it.
  ```typescript
  export const StudentRepo = {
    createStudent: (props) => {},
    editStudent: (id, props) => {},
    deleteStudent: (id) => {}
  }
  ```
- **[DO]**: Letting the namespace/object provide the context.
  ```typescript
  export const StudentRepo = {
    create: (props) => {},
    edit: (id, props) => {},
    del: (id) => {}
  }
  ```

### Member Prefixes
- **[DON'T]**: Prefixing variables to denote scope or model-type.
  ```typescript
  class UserController {
    constructor() {
      this._firstName = "";
      this.vmLastName = "";
    }
  }
  ```
- **[DO]**: Utilizing object properties or native access modifiers.
  ```typescript
  class UserController {
    constructor() {
      this.model.firstName = "";
      this.model.lastName = "";
    }
  }
  ```

### Numeric Constants
- **[DON'T]**: Using magic numbers directly in method signatures or logic.
  ```typescript
  function addMovieRating(rating = 8) {}
  ```
- **[DO]**: Assigning magic numbers to searchable constant variables.
  ```typescript
  const DEFAULT_MOVIE_RATING = 8;
  function addMovieRating(rating = DEFAULT_MOVIE_RATING) {}
  ```

### Pronounceability & Vowels
- **[DON'T]**: Smashing words together or dropping vowels.
  ```typescript
  type tmStmp = Date;
  function preparearead() {}
  ```
- **[DO]**: Retaining vowels and using camelCase for breaks.
  ```typescript
  type timeStamp = Date;
  function prepareARead() {}
  ```