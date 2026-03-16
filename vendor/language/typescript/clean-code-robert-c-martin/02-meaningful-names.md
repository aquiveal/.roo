@Domain
Trigger these rules whenever generating new code, refactoring existing code, conducting code reviews, defining software architecture, renaming variables/functions/classes, or creating file and directory structures. These rules apply to all programming languages and software artifacts.

@Vocabulary
- **Intention-Revealing Name**: A name that explicitly answers why the entity exists, what it does, and how it is used without requiring supplementary comments.
- **Implicity**: The degree to which context is obscured or missing from the code itself, forcing the reader to guess the meaning of variables or constants.
- **Disinformation**: False clues or entrenched terms used incorrectly that obscure the true meaning of the code (e.g., using "list" for a non-List data structure).
- **Noise Words**: Redundant, meaningless suffixes or prefixes (e.g., `Data`, `Info`, `Object`, `Manager`, `Processor`, `a`, `an`, `the`) that provide no functional distinction.
- **Noninformative Name**: A name (like a number series `a1, a2`) that provides absolutely no clue to the author's intention.
- **Hungarian Notation / Type Encoding**: The obsolete practice of encoding the data type or scope into the variable name (e.g., `phoneString`, `m_dsc`).
- **Mental Mapping**: Forcing the reader to mentally translate a placeholder name (like `c`) into the actual concept it represents.
- **Solution Domain**: Technical terminology familiar to programmers (e.g., computer science terms, design patterns, mathematical terms, algorithm names).
- **Problem Domain**: Terminology drawn strictly from the business or user problem being solved.
- **Pun**: Overloading a single term to mean two different things in the same codebase (e.g., using `add` for both mathematical addition and appending to a collection).
- **Gratuitous Context**: Unnecessary prefixes added to names (e.g., prepending every class with the application's acronym).

@Objectives
- Guarantee that every identifier in the codebase immediately and transparently communicates its purpose, usage, and context.
- Eliminate the need for explanatory comments by pushing all descriptive value directly into the names of variables, classes, and methods.
- Ensure all names are highly searchable and pronounceable to facilitate team communication and codebase navigation.
- Establish a strict, consistent lexicon that prevents mental translation overhead for future readers.

@Guidelines

**1. General Naming Rules**
- The AI MUST choose intention-revealing names that answer why it exists, what it does, and how it is used.
- The AI MUST NOT use single-letter variables EXCEPT for local loop counters (`i`, `j`, `k`) within extremely short, localized scopes.
- The AI MUST NOT use the lowercase letter `l` or the uppercase letter `O` as variable names, as they resemble `1` and `0`.
- The AI MUST use pronounceable, dictionary-valid words. Do not invent unpronounceable abbreviations (e.g., use `generationTimestamp` instead of `genymdhms`).
- The AI MUST prioritize searchable names. The length of a variable name MUST correspond to the size of its scope. Variables used across multiple scopes must have highly distinct, searchable names.
- The AI MUST replace magic numbers and literal primitives with searchable, named constants.
- The AI MUST maintain a consistent lexicon. Pick one word per abstract concept and use it exclusively (e.g., choose one of `fetch`, `retrieve`, or `get` and stick with it).
- The AI MUST NOT pun. Do not use the same term for semantically different operations. If `add` means mathematical addition, use `insert` or `append` for list manipulation.
- The AI MUST NOT be cute. Avoid slang, jokes, and cultural colloquialisms. Choose clarity over entertainment.

**2. Distinction and Disinformation**
- The AI MUST NOT use entrenched IT terms (like `hp`, `aix`, `sco`) unless they literally refer to those specific platforms.
- The AI MUST NOT append container types to names unless the variable is actually that exact type. For collections of accounts, use `accountGroup` or `accounts` rather than `accountList`.
- The AI MUST distinguish names meaningfully. Do not use number-series naming (`a1`, `a2`) or append noise words (`ProductInfo` vs `ProductData`).
- The AI MUST NOT include the word `variable` in a variable name or `table` in a table name.

**3. Encodings and Prefixes**
- The AI MUST NOT use Hungarian Notation or encode data types into variable names.
- The AI MUST NOT prefix member variables with `m_`, `_`, or any other scope identifier.
- The AI MUST leave interfaces unadorned. Do not prefix interfaces with `I`. If encoding is required, suffix the implementation class (e.g., `ShapeFactoryImpl` instead of `IShapeFactory`).

**4. Domain Terminology**
- The AI MUST use Solution Domain names (CS terms, patterns, algorithms) whenever a technical concept applies.
- The AI MUST use Problem Domain names (business logic terms) only when there is no appropriate technical programmer-jargon available.

**5. Classes and Objects**
- The AI MUST name classes and objects using nouns or noun phrases (e.g., `Customer`, `WikiPage`, `Account`, `AddressParser`).
- The AI MUST NOT use verbs for class names.
- The AI MUST NOT use vague, omnibus words like `Manager`, `Processor`, `Data`, or `Info` in class names.

**6. Methods and Functions**
- The AI MUST name methods using verbs or verb phrases (e.g., `postPayment`, `deletePage`, `save`).
- The AI MUST prefix accessors, mutators, and predicates with `get`, `set`, and `is`.
- The AI MUST prefer static factory methods over overloaded constructors. Factory methods MUST be named to describe their arguments (e.g., `Complex.FromRealNumber(23.0)`). Private constructors SHOULD be used to enforce this.

**7. Context Management**
- The AI MUST place variables into a meaningful context by grouping them into well-named classes (e.g., moving `firstName`, `lastName`, `state` into an `Address` class) rather than relying on prefixes (e.g., `addrFirstName`).
- The AI MUST NOT add gratuitous context. Do not prefix names with project abbreviations or module acronyms. Use the shortest name that remains fully clear and precise.

@Workflow
When analyzing, generating, or refactoring code, the AI must execute the following algorithmic sequence:

1. **Context Extraction**: Identify the exact purpose, scope, and domain of the entity being named.
2. **Type/Scope Stripping**: Remove any existing type encodings (e.g., `String`, `Int`), scope prefixes (`m_`), or interface prefixes (`I`).
3. **Noise Reduction**: Strip all noise words (`Info`, `Data`, `Manager`, `Object`) unless they carry explicit, verifiable architectural meaning.
4. **Lexicon Alignment**: Cross-reference the proposed name with the established codebase lexicon to ensure "one word per concept" and prevent punning.
5. **Categorical Formatting**:
   - If a Class: Format as a descriptive Noun phrase.
   - If a Method: Format as a Verb phrase. Convert overloaded constructors to descriptive static factory methods.
   - If a Variable/Constant: Ensure pronounceability. If global/widespread, expand the name for searchability. If a magic number, convert to a highly descriptive uppercase constant.
6. **Context Encapsulation**: Evaluate if the variable belongs to a broader concept. If 3+ variables share a prefix or logical grouping, extract them into a dedicated class (e.g., `GuessStatisticsMessage`).
7. **Final Review**: Validate that the name reads like well-written prose and answers "why, what, and how" without requiring a comment.

@Examples (Do's and Don'ts)

**Intention-Revealing Names**
- [DON'T]: `int d; // elapsed time in days`
- [DO]: `int elapsedTimeInDays;`
- [DON'T]: `if (cell[0] == 4)`
- [DO]: `if (cell.isFlagged())`

**Disinformation**
- [DON'T]: `Account[] accountList;`
- [DO]: `Account[] accounts;`
- [DON'T]: `int O1 = l;`
- [DO]: `int activeCount = offset;`

**Noise Words & Meaningful Distinctions**
- [DON'T]: `class CustomerInfo`, `class CustomerData`, `class CustomerObject`
- [DO]: `class Customer`, `class CustomerHistory`, `class CustomerAddress`
- [DON'T]: `getActiveAccount(); getActiveAccounts(); getActiveAccountInfo();` (When differences are unclear)
- [DO]: `getActiveAccount(); getActiveAccountList(); getActiveAccountProfile();`

**Pronounceable & Searchable Names**
- [DON'T]: `Date genymdhms;`
- [DO]: `Date generationTimestamp;`
- [DON'T]: `for (int j=0; j<34; j++) { s += (t[j]*4)/5; }`
- [DO]: `int realTaskWeeks = (realTaskDays / WORK_DAYS_PER_WEEK);`

**Encodings & Prefixes**
- [DON'T]: `String phoneString;`
- [DO]: `String phoneNumber;`
- [DON'T]: `private String m_dsc;`
- [DO]: `private String description;`
- [DON'T]: `interface IShapeFactory` and `class ShapeFactory`
- [DO]: `interface ShapeFactory` and `class ShapeFactoryImpl`

**Class and Method Names**
- [DON'T]: `class ParseData`
- [DO]: `class AddressParser`
- [DON'T]: `Complex fulcrumPoint = new Complex(23.0);`
- [DO]: `Complex fulcrumPoint = Complex.FromRealNumber(23.0);`

**Don't Be Cute**
- [DON'T]: `public void eatMyShorts()`, `public void whack()`
- [DO]: `public void abort()`, `public void kill()`

**Meaningful Context**
- [DON'T]: `String addrFirstName, addrLastName, addrState;`
- [DO]: `class Address { String firstName; String lastName; String state; }`

**Gratuitous Context**
- [DON'T]: `class GSDAccountAddress` (Where GSD is Gas Station Deluxe application)
- [DO]: `class PostalAddress` or `class Address`