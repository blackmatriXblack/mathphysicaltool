#!/usr/bin/env python3
"""
Math & Physics Toolkit - CLI
=============================
Comprehensive command-line calculator for all math and physics domains.
Usage: python main.py <domain> <subcommand> [--params ...]
       python main.py list              # Show all commands
       python main.py <domain> list     # Show domain commands
"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src import mechanics
from src import thermo
from src import electromagnetism
from src import optics
from src import acoustics
from src import relativity
from src import quantum
from src import atomic
from src import nuclear
from src import astrophysics
from src import nonlinear
from src import engineering
from src import specialized
from src import math_basic
from src import math_geometry
from src import discrete_math
from src import probability
from src import calculus
from src import linear_algebra
from src import differential_eq
from src import number_theory
from src import optimization
from src import numerical
from src import transforms
from src import geometry_advanced
from src import special_functions
from src import ai_math
from src import abstract_algebra

DOMAINS = {
    'mechanics': ('Classical Mechanics', mechanics.COMMANDS),
    'thermo': ('Thermodynamics & Statistical Physics', thermo.COMMANDS),
    'em': ('Electromagnetism', electromagnetism.COMMANDS),
    'optics': ('Optics & Photonics', optics.COMMANDS),
    'acoustics': ('Acoustics', acoustics.COMMANDS),
    'relativity': ('Relativity Physics', relativity.COMMANDS),
    'quantum': ('Quantum Mechanics', quantum.COMMANDS),
    'atomic': ('Atomic, Molecular & Condensed Matter', atomic.COMMANDS),
    'nuclear': ('Nuclear & Particle Physics', nuclear.COMMANDS),
    'astro': ('Astrophysics & Cosmology', astrophysics.COMMANDS),
    'nonlinear': ('Nonlinear Physics, Chaos & Fractals', nonlinear.COMMANDS),
    'engineering': ('Engineering Physics', engineering.COMMANDS),
    'specialized': ('Specialized Physics Branches', specialized.COMMANDS),
    'math-basic': ('Basic & Elementary Math', math_basic.COMMANDS),
    'geometry': ('Geometry & Trigonometry', math_geometry.COMMANDS),
    'discrete': ('Discrete Mathematics', discrete_math.COMMANDS),
    'probability': ('Probability & Statistics', probability.COMMANDS),
    'calculus': ('Calculus & Analysis', calculus.COMMANDS),
    'linalg': ('Linear Algebra', linear_algebra.COMMANDS),
    'diffeq': ('Differential Equations & Dynamical Systems', differential_eq.COMMANDS),
    'numtheory': ('Number Theory & Cryptography', number_theory.COMMANDS),
    'optimization': ('Optimization & Operations Research', optimization.COMMANDS),
    'numerical': ('Numerical Methods', numerical.COMMANDS),
    'transforms': ('Transforms & Signal Processing', transforms.COMMANDS),
    'geo-adv': ('Advanced Geometry & Topology', geometry_advanced.COMMANDS),
    'special-func': ('Special Functions', special_functions.COMMANDS),
    'ai-math': ('AI & Machine Learning Math', ai_math.COMMANDS),
    'algebra': ('Abstract Algebra', abstract_algebra.COMMANDS),
}


def run_command(domain_name: str, cmd_name: str, params: dict, as_json: bool = False) -> None:
    """Execute a command and print results."""
    _, commands = DOMAINS[domain_name]
    info = commands[cmd_name]
    func = info['func']

    result = func(**params)
    if as_json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"\n  {info.get('desc', cmd_name)}")
        print(f"  {'─' * 50}")
        for key, val in result.get('details', {}).items():
            print(f"  {key:20s} = {val}")
        print(f"  {'─' * 50}")
        print(f"  {'RESULT':20s} = {result['result']}")
        if result.get('unit'):
            print(f"  {'UNIT':20s} = {result['unit']}")
        print()


def cmd_list(args):
    """List all available commands."""
    if args.domain:
        if args.domain in DOMAINS:
            name, cmds = DOMAINS[args.domain]
            print(f"\n  {name}")
            print(f"  {'─' * 60}")
            for cname, info in cmds.items():
                params_str = ', '.join(info['params']) if info['params'] else 'none'
                print(f"  {cname:30s} | {params_str:30s} | {info['desc']}")
            print()
        else:
            print(f"Unknown domain: {args.domain}")
            print(f"Available: {', '.join(DOMAINS.keys())}")
    else:
        print(f"\n  Math & Physics Toolkit — {sum(len(c[1]) for c in DOMAINS.values())} commands in {len(DOMAINS)} domains\n")
        for dname, (dtitle, cmds) in DOMAINS.items():
            print(f"  [{dname:15s}] {dtitle} ({len(cmds)} commands)")
        print(f"\n  Use 'python main.py <domain> list' to see domain commands")
        print(f"  Use 'python main.py <domain> <command> --help' for parameter help\n")


def build_parser():
    """Build argparse with all domain subparsers."""
    parser = argparse.ArgumentParser(
        description='Math & Physics Toolkit — Comprehensive CLI Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    subparsers = parser.add_subparsers(dest='domain', help='Domain (use "list" to see all)')

    # Build subparser for each domain
    for dname, (dtitle, commands) in DOMAINS.items():
        dparser = subparsers.add_parser(dname, help=dtitle)
        dsub = dparser.add_subparsers(dest='command', help=f'{dtitle} commands')

        dsub.add_parser('list', help=f'List {dtitle} commands')

        for cname, info in commands.items():
            cparser = dsub.add_parser(cname, help=info.get('desc', cname))
            for param in info.get('params', []):
                cparser.add_argument(f'--{param}', type=str, default=None,
                                     help=f'{param}')

    # Add list as top-level subcommand
    list_parser = subparsers.add_parser('list', help='List all domains and commands')
    list_parser.add_argument('domain', nargs='?', help='Specific domain to list')

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Handle 'list' specially
    if args.domain == 'list':
        cmd_list(args)
        return

    if not args.domain:
        parser.print_help()
        return

    if args.domain not in DOMAINS:
        print(f"Unknown domain '{args.domain}'. Available: {', '.join(DOMAINS.keys())}")
        return

    # Handle domain-specific list
    if args.command == 'list':
        cmd_list(argparse.Namespace(domain=args.domain))
        return

    if not args.command:
        parser.parse_args([args.domain, '--help'])
        return

    _, commands = DOMAINS[args.domain]
    if args.command not in commands:
        print(f"Unknown command '{args.command}' in {args.domain}. Use '{args.domain} list'")
        return

    info = commands[args.command]
    import inspect
    sig = inspect.signature(info['func'])
    params = {}
    for param in info['params']:
        val = getattr(args, param, None)
        if val is not None:
            # Convert to proper type based on function signature
            if param in sig.parameters:
                ptype = sig.parameters[param].annotation
                if ptype is not inspect.Parameter.empty:
                    if ptype == int:
                        val = int(float(val))
                    elif ptype == float:
                        val = float(val)
                else:
                    # No annotation, try auto-detect
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            pass  # keep as string
            params[param] = val
        else:
            if param in sig.parameters:
                default = sig.parameters[param].default
                if default is not inspect.Parameter.empty:
                    params[param] = default
                else:
                    print(f"Error: Required parameter --{param} not provided")
                    return

    run_command(args.domain, args.command, params, args.json)


if __name__ == '__main__':
    main()
