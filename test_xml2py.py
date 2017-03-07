import StringIO
import unittest
import xml2py

class TestXml2Py(unittest.TestCase):

    def setUp(self):
        self.xml_string = """
        <Test a='1' b='2'>
            Test text
            <a>
                <b n='1' />
                <b n='2' />
                <c n='3' >
                    <cc n='3.3' m='mmm'>a.c.cc text</cc>
                </c>
                <d n='4' />
                <d n='5' />
                <b n='6' />
                <e>e text</e>
            </a>
        </Test>
        """
        self.xml_file = StringIO.StringIO(self.xml_string)

    def test_dict_load(self):
        self.xml_file.seek(0)
        d = xml2py.dict_load(self.xml_file)
        self.assertEqual(d['Test']['_a'], '1')
        self.assertEqual(d['Test']['_text_'].strip(), 'Test text')
        self.assertEqual(d['Test']['a']['b'][2]['_n'], '6')
        
    def test_dict_loads(self):
        d = xml2py.dict_loads(self.xml_string)
        self.assertEqual(d['Test']['a']['e'], 'e text')
        
    def test_dotdict_load(self):
        self.xml_file.seek(0)
        dd = xml2py.dotdict_load(self.xml_file)
        self.assertEqual(dd.Test.a.c.cc._text_, 'a.c.cc text')
        
    def test_dotdict_loads(self):
        dd = xml2py.dotdict_loads(self.xml_string)
        self.assertEqual(dd.Test.a.c.cc._text_, 'a.c.cc text')
        
    def test_to_dotdict(self):
        dd = xml2py.to_dotdict({})
        tup = xml2py.to_dotdict((dd, ))
        self.assertEqual(tup, ({}, ))

    def test_to_list(self):
        d = xml2py.dict_loads(self.xml_string)
        dd = xml2py.to_list(d['Test']['a'], 'd')
        self.assertEqual(dd, [{'_n': '4'}, {'_n': '5'}])
        de = xml2py.to_list(d['Test']['a'], 'e')
        self.assertEqual(de, ['e text', ])
        df = xml2py.to_list(d['Test']['a'], 'f')
        self.assertEqual(df, [])

if __name__ == '__main__':
    unittest.main()

