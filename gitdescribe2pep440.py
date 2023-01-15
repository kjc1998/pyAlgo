def main():
    print(convert_git_to_pep440(input()))


def convert_git_to_pep440(git_describe):
    components = git_describe.strip().split("-")
    if len(components) == 1:
        pep440_version = components[0]
    else:
        version, ncommits, digest = components
        pep440_version = f"{version}.dev{ncommits}+{digest}"
    return pep440_version


if __name__ == "__main__":
    main()

### built in tests ###
import unittest


class TestConversion(unittest.TestCase):
    def test_convert_git_to_pep440(self):
        self.assertEqual(convert_git_to_pep440("1.0"), "1.0")
        self.assertEqual(
            convert_git_to_pep440("2.3-179-ga6dfb71"), "2.3.dev179+ga6dfb71"
        )
        self.assertEqual(convert_git_to_pep440("2-3-ga6dfb71"), "2.dev3+ga6dfb71")
        self.assertEqual(
            convert_git_to_pep440("2.3.5-179-ga6dfb71"), "2.3.5.dev179+ga6dfb71"
        )
