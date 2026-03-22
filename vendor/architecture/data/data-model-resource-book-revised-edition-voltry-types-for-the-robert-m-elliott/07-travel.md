@Domain
These rules MUST trigger when the AI is tasked with data modeling, database design, software architecture, or querying for travel industry organizations. This includes enterprises involved in transporting passengers (airlines, train stations, bus depots, cruise lines) or accommodating travelers (hotels, car rental agencies, travel agencies, and full-service travel conglomerates). 

@Vocabulary
- **TRAVELER**: An individual who is planning on taking a trip or has taken trips.
- **INDIVIDUAL PAYER**: A person responsible for paying for travel.
- **TRAVEL ACCOUNT MEMBER**: An individual holding an account used to accumulate award points for free or discounted travel.
- **TRAVEL PROVIDER**: Organizations providing transportation or accommodations (subtyped into TRAVEL CARRIER, HOTEL PROVIDER, CAR RENTAL PROVIDER).
- **TRAVEL PORT AUTHORITY**: The organization managing travel facilities where embarkation and disembarkation occur.
- **DISTRIBUTION CHANNEL**: Organizations that sell passenger travel tickets (e.g., TRAVEL AGENCY).
- **TRAVEL PREFERENCE**: Specific accommodation desires expressed by a PARTY (e.g., non-smoking, coach seating, kosher meal).
- **TRAVEL PRODUCT**: The supertype for all travel offerings (subtyped into PASSENGER TRANSPORTATION OFFERING, HOTEL OFFERING, RENTAL CAR OFFERING, AMENITIES OFFERING, ITEM OFFERING).
- **PASSENGER TRANSPORTATION OFFERING**: A product defined by origin, destination, and regularly scheduled travel times.
- **SCHEDULED TRANSPORTATION**: A specific occurrence of a transportation offering on a specific date/time using a specific TRANSPORTATION VEHICLE.
- **ACCOMMODATION MAP**: The specification of spaces available for each class within a TRANSPORTATION VEHICLE or HOTEL.
- **SCHEDULED TRANSPORTATION OFFERING**: The specific seats or capacities available within certain ACCOMMODATION CLASSES on a SCHEDULED TRANSPORTATION.
- **RESERVATION**: The travel industry equivalent of an order, containing a header and multiple RESERVATION ITEMs.
- **ACCOMMODATION SPOT**: A specific reserved spot (SEAT NUMBER or ROOM NUMBER) corresponding to an ACCOMMODATION MAP.
- **TICKET**: A proof of payment and means to redeem travel, composed of one or more COUPONs.
- **COUPON**: A component of a ticket corresponding to a specific RESERVATION ITEM (e.g., a specific leg of a flight).
- **TRAVEL EXPERIENCE**: The transaction used to track the delivery of travel services to a TRAVELER.
- **TRAVEL EXPERIENCE EVENT**: All "touch points" in a traveler's journey (e.g., BAGGAGE HANDLING, TICKETING, CHECK IN, BOARDING).

@Objectives
- Accurately map complex travel networks including people, organizations, distribution channels, and travel partners.
- Implement highly granular travel product hierarchies that separate abstract scheduled offerings from specific, vehicle-bound scheduled transportation instances.
- Translate standard "order" concepts into travel-specific "reservation" and "ticketing" structures, enforcing up-front payment and coupon compilation rules.
- Replace tangible "shipment" delivery models with experiential tracking models (Travel Experience and Travel Experience Events) to record traveler touchpoints and satisfaction.
- Model dynamic travel incentive programs (Travel Accounts) that accumulate points based on programmatic rules, factors, and travel activity.
- Design analytical star schemas that differentiate performance metrics between transportation offerings (which require timing metrics) and non-transportation offerings (which do not).

@Guidelines
- **Party Roles & Relationships**:
  - The AI MUST subtype `PERSON ROLE` into `INDIVIDUAL CUSTOMER` (further subtyped to `PASSENGER`, `INDIVIDUAL PAYER`, `TRAVEL ACCOUNT MEMBER`), `TRAVELER`, `TRAVEL STAFF`, and `OPERATIONS CREW`.
  - The AI MUST subtype `ORGANIZATION ROLE` into `TRAVEL PROVIDER` (`TRAVEL CARRIER`, `HOTEL PROVIDER`, `CAR RENTAL PROVIDER`), `TRAVEL PORT AUTHORITY`, `DISTRIBUTION CHANNEL`, `TRAVEL PARTNER`, `TRAVEL ASSOCIATION`, and `REGULATORY AGENCY`.
- **Travel Preferences**:
  - The AI MUST maintain `TRAVEL PREFERENCE` at the `PARTY` level to track ongoing choices (linked to `TRAVEL PREFERENCE TYPE`, `ACCOMMODATION CLASS`, or `TRAVEL PRODUCT`).
  - The AI MUST allow general preferences to be overridden at the time of booking using the `RESERVATION PREFERENCE` entity.
- **Travel Products**:
  - The AI MUST NOT treat travel offerings as standard discrete inventory items.
  - The AI MUST relate a `PASSENGER TRANSPORTATION OFFERING` to two `FACILITY` entities representing origin and destination, and to `REGULARLY SCHEDULED TIME`.
  - The AI MUST define a `SCHEDULED TRANSPORTATION` as a specific date/time occurrence utilizing a `TRANSPORTATION VEHICLE` that contains an `ACCOMMODATION MAP`.
- **Reservations**:
  - The AI MUST replace standard `ORDER` and `ORDER ITEM` entities with `RESERVATION` and `RESERVATION ITEM`.
  - The AI MUST link a `RESERVATION ITEM` to an `ACCOMMODATION SPOT` (e.g., `ROOM NUMBER`, `SEAT NUMBER`) generated from the `ACCOMMODATION MAP`.
  - When multiple travelers share a single reservation item (e.g., lap child, shared hotel room), the AI MUST use the `RESERVED TRAVELER` entity to associate multiple individuals to the `RESERVATION ITEM`.
- **Ticketing & Payments**:
  - The AI MUST construct a `TICKET` out of one or more `COUPON`s.
  - The AI MUST relate each `COUPON` to a `RESERVATION ITEM`.
  - The AI MUST structure price breakdowns using `COUPON COMPONENT` and `TICKET COMPONENT` entities.
  - The AI MUST group `TICKET`s under a `SALE` entity, which is then paid via a `PAYMENT APPLICATION`.
- **Agreements**:
  - The AI MUST subtype `AGREEMENT` into `CORPORATE TRAVEL AGREEMENT`, `DISTRIBUTION CHANNEL AGREEMENT`, `PARTNERSHIP AGREEMENT`, and `TRAVELER AGREEMENT`.
  - The AI MUST link agreements and products to `PRICE COMPONENT`s to determine the pricing of a `RESERVATION ITEM` or `TICKET`.
- **Delivery (Travel Experience)**:
  - The AI MUST NOT use `SHIPMENT` entities to model the delivery of travel services. 
  - The AI MUST use the `TRAVEL EXPERIENCE` entity, related to a single `TRAVELER`, and optionally related to a `RESERVATION ITEM`, `TICKET`, or `COUPON`.
  - The AI MUST record granular touchpoints using `TRAVEL EXPERIENCE EVENT` (subtyped into `CHECK IN`, `BOARDING`, `BAGGAGE HANDLING`, etc.).
  - The AI MUST include `SATISFACTION RATING` and `TRAVELER FEEDBACK` (`COMMUNICATION EVENT`) linked to the experience or event.
- **Travel Programs**:
  - The AI MUST structure travel incentives using a `TRAVEL PROGRAM` governed by `TRAVEL PROGRAM RULE`s and `TRAVEL PROGRAM FACTOR`s.
  - The AI MUST capture earned points/amounts in `TRAVEL ACCOUNT ACTIVITY`, which MUST be linked to triggering events like `TRAVEL EXPERIENCE`, `SALE`, or `PAYMENT`.
- **Analytics (Star Schemas)**:
  - The AI MUST create a `TRANSPORTATION_OFFERING_FACT` table for passenger transportation featuring specific timing metrics: `number_of_on_time_arrivals`, `number_of_on_time_departures`, and `average_minutes_late`.
  - The AI MUST create a separate `TRAVEL_FACT` table for non-transportation products (hotels, car rentals) that EXCLUDES timing metrics, and uses a `TRAVEL_ACCOMMODATION_ASSETS` dimension instead of vehicles/facilities.

@Workflow
1. **Define Parties and Roles**: Establish the travel entities (`TRAVEL CARRIER`, `TRAVELER`, `INDIVIDUAL PAYER`) and record global `PARTY TRAVEL PREFERENCE`s.
2. **Structure Travel Products**: Define the abstract `PASSENGER TRANSPORTATION OFFERING`, then instantiate specific `SCHEDULED TRANSPORTATION` occurrences linked to specific `TRANSPORTATION VEHICLE`s and their `ACCOMMODATION MAP`s.
3. **Model the Reservation**: Create the `RESERVATION` header and `RESERVATION ITEM`s. Attach `RESERVED TRAVELER`s to items, override preferences via `RESERVATION PREFERENCE`, and reserve the `ACCOMMODATION SPOT`.
4. **Generate Tickets**: For paid/confirmed reservations, generate `COUPON`s linked to the reservation items, bundle them into a `TICKET`, assign `TICKET COMPONENT` costs, and associate with a `SALE` and `PAYMENT APPLICATION`.
5. **Track the Travel Experience**: Instantiate a `TRAVEL EXPERIENCE` for the traveler. Record each `TRAVEL EXPERIENCE EVENT` (check-in, boarding, baggage handling) along with associated `SATISFACTION RATING`s.
6. **Apply Travel Programs**: Calculate points earned from the travel experience or sale based on `TRAVEL PROGRAM RULE`s and post them to the `TRAVEL ACCOUNT ACTIVITY`.
7. **Deploy Analytics**: Extract event and satisfaction data into the appropriate Star Schema (Transportation vs. Non-Transportation) for service level analysis.

@Examples (Do's and Don'ts)

- **Products and Schedules**
  - [DO] Create a `PASSENGER TRANSPORTATION OFFERING` for "Flight 5489" and relate it to multiple `SCHEDULED TRANSPORTATION` records for October 2 and October 4, each specifying a physical `TRANSPORTATION VEHICLE` ID.
  - [DON'T] Model "Flight 5489" as a simple inventory item or single product instance without separating the abstract route schedule from the specific date/vehicle instance.

- **Reservations vs Orders**
  - [DO] Use `RESERVATION` and `RESERVATION ITEM` linked to a `SCHEDULED TRANSPORTATION OFFERING` and an `ACCOMMODATION SPOT` (e.g., Seat 12A). Use `RESERVED TRAVELER` to link multiple people (e.g., parents and a lap child) to the same seat item.
  - [DON'T] Use standard `ORDER` and `ORDER ITEM` entities, and do not assume a one-to-one relationship between an order item and a traveler without an associative `RESERVED TRAVELER` entity.

- **Ticketing**
  - [DO] Link a `COUPON` to a specific flight leg (`RESERVATION ITEM`), combine multiple `COUPON`s into a round-trip `TICKET`, and break down the price using `TICKET COMPONENT` (e.g., base fare, port taxes, security fees).
  - [DON'T] Treat a ticket as a generic invoice line item. Do not merge the concept of the reservation item and the physical coupon/ticket.

- **Travel Experience (Delivery)**
  - [DO] Record the delivery of the service using `TRAVEL EXPERIENCE` linked to the traveler, and log a `TRAVEL EXPERIENCE EVENT` of type `BAGGAGE HANDLING` indicating the status progression of the baggage.
  - [DON'T] Use `SHIPMENT` or `SHIPMENT ITEM` entities to record a passenger taking a flight or staying in a hotel room.

- **Analytics**
  - [DO] Include `average_minutes_late` and `number_of_on_time_arrivals` measures in the `TRANSPORTATION_OFFERING_FACT` table, analyzed by `TRANSPORTATION_VEHICLES` dimensions.
  - [DON'T] Include on-time departure or arrival metrics in the `TRAVEL_FACT` star schema used for analyzing Hotel or Car Rental offerings.