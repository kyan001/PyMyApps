import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kindle_highlight_formatter as khf  # noqa: linter (pycodestyle) should not lint this line.


class test_filetrack(unittest.TestCase):
    """filetrack unittest"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        self.assertIsInstance(khf.__version__, str)

    def test_export(self):
        markdown = khf.generate_markdown("tests/example.html")
        expect = """
# § 《月亮与六便士》毛姆

## 《高更代表画作》

> 我不记得是谁曾经说过，为了修炼自己的灵魂，一个人每天都要做两件他不喜欢做的事。

> The world was full of odd persons, who did odd things; and perhaps they knew that a man is not what he wants to be , but what he wants to be.

## 第一章

> 我说的这种伟大，并不是哪个政客因官场走运而显赫一时，也不是某个军人因骁勇善战而声名卓著——那种人的功成名就，与其说是因为他们自身具有伟大的品质，倒不如说是他们所处的地位成就了他们，一旦时过境迁，他们也就显得微不足道了。我们时常发现，一位卸任的首相当年只不过是个能言善辩的演说家，一位将军离开了军队无非是个无所作为的市井英雄。

## 第二章

> 我由此得到一个启示：作者应得的报酬就在写作本身的乐趣之中，就在终于卸下了思想的重负之中，其他的一切都可置之度外，作品成功或失败，获得赞誉或诋毁，都大可不必在意。

> 有时，一个人会在有生之年久久盛名不衰，然后忽然风光不再，进入一个让他感到陌生的时代。
        """.strip()
        self.assertEqual(markdown, expect)


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
