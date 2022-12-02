import launch

if not launch.is_installed("pillow"):
    launch.run_pip("install pillow")
if not launch.is_installed("glob"):
    launch.run_pip("install glob")
if not launch.is_installed("os"):
    launch.run_pip("install os")