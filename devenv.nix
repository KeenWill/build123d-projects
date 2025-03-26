{ pkgs, config, ... }: {

  packages = with pkgs; [
    cmake
    clang
    gcc
    opencascade-occt
    zlib
    git
    aws-crt-cpp
  ];

  cachix.enable = false;

  languages.python = {
    enable = true;
    version = "3.12";
    libraries = with pkgs; [
      cmake
      clang
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
      git
      aws-crt-cpp
      xorg.libxrender
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
      modal
      git+https://github.com/Ruudjhuu/gridfinity_build123d
    '';
    uv.enable = true;
  };

  # Runs on `git commit` and `devenv test`
  git-hooks.hooks = {
    black.enable = true;
  };
}

