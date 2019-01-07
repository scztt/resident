""" Main application entry point.

    python -m resident  ...

"""
import sys
import cli

def main():
    """ Execute the application.

    """
    cli.main(sys.argv)


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
