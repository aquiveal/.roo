# @Domain
These rules MUST be triggered whenever the AI is tasked with writing new code, refactoring existing code, conducting code reviews, organizing file structures, or configuring project formatting and linting tools. They apply strictly to code formatting, structural style, visual readability, and architectural organization within files.

# @Vocabulary
- **Formatting**: The visual appearance of the source code, dictated by whitespace, consistency, and structural layout.
- **Tokens**: The five atomic components of programming languages: Keywords (e.g., `class`), Identifiers (e.g., `user`), Operators (e.g., `+`, `=`), Separators (whitespace, tabs, newlines), and Literals (integers, strings).
- **Code Density**: A measurement of how many lines of code exist continuously without a vertical line break. Low density is preferred.
- **Newspaper Code Principle**: The practice of front-loading a file with the most important, high-level concepts first, pushing lower-level, less critical implementation details towards the bottom of the file.
- **Step-down Principle**: Organizing code so that it reads logically from top to bottom, descending in abstraction, ideally with method callers placed close to their callees.
- **Level of Abstraction**: The degree of detail within a block of code. High-level code orchestrates behavior; low-level code performs the granular operations.
- **ESLint**: A JavaScript/TypeScript linter used to enforce coding conventions and structural rules.
- **Prettier**: An opinionated code formatter that enforces automated whitespace, indentation, and horizontal layout rules.
- **Husky**: A Git hooks tool used to enforce formatting and linting policies prior to code being committed to source control.

# @Objectives
- **Maximize Readability via Whitespace**: The AI MUST use vertical and horizontal whitespace to separate thoughts, tokens, and algorithms, making the code visually digestible.
- **Build Comprehension Momentum**: The AI MUST adhere strictly to consistent naming, capitalization, and structural conventions so human readers can rely on mental pattern matching.
- **Tell a Story with Structure**: The AI MUST structure files and classes so that the primary intent is immediately visible at the top, preventing reader fatigue.
- **Maintain Abstraction Boundaries**: The AI MUST NOT mix high-level orchestration and low-level granular details within the same function or method.
- **Automate and Enforce**: The AI MUST rely on and configure standard tooling (ESLint, Prettier, Husky) to mechanically enforce these formatting rules across a project.

# @Guidelines

- **Whitespace and Spacing Rules**
  - The AI MUST apply horizontal spacing between all keywords, identifiers, operators, and literals.
  - The AI MUST indent code horizontally whenever stepping inside a class, method, function, or control block.
  - The AI MUST maintain low code density by inserting blank vertical lines to separate independent thoughts, logical chunks, and individual methods (acting as a "resting point" for the reader).

- **Horizontal Breaking**
  - The AI MUST strategically break code horizontally onto multiple lines when a statement surpasses a line length of 80 to 120 characters. 
  - When breaking long signatures or declarations, the AI MUST indent the broken lines consistently to align with the scope of the statement.

- **File Size Management**
  - The AI MUST monitor file sizes and aim to keep files small (ideally between 200 and 500 lines). 
  - If a file exceeds this size, the AI MUST evaluate it for violations of the Single Responsibility Principle and suggest extracting logic into new files.

- **Capitalization and Consistency (TypeScript/JavaScript Focus)**
  - The AI MUST use `camelCase` for variables, functions, class instances, and class members.
  - The AI MUST use `PascalCase` for classes, namespaces, types, and interfaces.
  - The AI MUST NOT mix capitalization conventions (e.g., do not use underscores `snake_case` in TS/JS unless explicitly working with a database or external API that strictly requires it).

- **Newspaper Code and Step-Down Principle**
  - When writing or refactoring a class, the AI MUST order the contents in the following sequence:
    1. Member variables (properties)
    2. Constructor
    3. Primary/Public methods (the most important behaviors intended for the client)
    4. Private/Low-level helper methods (the internal implementation details)
  - The AI MUST arrange code to descend in abstraction; the highest-level operations must appear first, delegating to lower-level private methods placed further down the file.

- **Consistent Level of Abstraction**
  - The AI MUST evaluate the methods it writes to ensure they operate at a single level of abstraction.
  - If a method contains both high-level orchestration (e.g., fetching an entity) and low-level details (e.g., raw string manipulation or bitwise math), the AI MUST extract the low-level details into separate, explicitly named helper methods.

- **Method Proximity**
  - The AI MUST group related methods physically adjacent to one another.
  - Specifically, if a property has a `get` and `set` method, the AI MUST place them immediately next to each other, uninterrupted by unrelated methods.

- **Tooling Configuration**
  - When tasked with setting up a new repository or formatting pipeline, the AI MUST configure ESLint (for code conventions), Prettier (for formatting), and Husky (for pre-commit enforcement).
  - When working within an existing project, the AI MUST respect and adopt the formatting rules defined in the local `.prettierrc` and `.eslintrc` files over its own default preferences.

# @Workflow
When generating, refactoring, or reviewing code, the AI MUST execute the following algorithm:

1. **Token & Whitespace Pass**: Apply standard spaces between all operators, identifiers, and keywords. Ensure all control blocks and class bodies are properly indented.
2. **Density Pass**: Scan contiguous blocks of logic. Insert vertical empty lines between variable declarations, distinct operations, and return statements. Ensure an empty line exists between every class method.
3. **Horizontal Width Pass**: Check for lines exceeding ~80-120 characters (like long dependency injection constructors or massive function arguments) and break them into multi-line, properly indented statements.
4. **Capitalization Pass**: Verify that all type/interface/class declarations use `PascalCase` and all instances/variables/functions use `camelCase`.
5. **Storytelling (Ordering) Pass**: Rearrange the class or module file. Move configuration and state (variables, constructors) to the top. Move the public API methods immediately below the constructor. Move all `private` helper methods to the bottom.
6. **Proximity Pass**: Locate paired methods (e.g., getters and setters) and move them next to each other.
7. **Abstraction Pass**: Review the public methods. If any public method contains deeply nested logic or low-level data manipulation, extract that logic into a private method and place it at the bottom of the file. Replace the extracted code in the public method with a call to the new private method.

# @Examples (Do's and Don'ts)

### Code Density and Whitespace
- **[DON'T]** Write dense code lacking horizontal and vertical separators.
  ```typescript
  const artists=this.artistRepo.getArtists();const artistNames:string=artists.map((a)=>a.name);
  class Employer{
  public update(details:CompanyDetails):Result<UpdateResult>{
  const x=12;const user={name:"khalil"}
  // dense logic here
  }}
  ```
- **[DO]** Use horizontal spaces around operators and vertical line breaks to separate distinct logical steps.
  ```typescript
  const artists = this.artistRepo.getArtists();
  const artistNames: string = artists.map((a) => a.name);

  class Employer {
    public update (details: CompanyDetails): Result<UpdateResult> {
      const x = 12;
      const user = { name: "khalil" };
      
      // logic separated by vertical whitespace
    }
  }
  ```

### Horizontal Breaking
- **[DON'T]** Allow long lines that force the reader to scroll horizontally.
  ```typescript
  export class UpvotePost implements UseCase<UpvotePostDTO, Promise<UpvotePostResponse>> {
    constructor (memberRepo: IMemberRepo, postRepo: IPostRepo, postVotesRepo: IPostVotesRepo, postService: PostService) {
      // ...
    }
  }
  ```
- **[DO]** Break long signatures cleanly across multiple lines.
  ```typescript
  export class UpvotePost implements UseCase<
    UpvotePostDTO, 
    Promise<UpvotePostResponse>
  > {
    constructor (
      memberRepo: IMemberRepo, 
      postRepo: IPostRepo, 
      postVotesRepo: IPostVotesRepo, 
      postService: PostService
    ) {
      // ...
    }
  }
  ```

### Capitalization and Consistency
- **[DON'T]** Mix capitalization styles or use underscores in TS/JS.
  ```typescript
  const DAYS_IN_WEEK = 7;
  const daysInMonth = 30; // Inconsistent constant casing
  
  function restore_database() {} // Underscores instead of camelCase
  
  type animal = { /* ... */ } // Lowercase type
  ```
- **[DO]** Use strictly consistent casing (`camelCase` for instances/methods, `PascalCase` for types).
  ```typescript
  const DAYS_IN_WEEK = 7;
  const DAYS_IN_MONTH = 30;
  
  function restoreDatabase() {} 
  
  type Animal = { /* ... */ }
  ```

### Newspaper Principle (Ordering)
- **[DON'T]** Place private implementation details at the top of the class, burying the primary public interface.
  ```typescript
  export class RecordingStudio {
    constructor (...) { ... }
    
    private prepareInstrument (instrument: Instrument): void { ... }
    private recordVocals (demo: Demo): void { ... }
    
    // Buried public method!
    public async recordSong (demoNameQuery: string, artist: Artist): void { ... }
  }
  ```
- **[DO]** Front-load the class with the public API, pushing private details to the bottom.
  ```typescript
  export class RecordingStudio {
    constructor (...) { ... }
    
    // Public method at the top
    public async recordSong (demoNameQuery: string, artist: Artist): void { ... }

    // Private details at the bottom
    private prepareInstrument (instrument: Instrument): void { ... }
    private recordVocals (demo: Demo): void { ... }
  }
  ```

### Method Proximity
- **[DON'T]** Break apart naturally related methods with unrelated ones.
  ```typescript
  export class Member {
    get username (): Username { ... }
    
    public logout (): void { ... } // Unrelated method in the middle
    
    set username (username: string): void { ... }
  }
  ```
- **[DO]** Keep related methods physically adjacent.
  ```typescript
  export class Member {
    get username (): Username { ... }
    set username (username: string): void { ... }
    
    public logout (): void { ... }
  }
  ```

### Consistent Level of Abstraction
- **[DON'T]** Mix high-level domain orchestration with granular, low-level manipulation in the same method.
  ```typescript
  public async recordSong (demoNameQuery: string, artist: Artist): void {
    const demo = this.getDemoFromLibrary(demoNameQuery, artist);
    
    // Low level detail mixed with high level orchestration
    const instruments = demo.getInstruments();
    for (let instrument of instruments) {
      this.prepareInstrument(instrument);
    }
    this.metronome.setBpm(demo.bpm);
    this.assembleMusiciansForInstruments(instruments);
    // ...
  }
  ```
- **[DO]** Extract the low-level details into a private helper method to maintain a single level of abstraction in the public method.
  ```typescript
  public async recordSong (demoNameQuery: string, artist: Artist): void {
    const demo = this.getDemoFromLibrary(demoNameQuery, artist);
    
    // High-level orchestration only
    await this.recordMusicFromDemo(demo);
    await this.recordVocals(demo);
  }

  // Low level details pushed down
  private async recordMusicFromDemo(demo: Demo): Promise<void> {
    const instruments = demo.getInstruments();
    for (let instrument of instruments) {
      this.prepareInstrument(instrument);
    }
    // ...
  }
  ```