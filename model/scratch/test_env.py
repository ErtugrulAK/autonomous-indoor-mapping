import sys
print("Python version:", sys.version)
try:
    import ultralytics
    print("Ultralytics imported")
except ImportError:
    print("Ultralytics not found")
