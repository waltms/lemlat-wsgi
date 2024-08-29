from urllib.parse import parse_qs
from html import escape
import sys, os, re
import subprocess
import tempfile

lemlat_bin = "lemlat"
lemlat_path = "/var/www/wsgi/lemlat/"
acceptable_referers = ['your.referer.com']
logeion_url = "https://logeion.uchicago.edu/"
need_referer = False

def referer_check(env):
    if 'HTTP_REFERER' in env and need_referer:
        referer = env['HTTP_REFERER']
        print(referer, file=sys.stderr)
        for host in acceptable_referers:
            if host in referer: return True
        return False
    return not need_referer

def word_check(env):
    params = parse_qs(env['QUERY_STRING'])
    word = params.get('word')

    if word:
        word = escape(word[0])
        return word
    return False

def link_lemma(results):

    in_LEMMA = False
    for line in results:

        if in_LEMMA:
            idx = results.index(line)
            # add a logeion url to the lemma 
            results[idx] = re.sub(r'^\t([A-Za-z]+)', r'\t<a href='+ logeion_url + r'\1' + r'>\1</a>', results[idx])
            in_LEMMA = False
        if re.search(r'LEMMA =+', line): in_LEMMA = True
    return results

def expand_lemlat_codes(code):

    parse_text = []

    for position in range(len(code)):

        tag = code[position]
        if position == 0: 
            if tag == 'N': parse_text.append("Noun") 
            if tag == 'V': parse_text.append("Verb")
            if tag == 'A': parse_text.append("Adj.")
            if tag == 'P': parse_text.append("Pronom.")
            if tag == 'R': parse_text.append("Adv.")
            if tag == 'S': parse_text.append("Prep.")
            if tag == 'C': parse_text.append("Conj.")
            if tag == 'I': parse_text.append("Interj.")
            if tag == 'Y': parse_text.append("Abbrev.")
            if tag == 'X': parse_text.append("Invar.")
            if tag == 'B': parse_text.append("Other")
            if tag == 'L': parse_text.append("Locut.")

        if position == 1: 
            if tag == 'c': parse_text.append("Common")
            if tag == 'p': parse_text.append("Proper")
            if tag == 'm': parse_text.append("Main")
            if tag == 'a': parse_text.append("Main/Auxiliary")
            if tag == 'f': parse_text.append("Qualifying")
            if tag == 'u': parse_text.append("Indefinite")
            if tag == 's': parse_text.append("Possessive")
            if tag == 'o': parse_text.append("Ordinal Number")
            if tag == 'n': parse_text.append("Cardinal Number")
            if tag == 'd': parse_text.append("Distributive Number")
            if tag == 'q': parse_text.append("Personal")
            if tag == 'y': parse_text.append("Demonstrative")
            if tag == 't': parse_text.append("Interrogative")
            if tag == 'b': parse_text.append("Relative")
            if tag == '3': parse_text.append("Determinative")
            if tag == 'e': parse_text.append("Exclamative")
            if tag == 'x': parse_text.append("Reflexive")
            if tag == '1': parse_text.append("Mutual")
            if tag == '2': parse_text.append("Indefinite/Relative")
            if tag == '4': parse_text.append("Indefinite/Interrogative")
            if tag == 'r': parse_text.append("Reducible")
            if tag == 'g': parse_text.append("Irreducible")
            if tag == '*': parse_text.append("To be defined")
            if tag == '5': parse_text.append("Interrogative/Relative")
            if tag == '6': parse_text.append("Indefinite/Ordinal Number")
            if tag == '7': parse_text.append("Indefinite/Relative/Interrogative")

        if position == 2: 
            if tag == 'A': parse_text.append("I decl.")
            if tag == 'B': parse_text.append("II decl.")
            if tag == 'C': parse_text.append("III decl.")
            if tag == 'D': parse_text.append("IV decl.")
            if tag == 'E': parse_text.append("V decl.")
            if tag == 'F': parse_text.append("I conjug.")
            if tag == 'G': parse_text.append("II conjug.")
            if tag == 'H': parse_text.append("III conjug.")
            if tag == 'L': parse_text.append("IV conjug.")
            if tag == 'M': parse_text.append("Conjug. e/i")
            if tag == 'N': parse_text.append("Irr. conjug.")
            if tag == 'P': parse_text.append("Uninflected")

        if position == 3: 
            if tag == 'a': parse_text.append("Act. ind.")
            if tag == 'b': parse_text.append("Pass./Dep. ind.")
            if tag == 'c': parse_text.append("Act. subj.")
            if tag == 'd': parse_text.append("Pass./Dep. subj.")
            if tag == 'e': parse_text.append("Act. imper.")
            if tag == 'f': parse_text.append("Pass./Dep. imper.")
            if tag == 'g': parse_text.append("Act. inf.")
            if tag == 'h': parse_text.append("Pass./Dep. inf.")
            if tag == 'j': parse_text.append("Act. participle")
            if tag == 'k': parse_text.append("Pass./Dep. part.")
            if tag == 'm': parse_text.append("Act. gerund")
            if tag == 'p': parse_text.append("Act. supine")
            if tag == 'q': parse_text.append("Pass./Dep. supine")
            if tag == 'r': parse_text.append("Pass./Dep. gerund")

        if position == 4: 
            if tag == '1': parse_text.append("Pres.")
            if tag == '2': parse_text.append("Imperf.")
            if tag == '3': parse_text.append("Fut.")
            if tag == '4': parse_text.append("Perf.")
            if tag == '5': parse_text.append("Plup.")
            if tag == '6': parse_text.append("Fut. perf.")

        if position == 5: 
            if tag == 'n': parse_text.append("Nom.")
            if tag == 'g': parse_text.append("Gen.")
            if tag == 'd': parse_text.append("Dat.")
            if tag == 'a': parse_text.append("Acc.")
            if tag == 'v': parse_text.append("Voc.")
            if tag == 'b': parse_text.append("Abl.")
            if tag == 'r': parse_text.append("Adv.l")

        if position == 6: 
            if tag == 'm': parse_text.append("Masc.")
            if tag == 'f': parse_text.append("Fem.")
            if tag == 'n': parse_text.append("Neut.")
            if tag == '1': parse_text.append("Masc. & neut.")
            if tag == '2': parse_text.append("Masc. & fem.")
            if tag == '3': parse_text.append("Neut. & fem.")

        if position == 7: 
            if tag == 's': parse_text.append("Sing.")
            if tag == 'p': parse_text.append("Pl.")

        if position == 8: 
            if tag == '1': parse_text.append("1st.")
            if tag == '2': parse_text.append("2nd.")
            if tag == '3': parse_text.append("3rd.")

        if position == 9: 
            if tag == '1': parse_text.append("posit.")
            if tag == '2': parse_text.append("comp.")
            if tag == '3': parse_text.append("sup.")

    return ' '.join(parse_text)

def parse_word(word):

    # create temporary files for batch use
    infile = tempfile.NamedTemporaryFile()
    inf = open(infile.name, "w+")
    inf.write(word)
    inf.seek(0)

    outfile = tempfile.NamedTemporaryFile()

    # run command
    lemlat = os.path.join(lemlat_path, lemlat_bin)
    command = ' '.join([lemlat, '-s 0 -i', infile.name, '-o', outfile.name])
    lemlat = subprocess.run([command], capture_output=True, shell=True, cwd=lemlat_path, encoding='utf8')

    output = []
    with open(outfile.name, "r") as outf:
        for line in outf:
            output.append(line)

    inf.close()
    outf.close()

    if len(output) > 0:
        return(output)
    return None

def lemlat_to_html(lemlat_result):

    path = os.path.join(lemlat_path, "lemlat.html")
    file = open(path, "r")
    html = file.read()

    lemlat_result = link_lemma(lemlat_result)

    # join with <br>
    out_html = '<div style="position:relative; margin: 0 auto; display: inline-block; border-radius: 10px; border: 2px solid #800000; padding: 20px;">%s</div>' % '<br>'.join(lemlat_result)
    html = html.replace("%WORDS%", out_html)

    return html

def application(env, start_response):

    start_response('200 OK', [('Content-Type','text/html')])

    if referer_check(env):
        word = word_check(env)
        if word:
            lemlat_result = parse_word(word)
            if lemlat_result:
                result = lemlat_to_html(lemlat_result)
                return[bytes(result, 'utf8')]
            else:
                return[b'Unknown word.']
        else:
            return[b'No word supplied.']
    else:
        return[b'Please search Logeion first.']
