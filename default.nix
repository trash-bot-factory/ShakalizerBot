{ pkgs ? import <nixpkgs> {} }:

with pkgs;
let
  telebot = python3Packages.buildPythonPackage rec {
    pname = "pyTelegramBotAPI";
    version = "3.6.6";
    src = python3Packages.fetchPypi {
      inherit pname version;
      sha256 = "00vycd7jvfnzmvmmhkjx9vf40vkcrwv7adas5i81r2jhjy7sks54";
    };
    doCheck = false;
    buildInputs = with python3Packages; [ requests six ];
  };
in python3Packages.buildPythonApplication rec {
  pname = "shakalizer";
  version = "1.0";
  src = lib.cleanSource ./.;
  checkPhase = "";

  propagatedBuildInputs = with python3Packages; [ pillow telebot requests six ];
}
