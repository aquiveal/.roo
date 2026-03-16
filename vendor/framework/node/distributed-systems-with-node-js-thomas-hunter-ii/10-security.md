# @Domain
Trigger these rules when performing tasks related to Node.js application security, configuration management, secrets handling, dependency auditing, npm package upgrades, Node.js version migrations, or HTTP request payload parsing.

# @Vocabulary
- **Attack Surface**: The entry points of an application susceptible to attack, including the "front door" (HTTP routes, queues) and "supply chain" (third-party npm packages intercepting core Node.js APIs).
- **Prototype Pollution**: A JavaScript-specific vulnerability where a malicious JSON payload includes a `__proto__` property that, when unsafely merged or cloned, overwrites the object prototype, potentially elevating privileges (e.g., setting `isAdmin: true` globally).
- **Typo Squatting**: A supply chain attack where malicious npm packages are published with names very similar to popular packages.
- **Env File (`.env`)**: A local file containing exported environment variables, strictly for local development, which must NEVER be committed to version control.
- **Secrets Management**: Tools/practices (e.g., Kubernetes Secrets) that securely store and inject credentials into applications at runtime as environment variables.
- **LTS (Long-Term Support)**: Even-numbered Node.js release lines that go through Current, Active, and Maintenance phases. Odd-numbered releases are betas and NEVER for production.
- **Naughty Generation**: Node.js applications running on unsupported (End-of-Life) or odd-numbered (non-LTS) versions.
- **Piecemeal Upgrades**: The practice of upgrading dependencies one at a time (or in tightly coupled groups) per Pull Request to isolate breaking changes.
- **Responsible Disclosure**: The practice of privately notifying a package author of a vulnerability (often with a patch) before making it public.

# @Objectives
- Eradicate hardcoded sensitive configuration and manage all credentials strictly through environment variables.
- Defend the application "front door" against Denial of Service (DoS) via massive payloads and Prototype Pollution via unsafe object cloning.
- Audit and upgrade vulnerable dependencies incrementally to prevent application regressions.
- Safely transition outdated Node.js services through LTS versions to maintain platform security.
- Minimize the third-party dependency footprint to reduce supply-chain attack vectors.

# @Guidelines
- **Application Configuration**:
  - The AI MUST NEVER hardcode sensitive data, credentials, hostnames, or API keys in configuration files (e.g., `config/production.js`) or source code.
  - The AI MUST extract sensitive values exclusively from `process.env`.
  - The AI MUST crash the application immediately at startup (using `process.exit(1)`) if required environment variables are missing, outputting a helpful usage message to `stderr`.
  - The AI MUST implement environment-specific configuration via a loader (e.g., `config/index.js`) that performs a shallow merge of an environment-specific file (`config/development.js`) over a default fallback file (`config/default.js`).
  - The AI MUST ensure `.env` files are explicitly listed in `.gitignore` and `.dockerignore`.
- **Payload & Deserialization Security**:
  - The AI MUST enforce a maximum request size limit for all HTTP body parsers (e.g., limiting JSON bodies to `1MB` or `100KB`).
  - The AI MUST NOT use naive shallow cloning techniques (e.g., `for (let key of Object.keys(obj)) clone[key] = obj[key];`) that blindly copy `__proto__` properties.
- **Dependency Management & Upgrades**:
  - The AI MUST keep the number of dependencies to a minimum and favor packages from reputable authors with fewer subdependencies.
  - The AI MUST run `npm outdated` to identify candidates for upgrades and `npm audit` to identify vulnerabilities (categorized as low, moderate, high, or critical).
  - The AI MUST isolate dependency upgrades. Do not upgrade 20 dependencies in one PR. Perform piecemeal updates (one package or one tightly coupled group per PR) to make debugging regressions feasible.
  - The AI MUST use `npm update <package>` to fix specific vulnerable packages or `npm audit fix` for automated ranges.
  - If a vulnerable package cannot be updated (abandoned or unpatched), the AI MUST either replace it, fork it to patch it, or wrap the function call to aggressively sanitize and type-coerce inputs before they reach the vulnerable package.
- **Node.js Upgrades**:
  - The AI MUST categorize applications into Generations: Current (Active LTS), Maintenance (Previous LTS), and Naughty (EOL or odd-numbered).
  - The AI MUST upgrade "Naughty" generation applications by jumping sequentially to the highest version of each intermediate LTS release (e.g., v10.x -> v12.x -> v14.x) and testing compatibility at each stage, rather than jumping directly to the latest release.

# @Workflow
1. **Audit the Ecosystem**: Determine the project's Node.js version, deployment environment, web server package, and identify if the Node.js version falls into the "Naughty" generation.
2. **Secure the Configuration**: 
   - Move all credentials to environment variables.
   - Implement the `config/default.js` and `config/<env>.js` hierarchy.
   - Add a startup validation check that immediately calls `process.exit(1)` if vital `process.env` values are undefined.
3. **Fortify the Front Door**: 
   - Apply explicit payload size limits to the web framework's body parser.
   - Review all JSON parsing and object cloning logic for Prototype Pollution vectors.
4. **Audit Dependencies**:
   - Execute `npm audit` and `npm outdated`.
   - Identify vulnerabilities.
5. **Execute Piecemeal Upgrades**:
   - Upgrade vulnerable packages one at a time using `npm update <package>`.
   - Implement data sanitization wrappers for unpatchable dependencies.
6. **LTS Migration**: If the Node.js version is unsupported, update the `Dockerfile` and CI configurations to the next chronological LTS version, test, and repeat until reaching the Current Active LTS.

# @Examples (Do's and Don'ts)

**Configuration at Startup**
- [DO]: Fail fast if required configuration is missing.
```javascript
if (!process.env.REDIS_URL) {
  console.error("Usage: REDIS_URL=<redis_conn> node server.js");
  process.exit(1);
}
const redis = new Redis(process.env.REDIS_URL);
```
- [DON'T]: Wait until the first request to realize the database connection string is missing.
```javascript
// BAD: Application starts but crashes on the first user request
const redis = new Redis(process.env.REDIS_URL); 
```

**Configuration Files**
- [DO]: Use default configurations merged with environment-specific overrides, relying on `process.env` for secrets.
```javascript
// config/default.js
module.exports = {
  REDIS: process.env.REDIS,
  MAX_PAYLOAD: 1024 * 1024
};

// config/development.js
module.exports = {
  ENV: 'development',
  REDIS: process.env.REDIS || 'redis://localhost:6379'
};
```
- [DON'T]: Hardcode sensitive data into environment configuration files.
```javascript
// BAD: config/production.js checked into version control
module.exports = {
  REDIS: 'redis://admin:superSecretPassword@192.168.2.1'
};
```

**Payload Limits**
- [DO]: Enforce limits on incoming JSON payloads.
```javascript
// Fastify example
const server = require('fastify')({ bodyLimit: 1048576 }); // 1MB limit
```
- [DON'T]: Accept boundless JSON payloads that consume memory and cause Denial of Service.
```javascript
// BAD: Relying on default unlimited parsers or manual JSON.parse(req.body) without size checks.
```

**Preventing Prototype Pollution**
- [DO]: Validate keys before cloning or explicitly deny `__proto__`.
```javascript
const obj = JSON.parse(requestBody);
if ('__proto__' in obj || 'constructor' in obj) {
  throw new Error('Invalid payload');
}
```
- [DON'T]: Use naive manual cloning that copies unsafe keys.
```javascript
// BAD: Allows prototype pollution if obj contains `{"__proto__": {"isAdmin": true}}`
function shallowClone(obj) {
  const clone = {};
  for (let key of Object.keys(obj)) {
    clone[key] = obj[key];
  }
  return clone;
}
```

**Unpatched Vulnerability Mitigation**
- [DO]: Wrap abandoned/vulnerable packages to aggressively sanitize input.
```javascript
const vulnerableLib = require('abandoned-lib');

module.exports.safeRun = function(userInput) {
  // Aggressive sanitization and type coercion before passing to vulnerable code
  const sanitized = String(userInput).replace(/[^a-zA-Z0-9]/g, '');
  return vulnerableLib.run(sanitized);
};
```
- [DON'T]: Pass raw, untyped user input directly into a package known to have Code Injection or ReDoS vulnerabilities.