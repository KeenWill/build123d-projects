{ pkgs, config, ... }: {

  packages = [
    pkgs.cmake
    pkgs.gcc
    pkgs.opencascade-occt
    pkgs.zlib
  ];

  cachix.enable = false;

  languages.python = {
    enable = true;
    version = "3.12";
    libraries = with pkgs; [
      cmake
      gcc
      opencascade-occt
      zlib
      ffmpeg
      libGL
      libGLU
      xorg.libX11
      libgcc 
      binutils
      coreutils
      expat
      libz
    ];
    venv.enable = true;
    venv.requirements = ''
      requests
      build123d
      ocp_tessellate
      ocp_vscode
      ipykernel
      cadquery
      pip
      pylance
      numpy
      ninja
      git+https://github.com/Ruudjhuu/gridfinity_build123d
    '';
    uv.enable = true;
  };

  # Runs on `git commit` and `devenv test`
  git-hooks.hooks = {
    black.enable = true;
  };
}

