# From brand strategy to visual concepts: documented methods

**Question.** What documented methods do professional brand-identity designers use to turn brand strategy into visual ideas, and which could an AI agent follow step by step? How do designers choose which routes to present, and how do they justify a concept?

**Purpose.** Input to the spec for a Claude Agent Skill that designs brand identities the way an identity designer does: strategy interview → concept routes → exploration → refinement → logo system, palette, type and graphic language.

> **How these sources were read. Please read this first.**
> This session's network policy blocked direct page fetches. `davidairey.com`, `logodesignlove.com`, `printmag.com`, `pentagram.com` and `books.google.com` all returned DNS or proxy refusals. Every source below was reached only through web-search result extracts of that page: the search tool quotes and paraphrases the page it links to. Each link below is the page the claim comes from. The wording, however, was checked against those extracts, not a full read of the page. **No page numbers are cited because no book page was seen.** A claim is marked **(unverified)** where even the extract was second-hand, the authorship was unclear, or the claim came from a reader comment. Before the spec relies on any quote, re-read it at its link once the hosts are reachable.

---

## 1. Answer

### The documented pipeline from brief to concept

Across the sources, the step from strategy to visual ideas follows the same sequence:

1. **Research and audit, including the competitive and visual landscape.** Wheeler's Phase 1, "Conducting research", includes a *competitive audit* and a *findings report* ([Wiley, 6th ed. contents](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818)). Pentagram case studies describe a "brand audit and a competitive assessment" before design ([Pentagram, A4TE](https://www.pentagram.com/work/advocates-for-trans-equality)). They also describe positioning against sector clichés ([Pentagram, Global Switch](https://www.pentagram.com/work/global-switch); [Pentagram, Visible](https://www.pentagram.com/work/visible)).
2. **Strategy distilled into a short brief or "big idea".** Wheeler's Phase 2, "Clarifying strategy", covers narrowing the focus, positioning and the *brand brief* ([Wiley](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818)). Wolff Olins anchors each system on one creative idea, such as "A new view of care" for Kenvue ([Wolff Olins, Kenvue](https://wolffolins.com/work/kenvue)) and "Regularly remarkable" as the "creative north star" for Blank Street ([Wolff Olins, Blank Street](https://wolffolins.com/work/blank-street)).
3. **A deliberate bridge from strategy to design.** Michael Johnson adds a "half step" between Strategy/Narrative and Design. He calls it the interface that causes "the most difficulty, discussion and disagreement" and lets design findings feed back into the narrative ([Johnson Banks, "Branding. In Five and a Half Steps"](https://www.johnsonbanks.co.uk/thoughts/branding-in-five-and-a-half-steps); [It's Nice That, 2016](https://www.itsnicethat.com/news/michael-johnson-branding-in-five-and-half-steps-book-260916)).
4. **Word mapping and mind mapping.** Brand attributes become word associations, and the designer highlights the words most likely to become sketches ([Airey, *Logo Design Love* free chapter](https://www.logodesignlove.com/images/books/Logo_Design_Love_free_chapter.pdf)).
5. **Divergent sketching at volume, mostly by hand and fast** ([Airey, "Is it still important to sketch"](https://archive.davidairey.com/personal/the-importance-of-sketching/)), followed by internal selection.
6. **Developing a few differentiated routes.** Typically three, and each route is tied back to the narrative ([Johnson Banks, Mozilla routes](https://www.johnsonbanks.co.uk/news/our-first-design-routes-for-mozilla)).
7. **Presenting with a rationale and in application.** Each route is shown with a story that links it to the strategy, on realistic applications ([Wheeler 6th ed. contents: "trial applications", "presentation"](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818); [Haviv on the LogoGeek podcast](https://logogeek.uk/podcast/sagi-haviv/)).
8. **Converging on one route** through client feedback, which is sometimes tested with audiences. The route is then refined into a system ([Johnson Banks, "Mozilla: the chosen route"](https://www.johnsonbanks.co.uk/news/mozilla-the-chosen-route)).

### Methods at a glance

| Method | What it is | Who documents it | Agent-followable? | Why, and the step's input → output for an agent |
|---|---|---|---|---|
| Competitive and visual landscape audit | Collect and map what competitors look like, then find the sector clichés to avoid | [Wheeler (contents)](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818); [Pentagram A4TE](https://www.pentagram.com/work/advocates-for-trans-equality), [Global Switch](https://www.pentagram.com/work/global-switch) | **Yes** | Procedural. In: competitor names or URLs, or images the user supplies. Out: a table of marks, colours, type and devices, plus a list of clichés. This depends on web or image access. |
| Brand brief / big idea | Compress the strategy into a one-line idea that every visual decision traces back to | [Wheeler (contents)](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818); [Wolff Olins, Blank Street](https://wolffolins.com/work/blank-street); [Koto's Carolyn Rush (interview)](https://the-brandidentity.com/interview/kotos-carolyn-rush-good-brands-only-happen-with-a-good-idea) | **Yes**, but the user must sign it off | In: interview answers. Out: positioning, 3 ranked values, audiences, and a one-line idea. |
| Attribute sliders / "this not that" | Place the brand between opposed pairs, such as Friend↔Authority and Playful↔Serious | [GV Three-Hour Brand Sprint](https://library.gv.com/the-three-hour-brand-sprint-3ccabf4b768a) | **Yes** | A structured questionnaire. In: user answers. Out: slider positions, which act as constraints on form, colour and type. |
| Word mapping / mind mapping | Branch out associations from the brand's words, then highlight the words that could become images | [Airey, *Logo Design Love*](https://www.logodesignlove.com/images/books/Logo_Design_Love_free_chapter.pdf) | **Yes** | In: brand words and the name. Out: a tree of associations with candidate motifs flagged. |
| Metaphor / sign-type choice | Choose a mark type (word, letterform, pictorial, abstract, emblem) and a sign relation (icon, index, symbol) | [Wheeler (contents)](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818); [Haviv, "To Abstract or Not Abstract?"](https://www.printmag.com/branding-identity-design/to-abstract-or-not-abstract/); [Peirce (SEP)](https://plato.stanford.edu/entries/peirce-semiotics/) | **Partly** | The decision rules are documented, for example Haviv's "a symbol needs a good reason". Judging whether a metaphor actually lands needs a human. In: the association tree and name length. Out: mark-type hypotheses for each route. |
| Moodboards / visual research | Assemble reference imagery for tone before drawing marks | Practitioner blogs only; no primary studio source was found **(unverified as studio practice)** | **Partly** | Assembly is procedural. The user's reaction is the useful output. |
| Sketch volume / divergent exploration | Make many quick variants and select internally | [Airey: 30-second sketches](https://archive.davidairey.com/personal/the-importance-of-sketching/); [Wolff Olins Uber: "60+ ideas"](https://wolffolins.com/work/uber); [Bass: ~100 concepts → ~5](https://www.logodesignlove.com/how-many-options) **(unverified, second-hand)** | **Yes** for generation, **partly** for selection | In: motifs and mark types. Out: N variants, scored against stated criteria. |
| Concept routes | 2–7 distinct directions, each with its own idea and narrative | [Johnson Banks, Mozilla](https://www.johnsonbanks.co.uk/news/our-first-design-routes-for-mozilla); [Koto, Coca-Cola: four routes](https://www.itsnicethat.com/features/lecture-in-progress-parts-of-the-process-koto-041016) | **Yes** | In: the brief and the variants. Out: 3 routes, each with a name, idea, mark, palette, type and application sketches. |
| Rationale and in-context presentation | A story linking each route to the strategy, shown on realistic applications | [Haviv (LogoGeek)](https://logogeek.uk/podcast/sagi-haviv/); [Haviv (Logo Design Love interview)](https://www.logodesignlove.com/sagi-haviv-interview); [Bierut (Design Observer)](https://designobserver.com/im-with-her/) | **Yes** | In: a route. Out: a rationale paragraph and mockups. |

---

## 2. Methods

### 2.1 Attribute and word mapping

- **Personality sliders.** GV's *Three-Hour Brand Sprint* has teams rank their top 3 values and top 3 audiences. Each list is narrowed by note-and-vote, and a "Decider" makes the final call. Teams then place the company on slider ranges such as "Friend"↔"Authority", "Young & Innovative"↔"Mature & Classic", "Playful"↔"Serious" and "Mass Appeal"↔"Elite". The article notes it helps "to be strongly opinionated on at least one or two ranges" ([GV Library](https://library.gv.com/the-three-hour-brand-sprint-3ccabf4b768a)). GV is a venture fund, not an identity studio, but the method is widely reused as a brand-workshop input.
- **Word mapping.** In *Logo Design Love*, chapter seven, "The language of marks", includes sections on word mapping and "turning words into symbols". In the chapter's framing, the starting question is which words the client wants associated with the brand ([free chapter PDF](https://www.logodesignlove.com/images/books/Logo_Design_Love_free_chapter.pdf); [book page](https://www.logodesignlove.com/book)).
- **"This, not that" opposite lists** (traits the brand is, beside traits that would misrepresent it) appear only in agency and freelancer workshop write-ups, not in the primary books or studio sources found here **(unverified as primary practice)**.
- **Adjective ladders:** no primary source was found **(unverified)**.

### 2.2 Metaphor and semiotics

- **Mark typology.** The contents of Wheeler and Meyerson's *Designing Brand Identity*, 6th ed., list brandmark types: wordmarks, letterform marks, pictorial marks, abstract marks, emblems and dynamic marks. The "sequence of cognition" is listed alongside them ([Wiley contents](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818)). Definitions of each type were seen only in pirated or secondary copies, so they are not cited here **(unverified wording)**.
- **When to use a symbol at all.** Sagi Haviv (Chermayeff & Geismar & Haviv) argues that a symbol needs a good reason, such as a very long name, sub-brands that need unifying, or a need for visual shorthand. Without one, the focus should stay on the name ([Logo Design Love interview, Haviv's own words](https://www.logodesignlove.com/sagi-haviv-interview)). He also writes that "an abstract symbol is only one possible tactic among many" and that the choice should grow out of strategy ([Haviv, Print, "To Abstract or Not Abstract?"](https://www.printmag.com/branding-identity-design/to-abstract-or-not-abstract/)). His worked examples:
  - **Conservation International** suited an abstract mark because the name is descriptive and the audience specific.
  - **The Chase octagon** is abstract but meaningful: it draws on a Chinese coin and suggests a vault, and so security.
  - **The Chase precedent** also relied on large advertising budgets. Tom Geismar is quoted warning that many have imitated it "in cases where they shouldn't have" (same source).
  - **Letterform-based marks** appear in the firm's work too, for example Princeton University Press, a "P" with a second "P" in its negative space ([CGH, Princeton U Press](https://cghnyc.com/work/project/princeton-u-press)).
- **Haviv's criteria for a good mark.** He describes walking "the line between simplicity and distinctiveness". He also tests whether a mark works as small as a 16×16 px favicon ([Logo Design Love interview](https://www.logodesignlove.com/sagi-haviv-interview)).
- **Metaphor from the mind map.** In Airey's Tenon case study, the word "shield" surfaced during mind-mapping as a symbol of defence and trust. The name, a woodworking joint, suggested a dependable connection. The final mark combines a T with a shield ([Logo Design Love free chapter](https://www.logodesignlove.com/images/books/Logo_Design_Love_free_chapter.pdf)).
- **Icon / index / symbol.** This is Peirce's trichotomy. Icons signify through resemblance, indices through a real or causal connection, and symbols through convention ([Stanford Encyclopedia of Philosophy, "Peirce's Theory of Signs"](https://plato.stanford.edu/entries/peirce-semiotics/)). **None of the practitioner sources found here use Peirce's terms in their process.** Applying it to logos comes from academic and teaching literature, so it is a lens the spec could adopt, not documented studio practice.

### 2.3 Mind mapping

Airey treats mind maps and pen-and-paper sketches as the two core idea-generation tools. He highlights the words he thinks "will adapt well to the sketching process" so he can focus on the stronger ideas ([*Logo Design Love* free chapter](https://www.logodesignlove.com/images/books/Logo_Design_Love_free_chapter.pdf)). An extract of his process page stresses producing as many ideas as possible before moving to the computer ([davidairey.com/process](https://www.davidairey.com/process)) **(unverified: the extract came from a copy of the page; the original could not be reached)**.

### 2.4 Moodboards and visual research

No identity-studio primary source (Pentagram, Wolff Olins, Koto, Johnson Banks, Moving Brands, CGH) describing moodboards was found. Moodboard practice appears in freelancer and small-studio blogs: approve the board before concepts, and leave other brands' logos out of it. These do not meet this note's source bar **(unverified as studio practice)**. The nearest primary evidence is the competitive and visual audit above, together with Johnson Banks' sharing of "the design journey" with the client ([Johnson Banks, "Transparency starts at home"](https://www.johnsonbanks.co.uk/templates/thought/transparency-starts-at-home)).

### 2.5 Sketch volume and divergent exploration

- **Airey.** He suggests time-boxing sketches ("try 30 seconds") ([Airey, "Is it still important to sketch"](https://archive.davidairey.com/personal/the-importance-of-sketching/)). He no longer shows clients "a ton of sketches", which he calls a terrible idea. Instead he shows four or five solid ideas in sketch form with a descriptive rationale, then narrows to two or three together with the client (same source; [Airey, "Showing sketches to clients"](https://archive.davidairey.com/self-employment/showing-sketches-to-clients/)).
- **Wolff Olins (Uber).** The team "brainstormed 60+ ideas", then tested them with consumers, iterated and prototyped ([Wolff Olins, Uber](https://wolffolins.com/work/uber)). This was experience work, not logo sketches only.
- **Ratio of explored to shown.** A Logo Design Love page says that to show 3 candidates you must make "at least ten times as many options that you never share" ([logodesignlove.com](https://www.logodesignlove.com/how-much-does-logo-design-cost)) **(unverified: authorship unclear and possibly a reader comment)**.
- **Saul Bass.** He reportedly pinned up "close to a hundred" preliminary concepts and narrowed them to about five semi-finalists ([logodesignlove.com](https://www.logodesignlove.com/how-many-options)) **(unverified: second-hand account)**.
- **Rand on variation.** Paul Rand, interviewed by Steven Heller, said that "many variations provide a good reason to be confused and indiscriminate" ([paulrand.design interviews](https://www.paulrand.design/life/interviews/)) **(unverified: exact interview page not confirmed)**.

**Finding:** no primary source gives a canonical sketch count. The documented numbers range from about 4–5 shown out of an unstated pool (Airey) to 60+ ideas (Wolff Olins), and about 100 (Bass, second-hand).

### 2.6 Concept routes

- **Definition from practice.** Johnson Banks' Mozilla work published seven first-round routes (The Eye, Protocol, Wireframe World, The Open Button, The Impossible M, Flik Flak and others). Each "jumped off" from the narrative work and the personality "Gutsy, Independent, Buoyant, For Good". The applications were "just notional at this stage" ([Johnson Banks, "Our first design routes for Mozilla"](https://www.johnsonbanks.co.uk/news/our-first-design-routes-for-mozilla)).
- **How routes narrow.** Routes were refined ("Protocol 2.0") or dropped. The Open Button went because it lacked a clear link to Mozilla's purpose. The team cut to four routes, then took three into public research. Protocol scored highest on 6 of 7 measures ([Johnson Banks, "Mozilla: the design development"](https://www.johnsonbanks.co.uk/news/mozilla-thedesign-development); [Johnson Banks, "Mozilla: the chosen route"](https://www.johnsonbanks.co.uk/news/mozilla-the-chosen-route); [Mozilla Open Design, "Roads not taken"](https://blog.mozilla.org/opendesign/roads-not-taken/)).
- **Strategy and design in parallel.** Johnson Banks has run "multiple scenarios that entail both strategy and design, in parallel". In one case, the Japanese space observatory idea "bringing the cosmos down to earth" was found during design and moved back into the narrative ([Johnson Banks, "Branding. In Five and a Half Steps"](https://www.johnsonbanks.co.uk/thoughts/branding-in-five-and-a-half-steps)).
- **Koto.** It showed four initial routes for Coca-Cola's emoji project, to show the range of its thinking ([It's Nice That / Lecture in Progress](https://www.itsnicethat.com/features/lecture-in-progress-parts-of-the-process-koto-041016)) **(design-press account)**.
- **Moving Brands.** It anchors exploration in a narrative line, for Carbon "a future fabricated with light", used "to guide our design explorations" ([Moving Brands, Carbon](https://movingbrands.com/work/carbon/)).

### 2.7 Other important methods

- **The strategy → design bridge.** Michael Johnson's five steps are Investigation, Strategy & Narrative, Design, Implementation and Engagement. The ".5" bridges strategy and design ([It's Nice That, 2016](https://www.itsnicethat.com/news/michael-johnson-branding-in-five-and-half-steps-book-260916); [Thames & Hudson](https://thamesandhudson.com/branding-in-five-and-a-half-steps-9780500518960)).
- **The big idea as a filter.** Koto's chief creative officer Carolyn Rush says every creative choice should trace back to the brand idea ([The Brand Identity interview, Rush's own words](https://the-brandidentity.com/interview/kotos-carolyn-rush-good-brands-only-happen-with-a-good-idea)).
- **The strategy–design gap as a discipline.** Neumeier's *The Brand Gap* frames branding as five disciplines: differentiate, collaborate, innovate, validate and cultivate ([martyneumeier.com](https://www.martyneumeier.com/the-brand-gap); [Peachpit](https://www.peachpit.com/store/brand-gap-revised-edition-9780321348104)). "Validate" supports testing routes with audiences, as Mozilla did. No specific procedure from the book was verified **(unverified beyond the chapter titles)**.
- **Identity system phase.** Wheeler's Phase 3, "Designing identity", runs from identity system design through look and feel, colour, typography, iconography, sound, trial applications and presentation ([Wiley contents](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818)). Wiley listings for different ISBNs show different section breakdowns, so check the physical book.

---

## 3. Choosing which routes to present

**The sources disagree, and the disagreement is the finding.**

| Position | Who | Reasoning given |
|---|---|---|
| **One solution** | Paul Rand. Steve Jobs recalled Rand saying, "I will solve your problem for you and you will pay me… If you want options go talk to other people" ([logodesignlove, NeXT](https://www.logodesignlove.com/next-logo-paul-rand); [Heller, "NeXT", paulrand.design](https://www.paulrand.design/life/books-articles/articles/print/1997-design-literacy-next.html)). This is Jobs's recollection reported second-hand, not Rand's own text. | A single answer signals confidence and discourages second-guessing (Heller's reading, same source). |
| **"One route" is risky** | Johnson Banks: "a hugely risky strategy. You only need one naysayer on the board, and things can very quickly unravel" ([Johnson Banks, "An insider's guide to The Design Presentation"](https://www.johnsonbanks.co.uk/thoughts/an-insiders-guide-to-the-design-presentation)) | Client politics. |
| **Two** | A Logo Design Love post says, "I like to show two options… two is quite sufficient to show legitimately different takes" ([logodesignlove, Paul Rand presentations](https://www.logodesignlove.com/paul-rand-logo-presentations)) **(unverified attribution: likely Airey, possibly a quoted designer)** | Two options are enough to show real difference without diluting the work. |
| **Three (safe / just right / unlikely)** | Johnson Banks calls "the obligatory 'three routes'" the time-honoured technique: "One is safe. One is 'just right'. And one is weird-and-very-unlikely-to-be-chosen" ([Johnson Banks, "Transparency starts at home"](https://www.johnsonbanks.co.uk/templates/thought/transparency-starts-at-home)). Airey: "one safe, one adventurous, one scary — from a client perspective". He attributes to Michael Johnson the tip to make the scary option scarier so the original one seems safer ([Airey, "The ideal design process?"](https://archive.davidairey.com/branding/the-ideal-design-process/)). | Framing the range lets the client choose. Johnson Banks warns that three routes "even with a clear recommendation" can backfire, and that a "crazy route" can be shown as a decoy ([insider's guide](https://www.johnsonbanks.co.uk/thoughts/an-insiders-guide-to-the-design-presentation)). |
| **4–5 in sketch form, then narrowed to 2–3** | Airey ([archive.davidairey.com](https://archive.davidairey.com/personal/the-importance-of-sketching/)) | Sketches with rationale make the client a collaborator in narrowing. |
| **Many routes, in the open** | Johnson Banks / Mozilla: 7 routes, then 4, then 3 tested ([Johnson Banks](https://www.johnsonbanks.co.uk/news/our-first-design-routes-for-mozilla)) | The client's open-design mandate. |
| **Process over count** | Bierut: "frequently, we take them through the process we used to come to their solution" ([Fast Company, "Parsing Pentagram"](https://www.fastcompany.com/65201/parsing-pentagram)) **(design press)** | Sharing the process builds belief in the answer. |

**How routes are differentiated.**
- **By idea first.** Each Mozilla route had its own concept (code/protocol, eye, button, impossible geometry), not variations of one mark ([Johnson Banks](https://www.johnsonbanks.co.uk/news/our-first-design-routes-for-mozilla)).
- **By "degrees of interesting".** Johnson Banks places routes along a scale from safe to unlikely ([insider's guide](https://www.johnsonbanks.co.uk/thoughts/an-insiders-guide-to-the-design-presentation)).

**Internal crits and selection criteria.**
- **CGH.** The partners discuss all options, pick the best by common agreement and throw out the seconds ([Print, "Marks Men"](https://www.printmag.com/branding-identity-design/marks-men-an-interview-with-ivan-chermayeff-tom-geismar-and-sagi-haviv-of-chermayeff-geisma/)) **(design-press interview, extract only)**. Candidates are checked against trademark databases before presenting ([Logo Design Love, Haviv interview](https://www.logodesignlove.com/sagi-haviv-interview)).
- **Haviv's mark criteria.** Simple yet distinctive, and works small (same source).
- **Airey's filter.** The designer should show "only those ideas that our training tells us are good enough" ([Airey, "Showing sketches to clients"](https://archive.davidairey.com/self-employment/showing-sketches-to-clients/)).
- **Johnson Banks (Mozilla).** Routes were dropped when the link to purpose was weak (The Open Button), or when development "floundered" (The Eye) ([Johnson Banks](https://www.johnsonbanks.co.uk/news/mozilla-thedesign-development)).

---

## 4. Justifying a concept: rationale and presentation

- **Show the mark in application, not on a white page.** CGH's Armani Exchange mark was rejected when shown "on a white piece of paper". It was approved at once when the "entire presentation" showed it on ads, storefronts and billboards ([Logo Design Love, Haviv interview](https://www.logodesignlove.com/sagi-haviv-interview)). CGH tests marks "in executions, in the context of communications": hang tags, labels, ads, websites ([LogoGeek podcast, Haviv](https://logogeek.uk/podcast/sagi-haviv/)). Wheeler's Phase 3 likewise ends with "trial applications" before "presentation" ([Wiley contents](https://www.wiley.com/en-ca/designing-brand-identity-a-comprehensive-guide-to-the-world-of-brands-and-branding-6th-edition-p-9781119984818)).
- **Prepare the client.** "We give a lot of warnings" (Haviv) ([LogoGeek](https://logogeek.uk/podcast/sagi-haviv/)). Johnson Banks says regular contact before the presentation helps, so an unusual route is not a surprise ([insider's guide](https://www.johnsonbanks.co.uk/thoughts/an-insiders-guide-to-the-design-presentation)).
- **A written rationale per idea.** Airey pairs each sketch with a "descriptive rationale" ([Airey](https://archive.davidairey.com/personal/the-importance-of-sketching/)). Rand's NeXT presentation was a booklet that explained the reasoning before revealing the mark ([logodesignlove, NeXT](https://www.logodesignlove.com/next-logo-paul-rand); [Heller, paulrand.design](https://www.paulrand.design/life/books-articles/articles/print/1997-design-literacy-next.html)). The booklet's details are disputed **(see §6)**.
- **Link back to strategy in one sentence.** Johnson Banks explained Protocol as "a simple and memorable idea which neatly represents how people and knowledge are linked" ([Johnson Banks, chosen route](https://www.johnsonbanks.co.uk/news/mozilla-the-chosen-route)). Bierut's Slack rationale argued the old hashtag was "not proprietary to Slack" and described the new mark as "weaving something to make something stronger" ([It's Nice That, Slack](https://www.itsnicethat.com/news/michael-bierut-pentagram-slack-rebrand-graphic-design-170119)). For Mastercard he gave a functional reason: the mark must work on billboards and watch screens ([It's Nice That, Mastercard](https://www.itsnicethat.com/news/mastercard-new-logo-michael-bierut-graphic-design-080119)). These are design-press pieces quoting Bierut directly.
- **The rationale is partly post-hoc.** Bierut writes that client presentation is "inevitably, at least in part, an exercise in bullshit", because intuitive choices need "something that sounds like a rational justification" ([Design Observer, "I'm With Her"](https://designobserver.com/im-with-her/)). He also stresses listening to how clients react ([Nicer Tuesdays 2025](https://nicertuesdays.itsnicethat.com/talks/michael-bierut-09-09-2025-new-york)).
- **Make the presentation a workshop.** "Share the design journey you have been on, and the presentation becomes a workshop: two-way, not one" ([Johnson Banks, "Transparency starts at home"](https://www.johnsonbanks.co.uk/templates/thought/transparency-starts-at-home)).
- **Evidence through testing.** Mozilla's routes were tested by survey with staff and developers, and through a pop-up exhibition visited by 150+ Mozillians ([Johnson Banks](https://www.johnsonbanks.co.uk/news/mozilla-the-chosen-route); [Mozilla Open Design](https://blog.mozilla.org/opendesign/roads-not-taken/)).

---

## 5. Implications for an agent (inference: my reasoning, not sourced)

- **Procedural, so encode as fixed steps:**
  - a strategy interview that produces values, audiences, sliders and a one-line idea (modelled on the GV sprint and Wheeler's brand brief);
  - a competitive and visual audit table;
  - a word map with flagged motifs;
  - choosing a mark type for each route using Haviv-style rules (long name or sub-brands means a symbol is justified; otherwise lean on the wordmark or letterform);
  - generating many variants for each motif;
  - scoring variants against explicit criteria (fit to idea, simplicity, distinctiveness, works at 16 px, differs from the competitor set);
  - assembling three routes that differ by **idea**, not styling, placed safe → just right → unexpected;
  - a rationale template (idea → link to strategy → how it works in the system);
  - mockups in application.
- **Needs human taste or reaction, so the user must be in the loop:**
  - signing off the brief or big idea before any visual work. Johnson Banks' half step suggests this sign-off should stay reopenable when a design route finds a better idea;
  - reacting to the moodboard or visual territory, if used;
  - choosing among routes. Every source puts this choice with the client; none has the designer choose silently, except Rand's one-solution stance;
  - judging whether a metaphor "lands" or reads wrongly, such as Mozilla's Eye recalling "Sauron";
  - trademark clearance, which an agent cannot perform reliably. Flag it, as CGH does before presenting.
- **Design choices the spec must make:**
  - **How many routes.** Three is the documented default, with the one-vs-many disagreement noted. A user-configurable 2–3 is a defensible default.
  - **Show internal divergence or hide it.** Airey and Johnson Banks both show some process. Hiding everything (Rand) suits a high-trust single answer, which an agent may not have earned.
  - **Sketch volume.** No canonical number exists, so the agent should generate a stated multiple of what it shows (for example ≥10×, the unverified Logo Design Love heuristic) and say so.
- **Weakest evidence for encoding:** moodboards and adjective ladders. No primary studio source was found, so treat them as optional.

---

## 6. Unverified claims and open disagreements

**Unverified**
- **All quotes** come from search-tool extracts of the linked pages, not full reads, because direct fetches were blocked in this session. Re-check before quoting in the spec.
- **"Produce as many ideas as possible before the computer"**, attributed to [davidairey.com/process](https://www.davidairey.com/process). The extract came from a third-party copy.
- **"At least ten times as many options"** ([logodesignlove](https://www.logodesignlove.com/how-much-does-logo-design-cost)). The author is unclear and it may be a comment.
- **"I like to show two options"** ([logodesignlove](https://www.logodesignlove.com/paul-rand-logo-presentations)). It is unclear whether this is Airey, Rand or a quoted designer.
- **Saul Bass's ~100 concepts → ~5.** Second-hand.
- **Rand's "many variations… confused"** quote. The exact interview page is not confirmed.
- **CGH "pick the best by common agreement, throw out the seconds"** (Print). Extract only.
- **Rand's NeXT booklet.** The date (1986 vs 1988), the fee (~$100k, "said to") and the booklet's described form are all disputed across accounts ([logodesignlove](https://www.logodesignlove.com/next-logo-paul-rand); [paulrand.design](https://www.paulrand.design/life/books-articles/articles/print/1997-design-literacy-next.html)).
- **Wheeler's definitions** of each brandmark type, and any Wheeler page numbers. Only the contents listing was reached, and Wiley listings for different ISBNs differ.
- **Neumeier's *Brand Gap*.** Only the five discipline titles were verified, not procedures.
- **Michael Johnson's book.** Only the step names and the half-step concept were verified, from his studio's site and It's Nice That. The book's internal methods were not seen.
- **Moodboards, "this not that" lists and adjective ladders.** No primary identity-studio source was found.
- **Peirce's icon/index/symbol.** Verified as theory ([SEP](https://plato.stanford.edu/entries/peirce-semiotics/)) but **not** found in any practitioner's documented process.
- **Not reached at all:** Pentagram, DesignStudio and Mucho process pages, and the full text of *Identify* and *Identity Designed*.

**Open disagreements**
1. **How many routes to present.** Positions range from one (Rand), through two (Logo Design Love post), three (Johnson Banks convention; Airey 2012), and 4–5 sketches narrowed to 2–3 (Airey), to seven-plus in public (Johnson Banks/Mozilla). Johnson Banks itself both describes three as standard and warns it can backfire.
2. **Whether to show sketches.** Airey now shows 4–5 sketch ideas with rationale. Readers commenting on his posts warn clients do not read sketches as concepts (reader comments, not primary). Rand did not show variations.
3. **Whether to share the process.** Rand's sealed single answer contrasts with Johnson Banks' "presentation as workshop" and Bierut's "take them through the process".
4. **Abstract versus literal marks.** Haviv holds that abstraction needs justification (resources, a descriptive name, a specific audience). The success of abstract marks like Chase led others to copy them "where they shouldn't have" (Geismar, via Haviv).
