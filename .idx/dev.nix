# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.git
    pkgs.git-lfs
  ];

  # Sets environment variables in the workspace
  env = { }; # Not recommended
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.black-formatter"
      "ms-python.python"
      "ms-python.debugpy"
      "visualstudioexptteam.vscodeintellicode"
      "ms-python.vscode-pylance"
      # "vscodevim.vim"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        # Web preview
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # SETUP: Create the environment when created the workspace
        install-git-lfs = "git lfs install";
        pull-LF = "git lfs pull";
        put-env = "cat .env.example > .env";
        setup = "python -m venv .venv && sleep 2 && bash -c '. .venv/bin/activate && sleep 4 && pip install -r requirements.txt'";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Example: start a background task
        pull = "git pull";
        pull-LF = "git lfs pull";
        setup = "sleep 1 && . .venv/bin/activate && sleep 3 && pip install -r requirements.txt";
      };
    };
  };
}
