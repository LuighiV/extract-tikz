import pytest

from extracttikz.test.data.tikz_object import tikz_appendix_contents
from extracttikz.io.save import save_file


@pytest.fixture(scope="session")
def tikz_file(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "tikz_appendix_file.png"
    save_file(fn, tikz_appendix_contents)
    return fn
