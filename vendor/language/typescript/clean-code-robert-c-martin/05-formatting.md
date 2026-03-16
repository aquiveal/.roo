@Domain
These rules are triggered whenever the AI is generating, refactoring, modifying, or reviewing source code, specifically when determining file layout, line breaks, indentation, spacing, and the structural arrangement of variables and functions within a file.

@Vocabulary
- **Newspaper Metaphor**: The structural concept where a source file reads like a newspaper article: a high-level, broad-brush synopsis at the top, with details increasing progressively as the reader scrolls downward.
- **Vertical Openness**: The practice of using blank lines as visual cues to separate distinct concepts, clauses, or complete thoughts within the code.
- **Vertical Density**: The practice of keeping lines of code that are tightly related visually close together, avoiding useless comments or blank lines that break their association.
- **Conceptual Affinity**: The natural pull certain bits of code have toward each other (e.g., overloaded methods, methods performing similar tasks) which dictates they should be kept vertically close.
- **Stepdown Rule**: The practice of formatting dependent functions such that the calling function is placed immediately above the called function, creating a top-down narrative flow.
- **Dummy Scope**: An empty body of a control statement (e.g., an empty `while` loop), which can be visually deceptive if not formatted correctly.

@Objectives
- Ensure code formatting is treated as a primary communication tool, not just an aesthetic afterthought.
- Establish a consistent, predictable, and readable code structure that survives iterations and refactoring.
- Structure files so that human readers can quickly grasp high-level intent without wading through low-level details immediately.
- Prevent visual clutter and cognitive overload by strictly managing vertical distance, horizontal width, spacing, and indentation.

@Guidelines
- **File Size and Length**: The AI MUST strive to keep source files small. Files SHOULD typically be around 200 lines and MUST NOT exceed 500 lines unless strictly necessary.
- **The Newspaper Metaphor (Vertical Ordering)**: 
  - The AI MUST place high-level concepts and algorithms at the top of the file.
  - The AI MUST place low-level details, utilities, and helper functions at the bottom of the file.
- **Vertical Openness**: The AI MUST insert a single blank line to separate package declarations, imports, classes, and individual functions. The AI MUST use blank lines to separate distinct logical blocks within a complex function.
- **Vertical Density**: The AI MUST NOT separate tightly related lines of code (e.g., a pair of related instance variables) with blank lines or meaningless comments.
- **Variable Declarations (Vertical Distance)**: 
  - The AI MUST declare local variables as close to their first usage as possible.
  - The AI MUST declare control variables for loops directly within the loop statement.
- **Instance Variables (Vertical Distance)**: The AI MUST declare all instance variables together in one well-known place, strictly at the very top of the class (avoiding the C++ "scissors rule" of putting them at the bottom).
- **Dependent Functions (Vertical Distance)**: If one function calls another, the AI MUST place them vertically close together. The caller MUST be placed above the callee.
- **Conceptual Affinity (Vertical Distance)**: The AI MUST place functions that share a common naming scheme or perform variations of the same task vertically close to one another, even if they do not directly call each other.
- **Horizontal Line Width**: The AI MUST keep lines short. Lines SHOULD NOT exceed 120 characters in length. Code MUST NOT require horizontal scrolling.
- **Horizontal Openness and Density**:
  - The AI MUST surround assignment operators (e.g., `=`) with white space to accentuate the left and right sides.
  - The AI MUST NOT place a space between a function name and its opening parenthesis.
  - The AI MUST place a space after commas within function argument lists.
  - The AI SHOULD use white space to accentuate the precedence of operators (e.g., no spaces around high-precedence operators like `*`, but spaces around lower-precedence operators like `+`).
- **Horizontal Alignment**: The AI MUST NOT horizontally align variable names, variable types, or assignment rvalues across multiple lines. If a list of unaligned declarations looks too long, the AI MUST split the class rather than aligning the text.
- **Indentation**: The AI MUST strictly indent lines in proportion to their position in the hierarchy of scopes (file, class, method, block). 
- **Breaking Indentation**: The AI MUST NOT collapse short `if` statements, `while` loops, or short functions down to a single line. The AI MUST expand and properly indent these scopes.
- **Dummy Scopes**: If a dummy scope (empty body) is unavoidable, the AI MUST NOT place the terminating semicolon silently at the end of the line. The AI MUST indent the semicolon on its own line or explicitly wrap it in braces.
- **Team Rules Precedence**: If the project contains an existing, established formatting convention (e.g., EditorConfig, Prettier, Checkstyle), the AI MUST follow the existing team rules over these individual guidelines.

@Workflow
1. **Initial Layout Planning**: Upon generating a class, place all instance variables at the top. Determine the high-level public APIs and place them next.
2. **Function Ordering**: Sort functions so that any private utility called by a public function is placed immediately below that public function. Group overloaded or similar functions sequentially.
3. **Density and Openness Pass**: Review the code vertically. Insert blank lines between concepts/functions. Remove blank lines and noise comments between tightly related variable declarations.
4. **Horizontal Formatting Pass**: Break any lines exceeding 120 characters. Ensure spacing around assignments and commas, and remove spaces between function names and parentheses.
5. **Alignment and Indentation Cleanup**: Strip any artificial horizontal alignment (e.g., lining up `=` signs). Expand any one-line `if` statements or collapsed functions into fully indented multi-line blocks. Fix any dummy scopes.

@Examples (Do's and Don'ts)

**Vertical Density & Instance Variables**
- [DO]: Group instance variables tightly at the top of the class.
```java
public class ReporterConfig {
    private String className;
    private List<Property> properties = new ArrayList<Property>();

    public void addProperty(Property property) {
        properties.add(property);
    }
}
```
- [DON'T]: Break up related instance variables with noisy, redundant comments or blank lines.
```java
public class ReporterConfig {

    /**
     * The class name of the reporter listener
     */
    private String className;

    /**
     * The properties of the reporter listener
     */
    private List<Property> properties = new ArrayList<Property>();
}
```

**Dependent Functions (Stepdown Rule)**
- [DO]: Place the calling function immediately above the called utility function.
```java
public Response makeResponse(Context context, Request request) {
    String pageName = getPageNameOrDefault(request, "FrontPage");
    loadPage(pageName, context);
    return makePageResponse(context);
}

private String getPageNameOrDefault(Request request, String defaultPageName) {
    String pageName = request.getResource();
    if (StringUtil.isBlank(pageName))
        pageName = defaultPageName;
    return pageName;
}
```
- [DON'T]: Bury the called function at the top of the file or far away from where it is first used.

**Horizontal Alignment**
- [DO]: Leave declarations and assignments unaligned.
```java
private Socket socket;
private InputStream input;
private OutputStream output;
private Request request;
```
- [DON'T]: Pad spaces to align variable names or assignment operators.
```java
private Socket       socket;
private InputStream  input;
private OutputStream output;
private Request      request;
```

**Indentation and Collapsed Scopes**
- [DO]: Expand short functions and conditionals to fully indented forms.
```java
public String render() throws Exception {
    return "";
}

if (condition) {
    doSomething();
}
```
- [DON'T]: Collapse scopes onto a single line to save vertical space.
```java
public String render() throws Exception { return ""; }

if (condition) doSomething();
```

**Dummy Scopes**
- [DO]: Indent the semicolon on a new line so the empty scope is highly visible.
```java
while (dis.read(buf, 0, readBufferSize) != -1)
    ;
```
- [DON'T]: Hide the semicolon at the end of the loop declaration.
```java
while (dis.read(buf, 0, readBufferSize) != -1);
```