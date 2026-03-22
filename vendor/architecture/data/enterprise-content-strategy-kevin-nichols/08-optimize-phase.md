# @Domain
Trigger these rules when the AI is tasked with content performance evaluation, analytics review, content auditing, content lifecycle optimization, or updating content strategy and planning calendars based on post-publishing data.

# @Vocabulary
- **Optimize Phase**: The final phase in the content plan lifecycle designed to ensure content remains relevant, contextual, and timely by determining whether to optimize, leave as is, or archive it.
- **Closed-Loop Lifecycle**: A continuous, performance-driven framework where published content is measured, analyzed, and the resulting data feeds directly back into future content planning.
- **As-Is Content**: Content that performs satisfactorily (meets or nearly meets objectives) and requires no immediate attention, though it still possesses a "shelf life" requiring periodic reassessment.
- **Exceptionally Well-Performing Content**: Content that exceeds expectations (e.g., high reads, downloads, social shares, conversions, or sales) and serves as a model for future investment.
- **Point of Entry**: The method and origin of a visitor's arrival to the content (e.g., journey step, keyword search, social media link).
- **Engagement**: The measurement of how a user interacts with the content, including conversion rates, duration of interaction, platform used, and specific user actions.
- **Social Relevance**: The measurement of content's impact on social media, including shareability, trending status, and consumer sentiment.
- **Unpublish**: The act of removing content from digital consumption or public access (e.g., removing a page from a website).
- **Archive / Sunset**: The process of retiring content that has run its course or proven ineffective, ensuring it is recorded and stored securely to meet legal and organizational requirements.
- **Content Planning Process**: A monthly or quarterly operational model where analytical findings and metrics dictate the focus areas (optimize, delete, archive) and update the content calendar.

# @Objectives
- The AI MUST categorize all analyzed content into one of three distinct action states: Optimize, Leave As Is, or Archive/Sunset.
- The AI MUST extract actionable insights from both high-performing and low-performing content to systematically fuel the ongoing content calendar.
- The AI MUST safeguard business and legal integrity by strictly adhering to preservation rules for unpublished content.
- The AI MUST apply a standardized, multi-tiered diagnostic framework to uncover the root causes of poor content performance.

# @Guidelines
- **High-Performing Content Handling**: 
  - The AI MUST NOT recommend changing, rewriting, or moving exceptionally well-performing content. 
  - The AI MUST recommend syndicating, elevating (e.g., moving to the homepage), or developing supplementary stories around well-performing content.
  - When recommending the addition of high-performing content to new areas, the AI MUST explicitly mandate the use of SEO best practices, such as adding a summary or a tag-line lead-in to prevent negative audience reactions.
- **Evaluation Criteria**: The AI MUST evaluate the success or failure of any content piece using five specific vectors: Point of Entry, Topics within the content, Social Relevance, Engagement, and Competition.
- **Cross-Disciplinary Input**: When assessing performance, the AI MUST recommend involving analytics, usability, social, and SEO subject matter experts in the diagnostic conversation.
- **Poor-Performing Content Handling**: 
  - If the content has low business value or no repercussions for removal, the AI MUST recommend removing it or relocating it to lower-priority digital real estate.
  - If the content is high-priority, the AI MUST execute a strict 6-step diagnostic sequence (see Workflow) before recommending any edits.
- **Archiving and Legal Compliance**: 
  - The AI MUST NEVER recommend the permanent, unrecorded deletion of content.
  - The AI MUST mandate that all unpublished content be archived in a searchable database or secured third-party environment.
  - The AI MUST flag archived content for legal compliance review, citing regulations such as the Sarbanes-Oxley Act, which requires the retention of internal and external communications.
- **Frequency of Review**: The AI MUST specify that content reviews and planning meetings occur at least quarterly or monthly (and in some cases, weekly).

# @Workflow
When tasked with evaluating published content or generating an optimization strategy, the AI MUST follow this algorithmic process:

1. **Categorization**:
   - Assess the content's performance metrics against its stated objectives.
   - Categorize the content as: 
     - *Leave As Is* (meets objectives)
     - *Optimize - High* (exceeds objectives)
     - *Optimize - Low* (fails to meet objectives)
     - *Archive* (ineffective, seasonal, or expired shelf life).

2. **Analysis by Category**:
   - **For "Leave As Is"**: Log the content's current shelf life and schedule a date for the next periodic reassessment (quarterly or semiannually).
   - **For "Optimize - High"**: Analyze the 5 success vectors (Point of Entry, Topics, Social Relevance, Engagement, Competition). Generate recommendations to replicate this success in other product lines and propose supplementary content investments.
   - **For "Optimize - Low" (High-Priority Content)**: Execute the 6-Step Diagnostic:
     1. *Check Visibility*: Does it receive any visitors? Is it hidden in navigation or buried on a long scrolling page?
     2. *Check Engagement*: Do users view briefly and leave? Is the format inappropriate for the device (e.g., long-form on mobile, PDF vs. HTML)?
     3. *Check Journey/Conversion*: Does it fail to drive the user to the next step? (If yes, reassess user/consumer journeys).
     4. *Check Suitability*: Is it well-written, on-brand, relevant, and free from errors?
     5. *Check Objectives*: Are the organization's goals for this content unrealistic?
     6. *Check Competition/Testing*: How do competitors handle this topic? (Recommend A/B or usability testing).
   - **For "Archive"**: Generate an unpublishing directive that includes strict instructions for database storage, legal review, and compliance mapping.

3. **Strategic Integration (The Planning Process)**:
   - Compile all insights from Step 2 into a "Performance Findings Report."
   - Translate findings into concrete project initiatives (e.g., "Create 3 new videos based on high-performing Topic X").
   - Output an updated Content Calendar reflecting the new priorities derived from the closed-loop feedback.

# @Examples (Do's and Don'ts)

**Principle: Handling Exceptionally Well-Performing Content**
- [DO]: "The Q3 User Guide is exceeding conversion objectives by 40%. **Recommendation**: Leave the existing page URL and core text exactly as is. Elevate its visibility by placing a link on the homepage with a new summary tag-line. Commission three new supplementary articles exploring the topics covered in the guide."
- [DON'T]: "The Q3 User Guide is performing exceptionally well. **Recommendation**: Move the content directly to the homepage and rewrite the introduction to make it punchier to capture even more traffic." *(Anti-pattern: Moving or altering high-performing content disrupts SEO and risks negative audience reactions).*

**Principle: Handling Low-Performing High-Priority Content**
- [DO]: "The 'Enterprise Features' landing page is failing to convert. Initiating 6-step diagnostic: 1. Visibility is high (10k visits). 2. Engagement is low (users abandon after 5 seconds). 3. Format issue detected: The content is served as a dense PDF instead of responsive HTML. **Recommendation**: Convert PDF to mobile-friendly HTML to fix engagement drop-off."
- [DON'T]: "The 'Enterprise Features' landing page is failing to convert. **Recommendation**: Delete the page and write a new one." *(Anti-pattern: Recommending immediate deletion without running the step-by-step diagnostic to determine WHY it failed).*

**Principle: Archiving and Sunset Procedures**
- [DO]: "The 2023 Holiday Campaign content has expired. **Recommendation**: Unpublish the pages from the live site. Transfer all text and multimedia assets to the secure internal database for archival to comply with Sarbanes-Oxley requirements. Retain a record even if no immediate use is foreseen."
- [DON'T]: "The 2023 Holiday Campaign content has expired. **Recommendation**: Permanently delete the pages from the CMS to free up server space." *(Anti-pattern: Deleting content without archiving violates legal compliance rules and enterprise governance).*