# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, architecting, or implementing analytical data systems, online analytical processing (OLAP) models, business intelligence (BI) data pipelines, machine learning (ML) data feeds, or whenever transitioning from monolithic data architectures (Data Warehouses or Data Lakes) to a decentralized analytical architecture (Data Mesh).

# @Vocabulary
- **OLTP (Online Transactional Processing):** Operational systems optimized for real-time business transactions, modeled around business entities, requiring exact precision and strong data consistency.
- **OLAP (Online Analytical Processing):** Analytical systems optimized for providing insights, training ML models, and flexible querying, modeled around facts and dimensions using aggregated data.
- **Fact Table:** An append-only analytical data structure representing business activities that have already happened (the "verbs" of a process). Records are never deleted or modified.
- **Dimension Table:** A highly normalized analytical data structure describing the attributes of a fact (the "adjectives" to the fact's verb), designed to support flexible and dynamic querying.
- **Star Schema:** An analytical model utilizing a many-to-one relationship where a fact's foreign key points to a single, flat dimension record.
- **Snowflake Schema:** An analytical model where dimensions are multilevel and further normalized into finer-grained dimensions. Saves space but requires more computational resources (joins) to query.
- **Data Warehouse (DWH):** A traditional analytical architecture relying on Extract-Transform-Load (ETL) scripts to pull data from operational databases into a centralized enterprise-wide analytical model.
- **Data Lake:** An analytical architecture that ingests and stores operational data in its raw, schema-less form for later transformation.
- **Data Swamp:** A degraded Data Lake where schema-less ingestion and lack of quality control make data chaotic and unusable at scale.
- **Data Mesh:** A decentralized analytical data architecture applying Domain-Driven Design principles to OLAP data, based on four core principles: Decompose data around domains, Data as a product, Enable autonomy, and Build an ecosystem.
- **Data Product:** Analytical data treated as a first-class citizen, served through well-defined, versioned, discoverable output ports with Service-Level Agreements (SLAs).
- **Polyglot Data Endpoints:** Output ports serving the same analytical data product in multiple formats (e.g., SQL queries, object storage) to suit different consumers' needs.
- **Federated Governance Body:** A group of data/product owners and platform engineers enforcing rules to ensure a healthy, interoperable analytical data ecosystem.

# @Objectives
- The AI MUST distinctly separate operational (OLTP) modeling concerns from analytical (OLAP) modeling concerns.
- The AI MUST prevent the coupling of analytical data pipelines to the internal implementation schemas of operational databases.
- The AI MUST decentralize analytical data ownership, aligning it strictly with the boundaries of operational Bounded Contexts.
- The AI MUST treat analytical data as a first-class product, ensuring it is discoverable, schema-defined, versioned, and served via explicit output ports rather than direct database extraction.
- The AI MUST leverage Command-Query Responsibility Segregation (CQRS) and the Open-Host Service pattern to bridge operational transactions and analytical data products.

# @Guidelines
- **Analytical vs. Transactional Modeling:** When designing for analytics, the AI MUST NOT use entity-lifecycle operational models. The AI MUST design Fact tables (append-only activities) and Dimension tables (normalized attributes).
- **Fact Granularity:** The AI MUST define the granularity of Fact tables based strictly on the needs of data analysts (e.g., time-boxed snapshots vs. individual event records) rather than operational precision.
- **Schema Selection (Star vs. Snowflake):** The AI MUST explicitly evaluate the trade-off between query simplicity and storage optimization. Use Star schemas for faster, simpler queries; use Snowflake schemas if dimension storage optimization and maintenance ease outweigh the cost of complex joins.
- **Avoid Enterprise-Wide Models:** The AI MUST NOT design monolithic, enterprise-wide analytical models. Analytical models MUST be task-oriented and scoped to specific business boundaries.
- **Prevent Database Schema Coupling (Anti-DWH):** The AI MUST NOT design ETL scripts that directly extract data from an operational database's internal tables. This trespasses operational boundaries and creates fragile coupling.
- **Prevent Data Swamps (Anti-Data Lake):** The AI MUST NOT dump raw, schema-less data into a centralized repository without strict quality control, schemas, and designated ownership.
- **Domain-Aligned Ownership:** The AI MUST assign ownership of both the operational model and its resulting analytical model to the exact same Bounded Context (and therefore the same product team).
- **Implement Data as a Product:** The AI MUST design analytical data as a public API. This requires:
  - Well-defined, explicit output ports.
  - Defined and enforced schemas.
  - Explicit versioning (handling breaking changes).
  - Discoverability and SLA monitoring.
- **Polyglot Serving:** The AI MUST design Data Products to offer Polyglot Data Endpoints, allowing consumers to fetch data in their required format (e.g., SQL, flat files, object storage).
- **Enable Autonomy via Infrastructure:** The AI MUST abstract the complexity of data serving by relying on a unified data infrastructure platform, rather than building custom data-serving infrastructure per Bounded Context.
- **Apply CQRS for Data Mesh:** The AI MUST use the CQRS pattern to project operational data (Command execution model) into the analytical model (Read models), enabling multiple concurrent versions of an analytical schema if necessary.
- **Apply DDD Integration Patterns to Analytics:** The AI MUST use Open-Host Service to expose analytical models as a published language. If a consumer requires a different analytical model from the producer's Data Product, the AI MUST implement an Anticorruption Layer (ACL) or use Partnership/Separate Ways patterns.

# @Workflow
When tasked with designing or implementing an analytical data system, the AI MUST follow this exact sequence:

1. **Boundary Alignment (Decompose around Domains):**
   - Identify the operational Bounded Context responsible for the source data.
   - Assign ownership of the corresponding analytical model to this exact Bounded Context.
2. **Analytical Modeling (Facts & Dimensions):**
   - Analyze the analytical requirements.
   - Define the business activities as append-only Fact tables.
   - Define the descriptive attributes as normalized Dimension tables.
   - Choose between a Star or Snowflake schema based on storage vs. compute trade-offs.
3. **Projection Generation (CQRS Integration):**
   - Implement a CQRS projection engine to listen to the operational Bounded Context's state changes/domain events.
   - Transform the operational data into the modeled Fact and Dimension tables.
4. **Data Product Definition (Data as a Product):**
   - Define a strict, versioned schema for the resulting analytical data.
   - Create explicit Output Ports (Polyglot Data Endpoints) to serve the data (e.g., exposing a SQL endpoint and an S3 bucket endpoint).
5. **Governance & Integration:**
   - Ensure the Data Product complies with the Federated Governance rules for interoperability.
   - If other Bounded Contexts consume this data, define the integration pattern (e.g., Open-Host Service for the provider, ACL for the consumer).

# @Examples (Do's and Don'ts)

- **[DO]** Use CQRS to project an analytical Read Model from operational events, exposing it via a dedicated, versioned API endpoint.
```python
# The Bounded Context projects operational events into an analytical Read Model
class SupportCaseAnalyticalProjector:
    def handle_case_resolved_event(self, event):
        # Insert into append-only Fact table
        fact_db.insert("Fact_SolvedCases", {
            "case_id": event.case_id,
            "resolution_time_minutes": event.duration,
            "timestamp": event.timestamp,
            "agent_dimension_id": event.agent_id
        })

# Exposing Data as a Product via an explicit Output Port
@app.route("/api/analytical/v1/support/solved-cases", methods=["GET"])
def get_analytical_solved_cases():
    return jsonify(fact_db.query("Fact_SolvedCases"))
```

- **[DON'T]** Write an external ETL script that reaches directly into another team's operational database, creating tight coupling to implementation details.
```sql
-- ANTI-PATTERN: Centralized DWH bypassing Bounded Context boundaries
SELECT * INTO DWH_Fact_SolvedCases
FROM Operational_Support_DB.internal_tables.support_cases -- Direct coupling to internal operational schema!
WHERE status = 'Resolved';
```

- **[DO]** Model analytical data using append-only Fact tables and normalized Dimension tables (Star Schema).
```sql
-- Fact Table (Append-only, captures the activity)
CREATE TABLE Fact_CustomerOnboardings (
    fact_id UUID PRIMARY KEY,
    customer_dim_id UUID REFERENCES Dim_Customer(id),
    plan_dim_id UUID REFERENCES Dim_Plan(id),
    onboarding_duration_seconds INT,
    recorded_at TIMESTAMP
);

-- Dimension Table (Attributes, normalized for slicing/dicing)
CREATE TABLE Dim_Plan (
    id UUID PRIMARY KEY,
    plan_name VARCHAR,
    tier_level INT,
    price DECIMAL
);
```

- **[DON'T]** Attempt to use an operational entity-lifecycle model directly for deep analytical processing and historical metric aggregation.
```sql
-- ANTI-PATTERN: Using mutable operational tables for analytical historical analysis
UPDATE Users 
SET plan_name = 'Enterprise', last_updated = NOW() 
WHERE user_id = '123'; 
-- Loses the historical fact of when they were on the 'Pro' plan, ruining analytical accuracy.
```

- **[DO]** Expose analytical data as Polyglot endpoints to serve different consumer needs.
```json
// Data Product Metadata Definition
{
  "product_name": "SalesAnalytics",
  "version": "v2.1",
  "owner": "Sales_Bounded_Context",
  "endpoints": {
    "sql": "jdbc:postgresql://data-mesh.local/sales_analytics_v2",
    "object_storage": "s3://data-mesh-bucket/sales_analytics/v2/parquet/"
  },
  "sla": "99.9% uptime, data freshness < 5 minutes"
}
```

- **[DON'T]** Build a monolithic "Enterprise Data Warehouse" model intended to cover all use cases for the entire organization in a single unified schema.