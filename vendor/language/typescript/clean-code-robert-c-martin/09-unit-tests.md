@Domain
This rule file is activated whenever the AI is instructed to write, read, review, refactor, or architect unit tests, integration tests, or any automated testing scripts. It also applies whenever the user invokes Test-Driven Development (TDD) workflows or asks the AI to evaluate the quality, structure, or coverage of existing test code.

@Vocabulary
- **The Three Laws of TDD**: The foundational rigid cycle of Test-Driven Development dictating the precise order of writing failing tests, writing minimal production code, and refactoring.
- **Test Rot**: The degradation of test code quality over time caused by the "quick and dirty" mentality, eventually resulting in tests becoming a maintenance liability and being abandoned.
- **The -ilities**: The architectural qualities (flexibility, maintainability, reusability) that are exclusively enabled and protected by a comprehensive, clean suite of unit tests.
- **BUILD-OPERATE-CHECK**: A structural pattern for unit tests dividing them into three clear states: building the test data, operating on that data, and checking the results. Synonymous with the Given-When-Then convention.
- **Domain-Specific Testing Language**: A specialized, highly readable API of utility functions and wrappers created specifically within the test suite to hide low-level setup/teardown details and express test intent clearly.
- **The Dual Standard**: The principle that test code must be as clean, simple, and expressive as production code, but does *not* need to adhere to the same stringent CPU or memory efficiency standards.
- **Single Concept per Test**: The principle that a single test function must evaluate only one logical concept or behavior, rather than chaining multiple independent checks together.
- **F.I.R.S.T.**: An acronym defining the five essential traits of clean tests: Fast, Independent, Repeatable, Self-Validating, and Timely.

@Objectives
- Treat test code as a first-class citizen; the AI must apply the exact same (if not higher) levels of design, care, and cleanliness to test code as it does to production code.
- Prevent "Test Rot" by actively refactoring messy, brittle, or overly complex test setups into a clean Domain-Specific Testing Language.
- Maximize test readability above all other metrics, utilizing clarity, simplicity, and high density of expression.
- Eradicate the fear of changing code by ensuring the generated test suite acts as an impenetrable safety net that clearly expresses the system's intended behavior.

@Guidelines

**1. The Three Laws of TDD**
- The AI MUST strictly enforce the 30-second TDD cycle when generating new features:
  - **Law 1**: The AI MUST NOT write any production code before writing a failing unit test.
  - **Law 2**: The AI MUST NOT write more of a unit test than is sufficient to fail (compilation failures count as failing).
  - **Law 3**: The AI MUST NOT write more production code than is sufficient to pass the currently failing test.

**2. Keeping Tests Clean**
- The AI MUST actively reject the "quick and dirty" testing mentality. If asked to write a "quick test just to get coverage," the AI MUST output clean, fully refactored test code regardless.
- The AI MUST continuously refactor test code as production code evolves to ensure tests do not become tangled or brittle.

**3. Test Structure and Readability**
- The AI MUST format every single test using the **BUILD-OPERATE-CHECK** (Given-When-Then) pattern.
- The AI MUST cleanly separate these three phases using whitespace or explicit method calls.
- The AI MUST eliminate distracting details, strange strings, and irrelevant API calls from the test body. Tests must read like well-written prose.

**4. Domain-Specific Testing Language**
- The AI MUST NOT force the reader to parse low-level production APIs within the test body.
- The AI MUST extract complex setup logic, object instantiation, and multi-step assertions into private helper methods with highly descriptive names (e.g., `makePages()`, `assertResponseIsXML()`).

**5. The Dual Standard**
- The AI MUST prioritize readability over efficiency in test code.
- If a less efficient operation (e.g., heavy string concatenation, redundant object creation) makes the test significantly easier to read and understand, the AI MUST choose the readable, less efficient approach.

**6. Assertions and Concepts**
- The AI MUST strive for one assert per test, or at minimum, minimize the number of asserts per test.
- The AI MUST enforce a **Single Concept per Test**. If a test checks multiple independent edge cases or sequenced behaviors, the AI MUST split it into multiple, independent test functions.

**7. F.I.R.S.T. Principles**
- **Fast**: The AI MUST NOT generate tests that inherently run slowly (e.g., avoid arbitrary `Thread.sleep()` or heavy network calls where mocks/stubs can be used).
- **Independent**: The AI MUST NOT write tests that depend on the state mutated by a previous test. Every test must set up and tear down its own state.
- **Repeatable**: The AI MUST ensure tests can run in any environment (production, QA, disconnected local machine) without failure.
- **Self-Validating**: The AI MUST use explicit assertions (booleans/assertions) that strictly pass or fail. The AI MUST NOT output tests that require a developer to manually read a log or compare files.
- **Timely**: The AI MUST generate the tests immediately before generating the production code that satisfies them.

@Workflow
When tasked with writing or refactoring code and tests, the AI MUST execute the following algorithmic process:

1. **Requirement Analysis**: Identify the specific, minimal behavior required.
2. **Timely Test Generation (Law 1 & 2)**: Write a single, focused test method targeting one concept. Leave the production code unimplemented (or mocked) so the test fails.
3. **Structure Enforcement**: Organize the test explicitly into BUILD (Given), OPERATE (When), and CHECK (Then) sections.
4. **Production Code Implementation (Law 3)**: Write the absolute minimum production code required to make the test pass.
5. **Readability Refactoring**:
    - Scan the test for raw API calls, excessive parameters, or irrelevant data types.
    - Extract these into a Domain-Specific Testing Language (private helper methods).
    - Apply the Dual Standard: if making the test less CPU-efficient makes it easier to read, do it.
6. **Concept Verification**: Analyze the test to ensure it contains only one logical concept and minimal asserts. If multiple concepts are detected, split the test into distinct test functions.
7. **F.I.R.S.T. Audit**: Validate that the test is Fast, entirely Independent of other tests, Repeatable anywhere, and Self-Validating.

@Examples (Do's and Don'ants)

**Principle: BUILD-OPERATE-CHECK Structure & Domain-Specific Testing Language**

[DON'T] Write tests cluttered with low-level details and duplicate setups.
```java
public void testGetPageHierarchyAsXml() throws Exception {
    crawler.addPage(root, PathParser.parse("PageOne"));
    crawler.addPage(root, PathParser.parse("PageOne.ChildOne"));
    crawler.addPage(root, PathParser.parse("PageTwo"));

    request.setResource("root");
    request.addInput("type", "pages");
    Responder responder = new SerializedPageResponder();
    SimpleResponse response = (SimpleResponse) responder.makeResponse(new FitNesseContext(root), request);
    String xml = response.getContent();

    assertEquals("text/xml", response.getContentType());
    assertTrue(xml.contains("<name>PageOne</name>"));
    assertTrue(xml.contains("<name>PageTwo</name>"));
    assertTrue(xml.contains("<name>ChildOne</name>"));
}
```

[DO] Extract details into a Domain-Specific Testing Language and use Given-When-Then structure.
```java
public void testGetPageHierarchyAsXml() throws Exception {
    // BUILD (Given)
    makePages("PageOne", "PageOne.ChildOne", "PageTwo");

    // OPERATE (When)
    submitRequest("root", "type:pages");

    // CHECK (Then)
    assertResponseIsXML();
    assertResponseContains(
        "<name>PageOne</name>", 
        "<name>PageTwo</name>", 
        "<name>ChildOne</name>"
    );
}
```

**Principle: Single Concept per Test**

[DON'T] Chain multiple independent concepts and chronological steps into a single, long test function.
```java
public void testAddMonths() {
    // Concept 1: 31-day month to 30-day month
    SerialDate d1 = SerialDate.createInstance(31, 5, 2004);
    SerialDate d2 = SerialDate.addMonths(1, d1);
    assertEquals(30, d2.getDayOfMonth());
    assertEquals(6, d2.getMonth());

    // Concept 2: 31-day month to 31-day month
    SerialDate d3 = SerialDate.addMonths(2, d1);
    assertEquals(31, d3.getDayOfMonth());
    assertEquals(7, d3.getMonth());

    // Concept 3: Nested additions
    SerialDate d4 = SerialDate.addMonths(1, SerialDate.addMonths(1, d1));
    assertEquals(30, d4.getDayOfMonth());
    assertEquals(7, d4.getMonth());
}
```

[DO] Split into distinct tests, each validating a single concept.
```java
public void testAddingOneMonthTo31DayMonthYields30DayMonth() {
    SerialDate may31 = SerialDate.createInstance(31, 5, 2004);
    SerialDate june30 = SerialDate.addMonths(1, may31);
    assertEquals(30, june30.getDayOfMonth());
    assertEquals(6, june30.getMonth());
}

public void testAddingTwoMonthsTo31DayMonthYields31DayMonth() {
    SerialDate may31 = SerialDate.createInstance(31, 5, 2004);
    SerialDate july31 = SerialDate.addMonths(2, may31);
    assertEquals(31, july31.getDayOfMonth());
    assertEquals(7, july31.getMonth());
}
```

**Principle: The Dual Standard (Readability over Efficiency in Tests)**

[DON'T] Write tedious, eye-bouncing assertions just to save CPU cycles or string allocations in a test.
```java
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
    hw.setTemp(WAY_TOO_COLD);
    controller.tic();
    assertTrue(hw.heaterState());
    assertTrue(hw.blowerState());
    assertFalse(hw.coolerState());
    assertFalse(hw.hiTempAlarm());
    assertTrue(hw.loTempAlarm());
}
```

[DO] Create an expressive, albeit technically inefficient (e.g., using heavy string concatenation behind the scenes), representation of state that can be parsed instantly by a human reader.
```java
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
    wayTooCold();
    assertEquals("HBchL", hw.getState()); // Upper case = on, lower case = off
}
```