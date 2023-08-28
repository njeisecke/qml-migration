# qml-migration

Some scripts to help migration of legacy code to the Qt 6.6 qml module system

## collect_modules.py

This one helps to convert code structured in the "old way":

[https://doc.qt.io/qt-6/qtqml-syntax-directoryimports.html]

to code structured using the cmake qt_add_qml_module command:

[https://www.qt.io/blog/whats-new-for-qml-modules-in-6.5]

The script writes a `CMakeLists.txt` for each directory containing `.qml` files.

It also outputs a shell script containing replace commands so that code like

    import "../.."
    import "../foo"

becomes

    import ui
    import ui.foo

The script follows the proposed directory structure, so if the project directory is `foo`, the
qml files should be located in some directory `foo/ui`. This will make tooling / QtCreator
work without further settings .

It's probably necessary to adjust the script but it should be a good starting point.
