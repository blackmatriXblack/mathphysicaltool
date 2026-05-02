#!/usr/bin/env python3
"""
Math & Physics Toolkit - GUI
==============================
Minimalist dark-themed GUI for all math and physics calculators.
Left: domain/command tree. Right: input form + result output.
Includes embedded terminal for CLI access.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font as tkfont
import sys
import os
import json
import subprocess
import threading
import importlib

sys.path.insert(0, os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# Theme constants
# ---------------------------------------------------------------------------
BG        = '#1a1a2e'
BG2       = '#16213e'
BG3       = '#0f3460'
FG        = '#e0e0e0'
FG2       = '#a0a0b0'
ACCENT    = '#e94560'
ACCENT2   = '#533483'
FONT_MONO = ('Consolas', 10)
FONT_SM   = ('Segoe UI', 9)
FONT_MD   = ('Segoe UI', 10)
FONT_LG   = ('Segoe UI', 11, 'bold')
FONT_HDR  = ('Segoe UI', 14, 'bold')

DOMAIN_REGISTRY = {
    'mechanics': 'Classical Mechanics',
    'thermo': 'Thermodynamics',
    'em': 'Electromagnetism',
    'optics': 'Optics & Photonics',
    'acoustics': 'Acoustics',
    'relativity': 'Relativity',
    'quantum': 'Quantum Mechanics',
    'atomic': 'Atomic & Condensed Matter',
    'nuclear': 'Nuclear & Particle Physics',
    'astro': 'Astrophysics & Cosmology',
    'nonlinear': 'Nonlinear & Chaos',
    'engineering': 'Engineering Physics',
    'specialized': 'Specialized Physics',
    'math-basic': 'Basic Mathematics',
    'geometry': 'Geometry & Trigonometry',
    'discrete': 'Discrete Mathematics',
    'probability': 'Probability & Statistics',
    'calculus': 'Calculus & Analysis',
    'linalg': 'Linear Algebra',
    'diffeq': 'Differential Equations',
    'numtheory': 'Number Theory',
    'optimization': 'Optimization',
    'numerical': 'Numerical Methods',
    'transforms': 'Transforms & Signals',
    'geo-adv': 'Advanced Geometry',
    'special-func': 'Special Functions',
    'ai-math': 'AI & ML Mathematics',
    'algebra': 'Abstract Algebra',
}

MODULE_MAP = {
    'mechanics': 'src.mechanics',
    'thermo': 'src.thermo',
    'em': 'src.electromagnetism',
    'optics': 'src.optics',
    'acoustics': 'src.acoustics',
    'relativity': 'src.relativity',
    'quantum': 'src.quantum',
    'atomic': 'src.atomic',
    'nuclear': 'src.nuclear',
    'astro': 'src.astrophysics',
    'nonlinear': 'src.nonlinear',
    'engineering': 'src.engineering',
    'specialized': 'src.specialized',
    'math-basic': 'src.math_basic',
    'geometry': 'src.math_geometry',
    'discrete': 'src.discrete_math',
    'probability': 'src.probability',
    'calculus': 'src.calculus',
    'linalg': 'src.linear_algebra',
    'diffeq': 'src.differential_eq',
    'numtheory': 'src.number_theory',
    'optimization': 'src.optimization',
    'numerical': 'src.numerical',
    'transforms': 'src.transforms',
    'geo-adv': 'src.geometry_advanced',
    'special-func': 'src.special_functions',
    'ai-math': 'src.ai_math',
    'algebra': 'src.abstract_algebra',
}


class MathPhysicsGUI:
    """Main GUI application."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Math & Physics Toolkit')
        self.root.geometry('1200x750')
        self.root.configure(bg=BG)
        self.root.minsize(900, 600)
        self.commands_cache = {}
        self.current_domain = None
        self.current_command = None
        self.param_entries = {}
        self._build_ui()
        self._load_all_commands()

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------
    def _build_ui(self):
        # -- Top bar ---------------------------------------------------------
        topbar = tk.Frame(self.root, bg=BG3, height=40)
        topbar.pack(fill=tk.X, side=tk.TOP)
        topbar.pack_propagate(False)

        tk.Label(topbar, text='MATH & PHYSICS TOOLKIT', font=FONT_HDR,
                 bg=BG3, fg=ACCENT).pack(side=tk.LEFT, padx=16, pady=6)

        btn_frame = tk.Frame(topbar, bg=BG3)
        btn_frame.pack(side=tk.RIGHT, padx=8, pady=4)
        tk.Button(btn_frame, text='CLI Terminal', font=FONT_SM, bg=BG2, fg=FG,
                  activebackground=ACCENT, activeforeground='#fff', relief=tk.FLAT,
                  cursor='hand2', padx=10, pady=3,
                  command=self._open_terminal).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='About', font=FONT_SM, bg=BG2, fg=FG,
                  activebackground=ACCENT, activeforeground='#fff', relief=tk.FLAT,
                  cursor='hand2', padx=10, pady=3,
                  command=self._show_about).pack(side=tk.LEFT, padx=4)

        # -- Main paned window ------------------------------------------------
        self.pw = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=BG, sashwidth=3,
                                 sashrelief=tk.FLAT)
        self.pw.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Left: domain tree
        self.left_frame = tk.Frame(self.pw, bg=BG2, width=280)
        self.pw.add(self.left_frame, minsize=220)
        self._build_tree()

        # Right: content area
        self.right_frame = tk.Frame(self.pw, bg=BG)
        self.pw.add(self.right_frame, minsize=500)

        # Right sub-layout
        self.form_frame = tk.Frame(self.right_frame, bg=BG)
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # Status bar
        self.status = tk.Label(self.root, text='Ready — Select a domain and command to begin.',
                               font=FONT_SM, bg=BG3, fg=FG2, anchor=tk.W, padx=12)
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def _build_tree(self):
        """Build the domain tree in the left sidebar."""
        lbl = tk.Label(self.left_frame, text='DOMAINS', font=('Segoe UI', 10, 'bold'),
                       bg=BG2, fg=FG2, anchor=tk.W)
        lbl.pack(fill=tk.X, padx=12, pady=(10, 4))

        tree_container = tk.Frame(self.left_frame, bg=BG2)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 8))

        self.tree = ttk.Treeview(tree_container, show='tree', selectmode='browse')
        self.tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background=BG2, foreground=FG, fieldbackground=BG2,
                        borderwidth=0, font=FONT_SM, rowheight=24)
        style.configure('Treeview.Heading', background=BG2, foreground=FG, borderwidth=0)
        style.map('Treeview', background=[('selected', ACCENT)],
                  foreground=[('selected', '#ffffff')])

        self.tree.tag_configure('domain', font=('Segoe UI', 10, 'bold'), foreground=ACCENT)
        self.tree.tag_configure('command', font=FONT_SM, foreground=FG2)

        physics_root = self.tree.insert('', tk.END, text='PHYSICS', open=True, tags=('domain',))
        math_root = self.tree.insert('', tk.END, text='MATHEMATICS', open=False, tags=('domain',))

        self.tree_nodes = {'physics': physics_root, 'math': math_root, 'items': {}}

        physics_domains = ['mechanics', 'thermo', 'em', 'optics', 'acoustics',
                           'relativity', 'quantum', 'atomic', 'nuclear', 'astro',
                           'nonlinear', 'engineering', 'specialized']
        math_domains = ['math-basic', 'geometry', 'discrete', 'probability', 'calculus',
                        'linalg', 'diffeq', 'numtheory', 'optimization', 'numerical',
                        'transforms', 'geo-adv', 'special-func', 'ai-math', 'algebra']

        for d in physics_domains:
            node = self.tree.insert(physics_root, tk.END, text=DOMAIN_REGISTRY[d],
                                    tags=('command',))
            self.tree_nodes['items'][d] = node

        for d in math_domains:
            node = self.tree.insert(math_root, tk.END, text=DOMAIN_REGISTRY[d],
                                    tags=('command',))
            self.tree_nodes['items'][d] = node

        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)

    # -----------------------------------------------------------------------
    # Command loading
    # -----------------------------------------------------------------------
    def _load_all_commands(self):
        """Lazy-load: commands loaded on demand when domain selected."""
        pass  # loaded in _on_tree_select

    def _load_domain_commands(self, domain_key: str):
        """Import module and get COMMANDS dict."""
        if domain_key in self.commands_cache:
            return self.commands_cache[domain_key]
        try:
            mod = importlib.import_module(MODULE_MAP[domain_key])
            cmds = getattr(mod, 'COMMANDS', {})
            self.commands_cache[domain_key] = cmds
            return cmds
        except Exception as e:
            messagebox.showerror('Load Error', f'Failed to load {domain_key}:\n{e}')
            return {}

    # -----------------------------------------------------------------------
    # Tree selection handler
    # -----------------------------------------------------------------------
    def _on_tree_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        text = self.tree.item(item, 'text')

        # Find which domain was selected
        selected_key = None
        for key, node in self.tree_nodes['items'].items():
            if node == item:
                selected_key = key
                break

        if not selected_key:
            return

        self.current_domain = selected_key
        commands = self._load_domain_commands(selected_key)
        self._show_command_picker(selected_key, commands)

    def _show_command_picker(self, domain_key: str, commands: dict):
        """Display command picker for the selected domain."""
        for w in self.form_frame.winfo_children():
            w.destroy()

        domain_name = DOMAIN_REGISTRY.get(domain_key, domain_key)

        # Header
        hdr = tk.Frame(self.form_frame, bg=BG)
        hdr.pack(fill=tk.X, pady=(0, 10))
        tk.Label(hdr, text=domain_name, font=FONT_LG, bg=BG, fg=ACCENT,
                 anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(hdr, text=f'{len(commands)} commands', font=FONT_SM, bg=BG, fg=FG2,
                 anchor=tk.W).pack(side=tk.LEFT, padx=8)

        if not commands:
            tk.Label(self.form_frame, text='No commands available.', font=FONT_MD,
                     bg=BG, fg=FG2).pack(pady=20)
            return

        # Scrollable command list
        canvas = tk.Canvas(self.form_frame, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.form_frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)

        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scroll_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mousewheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        canvas.bind_all('<MouseWheel>', _on_mousewheel)

        for cname, info in sorted(commands.items()):
            card = tk.Frame(scroll_frame, bg=BG2, cursor='hand2', padx=12, pady=8)
            card.pack(fill=tk.X, pady=2)

            tk.Label(card, text=cname.replace('-', ' ').title(), font=('Consolas', 10, 'bold'),
                     bg=BG2, fg=FG, anchor=tk.W).pack(anchor=tk.W)
            desc = info.get('desc', 'No description')
            params = ', '.join(info.get('params', []))
            tk.Label(card, text=f'{desc}  |  params: [{params}]',
                     font=FONT_SM, bg=BG2, fg=FG2, anchor=tk.W).pack(anchor=tk.W)

            for widget in [card] + list(card.winfo_children()):
                widget.bind('<Button-1>', lambda e, d=domain_key, c=cname, i=info:
                            self._show_input_form(d, c, i))
                widget.bind('<Enter>', lambda e, w=card: w.configure(bg=BG3))
                widget.bind('<Leave>', lambda e, w=card: w.configure(bg=BG2))

        self.status.config(text=f'{domain_name} — {len(commands)} commands loaded')

    # -----------------------------------------------------------------------
    # Input form
    # -----------------------------------------------------------------------
    def _show_input_form(self, domain_key: str, cmd_name: str, cmd_info: dict):
        """Display parameter input form for a command."""
        for w in self.form_frame.winfo_children():
            w.destroy()

        self.current_domain = domain_key
        self.current_command = cmd_name
        self.param_entries = {}

        domain_name = DOMAIN_REGISTRY.get(domain_key, domain_key)

        # Header
        hdr = tk.Frame(self.form_frame, bg=BG)
        hdr.pack(fill=tk.X, pady=(0, 10))
        tk.Label(hdr, text=cmd_name.replace('-', ' ').title(), font=FONT_LG,
                 bg=BG, fg=ACCENT, anchor=tk.W).pack(side=tk.LEFT)
        tk.Button(hdr, text='Back', font=FONT_SM, bg=BG2, fg=FG, relief=tk.FLAT,
                  cursor='hand2', padx=10,
                  command=lambda: self._show_command_picker(domain_key,
                           self._load_domain_commands(domain_key))
                  ).pack(side=tk.RIGHT, padx=4)

        # Description
        tk.Label(self.form_frame, text=cmd_info.get('desc', ''), font=FONT_MD,
                 bg=BG, fg=FG2, wraplength=600, anchor=tk.W).pack(fill=tk.X, pady=(0, 10))

        # Parameter inputs
        params = cmd_info.get('params', [])
        if params:
            param_frame = tk.Frame(self.form_frame, bg=BG)
            param_frame.pack(fill=tk.X, pady=6)

            for i, p in enumerate(params):
                row = tk.Frame(param_frame, bg=BG)
                row.pack(fill=tk.X, pady=3)
                tk.Label(row, text=p, font=FONT_MONO, bg=BG, fg=FG,
                         width=20, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 8))
                entry = tk.Entry(row, font=FONT_MONO, bg=BG3, fg=FG,
                                 insertbackground=FG, relief=tk.FLAT, width=20)
                entry.pack(side=tk.LEFT, ipady=4, ipadx=6)
                self.param_entries[p] = entry

            # Run button
            btn_row = tk.Frame(self.form_frame, bg=BG)
            btn_row.pack(fill=tk.X, pady=(10, 4))
            tk.Button(btn_row, text='COMPUTE', font=FONT_MD, bg=ACCENT, fg='#fff',
                      activebackground=ACCENT2, activeforeground='#fff',
                      relief=tk.FLAT, cursor='hand2', padx=24, pady=6,
                      command=lambda: self._run_calculation(domain_key, cmd_name, cmd_info)
                      ).pack(side=tk.LEFT, padx=(0, 8))
            tk.Button(btn_row, text='Clear', font=FONT_SM, bg=BG2, fg=FG,
                      relief=tk.FLAT, cursor='hand2', padx=16, pady=6,
                      command=self._clear_fields).pack(side=tk.LEFT)
        else:
            tk.Button(self.form_frame, text='COMPUTE', font=FONT_MD, bg=ACCENT, fg='#fff',
                      activebackground=ACCENT2, activeforeground='#fff',
                      relief=tk.FLAT, cursor='hand2', padx=24, pady=6,
                      command=lambda: self._run_calculation(domain_key, cmd_name, cmd_info)
                      ).pack(pady=10)

        # Result area
        result_label = tk.Label(self.form_frame, text='RESULT', font=('Segoe UI', 10, 'bold'),
                                bg=BG, fg=FG2, anchor=tk.W)
        result_label.pack(fill=tk.X, pady=(14, 4))

        self.result_text = scrolledtext.ScrolledText(
            self.form_frame, font=FONT_MONO, bg=BG3, fg=FG,
            insertbackground=FG, relief=tk.FLAT, height=12,
            wrap=tk.WORD, state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.status.config(text=f'{domain_name} > {cmd_name} — Enter parameters and click COMPUTE')

    # -----------------------------------------------------------------------
    # Computation
    # -----------------------------------------------------------------------
    def _run_calculation(self, domain_key: str, cmd_name: str, cmd_info: dict):
        """Execute the selected command with user parameters."""
        # Collect params
        params = {}
        for p in cmd_info.get('params', []):
            val = self.param_entries[p].get().strip()
            if val:
                try:
                    params[p] = float(val)
                except ValueError:
                    params[p] = val  # pass as string for non-numeric params

        # Run
        try:
            commands = self._load_domain_commands(domain_key)
            func = commands[cmd_name]['func']
            result = func(**params)
            self._display_result(result)
        except Exception as e:
            self._display_error(str(e))

    def _display_result(self, result: dict):
        """Pretty-print result in the result area."""
        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        lines = []
        lines.append('─' * 56)
        for key, val in result.get('details', {}).items():
            lines.append(f'  {key:22s} = {val}')
        lines.append('─' * 56)
        lines.append(f'  {"RESULT":22s} = {result["result"]}')
        if result.get('unit'):
            lines.append(f'  {"UNIT":22s} = {result["unit"]}')
        lines.append('─' * 56)

        self.result_text.insert(tk.END, '\n'.join(lines))
        self.result_text.configure(state=tk.DISABLED)
        self.status.config(text='Calculation complete')

    def _display_error(self, msg: str):
        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f'ERROR: {msg}')
        self.result_text.configure(state=tk.DISABLED)
        self.status.config(text='Error during calculation')

    def _clear_fields(self):
        for entry in self.param_entries.values():
            entry.delete(0, tk.END)
        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.configure(state=tk.DISABLED)

    # -----------------------------------------------------------------------
    # Terminal
    # -----------------------------------------------------------------------
    def _open_terminal(self):
        """Open CLI terminal in a new window."""
        term_win = tk.Toplevel(self.root)
        term_win.title('CLI Terminal — Math & Physics Toolkit')
        term_win.geometry('900x550')
        term_win.configure(bg=BG)

        tk.Label(term_win, text='CLI TERMINAL', font=FONT_HDR, bg=BG, fg=ACCENT
                 ).pack(pady=(10, 4))
        tk.Label(term_win, text='Type CLI commands below. "help" for commands, "exit" to close.',
                 font=FONT_SM, bg=BG, fg=FG2).pack()

        output = scrolledtext.ScrolledText(term_win, font=FONT_MONO, bg=BG3, fg=FG,
                                           insertbackground=FG, relief=tk.FLAT,
                                           height=18, wrap=tk.WORD, state=tk.DISABLED)
        output.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        input_frame = tk.Frame(term_win, bg=BG)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        tk.Label(input_frame, text='>', font=FONT_MONO, bg=BG, fg=ACCENT).pack(side=tk.LEFT)
        cmd_entry = tk.Entry(input_frame, font=FONT_MONO, bg=BG3, fg=FG,
                             insertbackground=FG, relief=tk.FLAT)
        cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, ipadx=6, padx=4)

        # Build CLI command list
        cli_path = os.path.join(os.path.dirname(__file__), 'main.py')

        def append_output(text):
            output.configure(state=tk.NORMAL)
            output.insert(tk.END, text + '\n')
            output.see(tk.END)
            output.configure(state=tk.DISABLED)

        def run_cli_command():
            cmd = cmd_entry.get().strip()
            if not cmd:
                return
            if cmd.lower() in ('exit', 'quit'):
                term_win.destroy()
                return

            cmd_entry.delete(0, tk.END)

            if cmd.lower() == 'help':
                append_output('─' * 50)
                append_output('  CLI Usage:')
                append_output('    python main.py <domain> <command> --param1 val1 --param2 val2')
                append_output('    python main.py list           # List all domains')
                append_output('    python main.py <domain> list   # List domain commands')
                append_output('    python main.py <domain> <cmd> --json  # JSON output')
                append_output('  Domains: ' + ', '.join(DOMAIN_REGISTRY.keys()))
                append_output('─' * 50)
                return

            append_output(f'> {cmd}')
            try:
                parts = ['python', cli_path] + cmd.split()
                result = subprocess.run(parts, capture_output=True, text=True, timeout=30,
                                        cwd=os.path.dirname(__file__))
                if result.stdout:
                    append_output(result.stdout.rstrip())
                if result.stderr:
                    append_output(f'[stderr] {result.stderr.rstrip()}')
            except subprocess.TimeoutExpired:
                append_output('[Timeout] Command took longer than 30 seconds.')
            except Exception as e:
                append_output(f'[Error] {e}')

        cmd_entry.bind('<Return>', lambda e: run_cli_command())

        append_output('Math & Physics Toolkit — CLI Terminal')
        append_output('Type "help" for usage. "exit" to close.')
        append_output('─' * 50)

        cmd_entry.focus_set()

    # -----------------------------------------------------------------------
    # About
    # -----------------------------------------------------------------------
    def _show_about(self):
        about = tk.Toplevel(self.root)
        about.title('About')
        about.geometry('460x320')
        about.configure(bg=BG)

        tk.Label(about, text='MATH & PHYSICS TOOLKIT', font=FONT_HDR, bg=BG, fg=ACCENT
                 ).pack(pady=(20, 8))
        tk.Label(about, text='Comprehensive CLI + GUI Calculator', font=FONT_MD, bg=BG, fg=FG
                 ).pack()
        tk.Label(about, text=f'  — 27 Domains of Mathematics & Physics', font=FONT_SM, bg=BG, fg=FG2
                 ).pack()
        tk.Label(about, text='All formulas computable. All equations solvable.',
                 font=FONT_SM, bg=BG, fg=FG2).pack()
        tk.Label(about, text='', bg=BG).pack()
        tk.Label(about, text='Usage:', font=FONT_MD, bg=BG, fg=ACCENT).pack()
        tk.Label(about, text='  GUI: Select domain > command > enter params > COMPUTE',
                 font=FONT_SM, bg=BG, fg=FG2).pack()
        tk.Label(about, text='  CLI: python main.py <domain> <command> --params',
                 font=FONT_SM, bg=BG, fg=FG2).pack()
        tk.Label(about, text='',
                 bg=BG).pack()
        tk.Button(about, text='Close', font=FONT_SM, bg=BG2, fg=FG, relief=tk.FLAT,
                  padx=20, pady=4, command=about.destroy).pack()

    # -----------------------------------------------------------------------
    # Run
    # -----------------------------------------------------------------------
    def run(self):
        self.root.mainloop()


def main():
    app = MathPhysicsGUI()
    app.run()


if __name__ == '__main__':
    main()
