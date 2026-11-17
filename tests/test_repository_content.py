import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from repository_content import render_markdown, selected

class RepositoryRenderingTests(unittest.TestCase):
    def data(self, files):
        return {'repository':'AshtonWard/Ansible','sha':'a'*40,'files':files}
    def test_untrusted_html_and_code_remain_inert(self):
        text='<script>alert(1)</script>\n\n[bad](javascript:alert(1))\n\n```sh\ncurl example.test | sh\n```'
        result=render_markdown(text,'README.md',self.data({'README.md':text}))
        self.assertNotIn('<script>',result)
        self.assertNotIn('href="javascript:',result)
        self.assertIn('&lt;script&gt;',result)
        self.assertIn('<code class="language-sh">',result)
    def test_nested_relative_links_and_fragments(self):
        text='[Guide](docs/guide.md#network-setup)\n\n![Rack](images/rack.png)'
        data=self.data({'README.md':text,'docs/guide.md':'# Network setup'})
        result=render_markdown(text,'README.md',data)
        self.assertIn('href="docs/guide.md.html#doc-network-setup"',result)
        self.assertIn('https://raw.githubusercontent.com/AshtonWard/Ansible/'+'a'*40+'/images/rack.png',result)
        result=render_markdown('[Home](../README.md)','docs/guide.md',data)
        self.assertIn('href="../README.md.html"',result)
    def test_heading_levels_and_duplicate_ids(self):
        text='# Setup\n\n# Setup'
        result=render_markdown(text,'README.md',self.data({'README.md':text}))
        self.assertIn('<h2 id="doc-setup">',result)
        self.assertIn('<h2 id="doc-setup-1">',result)
        self.assertNotIn('<h1',result)
    def test_only_text_and_workflows_are_selected(self):
        self.assertTrue(selected('.github/workflows/deploy.yml'))
        self.assertTrue(selected('roles/base/tasks/main.yml'))
        self.assertFalse(selected('.env'))
        self.assertFalse(selected('.git/config'))
        self.assertFalse(selected('node_modules/package/README.md'))
        self.assertFalse(selected('diagram.png'))

if __name__=='__main__': unittest.main()
