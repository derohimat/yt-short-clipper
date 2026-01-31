import sys
import traceback

try:
    # Import and run the app
    from app import YTShortClipperApp
    
    app = YTShortClipperApp()
    app.mainloop()
except Exception as e:
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"STARTUP ERROR:", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)
    sys.exit(1)
