# Tier-2 Source-Text Verification Against ctext

Date: 2026-07-02

Scope: G04-G10 from `data/gold/tier2_registry.yaml`.

Source policy: compared only the Chinese source text displayed by ctext.org. The page's English translation, where shown, was ignored.

Edition used: ctext.org displayed base text, `底本：《四部叢刊初編》本《世說新語》`, in the relevant `men` page.

Normalization rule inferred from G01-G03: verified local `source.zh.txt` files keep Chinese punctuation and quotation marks, while ctext displays the same passages on fewer lines. Therefore comparison strips whitespace and line breaks only; punctuation, variant characters, and quotation marks remain significant.

Diff table convention: `position` is 1-based in the whitespace-stripped local `source.zh.txt`. `∅` means the aligned character is absent on that side.

## G04 — 陳太丘與友期行

- `source_dir`: `data/sources/chen_taiqiu_appointment`
- ctext URL: https://ctext.org/shi-shuo-xin-yu/fang-zheng/zh
- ctext location: `方正`, article 1
- Edition/version: `底本：《四部叢刊初編》本《世說新語》：方正`
- Normalization: strip whitespace only; keep punctuation
- Verdict: DIFFS-FOUND
- Diff count: 1

| position | our char | ctext char | our context | ctext context |
|---:|---|---|---|---|
| 20 | 捨 | 舍 | 不至，太丘捨去，去後乃 | 不至，太丘舍去，去後乃 |

## G05 — 小時了了,大未必佳

- `source_dir`: `data/sources/kong_rong_visits_li`
- ctext URL: https://ctext.org/shi-shuo-xin-yu/yan-yu/zh
- ctext location: `言語`, article 3
- Edition/version: `底本：《四部叢刊初編》本《世說新語》：言語`
- Normalization: strip whitespace only; keep punctuation
- Verdict: DIFFS-FOUND
- Diff count: 6

| position | our char | ctext char | our context | ctext context |
|---:|---|---|---|---|
| 26 | 。 | ， | 為司隸校尉。詣門者，皆 | 為司隸校尉，詣門者皆俊 |
| 30 | ， | ∅ | 尉。詣門者，皆儁才清稱 | 尉，詣門者皆俊才清稱及 |
| 32 | 儁 | 俊 | 詣門者，皆儁才清稱及中 | ，詣門者皆俊才清稱及中 |
| 141 | ， | 。 | 以其語語之，韙曰：「小 | 以其語語之。韙曰：「小 |
| 155 | 。 | ！ | ，大未必佳。」文舉曰： | ，大未必佳！」文舉曰： |
| 171 | 。 | ！ | ，必當了了。」韙大踧踖 | ，必當了了！」韙大踧踖 |

## G06 — 望梅止渴

- `source_dir`: `data/sources/wang_mei_zhi_ke`
- ctext URL: https://ctext.org/shi-shuo-xin-yu/jia-jue/zh
- ctext location: `假譎`, article 2
- Edition/version: `底本：《四部叢刊初編》本《世說新語》：假譎`
- Normalization: strip whitespace only; keep punctuation
- Verdict: DIFFS-FOUND
- Diff count: 1

| position | our char | ctext char | our context | ctext context |
|---:|---|---|---|---|
| 30 | ∅ | ， | 饒子，甘酸可以解渴。」 | 饒子，甘酸，可以解渴。 |

## G07 — 七步詩

- `source_dir`: `data/sources/seven_step_poem`
- ctext URL: https://ctext.org/shi-shuo-xin-yu/wen-xue/zh
- ctext location: `文學`, article 66
- Edition/version: `底本：《四部叢刊初編》本《世說新語》：文學`
- Normalization: strip whitespace only; keep punctuation
- Verdict: EXACT-MATCH
- Diff count: 0

No diffs after normalization.

## G08 — 急不相棄

- `source_dir`: `data/sources/hua_wang_boat`
- ctext URL: https://ctext.org/shi-shuo-xin-yu/de-xing/zh
- ctext location: `德行`, article 13
- Edition/version: `底本：《四部叢刊初編》本《世說新語》：德行`
- Normalization: strip whitespace only; keep punctuation
- Verdict: EXACT-MATCH
- Diff count: 0

No diffs after normalization.

## G09 — 荀巨伯遠看友人疾

- `source_dir`: `data/sources/xun_jubo_friend`
- ctext URL: https://ctext.org/shi-shuo-xin-yu/de-xing/zh
- ctext location: `德行`, article 9
- Edition/version: `底本：《四部叢刊初編》本《世說新語》：德行`
- Normalization: strip whitespace only; keep punctuation
- Verdict: DIFFS-FOUND
- Diff count: 1

| position | our char | ctext char | our context | ctext context |
|---:|---|---|---|---|
| 48 | ， | ； | ，子令吾去，敗義以求生 | ，子令吾去；敗義以求生 |

## G10 — 舉目見日,不見長安

- `source_dir`: `data/sources/sun_and_changan`
- ctext URL: https://ctext.org/shi-shuo-xin-yu/su-hui/zh
- ctext location: `夙惠`, article 3
- Edition/version: `底本：《四部叢刊初編》本《世說新語》：夙惠`
- Normalization: strip whitespace only; keep punctuation
- Verdict: DIFFS-FOUND
- Diff count: 1

| position | our char | ctext char | our context | ctext context |
|---:|---|---|---|---|
| 40 | ， | ？ | 問何以致泣，具以東渡意 | 問何以致泣？具以東渡意 |

## Resolution (2026-07-02, owner-approved)

Owner-approved resolution:

- Variant-character alignment: update the local public source text to match the ctext `《四部叢刊初編》` base text for G04 `捨→舍` and G05 `儁→俊`.
- Punctuation differences are editorial convention in this repository, not source-text errors. G05 punctuation differences plus G06, G09, and G10 punctuation-only differences remain accepted.
- Final status after source-text alignment and metadata updates: all seven tier-2 articles are verified against the edition.

| scene_id | final verdict | source-text action | flag |
|---|---|---|---|
| G04 | VERIFIED | `捨→舍` aligned to 四部叢刊 base text | true |
| G05 | VERIFIED | `儁→俊` aligned to 四部叢刊 base text; punctuation convention accepted | true |
| G06 | VERIFIED | characters exact-match; punctuation convention accepted | true |
| G07 | VERIFIED | exact-match in original check | true |
| G08 | VERIFIED | exact-match in original check | true |
| G09 | VERIFIED | characters exact-match; punctuation convention accepted | true |
| G10 | VERIFIED | characters exact-match; punctuation convention accepted | true |
