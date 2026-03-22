@Domain
Trigger these rules when the user requests assistance with React frontend development involving form creation, form state management, form validation, form submission, the `react-hook-form` library, or the `react-router-dom` `<Form>` component.

@Vocabulary
- **Controlled Fields**: Form inputs whose values are strictly driven by React state (`useState`), updating on every keystroke via an `onChange` handler.
- **Uncontrolled Fields**: Form inputs whose values are maintained by the DOM rather than React state, accessed upon submission using the browser's native `FormData` API.
- **React Router Form**: A wrapper component (`<Form>`) provided by `react-router-dom` that intercepts native HTML form submission and routes it to a client-side `action` function without a full page reload.
- **React Hook Form**: A highly performant third-party React library that manages form state, validation, and submission using uncontrolled inputs under the hood to prevent unnecessary re-renders.
- **register**: A function returned by `useForm` (from React Hook Form) that returns `ref`, `name`, `onChange`, and `onBlur` properties to track field values and apply validation rules.
- **handleSubmit**: A function returned by `useForm` that intercepts the form submission, prevents the default server post, validates the fields, and only invokes the provided callback if all data is valid.
- **formState**: An object returned by `useForm` containing metadata about the form, crucially including `errors`, `isSubmitting`, and `isSubmitSuccessful`.
- **FormData**: A native browser API/interface used to easily extract key/value pairs from a submitted HTML form element.

@Objectives
- Optimize form performance by avoiding unnecessary component re-renders (specifically avoiding keystroke-level re-renders).
- Enforce strict TypeScript typing for all form data payloads.
- Select the most appropriate form architecture (Uncontrolled, React Router Form, or React Hook Form) based on the specific complexity and routing needs of the application.
- Deliver an excellent user experience by providing precise, immediate, and accessible validation feedback.

@Guidelines
- **Architecture Selection**:
  - For simple, isolated forms with minimal validation, the AI MUST use Uncontrolled Fields utilizing the native `FormData` API.
  - For forms heavily integrated with client-side routing and data mutation, the AI MUST use the React Router `<Form>` component paired with route `action` functions.
  - For forms requiring complex, custom, or UX-heavy validation, the AI MUST use the `react-hook-form` library.
- **Controlled Field Anti-Pattern**: The AI MUST NOT use Controlled Fields (binding `value` to `useState` and updating via `onChange` on every keystroke) without explicitly warning the user that this causes the entire form component to re-render on every keystroke, which severely degrades performance in larger forms.
- **Uncontrolled Field Implementation**:
  - The AI MUST ensure every `<input>`, `<select>`, and `<textarea>` element possesses a `name` attribute; otherwise, `FormData` cannot extract its value.
  - The AI MUST extract form data in the submit handler using `const formData = new FormData(e.currentTarget);`.
- **React Router Form Implementation**:
  - The AI MUST use `<Form method="post">` for data mutations to mimic HTTP POST behavior.
  - The AI MUST define a route action function typed with `ActionFunctionArgs` (e.g., `export async function someAction({ request }: ActionFunctionArgs)`).
  - The AI MUST extract data within the action using `await request.formData()`.
  - The AI MUST use the `redirect` function from `react-router-dom` to navigate after a successful action submission.
- **React Hook Form Implementation**:
  - The AI MUST strictly type the `useForm` hook: `const {...} = useForm<YourFormType>();`.
  - The AI MUST disable native HTML validation by adding the `noValidate` attribute to the `<form>` element to prevent browser validation UIs from conflicting with React Hook Form.
  - The AI MUST connect inputs by spreading the `register` function: `<input {...register('fieldName', { required: 'Message' })} />`.
  - The AI MUST wrap the submission handler in the `<form>` tag: `<form onSubmit={handleSubmit(onSubmit)}>`.
  - The AI MUST extract validation errors and submission state: `const { formState: { errors, isSubmitting, isSubmitSuccessful } } = useForm(...)`.
  - The AI MUST conditionally style invalid field editors (e.g., applying red borders) by checking if `errors.fieldName` exists.
  - The AI MUST render validation error messages using a dedicated component (e.g., `ValidationError`) that accepts a prop typed as `fieldError: FieldError | undefined` and renders a `<div role="alert">`.
  - The AI MUST disable submit buttons while the form is processing: `<button disabled={isSubmitting}>`.
  - The AI MUST configure validation timing to trigger on focus loss (blur) for better UX by initializing the hook with: `useForm<YourType>({ mode: "onBlur", reValidateMode: "onBlur" })`.
- **Native HTML Validation**: If instructed to use native validation, the AI MUST utilize attributes like `required` and `pattern` (e.g., `pattern="\S+@\S+\.\S+"`), but must advise the user that customizing native validation error messages requires the complex Constraint Validation API.

@Workflow
1. **Requirement Assessment**: Analyze the user's request to determine if the form requires simple native submission, React Router data mutations, or complex validation (React Hook Form).
2. **Type Definition**: Define a TypeScript `type` alias representing the exact structure of the form's data payload.
3. **Form Setup**:
   - Instantiate the form state/wrapper (e.g., `useForm<Type>()` or `<Form>`).
   - Define the `<form>` element, attaching `noValidate` if using a custom validation library, and assigning the proper submit handler (`onSubmit={handleSubmit(onSubmit)}` or `action`).
4. **Field Registration**:
   - Create the input fields.
   - For uncontrolled/Router forms: Apply exact `name` attributes matching the TypeScript type.
   - For React Hook Form: Spread the `register` function with associated validation rules (e.g., `required`, `pattern`).
5. **Validation UX**: Implement conditional CSS classes for invalid inputs and insert accessible error message components (`role="alert"`) below each field.
6. **Submission Handling**:
   - If manual uncontrolled: Call `e.preventDefault()`, extract `new FormData(e.currentTarget)`, and explicitly cast it to the defined TypeScript type.
   - If React Hook Form: Implement the strongly-typed `onSubmit(data: Type)` function. Ensure the submit button is bound to `disabled={isSubmitting}`.

@Examples (Do's and Don'ts)

[DO] Implement a highly performant, accessible form using React Hook Form with on-blur validation.
```tsx
import { useForm, FieldError } from 'react-hook-form';

type ContactData = {
  name: string;
  email: string;
};

export function ValidationError({ fieldError }: { fieldError: FieldError | undefined }) {
  if (!fieldError) return null;
  return <div role="alert" className="text-red-500 text-xs mt-1">{fieldError.message}</div>;
}

export function ContactForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ContactData>({
    mode: "onBlur",
    reValidateMode: "onBlur"
  });

  function onSubmit(data: ContactData) {
    console.log('Submitted:', data);
  }

  return (
    <form noValidate onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input 
          id="name" 
          className={errors.name ? 'border-red-500' : ''} 
          {...register('name', { required: 'You must enter your name' })} 
        />
        <ValidationError fieldError={errors.name} />
      </div>
      <button type="submit" disabled={isSubmitting}>Submit</button>
    </form>
  );
}
```

[DON'T] Implement Controlled Fields for large forms binding state to every keystroke (Anti-pattern).
```tsx
function ControlledForm() {
  // ANTI-PATTERN: Causes the entire form to re-render on every single keystroke.
  const [name, setName] = useState('');
  
  return (
    <form>
      <input 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
    </form>
  );
}
```

[DO] Implement Uncontrolled Fields using FormData for simple form data extraction.
```tsx
import { FormEvent } from 'react';

type SimpleSearch = { query: string };

function UncontrolledSearch() {
  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = {
      query: formData.get('query')
    } as SimpleSearch;
    console.log(data);
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="query" />
      <button type="submit">Search</button>
    </form>
  );
}
```

[DON'T] Omit the `name` attribute on inputs when using Uncontrolled forms or React Router Forms.
```tsx
function SearchForm() {
  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    // ERROR: This will return null because the input lacks a 'name' attribute.
    console.log(formData.get('search')); 
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="search" placeholder="Search ..." />
    </form>
  );
}
```

[DO] Use React Router's `<Form>` and action handlers for routing-based data mutations.
```tsx
import { Form, ActionFunctionArgs, redirect } from 'react-router-dom';

export async function contactAction({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);
  // process data...
  return redirect(`/thank-you/${data.name}`);
}

export function RouterContactForm() {
  return (
    <Form method="post">
      <input type="text" name="name" required />
      <button type="submit">Submit</button>
    </Form>
  );
}
```