{
  description = "ReproRestore starter implementation";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in {
      packages = forAllSystems (system:
        let pkgs = import nixpkgs { inherit system; };
        in {
          default = pkgs.python3Packages.buildPythonApplication {
            pname = "reprorestore";
            version = "0.1.0";
            pyproject = true;
            src = ./.;
            build-system = [ pkgs.python3Packages.setuptools ];
            nativeCheckInputs = [ pkgs.python3Packages.setuptools ];
            doCheck = true;
            checkPhase = ''
              python -m unittest discover -s tests -v
            '';
          };
        });

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/reprorestore";
        };
      });
    };
}
