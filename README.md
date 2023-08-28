# qml-migration

Some scripts to help migration of legacy code to the Qt 6.6 qml module system.

## collect_modules.py

It's probably necessary to adjust this script but it should be a good starting point.

The script helps to convert code structured in the "old way":

[https://doc.qt.io/qt-6/qtqml-syntax-directoryimports.html]

to code structured using the cmake qt_add_qml_module command:

[https://www.qt.io/blog/whats-new-for-qml-modules-in-6.5]

The script writes a `CMakeLists.txt` for each directory containing `.qml` files.

It also outputs a shell script `fix_imports.sh` containing replace commands so that code
like:

    import "../.."
    import "../foo"

is changed to:

    import ui
    import ui.foo

The script follows the proposed directory structure, so if the project directory is `foo`, the
qml files should be located in `foo/ui`, `foo/ui/module1`, .... This will make tooling / QtCreator
work without further settings.

Please note that any singleton component containing the `pragma Singleton` annotation must
be added to the CMakeLists.txt manually:

    set_source_files_properties(
      MySingleton.qml
      MyOtherSingleton.qml

      PROPERTIES
        QT_QML_SINGLETON_TYPE TRUE
    )

## enable_unity_builds.py

This script enables cmake unity builds for all the generated `CMakeLists.txt`. While this does
not make much difference for incrementals builds, it significantly saves time in rebuilds of a project.
