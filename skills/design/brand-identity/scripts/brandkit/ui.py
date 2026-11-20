"""Core components for the UI design system: Button, Input, Checkbox, Card, NavBar, Alert.

Writes the Claude Design System component files (bundle.js assigning window.<namespace>, bundle.css,
index.d.ts, components/<Comp>/{preview.html, README.md}) plus a Cover preview.
Components use React 18 via React.createElement (no JSX, no imports), styled only through the
--color-*, --space-*, --radius-*, --motion-* custom properties from tokens.css.

Usage: python -B -m brandkit.ui TOKENS_DIR OUT_DIR NAMESPACE
"""
import json
import sys
from pathlib import Path

CSS = """
.bk-btn{font:inherit;font-weight:600;border:0;cursor:pointer;min-height:44px;padding:0 var(--space-5);
  border-radius:var(--bk-btn-radius);background:var(--color-primary);color:var(--color-on-primary);
  transition:filter var(--motion-duration-fast) var(--motion-easing-standard)}
.bk-btn:hover{filter:brightness(0.95)}
.bk-btn:focus-visible,.bk-input:focus-visible,.bk-check input:focus-visible+span{outline:2px solid var(--color-focus);outline-offset:2px}
.bk-btn[disabled]{opacity:.45;cursor:not-allowed}
.bk-btn.secondary{background:transparent;color:var(--color-link);box-shadow:inset 0 0 0 1px var(--color-outline)}
.bk-field{display:flex;flex-direction:column;gap:var(--space-1);color:var(--color-on-surface)}
.bk-input{font:inherit;min-height:44px;padding:0 var(--space-3);border-radius:var(--radius-1);
  border:1px solid var(--color-outline);background:var(--color-surface);color:var(--color-on-surface)}
.bk-input[aria-invalid=true]{border-color:var(--color-danger-text)}
.bk-error{color:var(--color-danger-text);font-size:.875em}
.bk-check{display:inline-flex;align-items:center;gap:var(--space-2);min-height:44px;color:var(--color-on-surface);cursor:pointer}
.bk-check input{position:absolute;opacity:0}
.bk-check span{width:20px;height:20px;border:2px solid var(--color-outline);border-radius:4px;display:grid;place-items:center}
.bk-check input:checked+span{background:var(--color-primary);border-color:var(--color-primary);color:var(--color-on-primary)}
.bk-card{background:var(--color-surface-raised);color:var(--color-on-surface);border-radius:var(--radius-2);
  padding:var(--space-5);box-shadow:var(--bk-depth)}
.bk-nav{display:flex;align-items:center;gap:var(--space-5);padding:var(--space-3) var(--space-5);
  background:var(--color-surface);color:var(--color-on-surface);border-bottom:1px solid var(--color-outline-variant)}
.bk-nav a{color:var(--color-on-surface-variant);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.bk-nav a[aria-current=page]{color:var(--color-link);font-weight:600}
.bk-alert{display:flex;gap:var(--space-3);align-items:flex-start;padding:var(--space-3) var(--space-4);
  border-radius:var(--radius-1);background:var(--color-surface-raised);color:var(--color-on-surface);border-left:0}
.bk-alert b{color:var(--bk-tone)}
"""

JS = r"""(function(){
var h=React.createElement;
function Button(p){return h('button',{className:'bk-btn'+(p.variant==='secondary'?' secondary':''),disabled:p.disabled,onClick:p.onClick},p.children);}
function Input(p){var id=p.id||('i'+Math.random().toString(36).slice(2));
 return h('label',{className:'bk-field',htmlFor:id},p.label,
  h('input',{id:id,className:'bk-input',placeholder:p.placeholder,defaultValue:p.value,disabled:p.disabled,'aria-invalid':!!p.error}),
  p.error?h('span',{className:'bk-error'},'⚠ '+p.error):null);}
function Checkbox(p){return h('label',{className:'bk-check'},h('input',{type:'checkbox',defaultChecked:p.checked,disabled:p.disabled}),
  h('span',{'aria-hidden':true},p.checked?'✓':''),p.label);}
function Card(p){return h('div',{className:'bk-card'},p.title?h('h3',{style:{margin:'0 0 8px'}},p.title):null,p.children);}
function NavBar(p){return h('nav',{className:'bk-nav'},h('strong',null,p.brand),
  (p.items||[]).map(function(it,i){return h('a',{key:i,href:'#','aria-current':it.current?'page':undefined},it.label);}));}
var ICON={success:'✓',warning:'!',danger:'✕',info:'i'};
function Alert(p){var t=p.tone||'info';return h('div',{className:'bk-alert',role:'status',style:{'--bk-tone':'var(--color-'+t+'-text)'}},
  h('b',{'aria-hidden':true},ICON[t]),h('div',null,h('b',null,p.title),p.children?h('div',null,p.children):null));}
window.__NS__={Button:Button,Input:Input,Checkbox:Checkbox,Card:Card,NavBar:NavBar,Alert:Alert};
})();
"""

DTS = """declare namespace __NS__ {
  function Button(p: { children: any; variant?: 'primary' | 'secondary'; disabled?: boolean; onClick?: () => void }): any;
  function Input(p: { label: string; id?: string; placeholder?: string; value?: string; disabled?: boolean; error?: string }): any;
  function Checkbox(p: { label: string; checked?: boolean; disabled?: boolean }): any;
  function Card(p: { title?: string; children?: any }): any;
  function NavBar(p: { brand: string; items?: { label: string; current?: boolean }[] }): any;
  function Alert(p: { tone?: 'success' | 'warning' | 'danger' | 'info'; title: string; children?: any }): any;
}
"""

PREVIEWS = {
    "Button": ("Actions", 140, "h(N.Button,null,'Primary'),h(N.Button,{variant:'secondary'},'Secondary'),h(N.Button,{disabled:true},'Disabled')",
               "Primary and secondary actions. The consumer provides the label and the click handler."),
    "Input": ("Forms", 200, "h(N.Input,{label:'Email',placeholder:'you@example.com'}),h(N.Input,{label:'Postcode',value:'12',error:'Enter a full postcode'})",
              "A labelled text field with an error state. The consumer provides the label, value and error text."),
    "Checkbox": ("Forms", 120, "h(N.Checkbox,{label:'Send me updates',checked:true}),h(N.Checkbox,{label:'Remember me'}),h(N.Checkbox,{label:'Disabled',disabled:true})",
                 "A checkbox with a visible label. It is never fully round, whatever the radius factor."),
    "Card": ("Layout", 180, "h(N.Card,{title:'Card title'},'Body copy on the raised surface.')",
             "A raised container for grouped content. The consumer provides the title and body."),
    "NavBar": ("Navigation", 100, "h(N.NavBar,{brand:'__NAME__',items:[{label:'Home',current:true},{label:'About'},{label:'Contact'}]})",
               "Top navigation with a current-page state. The consumer provides the brand and items."),
    "Alert": ("Feedback", 260, "['success','warning','danger','info'].map(function(t){return h(N.Alert,{key:t,tone:t,title:t[0].toUpperCase()+t.slice(1)},'Status always carries an icon and a word.')})",
              "Status messages. Each tone carries an icon and a word, never colour alone."),
}


def write(tokens_dir, out_dir, namespace, name="Brand", depth="borders", pill=False):
    out = Path(out_dir) / "components"; out.mkdir(parents=True, exist_ok=True)
    radius_btn = "var(--radius-full)" if pill else "var(--radius-2)"
    shadow = "0 1px 2px rgba(0,0,0,.08),0 4px 12px rgba(0,0,0,.06)" if depth == "shadows" else "inset 0 0 0 1px var(--color-outline-variant)"
    (out / "bundle.css").write_text(f":root{{--bk-btn-radius:{radius_btn};--bk-depth:{shadow}}}\n" + CSS, encoding="utf-8")
    (out / "bundle.js").write_text(JS.replace("__NS__", namespace), encoding="utf-8")
    (out / "index.d.ts").write_text(DTS.replace("__NS__", namespace), encoding="utf-8")
    tokens_css = (Path(tokens_dir) / "tokens.css").read_text(encoding="utf-8")
    for comp, (group, height, body, readme) in PREVIEWS.items():
        d = out / comp; d.mkdir(exist_ok=True)
        body = body.replace("__NAME__", name)
        html = (f'<!-- @dsCard group="{group}" height={height} -->\n'
                f'<div id="root" style="display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start;padding:16px;'
                f'background:var(--color-surface);font-family:var(--font-text, system-ui)"></div>\n'
                f'<script>var h=React.createElement,N=window.{namespace};'
                f'ReactDOM.createRoot(document.getElementById("root")).render(h(React.Fragment,null,{body}));</script>\n')
        (d / "preview.html").write_text(html, encoding="utf-8")
        (d / "README.md").write_text(f"{readme}\n\nStyled only through tokens; see the root README for usage rules.\n",
                                     encoding="utf-8")
    # standalone review page (both themes) for the model-visual UI checks and for plain-file delivery
    scripts = "".join(
        f'<h3>{c}</h3><div class="row" id="r-{c}"></div>' for c in PREVIEWS)
    renders = ";".join(
        f'ReactDOM.createRoot(document.getElementById("r-{c}")).render(h(React.Fragment,null,{b.replace("__NAME__", name)}))'
        for c, (_, _, b, _) in PREVIEWS.items())
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{name} components</title>
<style>{tokens_css}{(out / 'bundle.css').read_text(encoding='utf-8')}
body{{margin:0;font-family:system-ui;background:var(--color-surface);color:var(--color-on-surface)}}
.theme{{padding:24px}} .row{{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}}</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js"></script>
<script>{(out / 'bundle.js').read_text(encoding='utf-8')}</script></head><body>
<div class="theme" data-theme="light">{scripts}</div>
<div class="theme" data-theme="dark" style="background:var(--color-surface)">{scripts.replace('id="r-', 'id="d-')}</div>
<script>var h=React.createElement,N=window.{namespace};{renders};{renders.replace('"r-', '"d-')}</script></body></html>"""
    (Path(out_dir) / "components.html").write_text(page, encoding="utf-8")
    return out


def cover(tokens_dir, out_dir, name):
    tok = json.loads((Path(tokens_dir) / "tokens.json").read_text(encoding="utf-8"))
    roles = {t["name"]: t["value"] for t in tok["color"]["tokens"] if isinstance(t["value"], dict)}
    cols = [roles[k]["light"] for k in ("primary", "primary-container", "on-surface", "surface-raised")]
    d = Path(out_dir) / "components" / "Cover"; d.mkdir(parents=True, exist_ok=True)
    blocks = "".join(f'<div style="flex:{f};background:{c}"></div>' for f, c in zip((3, 2, 1, 2), cols))
    (d / "preview.html").write_text(
        f'<!-- derivation: colour blocks cut from primary, primary-container, on-surface, surface-raised; '
        f'proportions follow the 60/30/10 restraint rule -->\n'
        f'<div style="position:relative;width:960px;height:300px;display:flex">{blocks}'
        f'<div style="position:absolute;left:32px;bottom:24px;font:600 64px/1 var(--font-display, system-ui);'
        f'color:{roles["on-primary"]["light"]}">{name}</div></div>\n', encoding="utf-8")


if __name__ == "__main__":
    write(sys.argv[1], sys.argv[2], sys.argv[3])
    cover(sys.argv[1], sys.argv[2], sys.argv[3])
    print("ok")
