## 2024-05-18 - JSON Loading Micro-Optimization
**Learning:** In a codebase heavily relying on runtime I/O (like reading local json configs during initialization), `json.loads(file.read())` creates an intermediate string representation that adds measurable memory and overhead over direct file object parsing with `json.load(file)`.
**Action:** Always prefer `json.load(file)` when reading JSON from files instead of `json.loads(file.read())` to avoid unnecessary memory overhead.
## 2024-05-18 - Avoid unconditional instantiation of heavy objects
**Learning:** Initializing heavy objects like `Translator()` unconditionally at script startup blocks execution and delays the app rendering, especially when it isn't even used most of the time (users default to English).
**Action:** Always conditionally instantiate heavy external libraries (like `Translator`) only if they are actually needed based on variables like language configs or online/offline mode.
