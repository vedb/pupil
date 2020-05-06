# -*- mode: python -*-


import platform, sys, os, os.path, numpy, glob, pathlib

av_hidden_imports = [
    "av.format",
    "av.packet",
    "av.buffer",
    "av.bytesource",
    "av.frame",
    "av.stream",
    "av.descriptor",
    "av.plane",
    "av.audio.plane",
    "av.container.streams",
    "av.dictionary",
    "av.audio.stream",
    "av.subtitles",
    "av.subtitles.stream",
    "av.subtitles.subtitle",
    "av.video.reformatter",
    "av.video.plane",
    "av.option",
    "av.container.pyio",
    "av.video.codeccontext",
    "av.audio.codeccontext",
    "av.filter.context",
    "av.filter.link",
    "av.filter.pad",
    "av.buffered_decoder",
]
if platform.system() != "Windows":
    av_hidden_imports.append("cysignals")

pyglui_hidden_imports = [
    "pyglui.pyfontstash.fontstash",
    "pyglui.cygl.shader",
    "pyglui.cygl.utils",
]

from pyglui import ui

if platform.system() == "Darwin":
    sys.path.append(".")
    from version import pupil_version

    del sys.path[-1]

    a = Analysis(
        ["../../pupil_src/main.py"],
        pathex=["../../pupil_src/shared_modules/"],
        hiddenimports=[] + av_hidden_imports + pyglui_hidden_imports,
        hookspath=None,
        runtime_hooks=None,
        excludes=["matplotlib"],
    )
    pyz = PYZ(a.pure)
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name="pupil_service",
        debug=False,
        strip=None,
        upx=False,
        console=True,
    )

    # exclude system lib.
    libSystem = [bn for bn in a.binaries if "libSystem.dylib" in bn]
    coll = COLLECT(
        exe,
        a.binaries - libSystem,
        a.zipfiles,
        a.datas,
        [("libuvc.0.dylib", "/usr/local/lib/libuvc.0.dylib", "BINARY")],
        [("libglfw.dylib", "/usr/local/lib/libglfw.dylib", "BINARY")],
        [("pyglui/OpenSans-Regular.ttf", ui.get_opensans_font_path(), "DATA")],
        [("pyglui/Roboto-Regular.ttf", ui.get_roboto_font_path(), "DATA")],
        [("pyglui/pupil_icons.ttf", ui.get_pupil_icons_font_path(), "DATA")],
        strip=None,
        upx=True,
        name="Pupil Service",
    )

    app = BUNDLE(
        coll,
        name="Pupil Service.app",
        icon="pupil-service.icns",
        version=str(pupil_version()),
        info_plist={"NSHighResolutionCapable": "True"},
    )


elif platform.system() == "Linux":
    a = Analysis(
        ["../../pupil_src/main.py"],
        pathex=["../../pupil_src/shared_modules/"],
        hiddenimports=[] + av_hidden_imports + pyglui_hidden_imports,
        hookspath=None,
        runtime_hooks=None,
        excludes=["matplotlib"],
    )

    pyz = PYZ(a.pure)
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name="pupil_service",
        debug=False,
        strip=False,
        upx=True,
        console=True,
    )

    # libc is also not meant to travel with the bundle. Otherwise pyre.helpers with segfault.
    binaries = [b for b in a.binaries if not "libc.so" in b[0]]

    # libstdc++ is also not meant to travel with the bundle. Otherwise nvideo opengl drivers will fail to load.
    binaries = [b for b in binaries if not "libstdc++.so" in b[0]]

    # required for 14.04 16.04 interoperability.
    binaries = [b for b in binaries if not "libgomp.so.1" in b[0]]

    # required for 17.10 interoperability.
    binaries = [b for b in binaries if not "libdrm.so.2" in b[0]]

    coll = COLLECT(
        exe,
        binaries,
        a.zipfiles,
        a.datas,
        [("libglfw.so", "/usr/local/lib/libglfw.so", "BINARY")],
        [("libGLEW.so", "/usr/lib/x86_64-linux-gnu/libGLEW.so", "BINARY")],
        [("pyglui/OpenSans-Regular.ttf", ui.get_opensans_font_path(), "DATA")],
        [("pyglui/Roboto-Regular.ttf", ui.get_roboto_font_path(), "DATA")],
        [("pyglui/pupil_icons.ttf", ui.get_pupil_icons_font_path(), "DATA")],
        strip=True,
        upx=True,
        name="pupil_service",
    )

elif platform.system() == "Windows":
    import sys, os, os.path

    np_path = os.path.dirname(numpy.__file__)
    np_dlls = glob.glob(np_path + "/core/*.dll")
    np_dll_list = []

    for dll_path in np_dlls:
        dll_p, dll_f = os.path.split(dll_path)
        np_dll_list += [(dll_f, dll_path, "BINARY")]

    scipy_imports = ["scipy.integrate"]
    scipy_imports += [
        "scipy.integrate._ode",
        "scipy.integrate.quadrature",
        "scipy.integrate.odepack",
        "scipy.integrate._odepack",
        "scipy.integrate.quadpack",
        "scipy.integrate._quadpack",
    ]
    scipy_imports += [
        "scipy.integrate.vode",
        "scipy.integrate.lsoda",
        "scipy.integrate._dop",
        "scipy.special._ufuncs",
        "scipy.special._ufuncs_cxx",
    ]

    external_libs_path = pathlib.Path("../../pupil_external")

    a = Analysis(
        ["../../pupil_src/main.py"],
        pathex=["../../pupil_src/shared_modules/", str(external_libs_path)],
        binaries=None,
        datas=None,
        hiddenimports=pyglui_hidden_imports + scipy_imports + av_hidden_imports,
        hookspath=None,
        runtime_hooks=None,
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        excludes=["matplotlib"],
    )

    pyz = PYZ(a.pure)
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name="pupil_service.exe",
        icon="pupil-service.ico",
        debug=False,
        strip=None,
        upx=True,
        console=False,
        resources=["pupil-service.ico,ICON"],
    )

    vc_redist_path = external_libs_path / "vc_redist"
    vc_redist_libs = [
        (lib.name, str(lib), "BINARY") for lib in vc_redist_path.glob("*.dll")
    ]

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        [("PupilDrvInst.exe", "../../pupil_external/PupilDrvInst.exe", "BINARY")],
        [("glfw3.dll", "../../pupil_external/glfw3.dll", "BINARY")],
        [("pyglui/OpenSans-Regular.ttf", ui.get_opensans_font_path(), "DATA")],
        [("pyglui/Roboto-Regular.ttf", ui.get_roboto_font_path(), "DATA")],
        [("pyglui/pupil_icons.ttf", ui.get_pupil_icons_font_path(), "DATA")],
        np_dll_list,
        vc_redist_libs,
        strip=False,
        upx=True,
        name="Pupil Service",
    )
