# @Domain
These rules MUST trigger when the AI is tasked with designing, analyzing, or refactoring relational database schemas, logical data models, or data warehouse star schemas for Retail E-Commerce systems, web tracking applications, online storefronts, content management systems, web analytics engines, or internet-based subscription services.

# @Vocabulary
*   **AUTOMATED AGENT**: A non-human actor (e.g., spider, web server, crawler, bot) involved in internet transactions.
*   **CONSUMER**: A supertype role encompassing VISITOR, SUBSCRIBER, CUSTOMER, or PROSPECT.
*   **VISITOR**: A party navigating a web site. The exact identity (name) may be anonymous/unknown, but the party entity must still exist.
*   **REFERRER**: The source (e.g., search engine, affiliated site) that linked or directed a VISITOR to the enterprise's web site.
*   **ISP (Internet Service Provider)**: The organization providing internet access to the VISITOR.
*   **CONTACT MECHANISM LINK**: A gateway relationship allowing one contact mechanism to act as a routing address for another (e.g., an email-to-fax gateway).
*   **WEB CONTENT**: A modular piece of information (HTML page, text, article) residing at a WEB ADDRESS. 
*   **OBJECT**: A multimedia asset (IMAGE OBJECT, ELECTRONIC TEXT, OTHER OBJECT like a Java applet or audio clip) separated from the core product record, capable of being reused across multiple WEB CONTENT pages, PRODUCTs, or PRODUCT FEATUREs.
*   **PARTY NEED**: A specific desire or interest of a CONSUMER deduced via a SERVER HIT (e.g., clicking a product image) or stated via a COMMUNICATION EVENT.
*   **SUBSCRIPTION**: An opt-in agreement (e.g., newsletter, user group) associated with a SUBSCRIBER and fulfilled via SUBSCRIPTION FULFILLMENT PIECEs.
*   **SERVER HIT**: A single, granular request logged by a web server, encompassing data such as referring URL, IP ADDRESS, USER AGENT, and Authuser.
*   **VISIT**: A logical session comprising one or more SERVER HITs, defined by business rules (e.g., inactivity timeouts, common cookies/authusers).
*   **USER AGENT**: The mechanism/software (browser, platform, protocol, spider) used to generate a SERVER HIT.
*   **AUTHUSER**: The user ID captured in a web log when a visitor accesses a secured/protected directory.

# @Objectives
*   Establish scalable, highly relational data models for web-based commerce that treat the web not just as a brochure, but as an interactive distribution, support, and marketing channel.
*   Architect systems capable of tracking anonymous and known web visitors comprehensively.
*   Decouple multimedia assets (Objects) from Products to maximize reusability across online storefronts and catalogs.
*   Design robust Web Log analysis structures that differentiate between raw server requests (Hits) and logical user sessions (Visits).
*   Implement multidimensional star schemas that empower the enterprise to analyze web traffic, visitor demographics, content popularity, and conversion rates.

# @Guidelines
*   **Automated Agents Modeling**: The AI MUST model `AUTOMATED AGENT` as a subtype of `PARTY` (or as a closely related entity if legal accountability constraints forbid non-humans as parties) to track transactions involving web servers, FTP servers, and spiders.
*   **Anonymous Party Tracking**: The AI MUST make `name` attributes (e.g., first name, last name, organization name) OPTIONAL within the `PARTY` entity to support the anonymous nature of the web. The relationship between `PARTY ROLE` (e.g., VISITOR) and `PARTY` MUST remain mandatory, tracking anonymous users via system-generated IDs until their identity is discovered.
*   **E-Commerce Party Roles**: The AI MUST utilize roles specific to web architecture, including `WEBMASTER`, `ISP`, `HOSTING SERVER`, `REFERRER`, `SUBSCRIBER`, and `VISITOR`.
*   **E-Commerce Party Relationships**: The AI MUST track Internet relationships explicitly using `WEBMASTER ASSIGNMENT`, `HOST SERVER VISITOR`, and `VISITOR ISP` (to deduce which ISPs access which servers for targeted marketing).
*   **Contact Mechanism Extensions**: The AI MUST extend electronic addresses to include `WEB ADDRESS (URL)` and `IP ADDRESS`.
*   **Contact Mechanism Gateways**: The AI MUST implement a `CONTACT MECHANISM LINK` entity to handle routing gateways (e.g., an email address that forwards to a telecom fax number).
*   **Web Site Content Management**: The AI MUST decouple the structural page (`WEB CONTENT`) from its assets (`OBJECT`). A `WEB CONTENT ASSOCIATION` MUST be used to map objects to content, supporting metadata like layout coordinates (`upper left coordinate`) and functional behaviors (`FUNCTION TYPE` like scrolling lists).
*   **User Login Customization**: The AI MUST model `USER LOGIN` accounts associated with `WEB USER PREFERENCE` to drive customized look-and-feel (e.g., background color, preferred default views). Password/login changes MUST be tracked via `LOGIN ACCOUNT HISTORY`.
*   **Reusable E-Commerce Objects**: The AI MUST NOT hardcode images or text into Product tables. Multimedia assets MUST be stored in an `OBJECT` entity and linked via associative entities like `PRODUCT OBJECT`, `FEATURE OBJECT`, or `PARTY OBJECT`.
*   **Capturing Web Needs**: The AI MUST model `PARTY NEED` entities that can be generated directly from a `SERVER HIT` (e.g., clicking a specific car image generates a need record for that car type) or from direct `COMMUNICATION EVENTs`.
*   **Opt-In Subscriptions**: The AI MUST track explicit permission marketing via the `SUBSCRIPTION` entity, linked to `SUBSCRIPTION ACTIVITY` and discrete `SUBSCRIPTION FULFILLMENT PIECE`s (e.g., individual newsletter editions sent).
*   **Hit vs. Visit Granularity**: The AI MUST model `SERVER HIT` for individual atomic requests and `VISIT` for the logical session.
*   **Visit Definition Rules**: The AI MUST enforce the following 3 business rules when transforming Hits into Visits:
    1.  A `VISITOR` is always related to a `PARTY`, even if the Party identity is solely represented by an ID with no known name.
    2.  Visits MUST be demarcated by an inactivity time interval (e.g., 30 minutes between clicks) or an external referring URL indicating the user left and returned.
    3.  Visitors MUST be identified by a hierarchy of confidence: `AUTHUSER` (strongest), `COOKIE` (strong), and `IP ADDRESS` (weakest, due to dynamic IP assignment/NAT).
*   **Hit-Level Data Storage**: The AI MUST store `IP ADDRESS`, `REFERRING URL`, `USER AGENT` (Platform, Browser, Protocol, Method), `AUTHUSER`, and `STATUS CODE` at the `SERVER HIT` level, not the Visit level, as these can change or provide granular context per request.
*   **Server Hit Star Schema**: The AI MUST design analytics using a `SERVER_HIT_FACT` table with measures: `num_of_hits`, `num_of_bytes`, `num_of_visits`. Dimensions MUST include: `VISITORS`, `ISPS`, `REFERRERS`, `WEB_CONTENTS`, `USER_AGENT_TYPES`, `PRODUCTS`, and `TIME_BY_HOUR`.
*   **Web Visit Star Schema**: The AI MUST design visit-level analytics using a `WEB_VISIT_FACT` table with measures: `num_of_hits`, `num_of_pages_visited`, `num_of_products_inquired`, `num_of_products_ordered`, `num_of_visits_resulting_in_orders`, and `average_visit_time`.

# @Workflow
1.  **Party and Role Initialization**: When generating an e-commerce schema, first define the core `PARTY` entity ensuring name fields are nullable. Add roles for `VISITOR`, `REFERRER`, `ISP`, and `AUTOMATED AGENT`.
2.  **Contact Routing Configuration**: Extend contact mechanisms to include IPs and URLs. Map gateway capabilities using `CONTACT MECHANISM LINK`.
3.  **Content and Object Abstraction**: Create the `OBJECT` table for multimedia assets. Create the `WEB CONTENT` table. Build associative entities linking objects to content, products, and features.
4.  **Needs and Subscriptions Architecture**: Establish the `PARTY NEED` entity linked to `SERVER HIT`. Establish `SUBSCRIPTION` tables to track opt-in communication and fulfillment histories.
5.  **Traffic Logging Design**: Create the `SERVER HIT` table mapped to `USER AGENT` and `USER LOGIN`. Create the parent `VISIT` table. Ensure foreign keys support the 3 visit definition business rules.
6.  **Analytical Schema Generation**: Define the multidimensional Star Schemas (`SERVER_HIT_FACT` and `WEB_VISIT_FACT`) referencing the transactional web log tables to facilitate enterprise analysis of browsing, routing, and purchasing behaviors.

# @Examples (Do's and Don'ts)

## Anonymous Party Handling
*   **[DO]**:
    ```sql
    CREATE TABLE Party (
        party_id INT PRIMARY KEY,
        party_type VARCHAR(50) NOT NULL, -- 'PERSON', 'ORGANIZATION', 'AUTOMATED_AGENT'
        first_name VARCHAR(100) NULL,    -- Nullable to support anonymous visitors
        last_name VARCHAR(100) NULL,     -- Nullable
        organization_name VARCHAR(255) NULL
    );
    CREATE TABLE Party_Role (
        party_id INT NOT NULL,
        role_type VARCHAR(50) NOT NULL,  -- e.g., 'VISITOR'
        FOREIGN KEY (party_id) REFERENCES Party(party_id)
    );
    ```
*   **[DON'T]**:
    ```sql
    -- Incorrect: Forces a name, breaking when a web visitor has no cookies or login.
    CREATE TABLE Party (
        party_id INT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL, 
        last_name VARCHAR(100) NOT NULL
    );
    ```

## Decoupling Objects from Products
*   **[DO]**:
    ```sql
    CREATE TABLE Object (
        object_id INT PRIMARY KEY,
        object_type VARCHAR(50), -- 'JPEG', 'HTML', 'WAV'
        file_path VARCHAR(255)
    );
    CREATE TABLE Product_Object (
        product_id INT,
        object_id INT,
        usage_type VARCHAR(50), -- 'THUMBNAIL', 'HI_RES_ZOOM'
        PRIMARY KEY (product_id, object_id)
    );
    ```
*   **[DON'T]**:
    ```sql
    -- Incorrect: Hardcodes the image into the product, preventing reuse across brochures, web content, and features.
    CREATE TABLE Product (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(100),
        thumbnail_image_url VARCHAR(255),
        hi_res_image_url VARCHAR(255)
    );
    ```

## Web Visits vs. Server Hits
*   **[DO]**:
    ```sql
    CREATE TABLE Visit (
        visit_id INT PRIMARY KEY,
        visitor_party_id INT NOT NULL,
        visit_start_datetime DATETIME,
        visit_end_datetime DATETIME,
        cookie_string VARCHAR(255)
    );
    CREATE TABLE Server_Hit (
        hit_id INT PRIMARY KEY,
        visit_id INT NOT NULL,
        web_content_id INT,
        ip_address VARCHAR(50),
        referring_url VARCHAR(255),
        authuser_id INT NULL,
        hit_datetime DATETIME,
        FOREIGN KEY (visit_id) REFERENCES Visit(visit_id)
    );
    ```
*   **[DON'T]**:
    ```sql
    -- Incorrect: Flattens hits and visits, losing granular request data (like changing referrers or navigating multiple pages in one session).
    CREATE TABLE Web_Traffic (
        session_id INT PRIMARY KEY,
        ip_address VARCHAR(50),
        pages_viewed TEXT
    );
    ```

## Server Hit Analytics (Star Schema)
*   **[DO]**:
    ```sql
    CREATE TABLE Server_Hit_Fact (
        visitor_dim_id INT,
        isp_dim_id INT,
        referrer_dim_id INT,
        web_content_dim_id INT,
        user_agent_dim_id INT,
        product_dim_id INT,     -- Can be NULL/Empty Dimension if hit is non-product
        time_by_hour_dim_id INT,
        num_of_hits INT,
        num_of_bytes BIGINT,
        num_of_visits INT
    );
    ```
*   **[DON'T]**:
    ```sql
    -- Incorrect: Mixing transactional logging with analytical fact modeling, or missing the distinct dimensions required for web analytics.
    CREATE TABLE Hit_Analytics (
        hit_id INT,
        user_name VARCHAR(100),
        bytes_downloaded INT
    );
    ```