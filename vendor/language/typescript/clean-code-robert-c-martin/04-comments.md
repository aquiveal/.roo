# @Domain
These rules MUST be triggered whenever the AI is writing, modifying, reviewing, analyzing, or refactoring code, specifically when dealing with code documentation, inline comments, Javadocs, or any natural language explanations placed within source files.

# @Vocabulary
- **Truth Source:** The code itself. Only the code can truly dictate what it does; comments are inherently prone to becoming lies as code evolves.
- **Expressive Code:** Code that is written so clearly, using well-named functions and variables, that it requires no comments to explain its intent or mechanics.
- **Cruft / Orphaned Comment:** A comment that has become obsolete, inaccurate, or separated from the code it originally described.
- **Journal Comment:** A running log of changes, dates, and authors maintained at the top of a source file.
- **Noise Comment:** A comment that restates the obvious, adds no new information, or simply satisfies an arbitrary formatting rule.
- **Mumbling:** A hastily written, vague comment that serves only as the programmer talking to themselves and requires reading other modules to decipher.
- **Position Marker:** Visual banners or ASCII art (e.g., `// Actions /////////////`) used to group code.
- **Amplification Comment:** A legitimate comment used to highlight the importance of a seemingly trivial line of code.

# @Objectives
- Treat every comment as a failure to express intent through code. The primary goal is to minimize comment usage by maximizing code clarity.
- Ensure any surviving comments explain the *why* (intent, consequences, clarifications) rather than the *what* (mechanics).
- Ruthlessly eradicate all forms of bad comments, including redundancy, dead code, historical logs, and formatting noise.
- Prevent the creation or preservation of comments that are likely to become obsolete, misleading, or disconnected from the code they describe.

# @Guidelines

**Code over Commentary**
- The AI MUST NOT use a comment to explain poorly written code. Instead, the AI MUST clean, refactor, and rename the code until the comment becomes unnecessary.
- The AI MUST extract complex logical conditions into properly named boolean functions or explanatory variables rather than commenting the conditional logic.

**Acceptable (Good) Comments**
- **Legal/Corporate:** The AI MUST allow necessary copyright, authorship, or license statements at the top of files, but SHOULD reference external standard licenses rather than dumping full legal text where permitted.
- **Intent and Decisions:** The AI MAY write comments to explain the underlying business intent or architectural decision behind a block of code if the code alone cannot convey it.
- **Warnings:** The AI MAY write comments to warn future programmers of specific consequences (e.g., "Do not run unless you have time to kill", "This class is not thread-safe").
- **Amplification:** The AI MAY write comments to amplify the importance of a specific line of code that might otherwise be accidentally altered or removed (e.g., why a specific `trim()` is required).
- **TODOs:** The AI MAY use `// TODO` comments to mark planned work, but MUST NOT use them as an excuse to leave broken or messy code in the current implementation.
- **Public API Documentation:** The AI MUST write detailed, accurate Javadocs (or equivalent) for public APIs, ensuring they do not contain misleading or obsolete information.

**Prohibited (Bad) Comments**
- **Commented-Out Code:** The AI MUST unconditionally delete any commented-out code. It MUST NOT leave commented-out code "just in case." Version control is responsible for retaining history.
- **Redundancy & Noise:** The AI MUST NOT write comments that restate what the code clearly does (e.g., `i++; // increment i`). The AI MUST delete existing noise comments and useless Javadocs that provide zero added value.
- **Journaling & Bylines:** The AI MUST delete change logs, modification histories, and author bylines (`/* Added by Rick */`) from source files.
- **Mandated Comments:** The AI MUST ignore arbitrary rules that dictate every function or variable must have a comment.
- **Mumbling & Venting:** The AI MUST NOT write vague comments, internal monologues, or complaints (e.g., `// Give me a break!`).
- **Position Markers:** The AI MUST NOT use ASCII banners to mark sections of code, except in exceedingly rare cases where the benefit is overwhelmingly significant. Existing clutter markers MUST be deleted.
- **Closing Brace Comments:** The AI MUST NOT comment closing braces (e.g., `} // while`). If a block is deeply nested enough to seemingly require a closing comment, the AI MUST extract the block into a smaller function instead.
- **HTML in Comments:** The AI MUST NOT embed HTML tags in source code comments. Formatting is the responsibility of extraction tools, not the source file.
- **Nonlocal Information:** The AI MUST strictly constrain comments to the immediate, adjacent code. It MUST NOT describe system-wide defaults, distant configurations, or external behaviors in a local comment.
- **Too Much Information:** The AI MUST NOT include historical essays, excessive specification details (e.g., full RFC text), or irrelevant trivia in comments.
- **Inobvious Connections:** If the AI writes a comment, the connection between the comment and the code MUST be immediately obvious. A comment MUST NOT require its own explanation.
- **Nonpublic Javadocs:** The AI MUST NOT generate formal Javadoc/Docblock comments for internal, private, or non-public classes and functions.

# @Workflow
1. **Analyze the Codebase:** Scan the provided code for existing comments, Javadocs, and commented-out code blocks.
2. **Refactor First:** For any comment that explains *what* a block of code does, extract that block into a well-named function or explanatory variable. Delete the original comment.
3. **Purge Violations:** Sweep the file and aggressively delete:
   - Commented-out code.
   - Journal/history logs and author bylines.
   - Redundant comments and noisy Javadocs (e.g., `@param name The name`).
   - Closing brace markers and ASCII position banners.
   - HTML tags inside comments.
4. **Evaluate Survivors:** For every remaining comment, verify that it provides context the code absolutely cannot express (e.g., warnings, amplifications, legal text, public API documentation).
5. **Refine and Localize:** Ensure the surviving comments are grammatically correct, concise, directly adjacent to the code they reference, and do not contain nonlocal or excessive information.

# @Examples (Do's and Don'ts)

**Explaining Intent via Code**
- [DON'T]:
  ```java
  // Check to see if the employee is eligible for full benefits
  if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))
  ```
- [DO]:
  ```java
  if (employee.isEligibleForFullBenefits())
  ```

**Redundant / Noise Comments**
- [DON'T]:
  ```java
  /**
   * Returns the day of the month.
   *
   * @return the day of the month.
   */
  public int getDayOfMonth() {
      return dayOfMonth;
  }
  ```
- [DO]:
  ```java
  public int getDayOfMonth() {
      return dayOfMonth;
  }
  ```

**Warnings of Consequences**
- [DO]:
  ```java
  // SimpleDateFormat is not thread safe,
  // so we need to create each instance independently.
  SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z");
  ```

**Position Markers**
- [DON'T]:
  ```java
  // Actions //////////////////////////////////
  ```
- [DO]: (Simply group related functions logically or split them into a new class; remove the banner).

**Commented-Out Code**
- [DON'T]:
  ```java
  // InputStream resultsStream = formatter.getResultStream();
  // StreamReader reader = new StreamReader(resultsStream);
  // response.setContent(reader.read(formatter.getByteCount()));
  ```
- [DO]: (Delete the lines completely).

**Closing Brace Comments**
- [DON'T]:
  ```java
      } // try
      catch (IOException e) {
          System.err.println("Error:" + e.getMessage());
      } // catch
  } // main
  ```
- [DO]: (Shorten the function to avoid deep nesting, and remove the brace comments).

**Amplification**
- [DO]:
  ```java
  String listItemContent = match.group(3).trim();
  // the trim is real important. It removes the starting
  // spaces that could cause the item to be recognized
  // as another list.
  new ListItemWidget(this, listItemContent, this.level + 1);
  ```