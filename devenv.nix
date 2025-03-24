{ pkgs, config, ... }: {

  packages = [
    pkgs.cmake
    pkgs.gcc
    pkgs.opencascade-occt
  ];

  cachix.enable = false;

  languages.python = {
    enable = true;
    version = "3.13";
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

