from __future__ import annotations

from source_items import Item


def item(
    question: str,
    correct: str,
    wrong: str,
    distractor_1: str,
    distractor_2: str,
    note: str,
) -> Item:
    return Item(
        question,
        correct,
        wrong,
        distractor_1,
        distractor_2,
        note,
    )


def build_easy_items() -> list[Item]:
    rows = [
        ("Which data structure removes the most recently added item first?", "Stack", "Queue", "Graph", "Hash table", "A stack follows last-in, first-out ordering."),
        ("Which operation adds an item to the top of a stack?", "Push", "Dequeue", "Merge", "Compile", "Push places a new item on a stack."),
        ("Which operation removes the front item from a queue?", "Dequeue", "Push", "Peek only", "Hash", "Dequeue removes the oldest queued item."),
        ("Which data structure stores a sequence of elements at indexed positions?", "Array", "Socket", "Process", "Compiler", "Arrays associate elements with numeric indices."),
        ("What does a linked-list node normally store besides its value?", "A link to another node", "An entire operating system", "A network password", "A CPU instruction decoder", "Links connect nodes into a list."),
        ("Which structure represents pairwise connections among vertices?", "Graph", "Stack", "Scalar", "Character", "Graphs model vertices and their connecting edges."),
        ("What is the topmost node of a rooted tree called?", "Root", "Leaf", "Edge", "Cycle", "The distinguished starting node of a rooted tree is its root."),
        ("What is a tree node with no children called?", "Leaf", "Root necessarily", "Loop", "Queue", "A leaf is a node without children."),
        ("A condition should pass only when two separate checks both pass. Which Boolean connector expresses this?", "AND", "OR", "NOT", "XOR", "Logical AND requires both inputs to be true."),
        ("Which Boolean operator reverses a truth value?", "NOT", "AND", "OR", "MOD", "NOT maps true to false and false to true."),
        ("What does a variable do in a program?", "Names a stored value", "Physically cools the processor", "Routes internet packets", "Encrypts every file automatically", "A variable associates a name with a value or storage location."),
        ("What is a function parameter?", "An input name in a function definition", "A disk partition", "A network cable", "A database row lock", "Parameters receive arguments supplied to a function."),
        ("What does a return statement normally do?", "Ends a function and supplies a result", "Starts the operating system", "Allocates every available byte", "Creates a network route", "Return transfers control to the caller and can provide a value."),
        ("Which control structure chooses between alternatives based on a condition?", "Conditional statement", "Comment", "Import only", "Array index", "An if/else conditional selects a branch based on a Boolean condition."),
        ("Which construct repeats statements while a condition remains true?", "While loop", "Class declaration", "Constant", "Exception message", "A while loop repeatedly executes while its condition is true."),
        ("What is an infinite loop?", "A loop that never reaches a stopping condition", "A loop that executes exactly once", "A sorted array", "A recursive type only", "An infinite loop continues indefinitely unless externally interrupted."),
        ("What is a syntax error?", "A violation of a language's grammatical rules", "A slow network response", "A correct program output", "A hardware temperature reading", "A parser reports syntax errors when code does not follow grammar."),
        ("What is a runtime error?", "An error occurring while a program executes", "A comment in source code", "A valid type annotation", "A completed backup", "Runtime errors arise during execution rather than parsing."),
        ("What is a logical bug?", "Code runs but produces unintended behavior", "Code cannot be stored as text", "A keyboard is disconnected", "The CPU has no clock", "Logical bugs produce incorrect results despite executable syntax."),
        ("What is debugging?", "Finding and correcting defects in software", "Compressing every file", "Replacing source code with images", "Turning off all tests", "Debugging identifies causes of incorrect behavior and fixes them."),
        ("What is source code?", "Human-readable program text", "Only the electrical voltage in RAM", "A printed network route", "A database index page only", "Source code is the textual representation written by programmers."),
        ("What does a compiler generally produce from source code?", "A translated form suitable for execution or further linking", "A stronger Wi-Fi signal", "A database transaction", "A user password", "Compilers translate source programs into lower-level representations."),
        ("What does an interpreter generally do?", "Executes or evaluates program instructions through another program", "Manufactures processors", "Routes Ethernet frames", "Formats every disk", "An interpreter processes source or intermediate instructions at runtime."),
        ("What is an algorithm?", "A finite procedure for solving a class of problems", "A physical memory chip", "A network address only", "A programming language logo", "An algorithm specifies ordered steps that produce a result."),
        ("What is recursion?", "A function solving a problem by calling itself on smaller cases", "A database deleting all rows", "A loop with no condition", "A file encryption key", "Recursive definitions reduce a problem to related subproblems."),
        ("What is a base case in recursion?", "A case that returns without another recursive call", "The largest possible input only", "A network base station", "An unhandled exception", "A base case stops recursive descent."),
        ("Which search checks elements one by one until a match is found?", "Linear search", "Binary search", "Hash encryption", "Depth compilation", "Linear search examines items sequentially."),
        ("Which sorting method repeatedly swaps adjacent out-of-order elements?", "Bubble sort", "Merge sort", "Binary search", "Breadth-first search", "Bubble sort uses repeated adjacent comparisons and swaps."),
        ("What does ascending sort order mean for numbers?", "Smallest to largest", "Largest to smallest", "Random order", "Only even numbers", "Ascending numeric order increases from lower to higher values."),
        ("What does Big O notation describe?", "How resource use grows with input size", "The exact clock time on every computer", "The shape of a database logo", "A network port number", "Big O expresses asymptotic growth of time or space."),
        ("Which storage is normally volatile?", "RAM", "SSD", "Hard disk", "Optical disc", "RAM generally loses its contents when power is removed."),
        ("Which component performs most general-purpose instruction execution?", "CPU", "Keyboard", "Monitor", "Router only", "The central processing unit fetches and executes instructions."),
        ("What is a CPU register?", "Small fast storage inside the processor", "A remote web server", "A disk directory", "A database relation only", "Registers hold operands and state close to execution units."),
        ("What does the arithmetic logic unit perform?", "Arithmetic and logical operations", "Permanent file storage", "Network naming", "Screen printing only", "The ALU carries out arithmetic and bitwise/logical operations."),
        ("What is a bit?", "A binary digit", "Eight bytes", "A network cable", "A database table", "A bit has one of two binary values."),
        ("What is a byte in common modern usage?", "Eight bits", "Two bits", "Sixteen kilobytes", "One decimal digit", "A byte conventionally consists of eight bits."),
        ("Which number system uses digits 0 and 1?", "Binary", "Decimal", "Hexadecimal", "Roman numerals", "Base-two binary notation uses only 0 and 1."),
        ("Which number system uses sixteen digit symbols?", "Hexadecimal", "Binary", "Octal", "Unary", "Hexadecimal is base 16, using 0-9 and A-F."),
        ("What is an operating system?", "Software that manages hardware and provides services to programs", "A single spreadsheet", "A web address", "A CPU transistor only", "An operating system coordinates resources and exposes system services."),
        ("What is a process?", "A program in execution", "A source file that never runs", "A network cable", "A database column", "A process is an executing program with associated state."),
        ("What is a thread?", "A schedulable execution sequence within a process", "A permanent disk partition", "A type of monitor", "A DNS name", "Threads are units of execution that can share process resources."),
        ("What is multitasking?", "Running multiple tasks with overlapping progress", "Using exactly one instruction forever", "Removing all processes", "Storing only one file", "Operating systems interleave or parallelize work across tasks."),
        ("What is a file system?", "A method for organizing and retrieving stored files", "A programming loop", "A web encryption algorithm only", "A CPU cache line", "File systems define names, directories, metadata, and storage mapping."),
        ("What is a directory?", "A container that organizes file-system entries", "A CPU instruction", "A network packet", "An SQL aggregate", "Directories group and name files and subdirectories."),
        ("What is a database?", "An organized collection of data", "A monitor resolution", "A keyboard layout", "A compiler flag", "Databases store structured information for retrieval and update."),
        ("What is a table in a relational database?", "A collection of rows sharing defined columns", "A network route", "A CPU pipeline", "A source-code comment", "Relational tables represent tuples using named attributes."),
        ("What does a primary key do?", "Uniquely identifies a table row", "Encrypts the entire database", "Sorts every query automatically", "Connects a monitor", "A primary key enforces a unique row identifier."),
        ("What does a foreign key represent?", "A reference to a key in another or the same table", "A password from another country", "A CPU cache miss", "An invalid data type", "Foreign keys encode referential relationships."),
        ("Which SQL command retrieves rows?", "SELECT", "DELETE", "DROP", "COMMIT only", "SELECT queries data from tables or views."),
        ("Which SQL command adds a new row?", "INSERT", "SELECT", "ALTER only", "ROLLBACK", "INSERT creates rows in a table."),
        ("Which SQL clause filters rows before grouping?", "WHERE", "ORDER BY", "SELECT only", "JOIN only", "WHERE applies a predicate to individual input rows."),
        ("Which SQL clause arranges query results?", "ORDER BY", "WHERE", "VALUES", "CREATE", "ORDER BY specifies result ordering."),
        ("What does a database index primarily improve?", "Lookup performance for supported queries", "Screen brightness", "Network cable length", "Programming-language syntax", "Indexes provide data structures for faster retrieval at storage and update cost."),
        ("What does ACID atomicity mean for a transaction?", "All its operations commit or none do", "Its rows are alphabetically sorted", "It always runs instantly", "It uses no storage", "Atomicity prevents partial transaction effects from being committed."),
        ("What is a computer network?", "Interconnected devices that exchange data", "A single local variable", "A sorting algorithm", "A processor register", "Networks enable communication among connected systems."),
        ("What does an IP address identify?", "A network interface in an IP network", "A person's legal identity necessarily", "A programming loop", "A database password", "IP addresses are logical network-layer interface identifiers."),
        ("What does a MAC address identify at the data-link layer?", "A network interface", "A web page's content", "A SQL row", "A process stack", "MAC addresses identify interfaces for local link-layer delivery."),
        ("What device forwards packets between IP networks?", "Router", "Keyboard", "Compiler", "Database trigger", "Routers select paths and forward network-layer packets."),
        ("What device connects devices on the same Ethernet LAN using frame addresses?", "Switch", "Printer driver", "Interpreter", "Text editor", "Ethernet switches forward frames based on MAC addresses."),
        ("What does DNS translate domain names into?", "IP addresses and related records", "Source code", "CPU instructions only", "Database primary keys", "DNS resolves names to resource records such as IP addresses."),
        ("What does a URL identify?", "A resource location and access scheme", "A CPU register", "A database transaction", "A Boolean value", "A URL describes how and where to access a resource."),
        ("What does HTTPS add to HTTP?", "Transport encryption and server authentication through TLS", "A faster CPU clock", "A relational schema", "A graphics processor", "HTTPS carries HTTP over TLS."),
        ("Which protocol reliably delivers an ordered byte stream?", "TCP", "UDP", "ARP only", "ICMP echo only", "TCP provides reliable ordered byte-stream transport."),
        ("Which transport protocol sends independent datagrams without delivery guarantees?", "UDP", "TCP", "HTTPS", "SQL", "UDP is connectionless and does not guarantee delivery or ordering."),
        ("What is a network port number used for?", "Identifying an application endpoint on a host", "Measuring cable length", "Naming a CPU core", "Sorting database rows", "Transport protocols use ports to demultiplex application traffic."),
        ("What is a web browser?", "A client that retrieves and presents web resources", "A database server only", "An operating-system scheduler", "A compiler linker", "Browsers request, interpret, and display web content."),
        ("What does HTML describe?", "Structure and semantics of web content", "Only visual color choices", "Database indexes", "CPU instruction timing", "HTML marks up document structure and meaning."),
        ("What does JavaScript commonly provide in web pages?", "Programmable behavior", "Physical network wiring", "Disk formatting", "SQL table storage only", "JavaScript runs logic that can respond to events and modify page state."),
        ("What is an API?", "A defined interface for software interaction", "A particular hard-disk brand", "A password format only", "A display pixel", "APIs specify operations and data formats exposed to other software."),
        ("What is version control?", "Tracking and coordinating changes to files", "Increasing processor voltage", "Deleting every previous version", "Encrypting network packets only", "Version-control systems record revisions and support collaboration."),
        ("What is a repository in version control?", "A collection of tracked content and history", "A CPU instruction queue", "A DNS cache only", "A database foreign key", "A repository stores project versions and metadata."),
        ("What is a commit?", "A recorded snapshot of selected changes", "A running operating-system process", "A network handshake", "A database read lock only", "A commit records a project state with metadata."),
        ("What is a branch in version control?", "A movable line of development", "A physical cable split", "A database column", "A compiler token", "Branches let development histories diverge and later merge."),
        ("What is a unit test?", "A test of a small isolated behavior", "A full production deployment", "A network route", "A disk partition", "Unit tests verify focused components or functions."),
        ("What is an assertion in a test?", "A condition expected to be true", "A database backup", "A CPU cooling method", "A file compression ratio", "Assertions fail a test when observed behavior violates expectations."),
        ("What is refactoring?", "Improving code structure without intentionally changing behavior", "Adding random output", "Deleting every test", "Changing hardware voltage", "Refactoring reorganizes implementation while preserving external behavior."),
        ("What is authentication?", "Verifying an identity claim", "Deciding what an identified user may do", "Compressing a file", "Sorting a list", "Authentication establishes who or what is making a request."),
        ("What is authorization?", "Determining permitted actions for an authenticated identity", "Proving a password is secret", "Compiling source code", "Assigning IP addresses", "Authorization enforces access permissions."),
        ("What is encryption?", "Transforming data using a key to protect confidentiality", "Irreversibly summarizing data without a key", "Sorting data", "Deleting metadata only", "Encryption produces ciphertext that authorized holders can decrypt."),
        ("What is a cryptographic hash function?", "A one-way mapping to a fixed-size digest", "A reversible encryption method with the same output as input", "A network cable", "A database join", "Cryptographic hashes create fixed-length digests designed to resist inversion and collisions."),
        ("What is phishing?", "Deceptive communication intended to steal information or access", "A safe backup method", "A sorting algorithm", "A CPU scheduling policy", "Phishing impersonates a trusted party to manipulate a victim."),
        ("What is malware?", "Software designed to cause harm or unauthorized actions", "Any open-source program", "A valid database query", "A network switch", "Malware includes malicious programs such as ransomware and spyware."),
        ("What is a firewall?", "A control that filters network traffic according to rules", "A physical fire detector only", "A compiler optimization", "A database table", "Firewalls permit or block traffic based on security policy."),
        ("Why should passwords be stored with salted password hashing?", "To resist recovery and precomputed lookup attacks", "To let administrators read every password", "To make all users share one password", "To remove authentication", "A unique salt defeats shared precomputed tables, while slow hashing raises attack cost."),
        ("What is least privilege?", "Granting only permissions needed for a task", "Giving every user administrator access", "Removing all auditing", "Using the longest possible variable name", "Least privilege limits damage from mistakes or compromise."),
        ("What is input validation?", "Checking input against expected type, format, and constraints", "Trusting all input automatically", "Deleting every request", "Increasing CPU speed", "Validation rejects or handles malformed and out-of-range input."),
        ("What is a backup?", "A separate copy used to restore lost or damaged data", "The only copy of a file", "A running thread", "A network broadcast", "Backups provide recovery from deletion, corruption, or device failure."),
        ("What does caching do?", "Stores reusable data closer to where it is needed", "Permanently deletes source data", "Makes every request cross the network", "Disables memory", "Caches trade storage and freshness complexity for faster repeated access."),
    ]

    return [item(*row) for row in rows]


def build_medium_items() -> list[Item]:
    items: list[Item] = []

    trace_cases = [
        ("x = 4; x = x + 3; output x", "7", "4", "3", "12", "x is updated from 4 to 7."),
        ("x = 10; x = x - 6; output x", "4", "16", "6", "-4", "x is updated from 10 to 4."),
        ("a = 3; b = 5; output a * b", "15", "8", "2", "35", "Multiplication gives 3 × 5 = 15."),
        ("n = 9; output n % 4", "1", "2.25", "4", "0", "Nine divided by 4 leaves remainder 1."),
        ("p = 2; p = p * p * p; output p", "8", "6", "4", "16", "The update computes 2 cubed, which is 8."),
    ]
    for code, correct, wrong, d1, d2, note in trace_cases:
        items.append(item(
            f"What value is output by this pseudocode: {code}?",
            correct, wrong, d1, d2, note,
        ))

    loop_cases = [
        ("sum = 0; for i from 1 through 4: sum = sum + i", "10", "4", "6", "16", "The loop adds 1+2+3+4 = 10."),
        ("count = 0; for each value in [3, 8, 2, 9]: if value > 5: count = count + 1", "2", "4", "1", "3", "Only 8 and 9 are greater than 5."),
        ("product = 1; for i from 1 through 4: product = product * 2", "16", "8", "4", "32", "Four multiplications by 2 give 2⁴ = 16."),
        ("x = 20; while x > 5: x = x - 5", "5", "0", "10", "15", "The values after iterations are 15, 10, and 5, where the loop stops."),
        ("result = 0; for i from 0 through 3: result = result + 2*i", "12", "6", "8", "16", "The sum is 0+2+4+6 = 12."),
    ]
    for code, correct, wrong, d1, d2, note in loop_cases:
        items.append(item(
            f"What final value results from this pseudocode: {code}?",
            correct, wrong, d1, d2, note,
        ))

    items.extend([
        item("A sorted array contains 128 elements. In the worst case, approximately how many halving steps does binary search need?", "7", "128", "64", "14", "Because 128 = 2⁷, seven halvings reduce the search interval to one element."),
        item("Which traversal explores all neighbors at one graph distance before moving farther away?", "Breadth-first search", "Depth-first search", "Binary search", "Insertion sort", "Breadth-first search uses a queue to explore level by level."),
        item("Which traversal naturally uses a stack or recursion to follow one path deeply?", "Depth-first search", "Breadth-first search", "Linear probing only", "Merge sort", "Depth-first search follows a branch before backtracking."),
        item("What is the worst-case time complexity of scanning every element of an n-element array once?", "O(n)", "O(1)", "O(log n)", "O(n squared)", "A single full scan performs work proportional to n."),
        item("What is the time complexity of direct indexed array access under the usual random-access model?", "O(1)", "O(n)", "O(log n)", "O(n squared)", "The address of an indexed element is computed directly."),
        item("What is the worst-case time complexity of two nested loops that each run n times?", "O(n squared)", "O(n)", "O(log n)", "O(2n only)", "The inner body executes n×n times."),
        item("Why must binary search receive sorted data?", "The ordering determines which half can be discarded", "Sorting makes every search O(1)", "Unsorted arrays contain no indices", "Binary search compares every element", "Without order, a comparison does not identify a safe half to eliminate."),
        item("Which data structure is commonly used to implement breadth-first search?", "Queue", "Stack", "Heap only", "Hash digest", "A queue preserves frontier order by discovery depth."),
        item("Which data structure is commonly used to implement depth-first search iteratively?", "Stack", "Queue", "Relational table only", "Network socket", "A stack stores the most recently discovered unfinished path."),
        item("What property must hold in a binary search tree for every node?", "Keys in the left subtree compare smaller and keys in the right compare larger under the tree's ordering", "Every node has exactly two children", "All leaves have different depths necessarily", "The root is always the smallest key", "The search-tree ordering enables directed lookup."),
        item("What advantage does a balanced binary search tree provide?", "Logarithmic-height search, insertion, and deletion", "Constant-time sorting of arbitrary input", "No memory usage", "Guaranteed O(1) lookup", "Keeping height logarithmic bounds root-to-leaf operations."),
        item("What does a hash-table collision mean?", "Two keys map to the same bucket or slot", "A key has no hash value", "The table becomes a tree automatically", "Two arrays have equal length", "Finite hash ranges can map different keys to the same location."),
        item("Why does a hash table need collision handling?", "Different keys can produce the same index", "Hash functions always return unique real numbers", "Arrays cannot store values", "Keys never repeat", "Chaining or probing preserves entries that share an index."),
        item("What does a min-heap guarantee at its root?", "The minimum key in the heap", "The maximum key", "The median key", "The most recently inserted key", "The min-heap order places a key no greater than its descendants at the root."),
        item("Which algorithmic strategy solves overlapping subproblems once and stores their results?", "Dynamic programming", "Blind exhaustive repetition", "Packet routing", "Lexical analysis", "Dynamic programming reuses solutions to repeated subproblems."),
        item("What is memoization?", "Caching results of function calls for reuse", "Deleting recursive results", "Sorting memory addresses", "Encrypting a stack", "Memoization avoids recomputing the same inputs."),
        item("What is a greedy algorithm?", "An algorithm that repeatedly chooses a locally preferred option", "An algorithm that always tries every possibility", "A database transaction", "A network retransmission", "Greedy methods build a solution through locally optimal choices."),
        item("Why is a stable sort useful?", "Equal-key records retain their previous relative order", "It uses no memory", "It makes all keys unique", "It always runs in constant time", "Stability preserves earlier ordering among ties."),
        item("Which sorting algorithm divides input, sorts subarrays, and merges them?", "Merge sort", "Bubble sort", "Linear search", "Breadth-first search", "Merge sort recursively sorts halves and combines them."),
        item("What is the usual worst-case time complexity of merge sort?", "O(n log n)", "O(n squared)", "O(log n)", "O(1)", "There are logarithmic merge levels with linear work per level."),
        item("What is the usual worst-case time complexity of insertion sort?", "O(n squared)", "O(n log n) in every case", "O(1)", "O(log n)", "Reverse-ordered input can require a quadratic number of shifts/comparisons."),
        item("What is an invariant in algorithm reasoning?", "A property maintained at specified points during execution", "A variable that must change every step", "A network packet", "A compiler executable", "Loop invariants support correctness proofs by remaining true across iterations."),
        item("What does amortized analysis describe?", "Average cost per operation over a worst-case sequence", "Average wall-clock time on one computer only", "Best case of a single operation", "Network latency", "Occasional expensive operations can be spread over many cheap ones."),
        item("A dynamic array is full and doubles its capacity. Why can append still be amortized O(1)?", "Costly resizes occur only after many cheap appends", "Every append copies the whole array", "The array never allocates memory", "Doubling makes lookup O(n)", "Geometric growth spreads each resize cost over preceding appends."),
        item("What does spatial locality mean?", "Programs often access addresses near recently accessed addresses", "Programs never reuse memory", "All data are stored remotely", "Only CPU registers are accessed", "Caches exploit nearby-address access patterns."),
        item("Why can cache memory speed computation?", "It holds recently or nearby used data with lower access latency", "It increases algorithmic correctness automatically", "It permanently replaces storage", "It removes instruction execution", "Fast cache reduces average memory-access time."),
        item("What is virtual memory?", "An address abstraction mapping process pages to physical memory or storage", "A cloud-only database", "A CPU arithmetic instruction", "A network protocol", "Virtual memory separates process address spaces from physical placement."),
        item("What is a page fault?", "An access requiring the operating system to bring or map a page", "A syntax error in HTML", "A failed database transaction only", "A broken monitor pixel", "The hardware traps when a referenced virtual page lacks a valid resident mapping."),
        item("What does the operating-system scheduler decide?", "Which runnable task receives CPU time", "How SQL tables are normalized", "Which DNS name is valid", "How source code is indented", "The scheduler allocates processor execution among runnable tasks."),
        item("What is a context switch?", "Saving one task's execution state and restoring another's", "Changing a variable's data type", "Routing a packet", "Committing a database row", "Context switching lets a CPU alternate among execution contexts."),
        item("What is mutual exclusion intended to prevent?", "Concurrent entry into a protected critical section", "All parallel execution", "Disk reads", "Function calls", "A mutex permits controlled exclusive access to shared state."),
        item("What is a race condition?", "Behavior that depends on uncontrolled timing of concurrent operations", "A loop that executes quickly", "A database index", "A network address collision only", "Unsynchronized interleavings can produce inconsistent outcomes."),
        item("Which four conditions are classically associated with deadlock?", "Mutual exclusion, hold and wait, no preemption, and circular wait", "Sorting, searching, hashing, and merging", "Read, write, execute, and delete", "Input, output, storage, and display", "The Coffman conditions characterize potential deadlock."),
        item("What is starvation in scheduling or locking?", "A task waits indefinitely because others repeatedly receive service", "Every task completes together", "A file is deleted", "A thread uses no CPU by design", "Unfair resource allocation can indefinitely postpone one task."),
        item("What does a system call provide?", "A controlled interface from user programs to kernel services", "A direct SQL join", "A web-page style", "A compiler comment", "System calls request privileged operating-system operations."),
        item("What is the difference between a process and a thread?", "Threads within a process share many resources, while processes have separate address spaces by default", "Processes always share every variable", "Threads cannot execute instructions", "They are identical terms", "The process is a resource container; threads are execution flows within it."),
        item("Why is memory isolation important between processes?", "It prevents one process from freely corrupting another's memory", "It makes every process use the same stack", "It removes the need for permissions", "It disables virtual memory", "Isolation supports reliability and security boundaries."),
        item("What does normalization reduce in relational database design?", "Redundant storage and update anomalies", "The number of possible queries to zero", "All table relationships", "Network packet size", "Normalization decomposes data around dependencies."),
        item("What does an INNER JOIN return?", "Rows with matching join conditions from both inputs", "Every row from both inputs regardless of match", "Only rows from the left with no match", "A new database server", "An inner join keeps paired rows satisfying the join predicate."),
        item("What does a LEFT JOIN preserve?", "Every row from the left input, with nulls where no right match exists", "Only matching right rows", "No rows from the left", "Only duplicate keys", "A left outer join retains unmatched left-side rows."),
        item("What does GROUP BY do in SQL?", "Forms groups of rows for aggregate calculation", "Sorts rows alphabetically necessarily", "Deletes duplicate tables", "Creates a network group", "GROUP BY partitions rows by key values for aggregation."),
        item("Which SQL aggregate counts rows?", "COUNT", "SUM only", "ORDER", "ALTER", "COUNT returns the number of qualifying rows or non-null expressions."),
        item("Why should a transaction use a rollback after a failed required operation?", "To undo its uncommitted partial changes", "To permanently commit partial data", "To drop every table", "To restart the network", "Rollback restores transactional consistency when a unit of work cannot complete."),
        item("What does transaction isolation control?", "How concurrent transactions observe one another's intermediate effects", "How passwords are encrypted", "How files are compressed", "How CPUs are cooled", "Isolation levels constrain visibility and anomalies across concurrent transactions."),
        item("What is a database view?", "A named query presenting a virtual table", "A physical monitor", "A network route", "A CPU register", "Views expose query results through a table-like interface."),
        item("What is parameterized SQL intended to prevent when handling user input?", "Injection caused by treating data as query syntax", "Every database error", "Slow networks", "Power loss", "Bound parameters keep values separate from SQL structure."),
        item("Why can indexing every database column be harmful?", "Indexes consume space and add write-maintenance cost", "Indexes always corrupt data", "Queries cannot use indexes", "Columns cease to exist", "Each index must be stored and updated when indexed data change."),
        item("What does a composite index contain?", "Keys from more than one column", "Multiple databases in one file necessarily", "Only encrypted passwords", "A network packet header", "Composite indexes order entries by a sequence of indexed columns."),
        item("What does the TCP three-way handshake establish?", "Synchronized connection state between endpoints", "A DNS domain", "A database transaction", "A Wi-Fi password", "SYN, SYN-ACK, and ACK establish initial sequence state."),
        item("Why does TCP use sequence numbers?", "To order bytes and detect missing or duplicate segments", "To encrypt payloads", "To assign IP addresses", "To choose HTML colors", "Sequence numbers support reliable ordered delivery."),
        item("What does packet loss cause TCP to do?", "Retransmit missing data and adjust its sending behavior", "Ignore ordering forever", "Change the destination domain name", "Delete the application", "Acknowledgment and timeout mechanisms trigger retransmission."),
        item("What is network latency?", "Delay from sending data until an expected delivery or response", "Amount of stored disk space", "Processor instruction count only", "Number of database columns", "Latency measures communication delay."),
        item("What is bandwidth?", "Maximum data-transfer capacity per unit time", "Delay of one packet", "A password length", "A CPU process identifier", "Bandwidth describes a channel's data rate capacity."),
        item("What does a subnet mask determine?", "Which address bits identify the network prefix", "The web page's font", "The SQL primary key", "The CPU clock rate", "A subnet mask separates network and host portions of an IP address."),
        item("What is NAT commonly used for in IPv4 networks?", "Translating private internal addresses to one or more external addresses", "Encrypting every packet end to end", "Compiling source code", "Sorting database rows", "Network address translation rewrites address and often port information."),
        item("What does DHCP commonly provide to a client?", "Network configuration such as an IP address and gateway", "A compiled executable", "A database password", "A cryptographic private key necessarily", "DHCP leases configuration parameters to hosts."),
        item("What does an HTTP 404 status indicate?", "The requested resource was not found", "The request succeeded with content", "The server permanently moved the resource", "The client is authenticated", "HTTP 404 is the Not Found client-error response."),
        item("What does an HTTP 301 status indicate?", "A permanent redirect", "Successful content with no redirect", "Server crash necessarily", "Unauthorized access", "HTTP 301 tells clients that the resource has moved permanently."),
        item("Why are cookies used in HTTP applications?", "To let a server associate state with later requests from a client", "To increase CPU clock speed", "To route packets between networks", "To normalize databases", "Cookies carry small pieces of client-side state with matching requests."),
        item("What is a REST-style resource identifier commonly expressed as?", "A URI", "A CPU opcode", "A database transaction ID only", "A source-code variable necessarily", "HTTP APIs commonly identify resources using URIs."),
        item("What does JSON represent?", "Structured values using objects, arrays, and primitives", "Machine instructions only", "A network cable standard", "An image compression algorithm", "JSON is a text serialization format for structured data."),
        item("Why must a server validate client input even if the client validates it?", "Clients can be bypassed or modified", "Server validation slows all attacks to zero", "Browsers guarantee truthful input", "Networks remove malformed data", "Security boundaries cannot trust controls running on an untrusted client."),
        item("What is same-origin policy intended to restrict?", "Cross-origin access by web content", "CPU access to RAM", "SQL joins", "File names", "Browsers use origin boundaries to limit one site's access to another's data."),
        item("What is cross-site scripting?", "Injection of script content that runs in another user's browser context", "A server disk failure", "A database deadlock", "A sorting method", "XSS occurs when untrusted content is interpreted as active script."),
        item("What does escaping output help prevent in HTML contexts?", "Untrusted text being interpreted as markup or script", "All network latency", "Database backups", "CPU overheating", "Context-appropriate encoding preserves data as text."),
        item("What is a software dependency?", "Another package or component required by the software", "A CPU cooling fan", "A database row only", "A network broadcast", "Dependencies provide functionality that a project uses."),
        item("What is semantic versioning's major version intended to signal?", "Incompatible public API changes", "Only documentation spelling changes", "A guaranteed security fix", "The number of developers", "Under semantic versioning, a major increment denotes breaking API changes."),
        item("What is continuous integration?", "Frequently building and testing integrated changes automatically", "Deploying every untested change", "A database transaction mode", "A network routing protocol", "CI gives rapid feedback on combined code changes."),
        item("Why are code reviews useful?", "They let others assess correctness, maintainability, and risks before integration", "They guarantee zero defects", "They replace all tests", "They compile code faster", "Review adds independent examination and knowledge sharing."),
        item("What is technical debt?", "Future cost created by expedient design or implementation choices", "A cloud invoice only", "A network packet", "A database key", "Short-term shortcuts can require later remediation and slow change."),
        item("What is an interface in software design?", "A contract describing available operations without requiring implementation details", "A specific monitor", "A database backup", "A CPU cache", "Interfaces separate what a component offers from how it works."),
        item("What does encapsulation do?", "Bundles state with behavior and controls access to implementation details", "Makes every field globally writable", "Deletes object state", "Routes network traffic", "Encapsulation limits coupling through defined boundaries."),
        item("What does inheritance model in object-oriented programming?", "A subtype reusing or extending behavior of a base type", "A database transaction", "A network packet copy", "A loop condition", "Inheritance relates classes through shared or specialized behavior."),
        item("What is polymorphism?", "Using a common interface with different implementations", "Storing only one data type globally", "Encrypting a file twice", "Assigning multiple IP addresses", "Polymorphism lets callers work through an abstraction."),
        item("What is immutability?", "An object's observable state cannot change after creation", "An object has no value", "A program cannot create objects", "Memory is always read-only", "Immutable values are replaced rather than modified."),
        item("Why can immutable data simplify concurrent programming?", "It cannot be changed by another thread after sharing", "It makes scheduling unnecessary", "It eliminates all memory use", "It forces every operation to be O(1)", "Absence of mutation removes many shared-state races."),
        item("What is dependency injection?", "Supplying a component's dependencies from outside it", "Downloading every dependency at runtime", "Injecting SQL text", "Adding CPU registers", "External provision reduces hard-coded coupling and improves testability."),
        item("What is a mock object in testing?", "A controlled substitute used to verify interactions or isolate dependencies", "A production database copy necessarily", "A compiler warning", "A network router", "Mocks simulate collaborators under test control."),
        item("What is regression testing?", "Checking that previously working behavior remains intact after changes", "Testing only brand-new features", "Measuring network bandwidth", "Deleting old tests", "Regression suites detect unintended reintroduction of defects."),
        item("What is property-based testing?", "Generating many inputs to check general behavioral properties", "Testing one hand-written input only", "Proving hardware safety", "A database indexing method", "Property-based tools explore input spaces against invariants."),
        item("What is fuzz testing?", "Feeding varied or malformed inputs to discover failures", "Sorting test names", "Encrypting test output", "Testing only valid empty input", "Fuzzers exercise parsers and interfaces with automatically varied data."),
        item("What is a stack overflow in program execution?", "Exhaustion of call-stack space, often from excessive recursion", "A network switch failure", "A database table with many rows", "A disk backup", "Unbounded or deep calls can consume the finite call stack."),
        item("What is a memory leak?", "Allocated memory remains unreachable or unreleased despite no longer being needed", "RAM contents are encrypted", "A file is copied", "A CPU register changes", "Leaks cause a program's retained memory to grow unnecessarily."),
        item("What is garbage collection?", "Automatic reclamation of unreachable managed objects", "Deleting source repositories", "Cleaning a keyboard", "Compressing network packets", "A garbage collector identifies objects no longer reachable by the program."),
        item("What is serialization?", "Encoding an in-memory value for storage or transmission", "Executing a thread serially only", "Deleting object fields", "Sorting data", "Serialization converts structured state into a transferable representation."),
        item("Why can deserializing untrusted data be dangerous?", "Some formats or libraries can trigger unsafe object construction or code paths", "Serialized data cannot contain bytes", "Networks guarantee safety", "Deserialization always validates permissions", "Unsafe deserialization may instantiate attacker-controlled types or state."),
        item("What does idempotent mean for an operation?", "Repeating it has the same intended effect as performing it once", "It can execute only once", "It always fails twice", "It uses no data", "Idempotence makes repeated application converge on the same state."),
        item("Why are idempotent operations useful in distributed systems?", "A request can be retried without duplicating its intended effect", "They remove all network failures", "They guarantee zero latency", "They eliminate storage", "Retries are safer when repeated execution does not multiply effects."),
        item("What does eventual consistency mean?", "Replicas may temporarily differ but converge if updates stop", "Every read always returns the latest global value", "No replica stores data", "Transactions cannot occur", "Asynchronous replication allows temporary divergence before convergence."),
        item("What is horizontal scaling?", "Adding more machines or instances", "Installing a faster CPU in one machine", "Reducing the number of servers", "Compressing source code", "Horizontal scaling distributes load across additional nodes."),
        item("What is vertical scaling?", "Increasing resources of one machine", "Adding more independent machines", "Splitting a database table", "Changing a URL", "Vertical scaling gives a node more CPU, memory, or storage."),
        item("What is load balancing?", "Distributing requests among multiple service instances", "Sorting data on disk", "Encrypting passwords", "Compiling programs", "A load balancer spreads work to improve capacity and availability."),
        item("What is redundancy used for in reliable systems?", "Providing alternate components when one fails", "Ensuring every component is unique", "Removing backups", "Disabling monitoring", "Redundant resources reduce single points of failure."),
        item("What is observability?", "Ability to infer internal system state from outputs such as logs, metrics, and traces", "A monitor's screen size", "Source-code formatting", "A database primary key", "Observability supports diagnosis through emitted telemetry."),
        item("What is a log message?", "A timestamped record of an event or state", "A CPU instruction set", "A database schema", "A network cable", "Logs capture discrete events useful for auditing and diagnosis."),
        item("What is a metric in system monitoring?", "A numeric measurement tracked over time", "A source-code comment", "A password", "A relational foreign key", "Metrics quantify behavior such as latency, error rate, or resource use."),
        item("What does a distributed trace show?", "A request's path and timing across services", "Only a server's disk layout", "A compiled binary", "A database backup", "Trace spans connect work performed across component boundaries."),
        item("What does backpressure mean in a data-processing pipeline?", "A slow consumer signals upstream producers to reduce or pause output", "A producer discards every result", "The network reverses packet direction", "The database removes constraints", "Backpressure prevents unbounded buffering when downstream capacity is lower."),
        item("Why is pagination useful for a large API result set?", "It bounds each response and lets clients retrieve results incrementally", "It guarantees every record fits in one packet", "It removes the need for ordering", "It encrypts the database", "Pagination limits per-request work and payload size."),
        item("What does a circuit breaker pattern do after repeated downstream failures?", "Temporarily stops calls so the dependency can recover and callers fail quickly", "Retries forever without delay", "Deletes the downstream service", "Commits database transactions", "Opening the circuit limits cascading load during an outage."),
    ])

    if len(items) != 110:
        raise ValueError(
            f"Expected 110 medium CS items, found {len(items)}"
        )

    return items


def build_hard_items() -> list[Item]:
    return [
        item("A recursive function splits an n-element input into two equal halves, solves both halves, and performs linear merge work. What recurrence and complexity fit it?", "T(n)=2T(n/2)+O(n), giving O(n log n)", "T(n)=T(n-1)+O(1), giving O(n)", "T(n)=2T(n)+O(1), giving O(1)", "T(n)=T(n/2)+O(1), giving O(log n)", "The recursion has two half-size subproblems and linear work at each of logarithmically many levels."),
        item("Dijkstra's algorithm is run on a graph containing a reachable negative-weight edge. What is the key problem?", "Its greedy finalized distances may be wrong", "It cannot store vertices", "It always becomes breadth-first search", "Negative edges make every path infinite", "Dijkstra's finalization argument requires nonnegative edge weights."),
        item("Why can a comparison sort not guarantee better than O(n log n) comparisons for arbitrary distinct inputs?", "Its decision tree needs at least n! leaves", "Every comparison takes O(n)", "Arrays cannot be indexed", "Sorting requires hashing", "Distinguishing n! orders requires decision-tree height at least log2(n!)."),
        item("A hash table has load factor far above its design target. What performance effect is most likely?", "More collisions and slower expected operations", "Guaranteed constant zero-time lookup", "Keys become sorted", "Memory use becomes zero", "Crowded buckets or probe sequences increase collision cost."),
        item("A directed graph has an edge from every task to each prerequisite. Which operation detects whether the dependency relation contains a cycle?", "Topological-sort failure or depth-first cycle detection", "Binary search on task names", "Bubble sorting edge weights", "Hashing each vertex once", "A directed cycle prevents a complete topological ordering."),
        item("Why can deleting a node with two children from a binary search tree use its in-order successor?", "The successor is the smallest key greater than the deleted key", "The successor is always the root", "It is the largest key in the left subtree", "It has two larger children necessarily", "Replacing with the next ordered key preserves search-tree ordering."),
        item("Two threads each increment a shared integer using read-modify-write without synchronization. Why can increments be lost?", "Both can read the same old value and overwrite one another's updates", "Integer addition is undefined", "Threads cannot share memory", "The scheduler always runs one thread to completion", "The compound operation is not atomic, so interleavings can collapse updates."),
        item("Thread A locks X then waits for Y, while thread B locks Y then waits for X. What condition is demonstrated?", "Circular wait causing deadlock", "Starvation without held resources", "A cache hit", "Database normalization", "Each thread waits for a resource held by the other, forming a wait cycle."),
        item("Why can copy-on-write make process creation cheaper?", "Parent and child share pages until one modifies them", "It copies every page twice immediately", "It disables virtual memory", "It prevents child execution", "Deferred copying avoids duplicating untouched pages."),
        item("A transaction reads the same row twice and sees different committed values. Which anomaly occurred?", "Non-repeatable read", "Dirty write only", "Lost packet", "Stack overflow", "Another committed update changed the row between the two reads."),
        item("A query filters by equality on columns A and B. Which index is most directly designed for this access?", "A composite index beginning with A and B in a useful order", "An index on unrelated column C only", "No index can support equality", "A text file backup", "A matching composite key can narrow candidates using both predicates."),
        item("Why can an index on (A, B) support a query on A more naturally than a query only on B?", "B-tree ordering is organized first by the leading column A", "B is never stored", "A indexes contain no keys", "SQL forbids B predicates", "The leftmost-prefix property follows the index's lexicographic order."),
        item("Two concurrent transactions both read balance 100, subtract 10, and write 90. What anomaly loses one subtraction?", "Lost update", "Dirty read", "Phantom read only", "Referential integrity", "One write overwrites the other because both derived from the same old value."),
        item("Why does TLS authenticate a server certificate chain?", "To bind the server's public key to a trusted identity", "To hide the server's IP from routers", "To compress HTML", "To assign database permissions", "Certificate validation checks signatures and names before trusting the presented key."),
        item("An attacker changes a message and its ordinary checksum. Why is a keyed MAC stronger for integrity?", "The attacker lacks the secret key needed to forge a valid tag", "A MAC contains no bits", "Checksums encrypt all data", "A MAC prevents packet loss", "Cryptographic authentication tags resist deliberate modification without the key."),
        item("Why should encryption normally use a unique nonce with modes that require it?", "Nonce reuse can reveal relationships or break security guarantees", "A nonce is the decryption password", "Unique nonces reduce key length to zero", "Reusing nonces increases randomness", "Many encryption modes assume nonce uniqueness under a key."),
        item("A web application concatenates user text into a shell command. What is the primary risk?", "Command injection", "Database normalization", "Deadlock", "Cache eviction", "Metacharacters can change the command structure if input is interpreted as shell syntax."),
        item("Why is checking authorization only in a user interface insufficient?", "A client can call backend endpoints directly", "User interfaces always encrypt requests", "Backends cannot identify users", "Buttons enforce kernel permissions", "Security decisions must be enforced at the trusted server boundary."),
        item("A replicated service requires responses from a majority of five nodes. How many node responses form a majority?", "3", "2", "4 necessarily", "5 only", "Any set of three is more than half of five and intersects every other majority."),
        item("Why do consensus systems use terms or epochs with leader identities?", "To distinguish newer leadership from stale messages", "To encrypt all client data", "To eliminate network partitions", "To sort database columns", "Monotonic terms help nodes reject outdated leaders and requests."),
        item("A cache uses write-through policy. What happens on a write?", "The cache and backing store are updated before completion", "Only the cache is updated indefinitely", "The value is discarded", "Every cache line is invalidated globally", "Write-through keeps backing storage current at the cost of write latency."),
        item("A service is healthy on average but has rare very slow requests. Which metric reveals this better than mean latency?", "A high percentile such as p99 latency", "Request count only", "CPU model name", "Median source-code line length", "Tail percentiles expose slow outliers hidden by an average."),
    ]


def build_cs_items() -> dict[str, list[Item]]:
    easy = build_easy_items()
    medium = build_medium_items()
    hard = build_hard_items()

    if len(easy) != 88:
        raise ValueError(
            f"Expected 88 easy CS items, found {len(easy)}"
        )

    if len(hard) != 22:
        raise ValueError(
            f"Expected 22 hard CS items, found {len(hard)}"
        )

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
    }
