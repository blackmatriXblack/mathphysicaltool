# Math & Physics Toolkit – GUI Technical Documentation

## 1. Overview

The **Math & Physics Toolkit** is a comprehensive desktop application designed to perform calculations across 27 domains of mathematics and physics. It features a minimalist, dark-themed Graphical User Interface (GUI) built with Python’s `tkinter` library, alongside an embedded Command Line Interface (CLI) terminal for advanced users.

This document details the architecture, module structure, user interface components, and operational logic of `gui_app.py`.

---

## 2. System Architecture

### 2.1 Core Technology Stack
- **Language:** Python 3
- **GUI Framework:** `tkinter` (standard library)
- **Styling:** Custom dark theme using hexadecimal color constants.
- **Module Loading:** Dynamic import via `importlib` for lazy loading of calculation modules.
- **CLI Integration:** `subprocess` module to execute external CLI commands (`main.py`) from within the GUI.

### 2.2 Directory Structure Assumptions
The GUI assumes the following project structure:
```text
project_root/
├── gui_app.py          # The GUI application (this file)
├── main.py             # The CLI entry point
└── src/                # Package containing calculation modules
    ├── mechanics.py
    ├── thermo.py
    ├── electromagnetism.py
    ├── ...
    └── abstract_algebra.py
```

---

## 3. Configuration & Constants

### 3.1 Theme Constants
The application uses a consistent dark theme defined by the following constants:
- **Backgrounds:** `BG` (#1a1a2e), `BG2` (#16213e), `BG3` (#0f3460)
- **Foregrounds:** `FG` (#e0e0e0), `FG2` (#a0a0b0)
- **Accents:** `ACCENT` (#e94560 - Red/Pink), `ACCENT2` (#533483 - Purple)
- **Fonts:**
  - `FONT_MONO`: Consolas, 10pt (for code/results)
  - `FONT_SM/MD/LG/HDR`: Segoe UI variants for UI elements.

### 3.2 Domain Registry
The application supports 27 specific domains, mapped between internal keys and display names.

| Internal Key | Display Name | Module Path (`src.*`) |
| :--- | :--- | :--- |
| `mechanics` | Classical Mechanics | `src.mechanics` |
| `thermo` | Thermodynamics | `src.thermo` |
| `em` | Electromagnetism | `src.electromagnetism` |
| `optics` | Optics & Photonics | `src.optics` |
| `acoustics` | Acoustics | `src.acoustics` |
| `relativity` | Relativity | `src.relativity` |
| `quantum` | Quantum Mechanics | `src.quantum` |
| `atomic` | Atomic & Condensed Matter | `src.atomic` |
| `nuclear` | Nuclear & Particle Physics | `src.nuclear` |
| `astro` | Astrophysics & Cosmology | `src.astrophysics` |
| `nonlinear` | Nonlinear & Chaos | `src.nonlinear` |
| `engineering` | Engineering Physics | `src.engineering` |
| `specialized` | Specialized Physics | `src.specialized` |
| `math-basic` | Basic Mathematics | `src.math_basic` |
| `geometry` | Geometry & Trigonometry | `src.math_geometry` |
| `discrete` | Discrete Mathematics | `src.discrete_math` |
| `probability` | Probability & Statistics | `src.probability` |
| `calculus` | Calculus & Analysis | `src.calculus` |
| `linalg` | Linear Algebra | `src.linear_algebra` |
| `diffeq` | Differential Equations | `src.differential_eq` |
| `numtheory` | Number Theory | `src.number_theory` |
| `optimization` | Optimization | `src.optimization` |
| `numerical` | Numerical Methods | `src.numerical` |
| `transforms` | Transforms & Signals | `src.transforms` |
| `geo-adv` | Advanced Geometry | `src.geometry_advanced` |
| `special-func` | Special Functions | `src.special_functions` |
| `ai-math` | AI & ML Mathematics | `src.ai_math` |
| `algebra` | Abstract Algebra | `src.abstract_algebra` |

---

## 4. Class Structure: `MathPhysicsGUI`

The entire application is encapsulated within the `MathPhysicsGUI` class.

### 4.1 Initialization (`__init__`)
- Initializes the main Tk window (`self.root`).
- Sets window title, geometry (1200x750), and background color.
- Initializes state variables:
  - `commands_cache`: Dictionary to store loaded module commands.
  - `current_domain` / `current_command`: Tracks user selection.
  - `param_entries`: Dictionary to hold input field widgets.
- Calls `_build_ui()` to construct the interface.
- Calls `_load_all_commands()` (currently a placeholder; loading is lazy).

### 4.2 UI Construction (`_build_ui`)
The UI is divided into three main sections:

1.  **Top Bar:**
    - Displays the application title "MATH & PHYSICS TOOLKIT".
    - Contains buttons for **CLI Terminal** and **About**.
2.  **Main Paned Window (`tk.PanedWindow`):**
    - **Left Pane (Sidebar):** Contains the Domain Tree.
    - **Right Pane (Content Area):** Displays command lists, input forms, and results.
3.  **Status Bar:**
    - Located at the bottom, provides context-sensitive feedback (e.g., "Ready", "Calculation complete").

### 4.3 Domain Tree (`_build_tree`)
- Uses `ttk.Treeview` to display a hierarchical list of domains.
- **Root Nodes:** "PHYSICS" and "MATHEMATICS".
- **Child Nodes:** Specific domains (e.g., "Classical Mechanics", "Calculus").
- **Styling:** Custom `ttk.Style` configured for the dark theme.
- **Event Binding:** `<<TreeviewSelect>>` triggers `_on_tree_select`.

---

## 5. Operational Logic

### 5.1 Lazy Loading (`_load_domain_commands`)
To optimize performance, modules are not imported at startup. Instead:
1.  When a user selects a domain in the tree, `_on_tree_select` is called.
2.  It checks `self.commands_cache`.
3.  If missing, it uses `importlib.import_module()` to load the corresponding module from `src/`.
4.  It extracts the `COMMANDS` dictionary from the module.
5.  Errors during import are caught and displayed via `messagebox.showerror`.

### 5.2 Command Picker (`_show_command_picker`)
When a domain is selected:
1.  The right pane is cleared.
2.  A header displays the Domain Name and command count.
3.  A scrollable list of commands is generated.
    - Each command card shows the **Name** and **Description**.
    - Parameters are listed briefly (e.g., `params: [mass, velocity]`).
4.  Clicking a command card triggers `_show_input_form`.

### 5.3 Input Form (`_show_input_form`)
When a specific command is selected:
1.  The right pane is cleared.
2.  A "Back" button is provided to return to the command list.
3.  **Parameter Inputs:**
    - For each parameter defined in the command's metadata, a labeled `tk.Entry` widget is created.
    - Labels use monospace font for clarity.
4.  **Action Buttons:**
    - **COMPUTE:** Triggers `_run_calculation`.
    - **Clear:** Resets input fields and result area.
5.  **Result Area:**
    - A `scrolledtext.ScrolledText` widget (read-only) is prepared to display output.

### 5.4 Calculation Execution (`_run_calculation`)
1.  Collects values from `self.param_entries`.
2.  Attempts to convert inputs to `float`. If conversion fails, the string value is passed (allowing for symbolic or non-numeric inputs if supported by the backend).
3.  Retrieves the function object from the loaded module: `commands[cmd_name]['func']`.
4.  Executes the function: `result = func(**params)`.
5.  Handles exceptions and displays errors via `_display_error`.
6.  On success, calls `_display_result`.

### 5.5 Result Display (`_display_result`)
Formats the output dictionary into a readable string:
```text
────────────────────────────────────────────────
  key1                   = value1
  key2                   = value2
────────────────────────────────────────────────
  RESULT                 = calculated_value
  UNIT                   = unit_string
────────────────────────────────────────────────
```

---

## 6. Embedded CLI Terminal

The application includes a feature to open a separate window acting as a CLI terminal.

### 6.1 Implementation (`_open_terminal`)
- Creates a `tk.Toplevel` window.
- Contains an output area (`ScrolledText`) and an input field (`Entry`).
- **Command Execution:**
    - Uses `subprocess.run` to execute `python main.py <args>`.
    - Captures `stdout` and `stderr`.
    - Displays output in the terminal window.
- **Special Commands:**
    - `help`: Displays usage instructions locally without calling subprocess.
    - `exit`/`quit`: Closes the terminal window.

### 6.2 CLI Usage Syntax
The terminal expects commands formatted for the underlying `main.py` script:
```bash
python main.py <domain> <command> --param1 val1 --param2 val2
python main.py list              # List all domains
python main.py <domain> list     # List commands in a domain
```

---

## 7. Error Handling

- **Import Errors:** Caught during module loading; displayed in a messagebox.
- **Calculation Errors:** Caught during `_run_calculation`; displayed in the result text area with prefix `ERROR:`.
- **Timeouts:** CLI commands are limited to a 30-second timeout.
- **Input Validation:** Basic type conversion (string to float) is attempted. Invalid numeric inputs may be passed as strings, relying on the backend module to handle validation or raise errors.

---

## 8. Extensibility

To add a new domain or command:

1.  **Create Module:** Add a new Python file in `src/` (e.g., `src/new_domain.py`).
2.  **Define COMMANDS:** Inside the module, define a `COMMANDS` dictionary:
    ```python
    COMMANDS = {
        'my-command': {
            'desc': 'Description of the command',
            'params': ['param1', 'param2'],
            'func': my_python_function
        }
    }
    ```
3.  **Update Registry:** Add the domain key and display name to `DOMAIN_REGISTRY` in `gui_app.py`.
4.  **Update Mapping:** Add the domain key and module path to `MODULE_MAP` in `gui_app.py`.
5.  **Update Tree:** Add the domain key to either `physics_domains` or `math_domains` list in `_build_tree`.

---

## 9. Dependencies

- **Standard Library:**
  - `tkinter`, `ttk`, `scrolledtext`, `messagebox`, `font`
  - `sys`, `os`, `json`, `subprocess`, `threading`, `importlib`
- **External Libraries:**
  - None explicitly required for the GUI itself.
  - *Note:* The backend modules in `src/` may require libraries like `numpy`, `scipy`, or `sympy`, but these are not imported in `gui_app.py`.

---

## 10. Version Information

- **Application Name:** Math & Physics Toolkit
- **File:** `gui_app.py`
- **Last Updated:** Based on provided code snapshot.
- **Author:** cagent (User Context)
