# @Domain
These rules trigger when the AI is tasked with designing, implementing, or modifying data integration layers, message transformation logic, data mapping, message payload manipulation, B2B data exchange protocols, or message formatting architectures between disparate systems. 

# @Vocabulary
*   **Message Translator**: A general component that converts a message from one format to another to resolve differences between applications.
*   **Envelope Wrapper**: A component that wraps application data inside an envelope (adding headers, security credentials, or encryption) to comply with the messaging infrastructure, and unwraps it at the destination.
*   **Promotion**: The process of extracting specific data fields from a message payload and elevating them to the message header so routing components can read them without parsing or unwrapping the payload.
*   **Tunneling**: Encapsulating one protocol format inside another to pass through a specific infrastructure (e.g., wrapping a SOAP message inside another SOAP envelope to cross a trust boundary).
*   **Content Enricher**: A specialized transformer that accesses an external data source (via computation, environment variables, or another system/database) to augment a message with missing, required information.
*   **Content Filter**: A component that removes unimportant, redundant, or sensitive data items from a message, often flattening complex hierarchical structures into simple lists.
*   **Claim Check**: A pattern that reduces data volume by storing the full message payload in a persistent store and passing only a reference key (the Claim Check) to subsequent components.
*   **Normalizer**: A router-translator hybrid that inspects messages arriving in multiple different formats, determines their type, and routes them through specific Message Translators to produce a single, uniform format.
*   **Canonical Data Model (CDM)**: A unified data format independent of any specific application. All applications translate their internal formats to and from this universal format to minimize integration dependencies.
*   **Double Translation**: The process of translating a message twice (Source Format -> Canonical Data Model -> Target Format) to maintain loose coupling. 
*   **Direct Translation**: Translating directly from Source Format to Target Format. Only used when extreme performance requirements prohibit Double Translation.
*   **Metadata**: Data that describes the format and structure of the message payload (e.g., XSD, DTD).

# @Objectives
*   Minimize dependencies between integrating applications by ensuring no application is required to understand the internal data formats of another.
*   Prevent the "N-Square Problem" (exponential explosion of translators) by enforcing a Canonical Data Model for multi-system integrations.
*   Optimize network bandwidth and system performance by minimizing the payload size of messages traveling through intermediate steps.
*   Enhance security by filtering sensitive data before it leaves trust boundaries and by encrypting payloads within Envelope Wrappers.
*   Maintain the structural integrity of message routing by ensuring intermediate routers only read message headers, not payloads.

# @Guidelines

## General Transformation Rules
*   When integrating disparate systems that use different data formats, the AI MUST NOT modify the applications to use a common format. The AI MUST implement a **Message Translator** external to the applications.
*   The AI MUST separate actual data translation logic from domain logic to maximize reuse.

## Envelope Wrapper
*   When a messaging infrastructure requires specific headers, security credentials, or encryption, the AI MUST implement an **Envelope Wrapper** to encapsulate the raw application message.
*   When intermediate routers need to route a wrapped or encrypted message based on payload data, the AI MUST use **Promotion** to extract the routing fields from the payload and place them in the unencrypted message header before wrapping.
*   When crossing trust boundaries, the AI MUST chain multiple Envelope Wrappers (e.g., tunneling) to protect payload data.

## Content Enricher
*   When a target system requires data not present in the source message, the AI MUST implement a **Content Enricher** to fetch or compute the missing data.
*   The AI MUST implement the connection between the Content Enricher and the external data source using synchronous protocols (e.g., HTTP, ODBC) rather than asynchronous messaging, as the enricher must wait for the data to proceed.
*   When processing large external standards (e.g., ebXML, RosettaNet), the AI MUST keep internal messages small and use a Content Enricher to append required fields just before the message exits the enterprise.

## Content Filter
*   When passing messages containing sensitive data (e.g., SSN, payroll info) to less-privileged services or external parties, the AI MUST implement a **Content Filter** to strip the sensitive fields.
*   When an incoming message has a deeply nested hierarchical structure (like a normalized database schema dump) but the consumer requires a simple format, the AI MUST use a Content Filter to flatten the hierarchy.

## Claim Check
*   When a message contains a large data payload that is not needed by intermediate routing steps, the AI MUST implement a **Claim Check** to store the payload in a persistent store (database, file system) and pass only a reference key through the messaging system.
*   When selecting a key for the Claim Check, the AI MUST NOT use the infrastructure-generated Message ID. Message IDs can change when messages are re-published, causing data retrieval to fail. The AI MUST use a generated abstract unique ID or a specific business key.
*   When using a Claim Check, the AI MUST define a garbage collection strategy (e.g., delete-on-read, or expiration timestamps) to prevent the persistent store from filling up with orphaned payload data.
*   When interacting with untrusted external parties, the AI MUST use a Claim Check to store sensitive data internally, send a reference key to the external party, and use a Content Enricher to retrieve and merge the sensitive data when the response returns.

## Normalizer
*   When receiving semantically equivalent data from multiple external partners in various formats (e.g., CSV, XML, EDI), the AI MUST implement a **Normalizer**.
*   The AI MUST implement detection logic in the Normalizer to determine the message type. If no explicit type header exists, the AI MUST inspect the XML root element, use XPath expressions, or evaluate file names/folder structures to determine the type.

## Canonical Data Model (CDM)
*   When integrating three or more applications, the AI MUST design a **Canonical Data Model** rather than creating direct point-to-point translators. 
*   The AI MUST restrict the scope of the Canonical Data Model to ONLY the data that actively participates in messaging. The AI MUST NOT attempt to model the entire enterprise data structure.
*   The AI MUST default to **Double Translation** (Source -> CDM -> Target) for all mappings. The AI MAY use **Direct Translation** (Source -> Target) ONLY if strict, explicitly stated performance/latency constraints override maintainability.

# @Workflow
When tasked with integrating systems with differing data formats, the AI MUST execute the following steps:
1.  **Analyze Data Discrepancy**: Identify the exact structural, syntactical, and semantic differences between the source and target formats.
2.  **Determine CDM Necessity**: If the architecture involves 3 or more systems, define an XML/JSON schema representing the Canonical Data Model for the exchanged data.
3.  **Apply Simplification (Filter/Claim Check)**: If the source payload is excessively large or contains sensitive/irrelevant data, inject a Content Filter (to strip data) or a Claim Check (to store data).
4.  **Apply Translation**: Implement the Message Translator (or Messaging Mapper if inside custom application code) to transform the source data into the CDM (or directly to the target if only 2 systems exist).
5.  **Apply Enrichment**: If the target requires data unavailable in the source or the payload was reduced via a Claim Check, inject a Content Enricher right before the target to query the missing data.
6.  **Apply Wrapping**: If the messaging infrastructure requires specific headers, routing tags, or encryption, apply an Envelope Wrapper immediately before putting the message on the channel.

# @Examples (Do's and Don'ts)

## Claim Check Keys
- **[DO]** Generate a unique, abstract identifier for a Claim Check and store it in a dedicated payload field.
```json
{
  "event": "OrderPlaced",
  "claimCheckId": "550e8400-e29b-41d4-a716-446655440000"
}
```
- **[DON'T]** Reuse the transport-layer Message ID as the Claim Check key, as it violates separation of concerns and breaks if the message is re-routed or duplicated.
```json
{
  "event": "OrderPlaced",
  "claimCheckId": "header.JMSMessageID" 
}
```

## Content Filtering (Flattening)
- **[DO]** Use a Content Filter to flatten deep, database-style hierarchies into consumer-friendly flat structures.
```xml
<!-- Output of Content Filter -->
<Customer>
    <Name>Joe Doe</Name>
    <Street>123 Main St</Street>
    <City>San Francisco</City>
    <Phone>415-555-1234</Phone>
</Customer>
```
- **[DON'T]** Pass deeply nested, normalized database representations directly to consumers who only need a flat summary.
```xml
<!-- Avoid passing this unaltered -->
<Customer>
    <Id>123</Id>
    <Name>Joe Doe</Name>
    <Customer_Address_Link>
        <Address_Id>456</Address_Id>
    </Customer_Address_Link>
    <Address>
        <Id>456</Id>
        <Street>123 Main St</Street>
        <City>San Francisco</City>
    </Address>
    <!-- ... -->
</Customer>
```

## Envelope Wrapper (Promotion)
- **[DO]** Promote routing fields to the envelope header so the messaging infrastructure can route without parsing the body.
```xml
<Envelope>
    <Header>
        <RouteToRegion>US-West</RouteToRegion> <!-- Promoted Field -->
    </Header>
    <Body>
        <EncryptedPayload>...</EncryptedPayload>
    </Body>
</Envelope>
```
- **[DON'T]** Force the messaging router to decrypt or deeply parse the payload just to make a routing decision.

## Canonical Data Model Translation
- **[DO]** Implement Double Translation to isolate systems from one another.
```python
// App A format to Canonical
CanonicalOrder cOrder = Translator.AppAToCanonical(appAOrder);
// Canonical to App B format
AppBOrder bOrder = Translator.CanonicalToAppB(cOrder);
```
- **[DON'T]** Hardcode App B's format requirements directly into App A's export logic, creating tight coupling.
```python
// BAD: Tight coupling
AppBOrder bOrder = appA.ExportToAppBFormat();
```