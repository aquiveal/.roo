# @Domain

This rule file activates when the user requests assistance with, creation of, or modifications to frontend frameworks (specifically React and Angular), backend database integrations, client-server API communication, or any DOM-manipulation in a TypeScript environment.

# @Vocabulary

- **JSX (JavaScript XML)**: A high-level, declarative Domain Specific Language (DSL) embedded straight into JavaScript code that compiles to regular JavaScript function calls (e.g., `React.createElement`).
- **TSX**: The TypeScript equivalent of JSX. It provides compile-time safety and assistance for JSX syntax and uses the `.tsx` file extension.
- **Function Component (React)**: A regular function that takes up to one parameter (the `props` object) and returns a React-renderable type (TSX, string, number, boolean, null, or undefined).
- **Class Component (React)**: A component declared by extending the `React.Component<Props, State>` base class.
- **Fragment**: A nameless TSX element (`<>...</>`) that wraps other TSX to avoid rendering extra unnecessary DOM elements.
- **AoT Compiler (Ahead-of-Time)**: Angular's built-in compiler that extracts TypeScript type annotations to compile code down to optimized JavaScript.
- **Dependency Injector (DI)**: Angular's mechanism for automatically instantiating services and passing them as arguments to components/services that depend on them.
- **Code-Generated APIs**: Tools (like Swagger, Apollo, gRPC) that rely on a common source of truth (schemas/models) to compile language-specific bindings, preventing client and server types from falling out of sync.
- **ORM (Object-Relational Mapper)**: A library (such as TypeORM) that generates code from database schemas to provide high-level, typesafe APIs for database queries, updates, and deletions.

# @Objectives

- Guarantee compile-time type safety across the entire stack, from the frontend view layer to the backend database.
- Enforce strict typing for React components, eliminating runtime type checking mechanisms like `PropTypes`.
- Ensure Angular applications leverage strict template checking and interface-driven lifecycle hooks.
- Eliminate manual type synchronization across client-server boundaries by mandating code-generated APIs.
- Prevent SQL injection and untyped data access by enforcing the use of ORMs for database interactions.

# @Guidelines

## DOM and Browser API Constraints
- The AI MUST ensure that the `tsconfig.json` file includes `"dom"` and `"es2015"` in the `compilerOptions.lib` array when utilizing DOM or browser APIs.

## React Constraints
- The AI MUST use the `.tsx` file extension for any file containing JSX.
- The AI MUST set `"jsx": "react"` in the `compilerOptions` of `tsconfig.json`.
- The AI MUST import React into every TSX file using `import React from 'react'` and MUST ensure `"esModuleInterop": true` is set in `tsconfig.json` (or use `import * as React from 'react'` if `esModuleInterop` is disabled).
- The AI MUST define a specific, explicitly named `Props` object type for every component.
- The AI MUST define a specific, explicitly named `State` object type for every class component that utilizes local state.
- The AI MUST type generic React components properly by passing the `Props` and `State` types (e.g., `class MyComponent extends React.Component<Props, State>`).
- The AI MUST use property initializers to declare default values for local state in class components.
- The AI MUST use TSX Fragments (`<>...</>`) when returning multiple sibling elements to avoid unnecessary DOM node overhead.
- The AI MUST use arrow functions for custom methods (e.g., event handlers) in class components to prevent `this` context rebinding issues.
- The AI MUST use React's specific synthetic event types (e.g., `React.MouseEvent<HTMLButtonElement>`) instead of standard DOM event types for component event handlers.
- The AI MUST NOT use React's `PropTypes` for runtime type checking, as TypeScript handles this at compile time.

## Angular Constraints
- The AI MUST implement explicitly imported lifecycle hook interfaces (e.g., `implements OnInit`) on component classes to allow TypeScript to enforce the presence of required methods (e.g., `ngOnInit()`).
- The AI MUST use decorators (`@Component`, `@Injectable`) to declare metadata for components and services.
- The AI MUST enable strict template type checking by setting `"fullTemplateTypeCheck": true` under `angularCompilerOptions` in `tsconfig.json`.
- The AI MUST utilize Angular's Dependency Injection by requesting required services as private parameters in the class `constructor`.

## API and Client-Server Communication Constraints
- The AI MUST NOT manually write and share interface types (e.g., `Request` types) across client and server network protocols (HTTP, TCP), as they are prone to falling out of sync.
- The AI MUST rely on typed, code-generated APIs leveraging a common source of truth:
  - Use **Swagger** for RESTful APIs.
  - Use **Apollo** or **Relay** for GraphQL APIs.
  - Use **gRPC** or **Apache Thrift** for RPC.

## Backend Database Constraints
- The AI MUST NOT use raw SQL queries or low-level, untyped database API calls (e.g., raw `client.query` or `db.collection.find`).
- The AI MUST use an Object-Relational Mapper (ORM), specifically **TypeORM**, to interact with databases to ensure typesafe returns and to prevent SQL injection attacks.

# @Workflow

1. **Environment Configuration**: Validate and configure `tsconfig.json` for the specific domain (`"lib": ["dom"]` for frontend, `"jsx": "react"` for React, `"fullTemplateTypeCheck": true` for Angular).
2. **Component Interface Definition**: Define rigid, explicit TypeScript types for `Props` and `State` before writing any view-layer logic or JSX/TSX.
3. **View Implementation**: Implement the UI component using the defined types, ensuring proper event typing, lifecycle interface implementation, and safe `this` binding (via arrow functions).
4. **Network Layer Setup**: Generate typed client/server bindings using an established code-generation tool (Swagger/Apollo/gRPC) rather than defining manual request/response types.
5. **Database Layer Setup**: Implement backend data access using an ORM (TypeORM) to ensure end-to-end type safety from the database to the API boundary.

# @Examples (Do's and Don'ts)

## React Components and Types
- **[DO]** Define explicit types for Props and State, and use arrow functions for methods:
  ```typescript
  import React from 'react'

  type Props = {
    firstName: string
    userId: string
  }

  type State = {
    isLoading: boolean
  }

  class SignupForm extends React.Component<Props, State> {
    state = {
      isLoading: false
    }

    render() {
      return (
        <>
          <h2>Welcome, {this.props.firstName}.</h2>
          <button onClick={this.signUp} disabled={this.state.isLoading}>Sign Up</button>
        </>
      )
    }

    private signUp = async () => {
      this.setState({isLoading: true})
      try {
        await fetch('/api/signup?userId=' + this.props.userId)
      } finally {
        this.setState({isLoading: false})
      }
    }
  }
  ```
- **[DON'T]** Use `PropTypes` or standard class methods that break `this` binding:
  ```javascript
  import React from 'react'
  import PropTypes from 'prop-types' // ANTI-PATTERN

  class SignupForm extends React.Component {
    constructor(props) {
      super(props)
      this.state = { isLoading: false }
      this.signUp = this.signUp.bind(this) // ANTI-PATTERN: Use arrow functions instead
    }

    signUp() {
      this.setState({isLoading: true})
    }
    // ...
  }

  SignupForm.propTypes = {
    firstName: PropTypes.string.isRequired // ANTI-PATTERN: Rely on TypeScript types
  }
  ```

## Angular Components
- **[DO]** Implement lifecycle interfaces explicitly:
  ```typescript
  import {Component, OnInit} from '@angular/core'
  import {MessageService} from '../services/message.service'

  @Component({
    selector: 'simple-message',
    templateUrl: './simple-message.component.html'
  })
  export class SimpleMessageComponent implements OnInit {
    message: string

    constructor(private messageService: MessageService) {}

    ngOnInit() {
      this.messageService.getMessage().subscribe(res => this.message = res.message)
    }
  }
  ```
- **[DON'T]** Define lifecycle methods without implementing the interface:
  ```typescript
  export class SimpleMessageComponent { // ANTI-PATTERN: Missing `implements OnInit`
    ngOnInit() {
      // TypeScript cannot guarantee this method is spelled correctly or required
    }
  }
  ```

## Client-Server APIs
- **[DO]** Use a code generator like Swagger/Apollo to consume APIs:
  ```typescript
  // DO: Rely on a code-generated client
  import { UserAPI } from './generated/api-client'
  
  async function startApp() {
    let user = await UserAPI.getUser() 
  }
  ```
- **[DON'T]** Manually define types that can fall out of sync with the backend:
  ```typescript
  // ANTI-PATTERN: Manual union and types that easily fall out of sync
  type Request = 
    | {entity: 'user', data: User}
    | {entity: 'location', data: Location}

  async function get<R extends Request>(entity: R['entity']): Promise<R['data']> {
    let res = await fetch(`/api/${entity}`)
    return await res.json()
  }
  ```

## Backend Database Access
- **[DO]** Use an ORM (like TypeORM) for typesafe, injection-proof database interactions:
  ```typescript
  import { UserRepository } from './repositories'

  async function getUser() {
    let user = await UserRepository.findOne({id: 739311}) // Typesafe User | undefined
    return user;
  }
  ```
- **[DON'T]** Use raw SQL or untyped API queries:
  ```typescript
  // ANTI-PATTERN: Untyped, potentially unsafe raw SQL
  let client = new Client()
  let res = await client.query('SELECT name FROM users where id = $1', [739311]) // returns `any`
  ```