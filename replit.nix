{pkgs}: {
  deps = [
    pkgs.bash
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.bash
    ];
  };
}
