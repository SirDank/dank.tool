## 2024-05-18 - JSON Loading Micro-Optimization
**Learning:** In a codebase heavily relying on runtime I/O (like reading local json configs during initialization), `json.loads(file.read())` creates an intermediate string representation that adds measurable memory and overhead over direct file object parsing with `json.load(file)`.
**Action:** Always prefer `json.load(file)` when reading JSON from files instead of `json.loads(file.read())` to avoid unnecessary memory overhead.
## 2024-05-18 - Avoid unconditional instantiation of heavy objects
**Learning:** Initializing heavy objects like `Translator()` unconditionally at script startup blocks execution and delays the app rendering, especially when it isn't even used most of the time (users default to English).
**Action:** Always conditionally instantiate heavy external libraries (like `Translator`) only if they are actually needed based on variables like language configs or online/offline mode.
## 2024-05-18 - Stream large file downloads
**Learning:** Calling `session.get(url).content` buffers the entire response into memory. This causes huge memory spikes and performance degradation when downloading very large files (like `dank.tool.zip` which is >100MB).
**Action:** Always use `session.get(url, stream=True)` and iterate over `response.iter_content(chunk_size=...)` when downloading large files instead of loading the entire content into memory at once.
## 2024-05-18 - Infinite retries caused by raise_for_status() in generic exception loops
**Learning:** When using `while True` loops with bare `except:` blocks for network retries, adding `response.raise_for_status()` can cause infinite loops if a legitimate error (like a 404 for a removed file) occurs, because the `HTTPError` gets caught and retried endlessly instead of allowing the application to gracefully handle the failure (like reading an HTML error page to report a broken download).
**Action:** Be extremely cautious adding `raise_for_status()` to existing retry loops. If required, explicitly catch `HTTPError` separately from connection errors to prevent endless retries on permanent 4xx/5xx failures.
## 2024-04-04 - Optimize Directory Iteration
**Learning:** `os.listdir()` combined with `os.path.isfile()` or subsequent `is_dir()` / string filtering checks requires fetching file details multiple times, increasing file system lookups. This matters especially on Windows for operations like clearing large icon/thumbnail caches.
**Action:** Replaced `os.listdir()` loops with `os.scandir()` blocks whenever I iterate over files and need to fetch their attributes (e.g. check if they are files or get their names). This caches metadata.

## 2025-02-12 - Lazy load Translator for faster module startup
**Learning:** Eagerly initializing `Translator()` at the top-level of module execution (e.g. inside `main()`) heavily impacts startup time since it fetches online resources to instantiate, blocking execution whether or not translations are actually required by any string (based solely on the `DANK_TOOL_LANG` environment variable).
**Action:** Always prefer lazy instantiation of heavy objects like `Translator()` inside the wrapper functions (e.g. `translate(text)`) only when they are actually accessed (e.g. `if translator is None: translator = Translator()`).
