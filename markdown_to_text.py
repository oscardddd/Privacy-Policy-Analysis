#Markdown compiling
import markdown as mkd
from bs4 import BeautifulSoup
import mistune
from mistune import HTMLRenderer
import mistune.plugins

#NLP
import nltk
import nltk.tokenize

nltk.download('punkt')
FLAG_COMPONENTS = False

valid_end_punct = set((".","!","?",'"',"'"))
def finish_incomplete_sentences(text,flag_components=False):
    sentences = nltk.tokenize.sent_tokenize(text)
    if len(sentences) == 0:
        return ""
    words = nltk.tokenize.word_tokenize(sentences[-1])
    if not words[-1] in valid_end_punct:
        if flag_components:
            sentences[-1] = sentences[-1] + "_inserted_ . _inserted_"
        else:
            #Close sentence
            sentences[-1] = sentences[-1] + "."
    return " ".join(sentences)

class StraightTextRenderer(HTMLRenderer):
    
    def text(self, text):
        return text
    
    def link(self, text, url, title=None):
        if text is None:
            return "link"
        else:
            return text

    def image(self, alt, url, title=None):
        return ""

    def emphasis(self, text):
        return text

    def strong(self, text):
        return text

    def codespan(self, text):
        if FLAG_COMPONENTS:
            return "\n_codespan_%s_codespan\n" % text
        else:
            return "\n"

    def linebreak(self):
        if FLAG_COMPONENTS:
            return "\n_line break_\n"
        else:
            return "\n"

    def inline_html(self, html):
        if FLAG_COMPONENTS:
            return '\n_inline-html_%s_inline-html_\n' % html
        else:
            #HTML isn't prose
            return "\n"

    def paragraph(self, text):
        if text == '': return text
        paragraphs = text.split('\n')
        paragraphs = (finish_incomplete_sentences(para,flag_components=FLAG_COMPONENTS) for para in paragraphs)
        text = "\n".join(paragraphs)
        if FLAG_COMPONENTS:
            return "\n_paragraph_\n" + text + "\n_paragraph_\n"
        else:
            return text + "\n"

    def heading(self, text, level):
        if FLAG_COMPONENTS:
            return '\n_heading %d_ %s\n' % (level,text)
        else:
            #Headings aren't prose
            return "\n"

    def newline(self):
        if FLAG_COMPONENTS:
            return '\n_newline_\n'
        else:
            return "\n"

    def thematic_break(self):
        if FLAG_COMPONENTS:
            return '\n_thematic-break_\n'
        else:
            return "\n"

    def block_text(self, text):
        if FLAG_COMPONENTS:
            return '\n_block-text_%s_block-text_\n' % text
        else:
            return "%s\n" % text

    def block_code(self, code, info=None):
        if FLAG_COMPONENTS:
            if not code.strip():
                return "\n"
            else:
                return '\n_block-code_%s_block-code_\n' % code
        else:
            #This stuff usually isn't code, treat it as a paragraph
            return self.paragraph(code)

    def block_quote(self, text):
        if FLAG_COMPONENTS:
            return '\n_block-quote_%s_block-quote_\n' % text
        else:
            return "%s\n" % text

    def block_html(self, html):
        if FLAG_COMPONENTS:
            return "\n_block-html_%s_block-html\n" % html
        else:
            #HTML isn't prose
            return  "\n"

    def block_error(self, html):
        if FLAG_COMPONENTS:
            return "\n_block-error_%s_block-error\n" % html
        else:
            #Errors aren't prose
            return "\n"

    def list(self, text, ordered, **attrs):
        if text == '': return text
        items = text.split('\n')
        items = [finish_incomplete_sentences(item,flag_components=FLAG_COMPONENTS) for item in items]
        text = " ".join(items)
        if FLAG_COMPONENTS:
            return "\n_list %s _\n%s\n_list_\n" % (ordered, text)
        else:
            return text + "\n"

    def list_item(self, text, **attrs):
        return "%s\n" % text
    
    def strikethrough(self, text):
        return ""
    
    def table(self, text):
        if FLAG_COMPONENTS:
            return '\n_table_%s_table_\n' % (text)
        else:
            return "\n"
    
    def table_cell(self, text, align=None, head=False):
        if FLAG_COMPONENTS:
            return '\n_cell_\n'
        else:
            return f"{text} "
    
    def table_head(self, text):
        if FLAG_COMPONENTS:
            return '\n_head_\n'
        else:
            return ""
        
    def table_row(self, text):
        if FLAG_COMPONENTS:
            return '_row_%s_row_\n' % text
        else:
            return f"{text}.\n"
        
    def table_body(self, text):
        if FLAG_COMPONENTS:
            return '_body_%s_body_\n' % text
        else:
            return text

markdown = mistune.create_markdown(renderer=StraightTextRenderer(False),
                                   plugins=['table', 'strikethrough']
                                   )

def clean_md(policy_text):
    return markdown(policy_text)

def clean_md_bs4(policy_text):
    html = mkd.markdown(policy_text)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()