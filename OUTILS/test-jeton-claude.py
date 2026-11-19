"""Contrôles locaux de jeton-claude.py : extraction du jeton dans une sortie de terminal fabriquée."""
import importlib.util
import os

s = importlib.util.spec_from_file_location("jc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "jeton-claude.py"))
jc = importlib.util.module_from_spec(s)
s.loader.exec_module(jc)


def main():
    n = 0
    faux = "sk-" + "ant-oat01-" + "Ab3_" * 21 + "-Zz9AA"
    cas = [
        ("Your OAuth token:\r\n\r\n " + faux + ". You won't be able to see it again.", "fin de phrase"),
        ("\x1b[1m" + faux + "\x1b[22m\x1b[1CStore\x1b[1Cthis\x1b[1Ctoken", "texte collé par déplacement de curseur"),
        ("\x1b]8;id=1;https://x\x07lien\x1b]8;;\x07 " + faux + "Store", "texte collé sans séparateur"),
    ]
    for brut, nom in cas:
        assert jc.extraire(brut) == faux, nom
        n += 1
        print("OK : " + nom)
    assert jc.extraire("aucun jeton ici") is None
    n += 1
    print("OK : sortie sans jeton")
    print("%d controles OK" % n)


if __name__ == "__main__":
    main()
